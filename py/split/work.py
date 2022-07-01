import pickle, os
from dijkstra import Graph
from createGraph import single_min
def test(fro, to):
	#load graph
	mydir = os.getcwd()
	fp = os.path.join(mydir,'graph.pickle')
	data = pickle.load(open(fp,'rb'))
	graph = Graph(data)


	cost = 0
	route = graph.dijkstra(fro, to) #get shortest route

	length = len(route)



	for station in range(length - 1):
		for i in data:
			if i[0] == route[station] and i[1] == route[station + 1]:
				cost += i[2]
			if i[0] == route[0] and i[1] == route[length - 1]:
				original = i[2]


	print(original)
	print(route)
	print(cost)
	return original, route, cost

test("LIV","BRI")