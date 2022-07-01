#File Purpose: -This is what is used on the site, returning the relevant data
import pickle, os
from .dijkstra import Graph

def run(fro, to):
	#load graph
	mydir = os.getcwd()
	fp = os.path.join(mydir,'ticketsplit','py','split','graph.pickle')
	data = pickle.load(open(fp,'rb'))
	graph = Graph(data)


	cost = 0
	epi = 0
	each_point = {}
	route = graph.dijkstra(fro, to) #get shortest path

	length = len(route)


	for station in range(length - 1):
		for i in data:
			if i[0] == route[station] and i[1] == route[station + 1]:
				cost += i[2]
				p_price = convert_price(i[2])
				each_point[epi] = {'fro':route[station], 'to':route[station + 1], 'cost': p_price}
				epi += 1
			if i[0] == route[0] and i[1] == route[length - 1]:
				original_price = i[2]
				origin = route[0]
				dest = route[length - 1]

	cost = convert_price(cost)
	original_price = convert_price(original_price)

	return original_price, route, cost, each_point, origin, dest


def convert_price(p):
	p = p/100
	p = "%.2f" % p
	return p

