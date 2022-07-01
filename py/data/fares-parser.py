#File Purpose: -Inserts data from file into table fares
import pickle, copy, datetime
from datetime import date
from tools import listDir
from ticket_parser import ticket_types


filepathFFL = listDir('fares','FFL')

#ticket_types = ('SOS', 'SOR', 'SDS', 'SDR','GTS', 'GTR', 'GPR', 'CDS', 'CDR', 'SVS', 'SVR', 'SVH', 'G2S', 'G2R',
#				'SSS', 'SSR', 'OPS', 'OPR', 'CBB', 'SOP', 'GDS', 'GDR', 'PDS', 'PDR', 'SOA', 'SOB', 'AM1', 'AM2',
 #   			'EGS', 'EGF', 'OPD', 'SRR', 'SWS', 'SCO', 'C1R', 'CBA',)

#SOS , SOR 			=> Anytime single/return 
#SDS, SDR 			=> Anytime day
#GTS, GTR 			=> Anytime single/return
#GPR 				=> Anytime day return
#CDS, CDR 			=> Off-peak day
#SVS, SVR, SVH 		=> Off-peak
#G2S, G2R, 			=> Offpeak
#SSS, SSR, OPS, OPR => Super off-peak single/return
#CBB				=> Super off-peak single
#SOP 				=> Super off-peak return
#GDS, GDR, PDS, PDR,
#SOA, SOB, AM1, AM2,
#EGS, EGF, OPD, SRR,
#SWS, SCO, C1R, CBA => Super off-peak day
data = {}
data_by_id ={}

with open(filepathFFL,'r') as fp:   
    line = fp.readline()
    for line in fp:
        record_type = line[1:2] #record type, f = flow record, t = fare record
        if record_type == 'T':
            flow_id = line[2:9]            
            if flow_id not in data_by_id: continue
            ticket_code = line[9:12]
            if ticket_code not in ticket_types: continue
            fare = line[12:20]
            restr_code = line[20:22]
            data_by_id[flow_id]['prices'][ticket_code] = [fare, restr_code]

        if record_type == 'F':
            origin = line[2:6]
            dest = line[6:10]
            route = line[10:15]
            status = line[15:18]
            direction = line[19:20]
            end_date= datetime.date(int(line[24:28]), int(line[22:24]),int(line[20:22]))
            start_date= datetime.date(int(line[32:36]), int(line[30:32]),int(line[28:30]))
            toc = line[36:39]
            nsd = line[40:41]
            flow_id = line[42:49]

            if nsd != '0': continue#Filtering what is valid to be used
            if start_date > date.today(): continue
            if end_date < date.today(): continue
            if status != '000': continue
            d = {'prices': {}, 'toc':toc, 'route': route,}

            data.setdefault(origin, {}).setdefault(dest, []).append(d)

            if direction == 'R': #if the direction is R then the origin and dest should be reversed
                data.setdefault(dest, {}).setdefault(origin, []).append(d)
                

            data_by_id[flow_id] = d

#data_copy = data.copy()			#unable to modify dictionary in for loop so a copy is made

#for fr, d1 in list(data_copy.items()):	#used to remove data that has no fare/prices
 #   for to, d2 in list(d1.items()):
  #      for i, d in enumerate(d2):
   #         if not d['prices']:
    #            try:
     #               del data[fr][to]
      #          except KeyError:	#kept on getting key error for some reason
       #         	pass			#so it will pass on those errors. Still works.
for fr, d1 in data.items():
	with open('pickle\\pickle_fares\\%s.pickle' % fr,'wb') as fp:
		pickle.dump(d1, fp)
