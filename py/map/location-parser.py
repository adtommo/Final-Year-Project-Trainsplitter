from bs4 import BeautifulSoup
import os, re, json, pickle, requests


def map_location_data():
	stations_location = {}
	mydir = os.getcwd()
	fp = os.path.join(mydir, '..', 'data', 'pickle', 'stations.pickle')

	for station in pickle.load(open(fp,'rb')):
		url = 'https://www.nationalrail.co.uk/stations_destinations/' + station + '.aspx'
		url_get = requests.get(url)
		soup = BeautifulSoup(url_get.content, 'lxml')
		col = str(soup.find('address'))

		if len(col)== 4:
			continue
		col = re.findall(r'[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}', col)


		url = 'http://api.postcodes.io/postcodes/' + str(col[0])


		r = requests.get(url)

		if r.status_code != 200:
			continue

		data = r.json()

		lon = data['result']['longitude']
		lat = data['result']['latitude']

		stations_location[station] = {'lon':lon, 'lat': lat}

	with open('station_location.pickle','wb') as fp:
	    pickle.dump(stations_location, fp)
