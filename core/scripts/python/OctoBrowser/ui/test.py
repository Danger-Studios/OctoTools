import sys

from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QFrame,
    QHeaderView
)

from layout_colorwidget import Color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OctoTree")
        show_tree_widget = QTreeWidget()
        show_tree_widget.setColumnCount(1)
        show_tree_widget.setMaximumSize(6000, 1000)
        show_tree_widget.setHeaderHidden(True)
        show_tree_widget.setIndentation(20)
        show_tree_widget.setAnimated(True)
        show_tree_widget.setAllColumnsShowFocus(True)
        show_tree_widget.setIconSize(QSize(32, 32))
        show_tree_widget.setUniformRowHeights(True)
        show_tree_widget.setRootIsDecorated(True)
        show_tree_widget.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
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

        self.setCentralWidget(show_tree_widget)
        


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()