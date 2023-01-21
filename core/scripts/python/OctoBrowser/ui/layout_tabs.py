import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
)

from layout_colorwidget import Color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)
        tabs = QTabWidget()
        tabs.setTabShape(QTabWidget.Rounded)
        tabs.setDocumentMode(True)
        # tabs stylesheet
        tabs.setStyleSheet(
            """
            QTabBar::tab {
                width: 200px;
                background: #333333;
                color: #999;
                font-size: 24px;
                border: 1px solid #333333;
                border-bottom-color: #333333;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                padding: 15px;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: #333333;
            }
            QTabBar::tab:!selected {
                margin-top: 10px;
            }

            """
        )   





        for n, color in enumerate(["red", "green", "blue", "yellow"]):
            tabs.addTab(Color(color), color)

        self.setCentralWidget(tabs)
        


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()