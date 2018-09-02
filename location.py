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
		loc_data['address'] = giver_data[ u'location']
		loc_data['item'] = giver_data[u'item']
		loc_data['type'] = 'give'
		loc.append(loc_data)
	for needer in needers:
		needer_data = needer.to_dict()
		loc_data = dict()
		loc_data['address'] = needer_data[ u'location']
		loc_data['item'] = needer_data[u'item']
		loc_data['type'] = 'need'
		loc.append(loc_data)
	coordinates = []
	for locate in loc:
		try:
			location = geolocator.geocode(locate)
			coordinates.append([location.latitude, location.longitude])
		except:
			continue

	return render_template("index.html", jslocation = coordinates)

if __name__ == "__main__":
	app.run('localhost', 5000)
