import os
import sys
import json
import base64
from PySide2 import QtCore, QtWidgets, QtGui
import styles

# get path of script and add to sys.path to avoid relative imports in other modules
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

class OctoTree(QtWidgets.QTreeWidget):

    # A Custom Qt Widget. This is the main widget for the OctoTree.
    
    def __init__(self, value) -> None:
        super().__init__()
        self.fill_item(self.invisibleRootItem(), value)
        self.setStyleSheet(styles.tree)
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setAnimated(True)
        self.setMinimumSize(600, 1000)
        self.setIndentation(40)
        self.setRootIsDecorated(True)
        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.setIconSize(QtCore.QSize(128, 128))
        self.setWordWrap(True)
        self.setAllColumnsShowFocus(True)
        self.itemClicked.connect(self.onItemClicked)
        # self.setUniformRowHeights(True) # <---- turn this on to crop menu thumbnails

    @staticmethod
    def fill_item(item: QtWidgets.QTreeWidgetItem, value) -> None:

        if value is None:
            return
        elif isinstance(value, dict):
            for key, val in sorted(value.items()):
                OctoTree.new_item(item, str(key), val)
        elif isinstance(value, (list, tuple)):
            for val in value:
                if isinstance(val, (str, int, float)):
                    OctoTree.new_item(item, str(val))
                else:
                    if isinstance(val, dict):  # skip root item [dict] <--- disable this 'if statement' to show root item           
                        for key, val in sorted(val.items()):
                            OctoTree.new_item(item, str(key), val)
                            
                            # remove specific stuff from recursive menu crawl
                            if key == 'thumbnail':
                                item.takeChild(item.childCount() - 1)
                            if key == 'status':
                                item.takeChild(item.childCount() - 1)
                            if key == 'attributes':
                                item.takeChild(item.childCount() - 1)
                            if key == 'metadata':
                                item.takeChild(item.childCount() - 1)
                            
                            # keep 'task' sub items and parent to 'shots'
                            if key == 'tasks':
                                item.takeChild(item.childCount() - 1)
                                # find 'title' in list and set as parent item under 'shot'
                                for key in val:
                                    for key, val in sorted(key.items()):
                                        if key == 'title':
                                            OctoTree.new_item(item, str(val))
                                            # and don't add sub keys...      
                    
                    # OctoTree.new_item(item, f"[{type(val).__name__}]", val) <---- enable this to show root item
                    
                    if isinstance(val, str) and val.startswith("iVBOR"): # dirty hacker... <--- disable this to hide menu thumbnails
                        pixmap = QtGui.QPixmap()
                        file_decoded = base64.urlsafe_b64decode(val)
                        pixmap.loadFromData(file_decoded)
                        pixmap = pixmap.scaled(320, 200, QtCore.Qt.KeepAspectRatio)
                        item.setIcon(0, QtGui.QIcon(pixmap))
        else:
            OctoTree.new_item(item, str(value))
   
    @staticmethod
    def new_item(parent: QtWidgets.QTreeWidgetItem, text:str, val=None) -> None:

        child = QtWidgets.QTreeWidgetItem([text])
        OctoTree.fill_item(child, val)
        parent.addChild(child)
        child.setExpanded(True)
        child.setTextAlignment(0, QtCore.Qt.AlignLeft)
        child.setTextAlignment(0, QtCore.Qt.AlignVCenter)

        # set icon for specific child items
        if text.startswith('SQ'):
            child.setIcon(0, QtGui.QIcon(seq_icon))

        if parent.text(0).startswith('SH') and parent.text(0) != 'SHOWS':
            # add tristate checkbox to 'task' items
            child.setIcon(0, QtGui.QIcon(task_icon))

        if parent.text(0) == 'SHOWS':
            child.setIcon(0, QtGui.QIcon(show_icon))

    @QtCore.Slot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, it, col):
        print(it.text(col))

# -----------------------------------------------------------------------------------------------

treeapp = QtWidgets.QApplication([])

# pull stuff from disk
seq_icon = QtGui.QIcon(path+'/icons/seq.svg').pixmap(24, 24)
show_icon = QtGui.QIcon(path+'/icons/show.svg').pixmap(24, 24)
task_icon = QtGui.QIcon(path+'/icons/task.svg').pixmap(24, 24)

# get menu data
showJson = 'X:/Shared drives/Pipeline/tools/OctoTools/core/scripts/python/OctoBrowser/shotData.json'
with open(showJson) as json_file:
    shows = json.load(json_file)
tree = OctoTree(shows)

if __name__ == "__main__":
    tree.show()
    sys.exit(treeapp.exec_())
