

from flask import Flask, request, redirect, session, make_response, render_template
app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route("/location")
def locations():
	loc = ['917 63rd St, Brooklyn, NY']
	return render_template("index.html", jslocation = loc)

if __name__ == "__main__":
	app.run('localhost', 5000)
