import sys
import os
import traceback
import json
from PySide2 import QtCore

# get path of script and add to sys.path
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)


# Build Show schema from request
class build(QtCore.QObject):
    def __init__(self, parent=None):
        super(build, self).__init__(parent)

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
            from OctoConnect import Client
            self.ob = Client(
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


# Load or get data
class dataWrangler(QtCore.QObject):

    def __init__(self, parent=None):
        super(dataWrangler, self).__init__(parent)
        print('\n[>] dataWrangler Activated')
        
        self.shows = {'SHOWS': []}
        self.zone = ''
        self.user = {'username': 'none'}
        self.rebuildJson = 0
        self.showJson = 'X:/Shared drives/Pipeline/tools/OctoTools/core/scripts/python/OctoBrowser/nodesData.json'
        
    def getData(self):

        print('\n[>] Fetching Data...')
        # get data from OctoConnect with doRebuild()
        request = build()
        self.shows = request.showsArr
        self.zone = request.zone
        self.user = request.user
        # Write data to file
        with open(self.showJson, 'w') as f:
            self.shows = json.dump(self.shows, f, indent=4)
        print('\n[>] Done.') 

    def loadData (self,rebuildJson,showJson):

        if rebuildJson == 0:
            print('\n[>] Loading Data...')    
            with open(showJson) as json_file:
                self.shows = json.load(json_file)
            print('\n[>] Done.')  
            # print('\n[>] SHOW SCHEMA:\n', json.dumps(self.shows, indent=4))
        else:
            self.getData()

        return self.shows, self.zone, self.user
