import pickle    
from tools import listDir

filepathTOC = listDir('fares','TOC')

data = {}
with open(filepathTOC,'r') as fp:   #Gets lists of train uids to compare with other file
    line = fp.readline()
    for line in fp:
    	if line[:1] != 'T' or line[41:42] == 'N':continue  #line[:1] is record type, 'T' is TOC record                                                 #line[41:42] indicates if it is active
    	name = line[3:33].strip()
    	if name == name.upper() and len(name)>3: name = name.title()
    	toc_id = line[4:6]
    	fare_toc = line[1:4]
    	data[toc_id] = name
with open('pickle\\tocs.pickle','wb') as fp:
    pickle.dump(data, fp)