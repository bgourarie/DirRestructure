import csv
import shutil
import os
import ConfigParser
from datetime import datetime

def logMessage(msg):
    try:
        logFile = open(logFileTXT,'a')
        logFile.write(msg)
    except IOError as ioe:
        shout("Error with log file!")
        exit(-1)
    finally:
        logFile.close()
# replacement for print statements :-)
def shout(msg):
    if not silent:
        print msg

config = ConfigParser.RawConfigParser()
config.read('directoryRestructure.cfg')
#get the info about the root paths
oldRootDir= config.get('FileDetails', 'oldrootdirectory')
newRootDir= config.get('FileDetails','newrootdirectory')
#print oldRootDir
#print newRootDir
# get info about the log file
logErrors= config.getboolean('FileDetails','log')
if logErrors:
    logFileTXT= config.get('FileDetails','logfile')
#print logFileTXT
# define silent mode
silent=config.getboolean('FileDetails','runsilent')
#print silent
#locate csv file
csvInstructions= config.get('FileDetails','csvfile')
#print csvInstructions
# are we doing a test run?
testMode=config.get('FileDetails','testmode')
#print testMode

# then we prepare to parse. first we split it based on line breaks
# this we split into a list of comma separated strings.
try:
    textList= open(csvInstructions)
    lines = textList.read().split('\n')
except IOError as ioe:
    shout("Error opening CSV. See logs and check config file")
    logMessage(ioe.strerror+"error opening csv file"+"\n")
finally:
    textList.close()
newDirectories = [] # this is just a temporary thing...
oldDirectories=[]
logText=[str] # this will store the log
newPaths=[] # this is where we actually store new paths.
shout("Found "+str(len(lines))+" many directories")
for i in lines:
    newDirectories.append(i.split(","))
#now newDirectories contains each row of the CSV...

for i in newDirectories:
    #we create the file path for each directory
    if len(i)>1: #skip blank lines
        #store the old directories:
        oldDirectories.append(os.path.join(oldRootDir,i[0]))
        # and the new
        newPathString = os.path.join(newRootDir,i[2],i[3],i[4],i[1])
        newPaths.append(newPathString)
#check the new paths are correct:        

if testMode == True:
    for i in range(len(newPaths)):
        shout(oldDirectories[i]+" --> "+newPaths[i])
else:
    #2)move the files within the old directory into the new one.
        # we use copytree, which expects the directories to all be brand new...
    # start by creating the new log file
    logMessage("copy started at " + datetime.now().isoformat()+" \n")
    for i in range(len(newPaths)):
        try:
            shout("trying to move " +oldDirectories[i] + " to " + newPaths[i])
            shutil.copytree(os.path.join(oldDirectories[i]),os.path.join(newPaths[i]),symlinks=True)
        except shutil.Error as error:
            logText.append(error.strerror+"\n")
            shout(error.strerror)
            logMessage("--failed to move "+oldDirectories[i]+ " to " + newPaths[i]+error.strerror+"\n")
        #if it makes it to here, then obviously it worked, so we remove the paths from the list
        except WindowsError as error:
            logText.append(error.strerror+"\n")
            shout(error.strerror)
            logMessage("--failed to move "+oldDirectories[i]+ " to " + newPaths[i]+error.strerror+"\n")
    shout("Copy Completed")


