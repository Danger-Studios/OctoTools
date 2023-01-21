# Modules
# ------------------------------------------------------------------------------
import sys
from PySide2 import QtGui, QtCore, QtSvg, QtWidgets
from random import randint

# widget
# ------------------------------------------------------------------------------
class Example(QtWidgets.QWidget):

    def __init__(self,):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        # formatting
        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle("Example")

        # widgets
        self.itemList = QtGui.QTreeWidget()
        self.itemList.setItemsExpandable(True)
        self.itemList.setAnimated(True)
        self.itemList.setItemsExpandable(True)
        self.itemList.setColumnCount(2)
        self.itemList.setHeaderLabels(['', ''])

        # Load the svg
        renderer = QtSvg.QSvgRenderer('D:/DEV/TMP/vimeo.svg')        
        # Prepare a QImage with desired characteritisc
        self.orig_svg = QtGui.QImage(500, 500, QtGui.QImage.Format_ARGB32);    
        # Get QPainter that paints to the image
        painter = QtGui.QPainter(self.orig_svg);
        renderer.render(painter);

        # add items
        color0 = QtGui.QColor( 255, 35, 35 )
        item0 = QtGui.QTreeWidgetItem(self.itemList, ['testing', ''])
        item0.setIcon(1, self.icon_colored( color0 ))  # 1 - we set image for second colomn

        color1 = QtGui.QColor( 32, 255, 35 )
        item1 = QtGui.QTreeWidgetItem(self.itemList, ['testing', ''])
        item1.setIcon(1, self.icon_colored( color1 ) )  # 1 - we set image for second colomn


        pixmap = QtGui.QPixmap.fromImage( self.orig_svg )
        self.lbl = QtGui.QLabel(self)
        self.lbl.setPixmap(pixmap)

        self.button = QtGui.QPushButton("rand color")

        self.button.clicked.connect( self.changeColor )

        # layout
        self.mainLayout = QtGui.QVBoxLayout(self)
        self.mainLayout.addWidget(self.button)
        self.mainLayout.addWidget(self.itemList)
        self.mainLayout.addWidget(self.lbl)
        self.show()

    @QtCore.Slot()
    def changeColor( self ):

        r = randint(0,255)
        g = randint(0,255)
        b = randint(0,255)

        # Copy the image
        new_image = self.orig_svg.copy()

        # We are going to paint a plain color over the alpha
        paint = QtGui.QPainter()
        paint.begin( new_image )
        paint.setCompositionMode( QtGui.QPainter.CompositionMode_SourceIn )
        paint.fillRect( new_image.rect(), QtGui.QColor( r, g, b ) )

        paint.end()

        self.lbl.setPixmap( QtGui.QPixmap.fromImage(new_image) )

    def icon_colored( self, color ):

        # Copy the image
        new_image = self.orig_svg.copy()

        # We are going to paint a plain color over the alpha
        paint = QtGui.QPainter()
        paint.begin( new_image )        
        paint.setCompositionMode( QtGui.QPainter.CompositionMode_SourceIn )       
        paint.fillRect( new_image.rect(), color )        
        paint.end()

        return QtGui.QIcon( QtGui.QPixmap.fromImage( new_image ) )


app = QtWidgets.QApplication(sys.argv)
ex = Example()
sys.exit(app.exec_())