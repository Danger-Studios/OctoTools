import sys
from PySide2.QtWidgets import QComboBox, QVBoxLayout, QWidget, QApplication, QStyledItemDelegate


def create_combobox():
    combo = QComboBox()
    # push to delegate for styling the items
    combo.setItemDelegate(QStyledItemDelegate(combo))
    combo.setStyleSheet(kombostylez)
    # Arry of pokemon
    pokemon = ["Bulbasaur", "Charmander", "Squirtle", "Pikachu", "Eevee", "Jigglypuff", "Snorlax", "Mewtwo", "Mew", "Clefable", "Vulpix", "Sandshrew", "Sandslash","Clefairy","Jigglypuff", "Golbat","Gloom", "Parasect"  ]
    combo.addItems(pokemon)
    return combo

kombostylez = '''

    /* main style */
    QComboBox {
        background-color: #3d3d3d;
        color: #888888;
        border: 1px solid #3a3a3a;
        border-radius: 5px;
        padding: 20px 20px 20px 30px;
        font-size: 21px;
        font-family: "Monospace";
        min-width: 6em;
    }

    /* Dropdown button thingy */
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        padding: 15px;
        width: 30px;
        font-size: 21px;
        font-family: "Monospace";
        border-left-width: 1px;
        border-left-color: #2d2d2d;
        border-left-style: solid;
        border-radius: 0px 5px 5px 0px;
    }

    QComboBox::down-arrow {
        image: url(down_arrow.png);
    }

    /* Items list */
    QComboBox QAbstractItemView {
        color: #888888;
        background-color: #1d1d1d;
        outline: none;
        padding: 25px;
    }

    /* Items individual */
    QComboBox QAbstractItemView::item {
        border: none;
        padding: 20px;
        margin-right: 35px;
    }

    /* Items individual selected*/
    QComboBox QAbstractItemView::item:selected {
        background-color: #2d2d2d;
        color: #ffffff;
        border-radius: 5px;
    }

    /* Scrollbar */
    QComboBox QScrollBar:vertical {
        background-color: black;
        width: 15px;
        margin: 0px 0px 0px 0px;
        outline: none;
        border-radius: 5px;
    }

    QComboBox QScrollBar::handle:vertical {
        background: #2d2d2d;
    }

    QComboBox QScrollBar::add-line:vertical {
        background: #1d1d1d;
    }

'''


# -------------------------------------/  Make an app /----------------------------------------------


# construct a QApplication 
app = QApplication(sys.argv)

# create a combobox
combo = create_combobox()
combo.setStyleSheet(kombostylez)


# create a widget and set the layout
widget = QWidget()
layout = QVBoxLayout()
layout.addWidget(combo)
#set size of the widget
widget.resize(600, 100)
widget.setLayout(layout)
widget.setWindowTitle("Choose Your Pokemon")
widget.setStyleSheet(
    '''
    QWidget {
        background-color: #2d2d2d;
        color: #ffffff;
        font-size: 21px;
        font-family: "Monospace";
    }
    '''
)

widget.show()
sys.exit(app.exec_())

