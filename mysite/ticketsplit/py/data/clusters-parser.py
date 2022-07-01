#File Purpose: -Inserts data from file into the cluster table
import pickle
from tools import listDir

filepathFSC = listDir('fares','FSC')

data = {}
with open(filepathFSC,'r') as fp:   
    line = fp.readline()
    for line in fp:
    	if line[0:1] == '/': continue	#skips the headers for the file
    	cluster_id = line[1:5]
    	member_id = line[5:9]
    	data.setdefault(member_id,[]).append(cluster_id)

with open('pickle\\clusters.pickle','wb') as fp:
    pickle.dump(data, fp)

    