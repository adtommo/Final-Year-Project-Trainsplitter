#File Purpose: -Inserts data from files into the trains table
import pickle    
from tools import listDir

filepathRST = listDir('fares','RST')
filepathMCA = listDir('timetable','MCA')

TRAINS = set()
with open(filepathRST,'r') as fp:   #Gets lists of train uids to compare with other file
    line = fp.readline()
    for line in fp:
        if line.startswith('RSR'):
            train_uid = line[6:12]
            TRAINS.add(train_uid)

stations = {}
started = None
data = {}
station_times =[]
with open(filepathMCA,'r') as fp:
    line = fp.readline()
    for line in fp:
        if line.startswith('TI'):   #TIPLOC insert record
            tiploc = line[2:9].strip()
            crs = line[53:56].strip()
            if not crs: continue
            stations[tiploc] = crs
            continue

        if line.startswith('BSN'):  #Basic Schedule record(New transcation type)
            if line[3:9] in TRAINS: #Train UID comparing as stated prev
                started = line[3:9]
            else:
                started = None

        if started:
            type = line[:2] #Record type
            if type == 'CR': continue

            if type == 'BS':#This indicates the start of a train record
                if line[21:29] == '0000000': continue
                days = line[21:29]
                valid_from = line[9:15]
                valid_to = line[15:21]
                data[started] = {"date_from": valid_from, "date_to": valid_to, "days": days}
            
            elif type == 'BX': continue#This inicates the end of a train record

            if type == 'LO':#Origin station
                station = line[2:10].strip()
                if station not in stations: continue
                time = line[15:19]
                data[started].setdefault('stops',{})[station]=[None, time]

            if type == 'LI' and line[42:43] == "T":#Stations it stops at
                station = line[2:10].strip()
                if station not in stations: continue
                ar_time = line[25:29]
                dp_time = line[29:33]

                station_times.append(ar_time)
                station_times.append(dp_time)
                data[started].setdefault('stops',{})[station]=[ar_time, dp_time]
                del station_times[:]
            if type == 'LT':#Station it terminates at
                station = line[2:10].strip()
                if station not in stations: continue
                time = line[15:19]
                data[started].setdefault('stops',{})[station]=[time, None]
                data[started]["uid"]=started

with open('pickle\\trains.pickle','wb') as fp:
    pickle.dump(data, fp)


