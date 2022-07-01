#File Purpose: -Compiles data from each file into one dictionary 
import os, pickle, itertools

mydir = os.getcwd()

data_files =['clusters', 'stations']
data = {}

for d in data_files:
	fp = os.path.join(mydir, 'ticketsplit', 'py', 'data', 'pickle',d + '.pickle')
	data[d] = pickle.load(open(fp,'rb'))

