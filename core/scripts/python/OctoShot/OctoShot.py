import sys
import os
import ctypes
from .ui_interface import *
from PySide2 import QtCore

# Icon for windows taskbar
myappid = 'danger.octotools.v1.0.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # window button functions:
        self.ui.actionClose.triggered.connect(self.closeWindow)
        self.ui.actionMaximize.triggered.connect(self.maximizeWindow)
        self.ui.actionMinimize.triggered.connect(self.minimizeWindow)


        self.show()
        self.loadLayout()


        #--------------------------------------------#
        # Show Window
    
        # self.setLayout(mainWindow)


    def closeEvent(self, event):
        print('Saving Layout...')
        settings = QSettings('Danger','OctoTools')
        settings.setValue('geometry',self.saveGeometry())
        settings.setValue('windowState',self.saveState())
        super(mainWindow, self).closeEvent(event)
    
    def loadLayout(self):
        print('Loading Layout...')
        settings = QSettings('Danger','OctoTools')
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))
    
    # Custom titleBar stuff ( not working in houdini)
    # def mousePressEvent(self, event):
    #     if event.button() == QtCore.Qt.LeftButton:
    #         self.offset = event.pos()
    #     else:
    #         super().mousePressEvent(event)

    # def mouseMoveEvent(self, event):
    #     if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
    #         self.move(self.pos() + event.pos() - self.offset)
    #     else:
    #         super().mouseMoveEvent(event)

    # def mouseReleaseEvent(self, event):
    #     self.offset = None
    #     super().mouseReleaseEvent(event)

    # Close Window Button
    def closeWindow(self):
        self.close()

    # Minimize Window Button
    def minimizeWindow(self):
        self.showMinimized()

    # Maximize Window Button
    def maximizeWindow(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()



# run app in standalone mode:
if __name__ == '__main__':

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = '1'
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    
    # Dark Palette
    light_palette = QPalette()
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Background, QColor(40, 40, 40))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(69, 176, 128))
    dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))

    app.setStyleSheet('''
    
    QMainWindow::toolBarArea {
        background-color: #2a2a2a;
        border: 1px solid #2a2a2a;
    }
    QToolBar::handle {
        background-color: #333333;
        height: 2px;
        padding: 10px;
    }
    QMainWindow::separator {
        background-color: #333333;
        height: 3px;
        padding: 3px;

    }
    QToolBar::separator {
        height: 2px;
        padding: 10px;
    }
    QToolTip { 
        color: #999999; 
        background-color: #2d2d2d; 
        border-radius: 5px; 
        padding: 5px; 
        border: 0px solid white; 
    }
    QDockWidget {
        border: 1px solid #000000;
        titlebar-close-icon: url(:icons/svg/material/outlined/Content/clear.svg);
        titlebar-normal-icon: url(:icons/svg/material/outlined/Content/add.svg);
    }
    QDockWidget::QTabsWidget {
        border: 1px solid #000000;
    }
    QDockWidget::close-button {
        icon-size: 0px;
        display: none;
    }
    QDockWidget::float-button {
        icon-size: 0px;
        display: none;
    }
    QDockWidget::title {
        text-align: center;
        spacing: 3px; /* spacing between items in the tool bar */
        background: #2a2a2a;
        padding: 15px;
        border-radius: 5px;
    }
    QDockWidget::QtabBar{
        background: #2a2a2a;
        border: 1px solid #2a2a2a;
        qproperty-drawBase: 0; /* kill top border style! yusss */
    }

    QTabBar {
        qproperty-drawBase: 0; /* kill top border style! yusss */
    }

    QTabBar:tab { 
        border: 0px solid #1d1d1d;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        min-width: 20px;
        padding-left: 20px;
        padding-right: 20px;
        padding-top: 5px;
        padding-bottom: 5px;
        background-color: #2a2a2a;
    }
    QTabBar:tab:selected, QTabBar:tab:hover {
        background-color: #2a2a2a;
    }
    QTabBar:tab:selected {
        border-bottom: 1px solid #2a2a2a;
    }
    QTabBar:tab:!selected {
        margin-top: 2px; /* make non-selected tabs look smaller */
        background-color: #222222;
        color: #666666
    }


    ''')

    app.setPalette(dark_palette)
    main_win = mainWindow()
    main_win.setWindowModified(True)
    main_win.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QTabWidget.North)
    # Cool, but can't be fucked making a custom menu at the moment:
    # main_win.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    main_win.show()
    sys.exit(app.exec_())  
    