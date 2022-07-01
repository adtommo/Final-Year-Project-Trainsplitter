import os, pickle, itertools

mydir = os.getcwd()

data_files =['clusters', 'restrictions', 'routes', 'stations', 'tocs', 'trains']
data = {}

for d in data_files:
	fp = os.path.join(mydir, '..', 'data', 'pickle',d + '.pickle')
	data[d] = pickle.load(open(fp,'rb'))