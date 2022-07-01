import datetime
from datetime import date
from tools import listDir


filepathTTY = listDir('fares','TTY')

ticket_types = []
blacklist = ["SVH", "SSH", "SSU", "SS2"]

with open(filepathTTY,'r') as fp:   
    line = fp.readline()
    for line in fp:
        if line[0:1] == '/': continue
        j_type = line[44:45]
        j_group = line[45:46]
        end_date= datetime.date(int(line[8:12]), int(line[6:8]),int(line[4:6]))
        start_date= datetime.date(int(line[16:20]), int(line[14:16]),int(line[12:14]))

        if end_date < date.today(): continue
        if start_date > date.today(): continue

        if j_group == 'S' and j_group == 'S':
            ticket_code = line[1:4]
            if ticket_code in blacklist: continue
            desc  = line[28:43]
            if desc.startswith('ANYTIME'):
                ticket_types.append(ticket_code)

