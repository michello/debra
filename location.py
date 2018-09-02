from geopy.geocoders import Nominatim
from flask import Flask, request, redirect, session, make_response, render_template
from google.cloud import firestore

app = Flask(__name__, static_url_path='/static', static_folder='static')

db = firestore.Client()

givers_ref = db.collection(u'GiverCalls')
needers_ref = db.collection(u'NeederCalls')

@app.route("/")
def locations():
	loc = []
	givers = givers_ref.get()
	needers = needers_ref.get()
	geolocator = Nominatim()
	for giver in givers:
		giver_data = giver.to_dict()
		loc_data = dict()
		loc_data['number'] = giver_data['number']
		loc_data['address'] = giver_data['location']
		loc_data['item'] = giver_data[u'item']
		loc_data['type'] = 'give'
		try:
			location = geolocator.geocode(loc_data['address'])
			loc_data['coordinates'] = [location.latitude, location.longitude]
		except:
			loc_data['coordinates'] = [0.0, 0.0]
		loc.append(loc_data)
	for needer in needers:
		needer_data = needer.to_dict()
		loc_data = dict()
		loc_data['number'] = needer_data['number']
		loc_data['address'] = needer_data['location']
		loc_data['item'] = needer_data[u'item']
		loc_data['type'] = 'need'
		try:
			location = geolocator.geocode(loc_data['address'])
			coordinates.append([location.latitude, location.longitude])
			loc_data['coordinates'] = [location.latitude, location.longitude]
		except:
			loc_data['coordinates'] = [0.0, 0.0]
		loc.append(loc_data)
	print (loc)

	return render_template("index.html", jslocation = loc)

if __name__ == "__main__":
	app.run('localhost', 5000)
