# fix for windows taskbar icon
import sys
import os
from pathlib import Path
import ctypes
from PySide2 import QtWidgets, QtNetwork, QtCore, QtGui, QtSvg

import main


# Icon for windows taskbar
myappid = 'danger.octolauncher.v1.0.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class OctoNodes(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(' OctoNodes')
        self.setStyleSheet('background-color: #333333;border: none;')
        self.setWindowIcon(QtGui.QIcon(str(Path(__file__).parent)+'/octo-tools.svg'))
        self.vlayout = QtWidgets.QVBoxLayout()
        nodz = main.nodes(self)
        nodz.loadConfig(filePath=str(Path(__file__).parent)+'/config.json')
        nodz.initialize()
        self.vlayout.addWidget(nodz)
        self.setLayout(self.vlayout)
        self.show()
        nodeA = nodz.createNode(name='SHOWS', preset='node_preset_1', position=None)
        nodz.createAttribute(node=nodeA, name='MGN', index=-1, preset='attr_preset_1',plug=True, socket=False, dataType=str)

        


# run app in standalone mode
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = OctoNodes()
    window.show()
    sys.exit(app.exec_())
