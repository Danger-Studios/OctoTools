import base64
from email import policy
import os
import sys
# import hou
import json
import traceback
from PySide2 import QtWidgets, QtNetwork, QtCore, QtGui
import numpy as np


class ImgDownloader(QtCore.QObject):
    def __init__(self, parent, req):
        self.req = req
        self.pixmap = QtGui.QPixmap()
        super(ImgDownloader, self).__init__(parent)

    def startFetch(self, netManager):
        self.fetch_task = netManager.get(self.req)
        self.fetch_task.finished.connect(self.onFetchFinished)

    def onFetchFinished(self):
        reply = self.fetch_task.readAll()
        self.setWidgetImage(reply)

    def setWidgetImage(self, reply):
        self.pixmap.loadFromData(reply)
        self.parent().setPixmap(self.pixmap)


class OctoConnectBak(QtCore.QObject):
    def __init__(self):
        # Connect to OctoBoards
        print('[>] Connecting to OctoBoards:')
        from . import OctoConnect
        ob = OctoConnect.Client(
            'https://octoboards.danger.studio/jsonrpc.php',
            'danger',
            'd7ca56c54bf6fec3f5470527d3f7e367a1536ca9cb26ef9fe93addda40e9'
        )

        projects = ob.getAllProjects()
        timezone = ob.getTimezone()
        getUser = ob.getMe()

        # Init vars
        self.show = ''
        self.seq = ''
        self.shot = ''
        self.task = ''
        self.showDict = {'SHOWS': []}
        self.shotThumbsArr = []

        print('[>] Loading show data...')
        # Parse data from Octoboards API into a custom json structure
        for project in projects:
            project_name = project['identifier']
            project_id = project['id']
            swimlanes = ob.getActiveSwimlanes(project_id=project_id)
            tasks = ob.getAllTasks(project_id=project_id, status_id=1)
            columns = ob.getColumns(project_id=project_id)

            show = {
                'show_name': project_name,
                'SEQS': []
            }

            self.show = show['show_name']
            self.showDict['SHOWS'].append(show)

            for swimlane in swimlanes:
                swimlane_name = swimlane['name']
                swimlane_id = swimlane['id']

                seq = {
                    'seq_name': swimlane_name,
                    'SHOTS': []
                }

                self.seq = seq['seq_name']
                self.showDict['SHOWS'][0]['SEQS'].append(seq)

                for task in tasks:  # task = shot in this case
                    if task['swimlane_id'] == swimlane_id:
                        task_title = task['title']
                        task_image = ob.getAllTaskFiles(task_id=task['id'])
                        subtasks = ob.getAllSubtasks(task_id=task['id'])

                        shot = {
                            'shot_name': task_title,
                            'shot_image': task_image,
                            'shot_image_data': '',
                            'shot_status': '',
                            'shot_tasks': []
                        }

                        self.shot = shot['shot_name']
                        self.showDict['SHOWS'][0]['SEQS'][0]['SHOTS'].append(
                            shot)

                        for image in shot['shot_image']:
                            # get first item in list
                            if image == shot['shot_image'][0] and image['is_image'] == 1:
                                file_id = image['id']
                                # print ('[>] loading thumbnail for',task_title)
                                file_encoded = ob.downloadTaskFile(file_id=file_id)
                                file_decoded = base64.urlsafe_b64decode(
                                    file_encoded)
                                file_dir = 'X:/Shared drives/Pipeline/tools/OctoTools/core/scripts/python/OctoBrowser/thumb_test/'
                                file_name = show['show_name'] + '_'+seq['seq_name'] + \
                                    '_' + shot['shot_name'] + '_thumb.png'

                                for shot in self.showDict['SHOWS'][0]['SEQS'][0]['SHOTS']:
                                    if shot['shot_name'] == task_title:
                                        # shot['shot_image_data'] = file_encoded # for json output
                                        # for image output
                                        shot['shot_image_data'] = file_decoded
                                        self.shotThumbsArr.append(file_decoded)
                                        # print ('[>] loaded thumbnail for',task_title)

                                # Write out thumbnail to disk
                                # try:
                                #     with open(file_dir+file_name, mode='wb+') as f:
                                #         f.write(file_decoded)
                                #         f.close()
                                # except:
                                #         print(traceback.format_exc())

                        for column in columns:
                            column_id = column['id']
                            if task['column_id'] == column_id:
                                status = column['title']
                                for shot in self.showDict['SHOWS'][0]['SEQS'][0]['SHOTS']:
                                    if shot['shot_name'] == task_title:
                                        shot['shot_status'] = status

                        if subtasks:
                            for subtask in subtasks:
                                subtask_title = subtask['title']

                                task = {
                                    'task_name': subtask_title,
                                    'task_status': '',
                                    'task_user': ''
                                }

                                self.task = task['task_name']
                                for shot in self.showDict['SHOWS'][0]['SEQS'][0]['SHOTS']:
                                    if shot['shot_name'] == task_title:
                                        shot['shot_tasks'].append(task)
                                        for task in shot['shot_tasks']:
                                            if task['task_name'] == subtask_title:
                                                task['task_user'] = subtask['username']
                                                task['task_status'] = subtask['status_name']

        # self.jsonDump = 'X:/Shared drives/Pipeline/tools/OctoTools/core/scripts/python/OctoBrowser/showData.json'
        # try:
        #     with open(self.jsonDump, "w+") as f:
        #         json.dump(self.showDict, f, indent=4)
        # except:
        #         print(traceback.format_exc())
        print('[>] Done.\n')


