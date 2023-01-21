from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt

class OctoTree(QtWidgets.QWidget):
    """
    Custom Qt Widget to show a QTreeWidget.
    """

    def __init__(self, *args, **kwargs):
        super(OctoTree, self).__init__(*args, **kwargs)

        show_tree_widget = QtWidgets.QTreeWidget()
        show_tree_widget.setColumnCount(1)
        show_tree_widget.setMaximumSize(6000, 1000)
        show_tree_widget.setHeaderHidden(True)
        show_tree_widget.setIndentation(20)
        show_tree_widget.setAnimated(True)
        show_tree_widget.setAllColumnsShowFocus(True)
        show_tree_widget.setIconSize(QtCore.QSize(32, 32))
        show_tree_widget.setUniformRowHeights(True)
        show_tree_widget.setRootIsDecorated(True)
        show_tree_widget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        show_tree_widget.setWordWrap(True)
        show_tree_widget.setStyleSheet('''
            QTreeWidget::item {
                padding: 10px;
                background-color: #222; 
                color: #666; 
                border: 1px solid #444; 
                border-radius: 5px;

                } 
            QTreeWidget::item:selected {
                background-color: #111; 
                color: #888; 
                border: 1px solid #333; 
                border-radius: 5px;
                }
            QTreeWidget::item:selected:active {
                background-color: #111;
                color: #fff;
                border: 1px solid #333;
                border-radius: 5px;
                }
            QTreeWidget::item:hover {
                background-color: #111;
                color: #888;
                border: 1px solid #444;
                border-radius: 5px;
                }
            QTreeWidget::item:open {
                background-color: #111;
                color: #999;
                border: 1px solid #444;
                border-radius: 5px;
                }
        ''')
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(show_tree_widget)
        self.setLayout(layout)