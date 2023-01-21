
from faulthandler import disable
import sys
import os
import base64
import json
from tkinter.ttk import Progressbar
import traceback
import webbrowser
from PySide2 import QtWidgets, QtNetwork, QtCore, QtGui, QtSvg

# get path of script and add to sys.path
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

# Add fonts to the font database
# fontDatabase = QtGui.QFontDatabase()
# try:
#     fontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), "fonts", "fa6_free_Regular-400.otf"))
#     print ('\n[>] -----------------------------------------------------------------')
#     print ('\n[>] Loaded fonts')
# except:
#     print ('[>] Failed to load fonts')



class OctoSearch(QtCore.QObject):
    def __init__(self, parent=None):
        super(OctoSearch, self).__init__(parent)

        #--------------------------------------------#
        # Connect to api

        print(r"""
           ____  ________________      __________  ____  __   _____
          / __ \/ ____/_  __/ __ \    /_  __/ __ \/ __ \/ /  / ___/
         / / / / /     / / / / / /_____/ / / / / / / / / /   \__ \
        / /_/ / /___  / / / /_/ /_____/ / / /_/ / /_/ / /______/ /
        \____/\____/ /_/  \____/     /_/  \____/\____/_____/____/

        """)
        print('[>] Connecting to OctoBoards...')
        
        try:
            from . import OctoConnect
            self.ob = OctoConnect.Client(
                'https://octoboards.danger.studio/jsonrpc.php',
                'danger',
                'd7ca56c54bf6fec3f5470527d3f7e367a1536ca9cb26ef9fe93addda40e9'
            )
        except:
            print('[>] oh no, check your credientials?')
            print('[>] ERROR:\n', traceback.format_exc())

        print('[>] Connected.')
        print('[>] Getting Data...\n')

        #--------------------------------------------#
        # Connect to OctoBoards


        print('[>] Getting Zone...')
        self.zone = self.ob.getTimezone()
        print('[>] Getting User...')
        self.user = self.ob.getMe()
        print('[>] Getting Shows...')
        shows = self.ob.getAllProjects()
        print('[>] Building Schema:')
        self.showsArr = {'SHOWS': []}

        # get shot names
        for show in shows:
            show_id = show['id']
            show_name = show['name']
            self.showsArr['SHOWS'].append({show_name: []})
            seqs = self.ob.getActiveSwimlanes(project_id=show_id)
            shots = self.ob.getAllTasks(project_id=show_id) 
            shots_status = self.ob.getColumns(project_id=show_id)
            print('\n../'+show_name)
            
            # get seq names
            for seq in seqs:
                seq_name = seq['name']
                seq_id = seq['id']
                
                # append seqs to array under show
                for show in self.showsArr['SHOWS']:
                    if show_name in show:
                        show[show_name].append({seq_name: []})
                        print('    |_'+seq_name)
                        
                        # append shots to array under seqs
                        for seq in show[show_name]:
                            if seq_name in seq:
                                for shot in shots:
                                    if shot['swimlane_id'] == seq_id:
                                        shot_name = shot['title']
                                        shot_id = shot['id']
                                        shot_status_id = shot['column_id']
                                        seq[seq_name].append({shot_name: []})
                                        seq[seq_name].sort(key=lambda x: list(x.keys())[0])
                                        shot_attribs = self.ob.getTask(task_id=shot_id)
                                        shot_meta = self.ob.getTaskMetadata(task_id=shot_id)
                                        shot_tasks = self.ob.getAllSubtasks(task_id=shot_id)
                                        shot_thumbs = self.ob.getAllTaskFiles(task_id=shot_id)
                                        print('      |_'+shot_name)

                                        # append attributes to tasks
                                        for shot in seq[seq_name]:
                                            if shot_name in shot:
                                                print('        |_Loading data...')
                                                # get shot status 
                                                for status in shots_status:
                                                    if status['id'] == shot_status_id:
                                                        shot[shot_name].append({'status': status['title']})  
                                                        break

                                                shot[shot_name].append({'metadata': shot_meta})
                                                shot[shot_name].append({'attributes': shot_attribs})
                                                shot[shot_name].append({'tasks': shot_tasks})
                                                if shot_thumbs:
                                                    for image in shot_thumbs:
                                                        if shot_thumbs[0] and image['is_image']:
                                                            print('        |_Loading Thumbnail [id:' + str(image['id']) + '] ')
                                                            shot[shot_name].append({'thumbnail': self.ob.downloadTaskFile(file_id=image['id'])})
                                                        else:
                                                            shot[shot_name].append({'thumbnail': 'none'})


