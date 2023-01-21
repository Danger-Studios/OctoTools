from PySide2.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QTextEdit, QAction
import sys
from PySide2.QtGui import QIcon
 
 
#our main window class
class WindowWidget(QMainWindow):
    count =0
    def __init__(self):
        super().__init__()
 
        self.init_ui()
 
 
 
 
    def init_ui(self):
 
        #title, geoemtry and icon for this window
        self.setWindowTitle("Pyside2 MDI Window")
        self.setGeometry(100,100, 900, 500)
        self.setWindowIcon(QIcon('pyicon.png'))
 
        #creating object of MDI
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
 
 
        #our menu bar
        menu_bar = self.menuBar()
 
 
        #our menu items
        file = menu_bar.addMenu("File")
        file.addAction("New")
        file.addAction("Cascade")
        file.addAction("Tiled")
 
        file.triggered[QAction].connect(self.window_triggered)
 
 
 
        self.show()
 
 
    def window_triggered(self, p):
 
        if p.text() == "New":
            WindowWidget.count = WindowWidget.count + 1
            sub = QMdiSubWindow()
            sub.setWidget(QTextEdit())
            sub.setWindowTitle("Sub Window " + str(WindowWidget.count))
            self.mdi.addSubWindow(sub)
            sub.show()
 
 
        if p.text() == "Cascade":
            self.mdi.cascadeSubWindows()
 
 
        if p.text() == "Tiled":
            self.mdi.tileSubWindows()
 
 
 
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowWidget()
    sys.exit(app.exec_())