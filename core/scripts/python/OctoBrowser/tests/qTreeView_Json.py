import json
import sys
import styles

from typing import Any, Iterable, List, Dict, Union
from PySide2.QtWidgets import QTreeView, QApplication, QHeaderView
from PySide2.QtCore import QAbstractItemModel, QModelIndex, QObject, Qt, QFileInfo


class TreeItem:
    #A Json item corresponding to a line in QTreeView

    def __init__(self, parent: "TreeItem" = None):
        self._parent = parent
        self._key = ""
        self._value = ""
        self._value_type = None
        self._children = []

    def appendChild(self, item: "TreeItem"):
        self._children.append(item)

    def child(self, row: int) -> "TreeItem":
        # Return the child of the current item from the given row
        return self._children[row]

    def parent(self) -> "TreeItem":
        # Return the parent of the current item
        return self._parent



    @classmethod
    def load(
        cls, value: Union[List, Dict], parent: "TreeItem" = None, sort=True) -> "TreeItem":
        
        """Create a 'root' TreeItem from a nested list or a nested dictonary

        Examples:
            with open("file.json") as file:
                data = json.dump(file)
                root = TreeItem.load(data)

        This method is a recursive function that calls itself.

        Returns:
            TreeItem: TreeItem
        """
        
        rootItem = TreeItem(parent)
        rootItem.key = "root"

        if isinstance(value, dict):
            items = sorted(value.items()) if sort else value.items()

            for key, value in items:
                child = cls.load(value, rootItem)
                child.key = key
                child.value_type = type(value)
                rootItem.appendChild(child)

        elif isinstance(value, list):
            for index, value in enumerate(value):
                child = cls.load(value, rootItem)
                child.key = index
                child.value_type = type(value)
                rootItem.appendChild(child)

        else:
            rootItem.value = value
            rootItem.value_type = type(value)

        return rootItem

# ----------------------------------------------------------------------

class JsonModel(QAbstractItemModel):

    # An editable model of Json data

    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self._rootItem = TreeItem()
        self._headers = ("key", "value")

    def clear(self):
        self.load({})

    def load(self, document: dict):      
        # Load model from a nested dictionary returned by json.loads()

        assert isinstance(document, (dict, list, tuple)), "`document` must be of dict, list or tuple, " f"not {type(document)}"
        self.beginResetModel()
        self._rootItem = TreeItem.load(document)
        self._rootItem.value_type = type(document)
        self.endResetModel()
        return True

    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> Any:
        # Return data from a json item according index and role

        if not index.isValid():
            return None
        item = index.internalPointer()

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return item.key
            if index.column() == 1:
                return item.value

        elif role == Qt.EditRole:
            if index.column() == 1:
                return item.value

    def setData(self, index: QModelIndex, value: Any, role: Qt.ItemDataRole):
        # Set json item according index and role: index (QModelIndex), value (Any), role (Qt.ItemDataRole)

        if role == Qt.EditRole:
            if index.column() == 1:
                item = index.internalPointer()
                item.value = str(value)
                self.dataChanged.emit(index, index, [Qt.EditRole])
                return True
        return False

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        # For the JsonModel, it returns only data for columns (orientation = Horizontal)

        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]

    def index(self, row: int, column: int, parent=QModelIndex()) -> QModelIndex:
        # Return index according row, column and parent

        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        # Return parent index of index

        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self._rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        # Return row count from parent index

        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def columnCount(self, parent=QModelIndex()):
        # Return column number. For the model, it always return 2 columns
        return 2

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        # Return flags of index

        flags = super(JsonModel, self).flags(index)
        if index.column() == 1:
            return Qt.ItemIsEditable | flags
        else:
            return flags

    def to_json(self, item=None):
        
        if item is None:
            item = self._rootItem
        nchild = item.childCount()
        if item.value_type is dict:
            document = {}
            for i in range(nchild):
                ch = item.child(i)
                document[ch.key] = self.to_json(ch)
            return document
        elif item.value_type == list:
            document = []
            for i in range(nchild):
                ch = item.child(i)
                document.append(self.to_json(ch))
            return document
        else:
            return item.value

if __name__ == "__main__":

    app = QApplication(sys.argv)
    view = QTreeView()
    model = JsonModel()
    view.setModel(model)
    json_path = QFileInfo(__file__).absoluteDir().filePath('X:/Shared drives/Pipeline/tools/OctoTools/core/scripts/python/OctoBrowser/shotData.json')

    with open(json_path) as file:
        document = json.load(file)
        model.load(document)

    view.show()
    view.header().setSectionResizeMode(0, QHeaderView.Stretch)
    #view.setAlternatingRowColors(True)
    view.setStyleSheet(styles.tree_widget)
    view.resize(500, 300)
    sys.exit(app.exec_())

