from staticmap import StaticMap, CircleMarker, Line

import os, pickle, re

def create_map(route):
	m = StaticMap(300, 300)

	mydir = os.getcwd()
	fp = os.path.join(mydir,'map', 'station_location.pickle')
	data = pickle.load(open(fp,'rb'))
#					Purple		Red 	Yellow		Blue  	Green	Magenta		Orange		White
	colour_list =['#800080','#FF0000','#FFFF00','#0000FF','#008000','#FF00FF','#FF4500','#FFFFFF']
	colour_list2 =['#800080','#FF0000','#FFFF00','#0000FF','#008000','#FF00FF','#FF4500','#FFFFFF']

#creates map as a whole
	for station in route:
		lon = data[station]['lon']
		lat = data[station]['lat']
		colour = colour_list[0]
		colour_list.remove(colour)
		marker_outline = CircleMarker((lon, lat), '#000000', 8)
		marker = CircleMarker((lon, lat), colour, 7)
		m.add_marker(marker_outline)
		m.add_marker(marker)
	for station in range(len(route)-1):
		a_lon = data[route[station]]['lon']
		a_lat = data[route[station]]['lat']
		b_lon = data[route[station+1]]['lon']
		b_lat = data[route[station+1]]['lat']

		colour = colour_list2[0]
		colour_list2.remove(colour)

		a_marker = CircleMarker((a_lon, a_lat), colour, 7)
		b_marker = CircleMarker((b_lon, b_lat), colour_list2[0], 7)

		m2 = StaticMap(300, 300)
		m2.add_marker(a_marker)
		m2.add_marker(b_marker)
		m2.add_line(Line(((a_lon, a_lat), (b_lon, b_lat)), 'blue', 3))
		image = m2.render()


		img_name = str(station) + 'map.png'

		fp = os.path.join(mydir,'split','..','map','maps',img_name)
		image.save(fp)

		m.add_line(Line(((a_lon, a_lat), (b_lon, b_lat)), 'blue', 3))
	image = m.render()
	fp = os.path.join(mydir,'split','..','map','maps','map.png')
	image.save(fp)

#create_map(['LIV','LVC','SNH','BRI'])
