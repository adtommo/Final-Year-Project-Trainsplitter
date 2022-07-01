#File Purpose: -Creates the graph
import os, pickle
import itertools
from .dijkstra import Graph
from .data_compile import data

def get_codes(stn_code):
	if stn_code not in data['stations'] : return []
	stn = data['stations'][stn_code]
	stn_codes = []
	stn_codes += data['clusters'].get(stn.get('fare_group'), [])
	stn_codes += data['clusters'].get(stn['code'], [])
	stn_codes += [ stn['fare_group'] ] if 'fare_group' in stn else []
	stn_codes += [ stn['code'] ]
	return stn_codes

def get_fare_entry(code):
	FARES = {}
	if code not in FARES:
		mydir = os.getcwd()
		try:
			fp = os.path.join(mydir, '..', 'data', 'pickle','pickle_fares', '%s.pickle'%code)
			with open(fp, "rb") as f:
				FARES[code] = pickle.load(f)
		except IOError:
				FARES[code] = None
		return FARES[code]

def get_fares(fro, to):
	fares_data = []
	codes_fr = get_codes(fro)
	codes_to = get_codes(to)
	for code_fr in codes_fr:
		fare_entry = get_fare_entry(code_fr)
		if fare_entry == None: continue
		for code in fare_entry:
			if code in codes_to:
				for i in range(len(fare_entry[code])):	#Removes the prices if theyre empty
					if fare_entry[code][i]['prices'] == {}: continue
					for t, p in fare_entry[code][i]['prices'].items():
						fares_data.append({
							'adult': {'fare': int(p[0])},
							})
	return fares_data

def single_min(fro, to):
	min_price = None
	min_price_fare = None
	price_data = get_fares(fro, to)
	for i in range(len(price_data)):
		if min_price == None:
				min_price = price_data[i]
		else:
			if (min_price['adult']['fare']) > (price_data[i]['adult']['fare']):
				min_price_fare = price_data[i]['adult']['fare']
	return min_price_fare

def single_graph():
	graph_data = []
	cnt = 0
	trains = data['stations'].keys()
	for a, b in itertools.combinations(trains, 2):
		min_price_fare = single_min(a,b)
		if min_price_fare == None:
			continue
		else:
			graph_data.append((a, b, min_price_fare))
			graph_data.append((b, a, min_price_fare))
	graph = Graph(graph_data)
	with open('graph.pickle','wb') as fp:
		pickle.dump(graph_data, fp)
	



