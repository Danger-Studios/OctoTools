import sys
import os
path = 'X:/Shared drives/Pipeline/tools/OctoTools/core/scripts/python/OctoBrowser/tests'

from PySide2.QtWidgets import QApplication, QMainWindow, QTreeView
from PySide2.QtCore import  Qt
from PySide2.QtGui import QFont, QColor, QImage, QStandardItemModel, QStandardItem

        
class StandardItem(QStandardItem):
    def __init__(self, txt='', image_path='', font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont('Consolas', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)

        if image_path:
            image = QImage(image_path)
            self.setData(image, Qt.DecorationRole)

class AppDemo(QMainWindow):
    def __init__(self, parent=None):       
        super(AppDemo, self).__init__(parent)   
        self.setWindowTitle('OctoTools')

        treeView = QTreeView()
        treeView.setHeaderHidden(True)
        treeView.header().setStretchLastSection(True)

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        photos = StandardItem('Scary Stuff', '', set_bold=True)

        cat = StandardItem('DEVIL', path+'/images/devil.png', 14)
        photos.appendRow(cat)

        taipei = StandardItem('LORD', path+'/images/lord.png', 16)
        photos.appendRow(taipei)

        rootNode.appendRow(photos)
        treeView.setModel(treeModel)
        treeView.expandAll()

        self.setCentralWidget(treeView)
        self.show()
        self.raise_()
                
try:
    jobToolsShelf.close()

except:
    pass
        
jobToolsShelf = AppDemo()