class OctoBrowser(QtWidgets.QWidget):
    
    shows = {'SHOWS': []}
    zone = ''
    user = {'username': 'none'}
    rebuildJson = 0
    showJson = 'X:/Shared drives/Pipeline/tools/OctoTools/core/scripts/python/OctoBrowser/shotData.json'
    
    def __init__(self):
        #--------------------------------------------#
        # Init
        
        print('\n[>] OctoBrowser Activated')
        self.gui()
        

    def loadData (self):
        #--------------------------------------------#
           
        if self.rebuildJson == 0:
            print('\n[>] Loading Data...')    
            with open(self.showJson) as json_file:
                self.shows = json.load(json_file)
            print('\n[>] Done.')  
            #print('\n[>] SHOW SCHEMA:\n', json.dumps(self.shows, indent=4))
            
        
        else:
            print('\n[>] Fetching Data...')
            # get data from OctoConnect with doRebuild()
            request = OctoSearch()
            shows = request.showsArr
            zone = request.zone
            user = request.user
            # Write data to file
            with open(self.showJson, 'w') as f:
                self.shows = json.dump(shows, f, indent=4)
            print('\n[>] Done.') 
    
        
    def gui(self):
        
        #--------------------------------------------#
        # init GUI

        super(OctoBrowser, self).__init__()
        self.setWindowTitle('OctoBrowser')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QtGui.QIcon('icon.png'))


        #--------------------------------------------#
        # Create UI Widgets

        showMenu = QtWidgets.QComboBox()
        showMenu.addItem('SHOW')
        showMenu.setMaximumSize(320, 40)

        seqMenu = QtWidgets.QComboBox()
        seqMenu.addItem('SEQ')
        seqMenu.setMaximumSize(320, 40)

        shotMenu = QtWidgets.QComboBox()
        shotMenu.addItem('SHOT')
        shotMenu.setMaximumSize(320, 40)

        info = QtWidgets.QTextEdit()
        info.setMaximumSize(320, 50)
        info.setReadOnly(True)
        info.setText('SHOW / SHOT / TASK')
        info.setFrameStyle(QtWidgets.QFrame.NoFrame)
        info.setFrameShadow(QtWidgets.QFrame.Plain)
        info.setStyleSheet('''
            background-color: #111; 
            text-align: center;
            color: #fff; 
            font-weight: bold;
            padding: 5px;
            padding-left: 10px;
            border: 1px solid #444;
            border-radius: 5px;
            shadow: 100px 100px 100px 100px #fff;
            border-opacity: 0.5;
        ''')

        user_info = QtWidgets.QTextEdit('USER: ' + self.user['username'])
        user_info.setMaximumSize(320, 40)
        user_info.setStyleSheet("background-color: #222; color: #fff;")

        zone_info = QtWidgets.QTextEdit('ZONE: ' + self.zone)
        zone_info.setMaximumSize(320, 40)
        zone_info.setStyleSheet("background-color: #222; color: #fff;")

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMaximumSize(320, 40)
        self.progress_bar.setMinimum(0)
        style = """
        QProgressBar {
            border: 1px solid #444;
            border-radius: 5px;
            text-align: center;
            background-color: #222;
            color: #555;
        }                       
        QProgressBar::chunk {
            background-color: #05B8CC;
            width: 20px;
        }
        """
        self.progress_bar.setStyleSheet(style)

        pixmap = QtGui.QPixmap(path+'/icons/octo-tools.svg').scaled(320, 200, QtCore.Qt.KeepAspectRatio)
        thumbnail = QtWidgets.QLabel('THUMBNAIL')
        thumbnail.setPixmap(pixmap)
        thumbnail.setMaximumSize(320, 240)
        thumbnail.setMinimumSize(320, 240)
        #thumbnail.setContentsMargins(10, 20, 10, 20)
        thumbnail.setStyleSheet('''
            background-color: #111; 
            color: #fff; 
            border: 1px solid #444;
            /*border-bottom: 50px solid #444;*/
            border-radius: 5px;
            border-color: #444;
        ''')
        thumbnail.setAlignment(QtCore.Qt.AlignCenter)
        
        rebuild_checkbox = QtWidgets.QCheckBox("Rebuild Schema", self)
        rebuild_checkbox.setChecked(False)

        meta_tree_label = QtWidgets.QTextEdit('STATUS')
        meta_tree_label.setMaximumSize(90, 40)
        # wrap text
        meta_tree_label.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        meta_tree_label.setReadOnly(True)
        meta_tree_label.setFrameStyle(QtWidgets.QFrame.NoFrame)
        meta_tree_label.setStyleSheet("padding-left: 5px; background-color: #333; color: #111;border: 0px solid #444; border-radius: 5px;")

        shot_meta_tree = QtWidgets.QTreeWidget()
        shot_meta_tree.setColumnCount(2)
        shot_meta_tree.setMaximumSize(6000, 1000)
        shot_meta_tree.setHeaderHidden(True)
        shot_meta_tree.setFrameStyle(QtWidgets.QFrame.NoFrame)
        shot_meta_tree.setFrameShadow(QtWidgets.QFrame.Plain)
        shot_meta_tree.setRootIsDecorated(False)
        # set column width to resize to contents
        shot_meta_tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        shot_meta_tree.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        shot_meta_tree.setWordWrap(True)
        shot_meta_tree.setStyleSheet('''
            QTreeWidget{
                /*background-color: #222;*/
                color: #fff;
                border: 1px solid #444;
                border-radius: 5px;
            }

            QTreeWidget::item {
                padding: 10px;
                background-color: #222;
                color: #fff;
                border: 1px solid #444;
                border-radius: 5px;
            }
            QTreeWidget::item:selected {
                
                background-color: #444;
                color: #fff;
                border: 1px solid #333;
                border-radius: 5px;
            }
            QTreeWidget::item:hover {
                background-color: #111;
                color: #fff;
                border: 1px solid #444;
                border-radius: 5px;
            }
        ''')
        
        attrib_tree_label = QtWidgets.QTextEdit('SHOT ATTRIBUTES')
        attrib_tree_label.setMaximumSize(6000, 40)
        attrib_tree_label.setReadOnly(True)
        attrib_tree_label.setFrameStyle(QtWidgets.QFrame.NoFrame)
        attrib_tree_label.setStyleSheet("padding-left: 5px; background-color: #333; color: #111;border: 0px solid #444; border-radius: 5px;")
        
        shot_attrib_tree = QtWidgets.QTreeWidget()
        shot_attrib_tree.setMaximumSize(6000, 200)
        shot_attrib_tree.setColumnCount(2)
        shot_attrib_tree.setHeaderHidden(True)
        shot_attrib_tree.setRootIsDecorated(False)
        shot_attrib_tree.setFrameStyle(QtWidgets.QFrame.NoFrame)
        shot_attrib_tree.setFrameShadow(QtWidgets.QFrame.Plain)
        # set column width to resize to contents
        shot_attrib_tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        shot_attrib_tree.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        shot_attrib_tree.setWordWrap(True)
        shot_attrib_tree.setStyleSheet('''
            QTreeWidget::item {
                padding: 10px;
                background-color: #222;
                color: #fff;
                border: 1px solid #444;
                border-radius: 5px;
            }
            QTreeWidget::item:selected {
                
                background-color: #444;
                color: #fff;
                border: 1px solid #333;
                border-radius: 5px;
            }
            QTreeWidget::item:hover {
                background-color: #111;
                color: #fff;
                border: 1px solid #444;
                border-radius: 5px;
            }
        ''')

        # Create collapsible QTreeWidget
        task_tree_Widget = QtWidgets.QTreeWidget()
        task_tree_Widget.setColumnCount(2)
        task_tree_Widget.setMaximumSize(6000, 1000)
        task_tree_Widget.setHeaderHidden(True)
        #task_tree_Widget.setHeaderLabels(['Task', 'Status'])
        task_tree_Widget.setIndentation(20)
        #task_tree_Widget.setSortingEnabled(True)
        task_tree_Widget.setAnimated(True)
        task_tree_Widget.setAllColumnsShowFocus(True)
        # set icons for items in QTreeWidget
        task_tree_Widget.setIconSize(QtCore.QSize(32, 32))
        task_tree_Widget.setUniformRowHeights(True)
        task_tree_Widget.setRootIsDecorated(True)
        # set column width to resize to contents
        task_tree_Widget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        task_tree_Widget.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        task_tree_Widget.setWordWrap(True)
        # task_tree_Widget.setAlternatingRowColors(True)
        # set row colors
        task_tree_Widget.setStyleSheet('''  
            QTreeWidget::item {
                padding: 10px;
                background-color: #222; 
                color: #fff; 
                border: 1px solid #444; 
                border-radius: 5px;
                } 
            QTreeWidget::item:selected {
                background-color: #444; 
                color: #fff; 
                border: 1px solid #333; 
                border-radius: 5px;
                }
            QTreeWidget::item:selected:active {
                background-color: #444;
                color: #fff;
                border: 1px solid #333;
                border-radius: 5px;
                }
            QTreeWidget::item:hover {
                background-color: #111;
                color: #fff;
                border: 1px solid #444;
                border-radius: 5px;
                }
            QTreeWidget::item:open {
                background-color: #111;
                color: #fff;
                border: 1px solid #444;
                border-radius: 5px;
                }
        ''')

        # A QTreeWidget to display the show tree
        show_tree_Widget = QtWidgets.QTreeWidget()
        show_tree_Widget.setColumnCount(1)
        show_tree_Widget.setMaximumSize(6000, 1000)
        show_tree_Widget.setHeaderHidden(True)
        show_tree_Widget.setIndentation(20)
        show_tree_Widget.setAnimated(True)
        show_tree_Widget.setAllColumnsShowFocus(True)
        show_tree_Widget.setIconSize(QtCore.QSize(32, 32))
        show_tree_Widget.setUniformRowHeights(True)
        show_tree_Widget.setRootIsDecorated(True)
        show_tree_Widget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        show_tree_Widget.setWordWrap(True)
        show_tree_Widget.setStyleSheet('''
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

        
        pull_shot_btns = QtWidgets.QPushButton("LOAD SHOT", self)
        #pull_btn = QtWidgets.QPushButton("PULL ALL SHOTS", self)
        push_btn = QtWidgets.QPushButton("PUSH UPDATES", self)

        
        
        #--------------------------------------------#  
        # Menu Functions

        
        # Rebuild Schema checkbox (download from octoboards)
        def doRebuild():
            if rebuild_checkbox.isChecked():
                self.rebuildJson = 1
            else:
                self.rebuildJson = 0
            print('[>] Rebuild Schema:', self.rebuildJson)
        rebuild_checkbox.stateChanged.connect(doRebuild)

        # Update UI on menu change
        def updateInfo():
            # Clear stuff
            thumbnail.clear()
            info.clear()
            shot_meta_tree.clear()
            shot_attrib_tree.clear()
            task_tree_Widget.clear()

            # Set stuff
            user_info.setText('USER: ' + self.user['username'])
            zone_info.setText('ZONE: ' + self.zone)

            # get selected item once
            shot = shotMenu.currentText()
            seq = seqMenu.currentText()
            show = showMenu.currentText()

            # update info
            info.setText(show+' / '+seq+' / '+shot) 

            # Update shot data from response
            for show in self.shows['SHOWS']:
                if showMenu.currentText() in show:
                    for seq in show[showMenu.currentText()]:
                        if seqMenu.currentText() in seq:
                            for shot in seq[seqMenu.currentText()]:
                                if shotMenu.currentText() in shot:
                                    for data in shot[shotMenu.currentText()]:
                                        for key, value in data.items():      
                                            
                                            # add status to info
                                            if key == 'status':
                                                if value:
                                                    meta_tree_label.setText(value)

                                            if key == 'tasks':

                                                # get 'title' key and add to tree as parent get remaining keys and add as children
                                                    for task in value:
                                                        #task_tree_Widget.clear()
                                                        task_item = QtWidgets.QTreeWidgetItem(task_tree_Widget)
                                                        task_item.setText(0, task['title'])
                                                        task_item.setIcon(0, QtGui.QIcon(path+'/icons/task.svg'))
                                                        task_item.setExpanded(False)
                                                        for key, value in task.items():
                                                            if key != 'title':
                                                                itemArr = ['status', 'status_name', 'username', 'time_estimated', 'time_spent', 'id']
                                                                if key in itemArr:  
                                                                    task_subitem = QtWidgets.QTreeWidgetItem(task_item)
                                                                    task_subitem.setText(0, key)
                                                                    task_subitem.setText(1, str(value))
                                                                    task_subitem.setIcon(0, QtGui.QIcon(path+'/icons/task.svg'))
                                                                    task_subitem.setExpanded(False)
                                                                    task_subitem.setFlags(task_subitem.flags() | QtCore.Qt.ItemIsEditable)
                                                                    task_subitem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                                                                    task_tree_Widget.addTopLevelItem(task_subitem)
                                                        task_tree_Widget.addTopLevelItem(task_item)
                                                    task_tree_Widget.resizeColumnToContents(0)
                                                    task_tree_Widget.resizeColumnToContents(1)
                                                                
                                                                    
                                            if key == 'thumbnail':
                                                # get the thumbnails
                                                if value:
                                                    pixmap = QtGui.QPixmap()
                                                    file_decoded = base64.urlsafe_b64decode(value)
                                                    pixmap.loadFromData(file_decoded)
                                                    pixmap = pixmap.scaled(320, 200, QtCore.Qt.KeepAspectRatio)
                                                    thumbnail.setPixmap(pixmap)
                                                elif value == "":
                                                    pixmap = QtGui.QPixmap(path+'/icons/octo-tools.svg').scaled(320, 200, QtCore.Qt.KeepAspectRatio)
                                                    thumbnail.setPixmap(pixmap)
                                            
                                            if key == 'metadata':
                                                for key, value in data['metadata'].items():
                                                    item = QtWidgets.QTreeWidgetItem(shot_meta_tree)
                                                    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                                                    item.setText(0, key)
                                                    item.setText(1, str(value))
                                            
                                            if key == 'attributes':
                                                for key, value in data['attributes'].items():
                                                    
                                                    # if key is in item array, add to tree
                                                    itemArr = ['title', 'url', 'description', 'color_id', 'date_due', 'time_estimated', 'time_spent', 'priority']
                                                    if key in itemArr:
                                                        item = QtWidgets.QTreeWidgetItem(shot_attrib_tree)
                                                        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                                                        item.setText(0, key)
                                                        item.setText(1, str(value))
                                                        
                                                        if key == 'color_id':
                                                            print('color_id')
                                                            # set thumbnail border color to value
                                                            thumbnail.setStyleSheet('''
                                                                background-color: #111; 
                                                                color: #fff; 
                                                                border: 1px solid #444;
                                                                border-radius: 5px;
                                                                border-color: '''+value+''';
                                                                shadow: 100px 100px 100px 100px #fff;
                                                                border-opacity: 0.5;
                                                            ''')
                                                            # set shot status color to value
                                                            meta_tree_label.setStyleSheet('''
                                                                background-color: '''+value+'''; 
                                                                text-align: center;
                                                                color: #000; 
                                                                font-weight: bold;
                                                                padding-top: 2px;
                                                                padding-left: 10px;
                                                                border: 1px solid #444;
                                                                border-radius: 5px;
                                                                border-color: '''+value+''';
                                                                shadow: 100px 100px 100px 100px #fff;
                                                                border-opacity: 0.5;
                                                            ''')
                                                            # set info color to value
                                                            info.setStyleSheet('''
                                                                background-color: #111; 
                                                                text-align: center;
                                                                color: '''+value+'''; 
                                                                font-weight: bold;
                                                                padding: 5px;
                                                                padding-left: 10px;
                                                                border: 1px solid #444;
                                                                border-radius: 5px;
                                                                shadow: 100px 100px 100px 100px #fff;
                                                                border-opacity: 0.5;
                                                            ''')                                                           
                                                    
                                                        # if key is a url add link
                                                        if key == 'url':
                                                            print(value)
                                                            print('url')
                                                            link = QtWidgets.QTreeWidgetItem(shot_attrib_tree)
                                                            link.setFlags(link.flags() | QtCore.Qt.ItemIsEditable)
                                                            link.setText(0, 'Shot Link')
                                                            link.setText(1, '<a href="'+str(value)+'">'+str(value)+'</a>')
                                                            shot_attrib_tree.setItemWidget(link, 1, QtWidgets.QPushButton('View', self))
                                                            shot_attrib_tree.itemWidget(link, 1).setStyleSheet('''
                                                                QPushButton {
                                                                    padding: 5px;
                                                                    background-color: #333;
                                                                    color: #fff;
                                                                    border: 1px solid #222;
                                                                    border-radius: 5px;
                                                                }
                                                                QPushButton:hover {
                                                                    background-color: #222;
                                                                    color: #fff;
                                                                    border: 1px solid #111;
                                                                    border-radius: 5px;
                                                                }
                                                            ''')
                                                            
                                                            # open link in browser: some bullshit going on here...
                                                            task_link = value
                                                            shot_attrib_tree.itemWidget(link, 1).clicked.connect(lambda: webbrowser.open(f'{task_link}'))

        def shotMenuFunc():
            shotMenu.clear()
            shotMenu.addItem('SHOT')
            for show in self.shows['SHOWS']:
                if showMenu.currentText() in show:
                    for seq in show[showMenu.currentText()]:
                        if seqMenu.currentText() in seq:
                            for shot in seq[seqMenu.currentText()]:
                                shotMenu.addItem(list(shot.keys())[0])
            shotMenu.currentIndexChanged.connect(updateInfo)

        def seqMenuFunc():
            seqMenu.clear()
            seqMenu.addItem('SEQ')
            for show in self.shows['SHOWS']:
                if showMenu.currentText() in show:
                    for seq in show[showMenu.currentText()]:
                        seqMenu.addItem(list(seq.keys())[0])
            seqMenu.currentIndexChanged.connect(shotMenuFunc)

        def showMenuFunc():
            showMenu.clear()
            showMenu.addItem('SHOW')
            for show in self.shows['SHOWS']:
                showMenu.addItem(list(show.keys())[0])
            showMenu.currentIndexChanged.connect(seqMenuFunc)
        
        # Enable pull_shot_btns
        def build():
            self.loadData()  
        pull_shot_btns.clicked.connect(build)

        
        # Updte the show_tree_Widget with self.shows data
        def updateShowTree(self):

            show_tree_Widget.clear()
            build()
            showMenuFunc()

            show_icon = QtGui.QIcon(path+'/icons/show.svg').pixmap(24, 24)
            seq_icon = QtGui.QIcon(path+'/icons/seq.svg').pixmap(24, 24)
            shot_icon = QtGui.QIcon(path+'/icons/shot.svg').pixmap(24, 24)
            task_icon = QtGui.QIcon(path+'/icons/task.svg').pixmap(24, 24)
            link_icon = QtGui.QIcon(path+'/icons/link.svg').pixmap(24, 24)

            # get shows from self.shows and add to tree as parent
            for show in self.shows['SHOWS']:
                show_parent = QtWidgets.QTreeWidgetItem(show_tree_Widget)
                show_parent.setText(0, list(show.keys())[0])
                show_parent.setIcon(0, show_icon)
                show_parent.setFlags(show_parent.flags() | QtCore.Qt.ItemIsEditable)
                # add link button
                show_tree_Widget.setItemWidget(show_parent, 0, QtWidgets.QPushButton('', self))
                show_tree_Widget.itemWidget(show_parent, 0).setIcon(link_icon)
                show_tree_Widget.itemWidget(show_parent, 0).clicked.connect(lambda: webbrowser.open(f'{self.shows}'))
                show_tree_Widget.itemWidget(show_parent, 0).setStyleSheet('''
                    QPushButton {
                        padding: 5px;
                        margin-left: 240px;
                        background-color: #111;
                        color: #fff;
                        border: 1px solid #222;
                        border-radius: 5px;
                        align: right;
                    }
                    QPushButton:hover {
                        background-color: #005950;
                        color: #fff;
                        border: 1px solid #111;
                        border-radius: 5px;
                    }
                ''')
                # get sequences from self.shows and add to tree as child
                for seq in show[list(show.keys())[0]]:
                    seq_child = QtWidgets.QTreeWidgetItem(show_parent)
                    seq_child.setText(0, list(seq.keys())[0])
                    seq_child.setIcon(0, seq_icon)
                    seq_child.setFlags(seq_child.flags() | QtCore.Qt.ItemIsEditable)
                    show_tree_Widget.addTopLevelItem(seq_child)
                    # set icon on expended state
                    
              
                    # get shots from self.shows and add to tree as child
                    for shot in seq[list(seq.keys())[0]]:
                        shot_child = QtWidgets.QTreeWidgetItem(seq_child)
                        shot_child.setText(0, list(shot.keys())[0])
                        shot_child.setIcon(0, shot_icon)
                        shot_child.setFlags(shot_child.flags() | QtCore.Qt.ItemIsEditable)
                        show_tree_Widget.addTopLevelItem(shot_child)
                        # add link button
                        show_tree_Widget.setItemWidget(shot_child, 0, QtWidgets.QPushButton('', self))
                        show_tree_Widget.itemWidget(shot_child, 0).setIcon(link_icon)
                        show_tree_Widget.itemWidget(shot_child, 0).clicked.connect(lambda: webbrowser.open(f'{self.shows}'))
                        show_tree_Widget.itemWidget(shot_child, 0).setStyleSheet('''
                            QPushButton {
                                padding: 5px;
                                margin-left: 200px;
                                background-color: #111;
                                color: #fff;
                                border: 1px solid #222;
                                border-radius: 5px;
                                align: right;
                            }
                            QPushButton:hover {
                                background-color: #005950;
                                color: #fff;
                                border: 1px solid #111;
                                border-radius: 5px;
                            }
                        ''')

                        # get tasks from self.shows and add to tree as child
                        for tasks in shot[list(shot.keys())[0]]:
                            for key, value in tasks.items():            
                                if key == 'tasks':
                                    for task in value:  
                                        task_child = QtWidgets.QTreeWidgetItem(shot_child)
                                        # add icon to task
                                        task_child.setText(0, task['title'])
                                        task_child.setIcon(0, task_icon)
                                        task_child.setFlags(task_child.flags() | QtCore.Qt.ItemIsEditable)
                                        show_tree_Widget.addTopLevelItem(task_child)
                                        # add tri-state checkbox
                                        show_tree_Widget.setItemWidget(task_child, 0, QtWidgets.QCheckBox('', self))
                                        show_tree_Widget.itemWidget(task_child, 0).setCheckState(QtCore.Qt.Unchecked)
                                        show_tree_Widget.itemWidget(task_child, 0).setStyleSheet('''
                                            QCheckBox {
                                                padding: 5px;
                                                margin-left: 180px;
                                                color: #fff;
                                                border-radius: 3px;
                                                align: right;
                                            }
                                            QCheckBox:hover {
                                                background-color: #005950;
                                                color:  #fff;
                                                border-radius: 3px;
                                            }
                                        ''')

        
        # Load the show tree
        updateShowTree(self)


        # push_btn on click
        def update():
            print('[>] Pushing...')
            print('[>] Done.')
        push_btn.clicked.connect(update)
        
        
        #--------------------------------------------#
        # Add to Menus to UI
        
        self.setWindowTitle("OctoBrowser")
        self.setWindowIcon(QtGui.QIcon('X:/Shared drives/Pipeline/tools/OctoTools/core/config/Icons/favicon.png'))
        self.setStyleSheet("background-color: #222; color: #ccc;")
        gui = QtWidgets.QHBoxLayout(self)
        gui.setContentsMargins(8,0,8,10)

        
        # Shot show_tree_Widget gui
        shot_tree_group = QtWidgets.QGroupBox("SHOWS", self, flat=True)
        shot_tree_group.setStyleSheet("background-color: #333; color: #fff;")
        shot_tree_group.setMaximumWidth(1000)

        shot_tree_layout = QtWidgets.QVBoxLayout(shot_tree_group)
        shot_tree_layout.setSpacing(20)
        shot_tree_layout.setMargin(20)

        shot_tree_layout.addWidget(show_tree_Widget)


        # Shot selection gui
        shot_select_group = QtWidgets.QGroupBox("SHOT", self, flat=True)
        shot_select_group.setStyleSheet("background-color: #333; color: #fff;")
        #shot_select_group.setMaximumSize(400, 1000)
        shot_select_group.setMaximumWidth(400)

        shot_select_layout = QtWidgets.QGridLayout(shot_select_group)
        shot_select_layout.setSpacing(20)
        shot_select_layout.setMargin(20)
        
        shot_select_layout.addWidget(info)
        shot_select_layout.addWidget(thumbnail)
        shot_select_layout.addWidget(user_info)
        shot_select_layout.addWidget(zone_info)
        shot_select_layout.addWidget(rebuild_checkbox)
        shot_select_layout.addWidget(pull_shot_btns)
        shot_select_layout.addWidget(showMenu)
        shot_select_layout.addWidget(seqMenu)
        shot_select_layout.addWidget(shotMenu)
        shot_select_layout.addWidget(self.progress_bar)

        # Shot metadata gui
        metadata_group = QtWidgets.QGroupBox("INFO", self, flat=True)
        metadata_group.setStyleSheet("background-color: #333; color: #fff;")
       #metadata_group.setMaximumSize(600, 1000)
        metadata_group.setMaximumWidth(1000)

        metadata_layout = QtWidgets.QVBoxLayout(metadata_group)
        metadata_layout.setSpacing(20)
        metadata_layout.setMargin(20)

        metadata_layout.addWidget(meta_tree_label)
        metadata_layout.addWidget(shot_meta_tree)
        metadata_layout.addWidget(attrib_tree_label)
        metadata_layout.addWidget(shot_attrib_tree)
        metadata_layout.addWidget(push_btn)

        # add shot tasks to gui layout
        shot_tasks_group = QtWidgets.QGroupBox("TASKS", self, flat=True)
        shot_tasks_group.setStyleSheet("background-color: #333; color: #fff;")
        #shot_tasks_group.setMaximumSize(600, 1000)

        task_layout = QtWidgets.QVBoxLayout(shot_tasks_group)
        task_layout.setSpacing(20)
        task_layout.setMargin(20)
        task_layout.addWidget(task_tree_Widget)
    
      
        #--------------------------------------------#
        # Add UI groups to Main Window
        #gui.addSpacing(20)
        gui.addWidget(shot_tree_group)
        gui.addWidget(shot_select_group)
        gui.addWidget(metadata_group)
        gui.addWidget(shot_tasks_group)


        #--------------------------------------------#
        # Show Window
        
        self.setLayout(gui)




# run app in standalone mode
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = OctoBrowser()
    window.show()
    sys.exit(app.exec_())