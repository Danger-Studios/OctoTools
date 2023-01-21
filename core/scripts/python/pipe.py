'''

 A collection of useful functions for houdini

'''
import glob, os, json, subprocess
import hou
import toolutils as tu

# shot name template: s010_shotName_fx_cloudSetup_jtomori_v001.hipnc
# asset name template: fx_cloudRig_jtomori_v001.hipnc
# initializes global variables in houdini session
def initVars():
	hipname = hou.getenv('HIPNAME')
	if hipname != 'untitled':
		attribs = hipname.split("_")
		if len(attribs) == 6:
			hou.putenv('SHOT', attribs[0])
			hou.putenv('SHOTNAME', attribs[1])
			hou.putenv('TASK', attribs[2])
			hou.putenv('TASKNAME', attribs[3])
			hou.putenv('USER', attribs[4])
			hou.putenv('VER', attribs[5])
		elif len(attribs) == 4:
			hou.putenv('TASK', attribs[0])
			hou.putenv('ASSET', attribs[1])
			hou.putenv('USER', attribs[2])
			hou.putenv('VER', attribs[3])
		elif len(attribs) > 0:
			hou.putenv('VER', attribs[-1])
	else:
		print('Name your file')

# splits versioning string into letter and number, e.g. v025 -> ['v','025']
def verSplit(ver):
	head = ver.rstrip('0123456789')
	tail = ver[len(head):]
	return head, tail

# save incremental, preserves version formatting
def saveInc():
	hipname = hou.getenv('HIPNAME')
	if hipname != 'untitled':
		v, num = verSplit( hipname.split("_")[-1] )
		num = str( int(num) + 1 ).zfill( len(num) )
		newName = hipname.split("_")
		newName[-1] = v + num
		newNameStr = hou.getenv('HIP') + "/" + "_".join(newName) + "." + hou.getenv('HIPFILE').split(".")[-1]
		hou.hipFile.save(newNameStr)
		initVars()
	else:
		print("cannot increment version name in untitled.hip")

# loads back last crashed file
def crashRecovery():
	path = hou.getenv("HOUDINI_TEMP_DIR")
	os.chdir(path)
	files = [file for file in glob.glob("*.hip*")]
	if len(files) != 0:
		hou.hipFile.load( path + "/" + files[-1] )
	else:
		print("no crashed files found")

# flattens down list of lists
def flatten(A):
    rt = []
    for i in A:
        if isinstance(i,list): rt.extend(flatten(i))
        else: rt.append(i)
    return rt

# return list of folders inside specified folder
def getFoldersPaths(path):
	folders = [x[0] for x in os.walk(path)]
	del folders[0]
	return folders

# return list of files matching mask inside specified folder
def getFilesByMask(path, mask):
	os.chdir(path)
	lods = [file for file in glob.glob(mask)]
	return lods
	
# batch rename incoming nodes (from  selection) by specified prefix and selection order
def batchRename(nodes):
	prefix = hou.ui.readInput("name prefix:", buttons=("rename",), title="rename nodes")[1]
	if prefix != '':
		for i, node in enumerate(nodes):
			node.setName(prefix + str(i), unique_name=True)

# tool for quick and easy creating of viewport flipbooks, to be implemented later.., watermark can be done maybe with hwatermark or something, settings does not have an option for that
def flipBooker():
	viewer = tu.sceneViewer()
	settings = viewer.flipbookSettings().stash()

	path = hou.getenv("HIP") + "/prev/" + hou.getenv("VER") + "/"
	if not os.path.isdir(path):
		os.makedirs(path)
	path = path + "out_$F4.jpg"
	settings.output(path)

	viewer.flipbook(settings=settings)

# function to convert image path to path with "deep" suffix, intended for automatic deep id pass setup
# for example:
# F:/05_user/jtomori/rnd/deep_ids/ren/img_5.exr -> F:/05_user/jtomori/rnd/deep_ids/ren/img_deep_8.exr
def idPath(node, suffix, src="img"):
	if src == "img":
		path = node.evalParm("vm_picture")
	elif src == "ifd":
		path = node.evalParm("soho_diskfile")
	path = path.split(".")
	pathInner = path[0].split("_")
	pathInner.insert(len(pathInner)-1, suffix)
	pathInner = "_".join(pathInner)
	path[0] = pathInner
	path = ".".join(path)
	return path

# function to convert image path to IFD path
def ifdPath(pathImg):
	pathImg = pathImg.split("/")
	#pathImg.insert(len(pathImg)-1, "ifd")
	pathImg[-2] = pathImg[-2] + "_ifd"
	pathImg = "/".join(pathImg)
	pathImg = pathImg.split(".")
	pathImg[-1] = "ifd"
	pathImg = ".".join(pathImg)
	return pathImg

# return the first instance of the folder name
def dirFinder(atom, root='$HIP'):
    for path, dirs, files in os.walk(root):  
        if atom in dirs:
            print('[>] FOUND:',atom)
            print('[>] PATH:',os.path.join(path, atom))
            print('[>] ROOT:',root)
            return os.path.join(path, atom)

# Listing files in directories recursively
def fileFinder(root):
	for dirpath, dirs, files in os.walk(root):
		path = dirpath.split('/')
		print('|', (len(path))*'---', '[',os.path.basename(dirpath),']')
		for f in files:
			print('|', len(path)*'---', f)