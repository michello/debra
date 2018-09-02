from geopy.geocoders import Nominatim
from flask import Flask, request, redirect, session, make_response, render_template
app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route("/location")
def locations():
	geolocator = Nominatim()
	loc = ['917 63rd St, Brooklyn, NY']
	coordinates = []
	for locate in loc:
		location = geolocator.geocode(locate)
		coordinates.append([location.latitude, location.longitude])

	return render_template("index.html", jslocation = coordinates)

if __name__ == "__main__":
	app.run('localhost', 5000)
