from staticmap import StaticMap, CircleMarker, Line

import os, pickle, re

def create_map(route):
	m = StaticMap(300, 300)

	mydir = os.getcwd()
	fp = os.path.join(mydir, 'ticketsplit','py','map','station_location.pickle')
	data = pickle.load(open(fp,'rb'))
	length = len(route) - 1

#creates seperate maps for split
	for station in range(length):
		a_lon = data[route[station]]['lon']
		a_lat = data[route[station]]['lat']
		b_lon = data[route[station+1]]['lon']
		b_lat = data[route[station+1]]['lat']

		o_a_lon = data[route[0]]['lon']
		o_a_lat = data[route[0]]['lat']
		o_b_lon = data[route[length]]['lon']
		o_b_lat = data[route[length]]['lat']


		a_marker = CircleMarker((a_lon, a_lat), '#008000', 7)
		b_marker = CircleMarker((b_lon, b_lat), '#FF0000', 7)

		m2 = StaticMap(300, 300)
		m2.add_marker(a_marker)
		m2.add_marker(b_marker)
		m2.add_line(Line(((a_lon, a_lat), (b_lon, b_lat)), 'blue', 3))
		image = m2.render()
		img_name = str(station) + 'map.png'

		fp = os.path.join(mydir, 'ticketsplit','static','img',img_name)
		image.save(fp)
	
	#creates map for original
	o_a_marker = CircleMarker((o_a_lon, o_a_lat), '#008000', 7)
	o_b_marker = CircleMarker((o_b_lon, o_b_lat), '#FF0000', 7)
	m.add_marker(o_a_marker)
	m.add_marker(o_b_marker)
	m.add_line(Line(((o_a_lon, o_a_lat), (o_b_lon, o_b_lat)), 'blue', 3))

	image = m.render()

	fp = os.path.join(mydir, 'ticketsplit','static','img','original.png')
	image.save(fp)

