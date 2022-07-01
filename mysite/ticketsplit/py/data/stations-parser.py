#File Purpose: -Inserts data from file into the station table
import re, pickle, datetime
from datetime import date
from tools import listDir

filepathLOC = listDir('fares','LOC')
x = 0
data = {}
with open(filepathLOC,'r') as fp:   
    line = fp.readline()
    for line in fp:
        record_type = line[1:2]
        record_list = ['G','R','S','M']
        if any(x in record_list for x in record_type) or line[:1] == '/': continue

        end_date= datetime.date(int(line[13:17]), int(line[11:13]),int(line[9:11]))
        if end_date < date.today(): continue

        if record_type == 'L':   #Location record
            crs_code = line[56:59]    #Where present, the location code used by the CRS
            admin_area_code = line[33:36].strip()
            if admin_area_code != '70' : continue #admin area code 70 = Britain
            if crs_code == '   ' : continue

            #checking the stations used on national rail, found 
            #out non start with x or z (as they are in Ireland) but it this some returned
            # (apart from ZFD)
            if re.search('X|Z', crs_code[0]) != None and crs_code != 'ZFD':continue
    
            desc = line[40:56].strip()    #Location description(name of the location)
            name = re.sub('([a-z])\.$',r'\1', desc.title())   #Converts from all caps to format:'Liverpool'
            
            nlc_code = line[36:40]  #National location code, for British locations only
            
            fare_group = line[69:75].strip()    #Fare group identification, if not part of group will just
                                                #use nlc code
            data[crs_code] = {'description': name, 'code': nlc_code}

            if fare_group != nlc_code:
                data[crs_code]['fare_group'] = fare_group
                x = x + 1
with open('pickle\\stations.pickle','wb') as fp:
    pickle.dump(data, fp)


