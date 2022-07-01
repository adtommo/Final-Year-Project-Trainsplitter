import pickle
from tools import listDir

filepathRST = listDir('fares','RST')

data = {}
with open(filepathRST,'r') as fp:   
    line = fp.readline()
    for line in fp:
    	record_type = line[1:3]    #File contains a number of record types which have to be filtered

    	cf_mkr = line[3:4] #Either ‘C’ or ‘F’. Used to determine if it's current or future.

    	if cf_mkr == 'F': continue
    	if record_type in {'TP', 'TE', 'SP', 'SE', 'RD', 'EC', 'CA', 'RR', 'SD', 'SQ', 'HD', 'TD','!!'}: continue

    	code = line[4:6]
    	data.setdefault(code,{})
    	if record_type == 'RH':
    		desc = line[6:36].strip()    #Restriction description
    		desc_out = line[36:86].strip()
    		desc_rtn = line[86:136].strip()
    		type_out = line[136:137]#‘P’ = positive restriction,
    		type_rtn = line[137:138]#‘N’ = negative restriction
    		data[code]['info'] = {'desc':desc, 'desc_out':desc_out, 'desc_rtn':desc_rtn, 'type_out':type_out, 'type_rtn':type_rtn}
    	elif record_type == 'HD':
    		date_from = line[6:10]
    		date_to = line[10:14]
    		days = line[14:21]
    		data[code].setdefault('days',[]).append({'date_from':date_from,'date_to':date_to, 'days':days})
    	elif record_type == 'TR':
    		seq_no = line[6:11]
    		f = line[11:15]
    		t = line[15:19]
    		adv = line[19:20]
    		data[code].setdefault('times',{}).setdefault(seq_no,{}).update({'f':f, 't':t, 'adv':adv,})
    	elif record_type == 'TT':
    		seq_no = line[6:11]
    		toc = line[11:13]
    		data[code].setdefault('times',{}).setdefault(seq_no, {}).setdefault('tocs',[]).append(toc)
    	elif record_type == 'TD':
    		seq_no = line[6:11]
    		out_ret = line[10:11]
    		date_from = line[11:15]
    		date_to = line[15:19]
    		days = line[19:26]
    		data[code].setdefault('times',{}).setdefault(seq_no, {}).setdefault('dates',[]).append({'out_ret':out_ret, 'date_from':date_from, 'date_to':date_to, 'days':days})
    	elif record_type == 'SR':
    		direction = line[12:13]
    		train_no = line[6:12]
    		data[code].setdefault('trains',[]).append({'dir':direction,'id':train_no})

with open('pickle\\restrictions.pickle','wb') as fp:
    pickle.dump(data, fp)