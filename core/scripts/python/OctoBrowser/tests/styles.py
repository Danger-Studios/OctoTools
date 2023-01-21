tree_widget = '''

/**********************************************
QTreeView | Styling 
**********************************************/

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

'''