class OctoConnect(QtCore.QObject):
    def __init__(self):

        # Connect to api
        #--------------------------------------------#
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
        print('')

        # Menu arrays
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
                        
                        # this takes ages atm:
                        shot_images = self.ob.getAllTaskFiles(task_id=shot_id)
                        # get all shot images
                        for image in shot_images:
                            if image == shot_images[0] and image['is_image']:   
                                file_id = image['id']
                                print('[>] Loading Thumbnail (id:' + str(file_id) + ') for ' + shot_name)
                                file_encoded = self.ob.downloadTaskFile(file_id=file_id)
                                print('[>] deocding...')
                                file_decoded = base64.urlsafe_b64decode(file_encoded)
                                # append to array
                                

                        # getShot = '[>]     |_SHOT:' + shot_name
                        # append shots and sort shot_name by name
                        for show in self.showsArr['SHOWS']:
                            if show_name in show:
                                for seq in show[show_name]:
                                    if seq_name in seq:
                                        seq[seq_name].append({shot_name: []})
                                        seq[seq_name].sort(key=lambda x: list(x.keys())[0])


                        for status in shots_status:
                            if shot_status_id == status['id']:
                                shot_status = status['title']
                                # print(getShot+' >', shot_status)
                                for shot in seq[seq_name]:
                                    if shot_name in shot:
                                        shot[shot_name].append({'status': shot_status})
                                        shot[shot_name].append({'thumbnail': file_decoded})


