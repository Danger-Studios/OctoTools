import os
import hou
import sys
import random
import json

#bring in some env vars
hip = hou.getenv('HIP')

##############################################
#               OctoTools
#             Captain's log             
##############################################

def logit(msg):
    path = os.path.normpath('$OCTOCOREoctoLog.log') #.replace("\\",'/')
    print(path)
    if os.path.exists(path):
        mode = 'a' # append if already exists
        logz = open(path,mode)
        logz.write("[>] {}\n".format(msg))
        logz.close()
        hou.node('.').parm('logger').set(hou.readFile(path))
    else:
        mode = 'w' # make a new file if not
        logz = open(path,mode)
        details = '[>] {}\n'
        logz.write(details.format(msg))
        logz.close()
        hou.node('.').parm('logger').set(hou.readFile(path))

##############################################
#               OctoTools
#              Path Finder             
##############################################

def pathFinder(kwargs):
    root = kwargs["node"].parm("show").eval()
    value = kwargs["node"].parm("value").eval()
    atom = kwargs["node"].parm("key").eval()
    print(root)
    var = random.randrange(1, 9999, 1)
    print('\nPathFinding',var)
    for path, dirs, files in os.walk(root):
        if atom in dirs:
            print('[>] FOUND:',atom)
            foundPath = os.path.join(path, atom)
            print('[>] PATH:',foundPath)
            hou.pwd().parm('msg').set('Path Found')
            hou.pwd().parm('value').set(foundPath)
            hou.pwd().parm('env').set({atom:foundPath})
            return foundPath
        else:
            hou.pwd().parm('msg').set('Path Not Found')
            hou.pwd().parm('value').set('Path Not Found')
            #hou.pwd().parm('env').set({atom:value})
            

    
def jsonWrangler(kwargs):

    with open(hip+'/env.json') as json_file:
        data = json.load(json_file)
        #kwargs["node"].parm("env").set(data)
        print(data)

    













