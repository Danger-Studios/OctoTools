# fix for windows taskbar icon
import sys
import os
from pathlib import Path
import ctypes
from PySide2 import QtWidgets, QtNetwork, QtCore, QtGui, QtSvg
# add nodes to sys path fucking python import system
nodesPath = sys.path.append(os.path.join(os.path.dirname(__file__), 'nodes'))
from nodes import main
from OctoBuild import dataWrangler


# Icon for windows taskbar
myappid = 'danger.octolauncher.v1.0.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Main function
class OctoNodes(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        rebuildJson = 0
        showJson = 'X:/Shared drives/Pipeline/tools/OctoTools/core/scripts/python/OctoBrowser/nodesData.json'
        
        self.wrangleData = dataWrangler()
        self.wrangleData.getData
        self.wrangleData.loadData(rebuildJson,showJson)
        
        self.setWindowTitle(' OctoNodes')
        self.setStyleSheet('background-color: #333333;border: none;')
        self.setWindowIcon(QtGui.QIcon(str(Path(__file__).parent)+'/icons/octo-tools.svg'))

        self.vlayout = QtWidgets.QVBoxLayout()
        self.nodz = main.nodes(self)
        self.nodz.loadConfig((str(Path(__file__).parent)+'/nodes/config.json'))
        self.nodz.initialize()
        self.vlayout.addWidget(self.nodz)
        self.setLayout(self.vlayout)
        self.show()
        self.CreateNode()
    
    def CreateNode(self):
        attrib_id = 0
        seq_id = 0
        shot_id = 0
        task_id = 0

        # Create Root Node 
        shows_node = self.nodz.createNode(name='SHOWS', preset='node_preset_1', position=QtCore.QPointF(100.000000, 1000.000000+attrib_id))
        self.nodz.createAttribute(node=shows_node, name='SHOWS', index=-1, preset='attr_preset_1',plug=True, socket=False, dataType=str)
        for shows in self.wrangleData.shows['SHOWS']:
            
            # Create Show Nodes   
            for show_name in shows:
                attrib_id += 200
                show_attrib_id = show_name + '_' + str(attrib_id) 
                show_node = self.nodz.createNode(name=show_name, preset='node_preset_1', position=QtCore.QPointF(500.000000, 600.000000+attrib_id))
                self.nodz.createAttribute(node=show_node, name=show_name, index=-1, preset='attr_preset_1',plug=False, socket=True, dataType=str)
                self.nodz.createConnection('SHOWS', 'SHOWS',show_name, show_name)

            # Create Sequence Nodes
            for seq in shows[show_name]:
                for seq_name in seq:
                    seq_id += 200
                    seq_uname = show_name + '/' + seq_name
                    #seq_node = self.nodz.createNode(name=seq_uname, preset='node_preset_1', position=QtCore.QPointF(800.000000, 300.000000+seq_id))
                    self.nodz.createAttribute(node=show_node, name=seq_name, index=-1, preset='attr_preset_2',plug=True, socket=False, dataType=str)
                    #self.nodz.createConnection(show_name, show_attrib_id,seq_uname, seq_name)
            
                # Create Shot Nodes
                for shot in seq[seq_name]:
                    for shot_name in shot:
                        shot_id += 400
                        shot_uname = seq_uname + '/' + shot_name
                        shot_node = self.nodz.createNode(name=shot_uname, preset='node_preset_1', position=QtCore.QPointF(1300.000000, -800.000000+shot_id))
                        self.nodz.createAttribute(node=shot_node, name=shot_name, index=-1, preset='attr_preset_1',plug=False, socket=True, dataType=str)
                        self.nodz.createConnection(show_name, seq_name,shot_uname, shot_name)

                    # Create Task Nodes
                    for tasks in shot[list(shot.keys())[0]]:
                        for key, value in tasks.items():            
                            if key == 'tasks':
                                for task in value:
                                    task_name = task['title']
                                    task_id += 200
                                    task_uname = shot_uname + '_' + task_name
                                    self.nodz.createAttribute(node=shot_node, name=task_name, index=-1, preset='attr_preset_2',plug=True, socket=False, dataType=str)















# run app in standalone mode
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = OctoNodes()
    window.show()
    sys.exit(app.exec_())
