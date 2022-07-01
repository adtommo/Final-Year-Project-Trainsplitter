import pickle, datetime
from datetime import date
from tools import listDir

filepathRTE = listDir('fares','RTE')

data = {}
with open(filepathRTE,'r') as fp:   
    line = fp.readline()
    for line in fp:
    	record_type = line[1:2]
    	if record_type == '!': continue
    	end_date= datetime.date(int(line[11:15]), int(line[9:11]),int(line[7:9]))

    	if end_date < date.today(): continue

    	route_code = line[2:7]
    	incl_excl = line[25:26]
    	crs_code = line[22:25]
    	desc = line[31:47].strip()

    	if record_type == 'L':
    		data.setdefault(route_code,{}).setdefault(incl_excl,[]).append(crs_code)
    	else:
    		data.setdefault(route_code,{})['desc'] = desc

with open('pickle\\routes.pickle','wb') as fp:
    pickle.dump(data, fp)