#File Purpose: -Provides functions used by all the parser files
import sys, os
#Used to provide the file path
def listDir(data,file):
    mydir = os.getcwd()+'\\' + data
    for files in os.listdir(mydir):
    	if files.endswith('.' + file):
    		return (os.path.join(mydir ,files))