class OctoBrowser(QtWidgets.QWidget):
    def __init__(self):

        # Get shot name from data
        def search(json_object, target_key):
            if type(json_object) is dict and json_object:
                for key in json_object:
                    if key == target_key:
                        print("{}: {}".format(target_key, json_object[key]))
                    search(json_object[key], target_key)
            elif type(json_object) is list and json_object:
                for item in json_object:
                    search(item, target_key)

        request = OctoConnect()
        zone = request.zone
        user = request.user
        shows = request.showsArr
        # print('\n[>] SHOW MENU:\n', json.dumps(shows, indent=4))
        #search(shows, 'thumbnail')

        # Create UI
        print('\n[>] OctoBrowser Activated')
        super(OctoBrowser, self).__init__()
        self.setWindowTitle("OctoBrowser")
        mainUI = QtWidgets.QGridLayout(self)

        group_box_settings = QtWidgets.QGroupBox(
            "Select A Shot", self, flat=True)
        group_box_settings_layout = QtWidgets.QGridLayout(group_box_settings)

        #--------------------------------------------#

        # Create UI Elements
        showMenu = QtWidgets.QComboBox()
        showMenu.setMaximumSize(320, 40)

        seqMenu = QtWidgets.QComboBox()
        seqMenu.addItem('SEQ')
        seqMenu.setMaximumSize(320, 40)

        shotMenu = QtWidgets.QComboBox()
        shotMenu.addItem('SHOT')
        shotMenu.setMaximumSize(320, 40)

        info = QtWidgets.QTextEdit()
        info.setMaximumSize(320, 40)

        pixmap = QtGui.QPixmap("X:/Shared drives/Pipeline/tools/OctoTools/core/config/Icons/favicon.png")
        pixmap = pixmap.scaled(320, 200, QtCore.Qt.KeepAspectRatio)
        thumbnail = QtWidgets.QLabel()
        thumbnail.setPixmap(pixmap)
        thumbnail.setMaximumSize(320, 200)
        thumbnail.setScaledContents(True)

        user_info = QtWidgets.QTextEdit('USER: ' + user['username'])
        user_info.setMaximumSize(320, 40)
        zone_info = QtWidgets.QTextEdit('ZONE: ' + zone)
        zone_info.setMaximumSize(320, 40)


        
        

        # Create info box
        info.setReadOnly(True)
        info.setText('Select something...')
        # info.setStyleSheet("background-color: #333; color: #fff;")
        info.setFrameStyle(QtWidgets.QFrame.NoFrame)
        info.setFrameShadow(QtWidgets.QFrame.Plain)

        # Menu Functions

        def updateInfo():
            shot = shotMenu.currentText()
            seq = seqMenu.currentText()
            show = showMenu.currentText()
            # update info
            info.setText(show+' / '+seq+' / '+shot) 
            # update thumbnail
            for show in shows['SHOWS']:
                if showMenu.currentText() in show:
                    for seq in show[showMenu.currentText()]:
                        if seqMenu.currentText() in seq:
                            for shot in seq[seqMenu.currentText()]:
                                if shotMenu.currentText() in shot:
                                    for data in shot[shotMenu.currentText()]:
                                        if 'thumbnail' in data:
                                            # print(data['thumbnail'])
                                            # encode string to bytes
                                            pixmap.loadFromData(data['thumbnail'])
                                            thumbnail.setPixmap(pixmap)

        def shotMenuFunc():
            shotMenu.clear()
            shotMenu.addItem('SHOT')
            for show in shows['SHOWS']:
                if showMenu.currentText() in show:
                    for seq in show[showMenu.currentText()]:
                        if seqMenu.currentText() in seq:
                            for shot in seq[seqMenu.currentText()]:
                                shotMenu.addItem(list(shot.keys())[0])
            shotMenu.currentIndexChanged.connect(updateInfo)

        def seqMenuFunc():
            seqMenu.clear()
            seqMenu.addItem('SEQ')
            for show in shows['SHOWS']:
                if showMenu.currentText() in show:
                    for seq in show[showMenu.currentText()]:
                        seqMenu.addItem(list(seq.keys())[0])
            seqMenu.currentIndexChanged.connect(shotMenuFunc)

        def showMenuFunc():
            showMenu.clear()
            showMenu.addItem('SHOW')
            for show in shows['SHOWS']:
                showMenu.addItem(list(show.keys())[0])
            showMenu.currentIndexChanged.connect(seqMenuFunc)

        showMenuFunc()

        #--------------------------------------------#

        # Add to Menus to UI
        
        group_box_settings_layout.addWidget(user_info, 0, 0)
        group_box_settings_layout.addWidget(zone_info, 1, 0)
        group_box_settings_layout.addWidget(thumbnail, 2, 0)
        group_box_settings_layout.addWidget(info, 3, 0)
        group_box_settings_layout.addWidget(showMenu, 4, 0)
        group_box_settings_layout.addWidget(seqMenu, 5, 0)
        group_box_settings_layout.addWidget(shotMenu, 6, 0)
        group_box_settings_layout.setColumnStretch(0, 1)

        #--------------------------------------------#

        # Add UI to Main Window
        mainUI.addWidget(group_box_settings, 0, 0)
        
        #mainUI.setColumnStretch(0, 1,)
        mainUI.setRowStretch(0, 1)

        #--------------------------------------------#

        # Show Window

        # grid.addWidget(seqMenu)
        # grid.addWidget(shotMenu)

        self.setLayout(mainUI)

        # Add a button to the UI
        # mainUI.addWidget(QtWidgets.QPushButton('Button 1'))
        # img_lbl = QtWidgets.QLabel("text label")

        # Add a list view
        # iconView = QtWidgets.QListWidget()
        # Set to icon view (default is list view) - diable line for default view
        # iconView.setViewMode(QtWidgets.QListWidget.IconMode)

        # Run OctoConnect function
        # connect = OctoConnect()
        # data = connect.showDict
        # thumbs = connect.shotThumbsArr

        # for thumb in thumbs:
        #     # decoded string to bytes
        #     Qp = QtGui.QPixmap()
        #     Qp.loadFromData(thumb)
        #     img_lbl = QtWidgets.QLabel('a name',alignment=QtCore.Qt.AlignCenter)

        #     # req = QtNetwork.QNetworkRequest(QtCore.QUrl(thumb))
        #     # downloader = ImgDownloader(img_lbl, req)
        #     # downloader.startFetch(self.downloadQueue)

        #     item = QtWidgets.QListWidgetItem()
        #     item.setSizeHint(QtCore.QSize(192, 108))
        #     item.setIcon(QtGui.QIcon(Qp))
        #     # item.setIcon(QtGui.QIcon(Qp))
        #     iconView.addItem(item)
        #     iconView.setItemWidget(item, img_lbl)

        # #img = QtGui.QImage()
        # # img.loadFromData(requests.get('https://octoboards.danger.studio/assets/img/favicon.png').content)
        # # img_lbl.setPixmap(QtGui.QPixmap(img))

        # mainUI.addWidget(iconView)
