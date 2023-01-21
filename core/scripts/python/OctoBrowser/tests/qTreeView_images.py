import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QTreeView
from PySide2.QtCore import  Qt
from PySide2.QtGui import QFont, QColor, QImage, QStandardItemModel, QStandardItem

# get path of script and add to sys.path
import os
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

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
    def __init__(self):
        super().__init__()
        self.resize(1200, 1200)

        treeView = QTreeView()
        treeView.setHeaderHidden(True)
        treeView.header().setStretchLastSection(True)

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        photos = StandardItem('My Photos', '', set_bold=True)

        cat = StandardItem('Cats', path+'/images/devil.png', 14)
        photos.appendRow(cat)

        taipei = StandardItem('Taipei', path+'/images/lord.png', 16)
        photos.appendRow(taipei)

        rootNode.appendRow(photos)
        treeView.setModel(treeModel)
        treeView.expandAll()

        self.setCentralWidget(treeView)

app = QApplication(sys.argv)        
demo = AppDemo()
demo.show()
sys.exit(app.exec_())