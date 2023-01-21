
import OctoConnect


# from OctoBoards import OctoConnect

ob = OctoConnect.Client('https://octoboards.danger.studio/jsonrpc.php', 'danger', 'd7ca56c54bf6fec3f5470527d3f7e367a1536ca9cb26ef9fe93addda40e9')

projects = ob.getAllProjects()
timezone = ob.getTimezone()
getUser = ob.getMe()
print('\n[',timezone,']\n')
print('USER:',getUser['username'])


for project in projects:
    project_name = project['name']
    project_id = project['id']
    print('SHOW:',project_name)
    print('SHOW-ID:',project_id,'\n')
    swimlanes = ob.getActiveSwimlanes(project_id=project_id)
    tasks = ob.getAllTasks(project_id=project_id, status_id=1)
    columns = ob.getColumns(project_id=project_id)

    for swimlane in swimlanes:
        swimlane_name = swimlane['name']
        swimlane_id = swimlane['id']
        print('['+swimlane_name+']')
        
        for task in tasks: # task = shot in this case

            if task['swimlane_id'] == swimlane_id:
                task_title = task['title']
                subtasks = ob.getAllSubtasks(task_id=task['id'])

                for column in columns:
                    column_id = column['id']
                    if task['column_id'] == column_id:
                        print(' /'+task_title+' - status:'+column['title']) # print shot name & status
                if subtasks:
                    for subtask in subtasks:
                        subtask_title = subtask['title']
                        if subtask['status'] == 0: # not started
                            print('   |_[ ]'+subtask_title)
                        elif subtask['status'] == 1: # in progress
                            print('   |_[i]'+subtask_title)
                        elif subtask['status'] == 2: # done
                            print('   |_[x]'+subtask_title)
                else:
                    print('   |_[ ]No Tasks')
        print('\n')



# # Asynchronous I/O version
'''
import asyncio
import OctoConnect

ob = OctoConnect.Client('https://octoboards.danger.studio/jsonrpc.php', 'danger', 'd7ca56c54bf6fec3f5470527d3f7e367a1536ca9cb26ef9fe93addda40e9')
loop = asyncio.get_event_loop() # Asynchronous I/O

projects = loop.run_until_complete(ob.getAllProjects_async())
timezone = ob.getTimezone()
getUser = ob.getMe()
print('\n[',timezone,']\n')
print('USER:',getUser['username'])


for project in projects:
    project_name = project['name']
    project_id = project['id']
    print('SHOW:',project_name)
    print('SHOW-ID:',project_id,'\n')

    swimlanes = loop.run_until_complete(ob.getActiveSwimlanes_async(project_id=project_id))
    tasks = loop.run_until_complete(ob.getAllTasks_async(project_id=project_id, status_id=1))
    columns = loop.run_until_complete(ob.getColumns_async(project_id=project_id))

    for swimlane in swimlanes:
        swimlane_name = swimlane['name']
        swimlane_id = swimlane['id']
        print('['+swimlane_name+']')
        
        for task in tasks: # task = shot in this case

            if task['swimlane_id'] == swimlane_id:
                task_title = task['title']
                subtasks = loop.run_until_complete(ob.getAllSubtasks_async(task_id=task['id']))

                for column in columns:
                    column_id = column['id']
                    if task['column_id'] == column_id:
                        print(' /'+task_title+' - status:'+column['title']) # print shot name & status
                if subtasks:
                    for subtask in subtasks:
                        subtask_title = subtask['title']
                        if subtask['status'] == 0: # not started
                            print('   |_[ ]'+subtask_title)
                        elif subtask['status'] == 1: # in progress
                            print('   |_[i]'+subtask_title)
                        elif subtask['status'] == 2: # done
                            print('   |_[x]'+subtask_title)
                else:
                    print('   |_[ ]No Tasks')
        print('\n')
        
'''