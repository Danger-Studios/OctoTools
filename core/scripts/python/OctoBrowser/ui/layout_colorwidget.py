import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGridLayout, QStackedLayout  
from PySide2.QtGui import QPalette, QColor




class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


