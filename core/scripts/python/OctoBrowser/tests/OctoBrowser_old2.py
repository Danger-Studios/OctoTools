
import sys
import os
import base64
import json
import time
from tkinter.ttk import Progressbar
import traceback
import webbrowser
from PySide2 import QtWidgets, QtNetwork, QtCore, QtGui
import timeit

class OctoConnect(QtCore.QObject):
    def __init__(self, getThumbnail):     
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

        shows = self.ob.getAllProjects()
        self.zone = self.ob.getTimezone()
        self.user = self.ob.getMe()

        print('[>] USER:', self.user['username'])
        print('[>] ZONE:', self.zone)

        # Search keys function
        def search(json_object, target_key):
            if type(json_object) is dict and json_object:
                for key in json_object:
                    if key == target_key:
                        print("{}: {}".format(target_key, json_object[key]))
                    search(json_object[key], target_key)
            elif type(json_object) is list and json_object:
                for item in json_object:
                    search(item, target_key)
        
        # search(shows, 'thumbnail')
        #--------------------------------------------#

        def progressBar(anIterableItem, prefix = '', suffix = '', decimals = 1, length = 100, fill = '|', printEnd = "\r"):
            total = len(anIterableItem)
            # Progress Bar Printing Function
            def printProgressBar (iteration):
                percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
                filledLength = int(length * iteration // total)
                bar = fill * filledLength + '-' * (length - filledLength)
                print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
            # Initial Call
            printProgressBar(0)
            # Update Progress Bar
            for i, item in enumerate(anIterableItem):
                yield item
                printProgressBar(i + 1)
            # Print New Line on Complete
            print()

        #--------------------------------------------#
        # Build menu array (json style)

        self.showsArr = {'SHOWS': []}

        for show in shows:

            show_id = show['id']
            show_name = show['name']
            self.showsArr['SHOWS'].append({show_name: []})
            seqs = self.ob.getActiveSwimlanes(project_id=show_id)
            shots = self.ob.getAllTasks(project_id=show_id)
            shots_status = self.ob.getColumns(project_id=show_id)
            search_shots = self.ob.searchTasks(project_id=show_id, query='*')
            
            # print('\n[>] SHOW:', show_name)

            for seq in seqs:
                seq_name = seq['name']
                seq_id = seq['id']
                # print('[>]  |_SEQ:', seq_name)

                for show in self.showsArr['SHOWS']:
                    if show_name in show:
                        show[show_name].append({seq_name: []})

                for shot in shots:
                    if shot['swimlane_id'] == seq_id:
                        shot_name = shot['title']
                        shot_id = shot['id']
                        shot_status_id = shot['column_id']
                        shot_attribs = self.ob.getTask(task_id=shot_id)
                        shot_meta = self.ob.getTaskMetadata(task_id=shot_id)
                        shot_tasks = self.ob.getAllSubtasks(task_id=shot_id)

                        # append shots and sort shot_name by name
                        for show in self.showsArr['SHOWS']:
                            if show_name in show:
                                for seq in show[show_name]:
                                    if seq_name in seq:
                                        seq[seq_name].append({shot_name: []})
                                        seq[seq_name].sort(key=lambda x: list(x.keys())[0])
                                        # append meta data
                                        for shot in seq[seq_name]:
                                            if shot_name in shot:
                                                
                                                # get shot status 
                                                for status in shots_status:
                                                    if status['id'] == shot_status_id:
                                                        shot[shot_name].append({'status': status['title']})  
                                                        break
                                                
                                                # get shot meta data
                                                shot[shot_name].append({'metadata': shot_meta})
                                                shot[shot_name].append({'attributes': shot_attribs})
                                                shot[shot_name].append({'tasks': shot_tasks})
                                                # get shot_tasks
                                                for task in shot_tasks:
                                                    #shot[shot_name].append({'task': task['title']})
                                                    pass

                                                shot[shot_name].append({'thumbnail': ''})
                                                
                                                # get shot thumbnail
                                                if getThumbnail:
                                                    shot_images = self.ob.getAllTaskFiles(task_id=shot_id)
                                                    # append empy key for thumbnail
                                                    if shot_images:
                                                        for image in shot_images:  
                                                            if shot_images[0] and image['is_image']:
                                                                print('[>] Loading Thumbnail (id:' + str(image['id']) + ') for ' + shot_name)
                                                                shot[shot_name][3]['thumbnail'] = self.ob.downloadTaskFile(file_id=image['id'])
                                                                #shot[shot_name].append({'thumbnail': self.ob.downloadTaskFile(file_id=image['id'])})
                                                                # for i in progressBar(file_range, prefix = 'Progress:', suffix = 'Complete', length = 50):
                                                                #     # Do stuff...
                                                                #     time.sleep(0.1)
                                                                break
                                                break
                                        break
                                            
        print('[>] Done.')


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

        progress = 1

        print('[>] Getting Zone...')
        self.zone = self.ob.getTimezone()
        
        print('[>] Getting User...')
        self.user = self.ob.getMe()
        
        print('[>] Getting Shows...')
        shows = self.ob.getAllProjects()

        print('[>] Building Schema:')
        self.showsArr = {'SHOWS': []}

        # build json schema recursivly to get all data

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
                        progress = progress+1
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
                                                print('        |_Loading Attributes...')
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
    thumbnail = 0
    showJson = 'X:/Shared drives/Pipeline/tools/OctoTools/core/scripts/python/OctoBrowser/shotData.json'
    
    def __init__(self):
        #--------------------------------------------#
        # Init
        
        print('\n[>] OctoBrowser Activated')
        self.gui()
        
    
    def getData (self):
        #--------------------------------------------#
        # Connect to Octoboard

        # get data from OctoConnect with getThumbnail()
        self.request = OctoConnect(self.thumbnail)
        self.shows = self.request.showsArr
        self.zone = self.request.zone
        self.user = self.request.user

        # Write data to file
        with open('X:/Shared drives/Pipeline/tools/OctoTools/core/scripts/python/OctoBrowser/showData.json', 'w') as outfile:
            json.dump(self.shows, outfile, indent=4)
        try:
            print('\n[>] SHOW MENU:\n', json.dumps(self.shows, indent=4))
        except:
            print('[>] [ PRO-TIP ] Turn off "Pull Thumbnails" if you want to view the json response\n')

        # function Progress bar for loading data from OctoConnect
        def progressUpdate(value):

            self.progress_bar.setValue(value)
            QtWidgets.QApplication.processEvents()
            if value == 100:
                self.progressBar.hide()
                self.progressBar.setValue(0)
            
        # progressUpdate(self.progress)

    def searchData (self):
        #--------------------------------------------#
        # Connect to Octoboard
        

        if self.thumbnail == 0:
                
            with open(self.showJson) as json_file:
                self.shows = json.load(json_file)
                # print('\n[>] SHOW SCHEMA:\n', json.dumps(self.shows, indent=4))
        
        else:

            # get data from OctoConnect with getThumbnail()
            self.request = OctoSearch()
            self.shows = self.request.showsArr
            self.zone = self.request.zone
            self.user = self.request.user
            # Write data to file
            with open(self.showJson, 'w') as f:
                json.dump(self.shows, f, indent=4)
        

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
        info.setMaximumSize(320, 40)
        info.setReadOnly(True)
        info.setText('Select something...')
        info.setFrameStyle(QtWidgets.QFrame.NoFrame)
        info.setFrameShadow(QtWidgets.QFrame.Plain)

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

        pixmap = QtGui.QPixmap("X:/Shared drives/Pipeline/tools/OctoTools/core/config/Icons/favicon.png").scaled(320, 200, QtCore.Qt.KeepAspectRatio)
        thumbnail = QtWidgets.QLabel('THUMBNAIL')
        thumbnail.setPixmap(pixmap)
        thumbnail.setMaximumSize(320, 240)
        thumbnail.setMinimumSize(320, 240)
        #thumbnail.setContentsMargins(10, 20, 10, 20)
        thumbnail.setStyleSheet('''
            background-color: #000; 
            color: #fff; 
            border: 1px solid #444;
            /*border-bottom: 50px solid #444;*/
            border-radius: 5px;
            border-color: #444;
        ''')
        thumbnail.setAlignment(QtCore.Qt.AlignCenter)
        
        thumb_checkbox = QtWidgets.QCheckBox("Pull Thumbnails", self)
        thumb_checkbox.setChecked(False)

        meta_tree_label = QtWidgets.QTextEdit(' SHOT STATUS')
        meta_tree_label.setMaximumSize(6000, 40)
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

        pull_shot_btn = QtWidgets.QPushButton("LOAD SHOT", self)
        pull_btn = QtWidgets.QPushButton("PULL ALL SHOTS", self)
        push_btn = QtWidgets.QPushButton("PUSH UPDATES", self)


        
        
        #--------------------------------------------#  
        # Menu Functions



        # Search keys function
        # def search(json_object, target_key):
        #     if type(json_object) is dict and json_object:
        #         for key in json_object:
        #             if key == target_key:
        #                 print("{}: {}".format(target_key, json_object[key]))
        #             search(json_object[key], target_key)
        #     elif type(json_object) is list and json_object:
        #         for item in json_object:
        #             search(item, target_key)
        # # search(shows, 'thumbnail')

        # Thumbnail checkbox
        def getThumbnail():
            if thumb_checkbox.isChecked():
                self.thumbnail = 1
            else:
                self.thumbnail = 0
            print('[>] Thumbnail:', self.thumbnail)
        thumb_checkbox.stateChanged.connect(getThumbnail)

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

            # get selected item
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
                                                    meta_tree_label.setText('SHOT STATUS > '+value)

                                            if key == 'tasks':
                                                # get 'title' key and add to tree as parent get remaining keys and add as children
                                                for task in value:
                                                    #task_tree_Widget.clear()
                                                    task_item = QtWidgets.QTreeWidgetItem(task_tree_Widget)
                                                    task_item.setText(0, task['title'])
                                                    task_item.setIcon(0, QtGui.QIcon('icons/task.png'))
                                                    task_item.setExpanded(False)
                                                    for key, value in task.items():
                                                        if key != 'title':
                                                            task_subitem = QtWidgets.QTreeWidgetItem(task_item)
                                                            task_subitem.setText(0, key)
                                                            task_subitem.setText(1, str(value))
                                                            task_subitem.setIcon(0, QtGui.QIcon('icons/task.png'))
                                                            task_subitem.setExpanded(False)
                                                            task_subitem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                                                            task_tree_Widget.addTopLevelItem(task_subitem)
                                                    task_tree_Widget.addTopLevelItem(task_item)
                                                #task_tree_Widget.expandAll()
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
                                                elif value == None:
                                                    pixmap = QtGui.QPixmap("X:/Shared drives/Pipeline/tools/OctoTools/core/config/Icons/favicon.png").scaled(320, 200, QtCore.Qt.KeepAspectRatio)
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
                                                                background-color: #000; 
                                                                color: #fff; 
                                                                border: 1px solid #444;
                                                                border-radius: 5px;
                                                                border-color: '''+value+''';
                                                                shadow: 100px 100px 100px 100px #fff;
                                                                border-opacity: 0.5;
                                                            ''')
                                                            # set shot status color to value
                                                            meta_tree_label.setStyleSheet('''
                                                                background-color: #000; 
                                                                color: '''+value+'''; 
                                                                border: 1px solid #444;
                                                                border-radius: 5px;
                                                                border-color: '''+value+''';
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
        
        
        # pull_shot_btn on click
        def search():
            self.searchData()
            showMenuFunc()
        pull_shot_btn.clicked.connect(search)
        
        # pull_btn on click
        def pull():
            self.getData()
            showMenuFunc()
        pull_btn.clicked.connect(pull)

        # push_btn on click
        def push():
            print('[>] Pushing...')
            print('[>] Done.')
        push_btn.clicked.connect(push)
        
        
        #--------------------------------------------#
        # Add to Menus to UI
        
        self.setWindowTitle("OctoBrowser")
        self.setWindowIcon(QtGui.QIcon('X:/Shared drives/Pipeline/tools/OctoTools/core/config/Icons/favicon.png'))
        self.setStyleSheet("background-color: #222; color: #ccc;")
        gui = QtWidgets.QHBoxLayout(self)
        gui.setContentsMargins(8,0,8,10)

        # Shot selection gui
        shot_select_group = QtWidgets.QGroupBox("SHOT", self, flat=True)
        shot_select_group.setStyleSheet("background-color: #333; color: #fff;")
        #shot_select_group.setMaximumSize(400, 1000)
        shot_select_group.setMaximumWidth(400)

        shot_select_layout = QtWidgets.QGridLayout(shot_select_group)
        shot_select_layout.setSpacing(20)
        shot_select_layout.setMargin(20)
        
        shot_select_layout.addWidget(thumbnail)
        shot_select_layout.addWidget(info)
        shot_select_layout.addWidget(user_info)
        shot_select_layout.addWidget(zone_info)
        shot_select_layout.addWidget(pull_shot_btn)
        shot_select_layout.addWidget(showMenu)
        shot_select_layout.addWidget(seqMenu)
        shot_select_layout.addWidget(shotMenu)      
        shot_select_layout.addWidget(thumb_checkbox)
        shot_select_layout.addWidget(pull_btn)
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