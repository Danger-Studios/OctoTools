import hou
import os
import SubmitHoudiniToDeadlineFunctions as SHDF


class DeadlineSlapJob(object):
    def __init__(self, dlNode, rop, dependencies):
        self.dlNode = dlNode
        self.rop = rop
        self.dependencies = dependencies
        self.submittedIDs = None

    def submitJob(self):
        jobDeps = [SubmitSlapJob(
            self.rop,
            self.dlNode,
            ",".join([dep.submittedIDs for dep in self.dependencies if dep.submittedIDs]))]
        self.submittedIDs = ",".join(jobDeps)


def SubmitSlapJob(node, dlNode, dependencies):
    import tempfile
    import json
    import sgtk

    engine = sgtk.platform.current_engine()
    slap_description = createSlapDescription(node)

    jobProperties = {
        "Plugin": "NukeProcessRender",
        "Name": os.path.basename(slap_description["slap_render_path"]),
        "LimitGroups": "nuke",
        "JobDependencies": dependencies,
        "Comment": ""
    }

    processor_script = SHDF.CallDeadlineCommand([
        "-GetRepositoryFilePath",
        "plugins/NukeProcessRender/nuke_slap_script.py"])

    plugin_props = {
        "processor_script": processor_script,
        "sg_input_color_space": "",
        "sg_output_color_space": "",
        "shot_code": engine.context.entity["name"],
        "shot_client_code": "",
        "shot_id": engine.context.entity["id"],
        "project_name": engine.context.project["name"],
        "sg_cdl": "",
        "sg_cccid": "",
        "sg_slate_switch2": "",
        "artist_name": engine.context.user["login"],
        "step": engine.context.step["name"],
        "original_frames": SHDF.GetFrameInfo(dlNode),
        "has_slate": "False",
        "scene_path": hou.hipFile.path(),
        "input_path": "",
        "submit_renders": True
    }

    with tempfile.NamedTemporaryFile("w", suffix="job_props", delete=False) as f:
        job_props_file = f.name
        for k, v in jobProperties.items():
            f.write("{}={}\n".format(k, v))

    with tempfile.NamedTemporaryFile("w", suffix="plugin_props", delete=False) as f:
        plugin_props_file = f.name
        for k, v in plugin_props.items():
            f.write("{}={}\n".format(k, v))

    with tempfile.NamedTemporaryFile("w", suffix="slap_description", delete=False) as f:
        slap_description_file = f.name
        json.dump(slap_description, f)

    jobResult = SHDF.CallDeadlineCommand([
        job_props_file,
        plugin_props_file,
        slap_description["template_scene_path"],
        slap_description_file])

    jobId = SHDF.GetJobIdFromSubmission(jobResult)

    # delete temp files
    os.unlink(job_props_file)
    os.unlink(plugin_props_file)
    os.unlink(slap_description_file)

    return jobId


def createSlapDescription(rop):
    def createLayerDescription(rop, index):
        source_type = rop.parm("source_type{}".format(index)).eval()
        if source_type == "rop":
            source_node = rop.parm("source_rop{}".format(index)).evalAsNode()
            if source_node is None:
                raise ValueError(
                    "Linked node not found {}".format(
                        rop.parm("source_rop{}".format(index)).eval()))

            return {
                "node_name": rop.parm("node_name{}".format(index)).eval(),
                "source_path": SHDF.GetOutputPath(source_node).eval(),
                "source_type": source_type,
                "source_rop": source_node.path()
            }
        else:
            return {
                "node_name": rop.parm("node_name{}".format(index)).eval(),
                "source_path": rop.parm("source_path{}".format(index)).eval(),
                "source_type": source_type
            }
    return {
        "source_scene_path": hou.hipFile.path(),
        "template_scene_path": rop.parm("template_scene").eval(),
        "slap_render_path": rop.parm("slap_render_path").eval(),
        "layers": [createLayerDescription(rop, index + 1)  # multiparms are 1-based
                   for index in range(rop.parm("layers").eval())]}


def getDependencyNodes(rop):
    return [rop.parm("source_rop{}".format(index + 1)).evalAsNode()
            for index in range(rop.parm("layers").eval())
            if rop.parm("source_type{}".format(index + 1)).eval() == "rop"]
