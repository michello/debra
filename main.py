import os
import Cookie

from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from flask import Flask, request, redirect, session, make_response, render_template
from google.cloud import firestore

from geopy.geocoders import Nominatim

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config.from_object(__name__)

TWILIO_SID = os.environ['TWILIO_SID']
TWILIO_TOKEN = os.environ['TWILIO_TOKEN']

t_client = Client(TWILIO_SID, TWILIO_TOKEN)

C = Cookie.SimpleCookie()

db = firestore.Client()

givers_ref = db.collection(u'GiverCalls')
needers_ref = db.collection(u'NeederCalls')

@app.route("/incoming_sms", methods=['GET', 'POST'])
def incoming_sms():
  resp = MessagingResponse()
  resp_message = ""

  if request.method == 'POST':
    message_body = request.values.get('Body', None)
    number = request.values.get('From', None)


    
    if message_body.upper() == 'HI DEBRA':
    	resp_message = "Hello! I am DEBRA (Disaster Emergency Bot Relief Alert). First, please provide the address you currently are at by typing, 'I am currently at...'"
    elif 'I am currently at' in message_body:
    	C["cookie_location"] = message_body.replace('I am currently at ','')
        print(C["cookie_location"])
        resp_message = "Thanks! If you wish to receive supplies or help, please start your text either with 'I can provide...' or 'I need these supplies...'"
    elif 'I need these supplies' in message_body:
    	# save stuff into db
      item = message_body.split("I need these supplies")[-1].strip()
      #C["cookie_request"] = message_body.replace('I am currently at ','')
      #print(C["cookie_location"])
      needer = {
          u'number': number,
          u'item': item,
          u'user_id': 1,
          u'location': C["cookie_location"].value,
          u'completion': False
      }
      needers_ref.document(number).set(needer)
      needers = needers_ref.get()
      for needer in needers:
        print (u'{} => {}'.format(needer.id, needer.to_dict()))
      givers = givers_ref.get()
      givers_lst = []
      for giver in givers:
        giving = giver.to_dict()
        if giving[u'item'] == item:
          givers_lst.append([giving[u'location'], giving[u'number']])
      if len(givers_lst) == 0:
        resp_message = "Thanks for your request! I'll update you when there's someone with your supplies ASAP. (:"
      else:
        resp_message = "Thanks for your request! Here are the locations with the supplies you need!\n"
        for givering in givers_lst:
          resp_message += givering[0] + ":" + givering[1] + "\n"
    elif 'I can provide' in message_body:
    	# save stuff into db
      item = message_body.split("I can provide")[-1].strip()
      giver = {
          u'number': number,
          u'item': item,
          u'user_id': 1,
          u'location':C["cookie_location"].value,
          u'supply': True
      }
      givers_ref.document(number).set(giver)
      givers = givers_ref.get()
      for giver in givers:
        print (u'{} => {}'.format(giver.id, giver.to_dict()))
      resp_message = "Thanks for your request! I'll update you."
      needers_lst = []
      needers = needers_ref.get()
      for needer in needers:
        needy = needer.to_dict()
        if needy[u'item'] == item:
          needers_lst.append(needy[u'number'])
      for person in needers_lst:
        print(person)
        s_client = Client("ACbb4b9650631364e99781ded800fa9699", "0a068601c149167e134887defd6fc2a9")
        message = s_client.messages.create(
                              from_='+19893682123',
                              body="Hey! Here's a new location with your supplies!\n" +  C["cookie_location"].value + ":" + number,
                              to=person
                          )
    elif message_body.upper() == "HELP!":
      resp_message = "Hi DEBRA: Activate DEBRA bot"
    else:
    	resp_message = "Whoops, that is an invalid text! Feel free to text 'Help!' for a full list of commands. :)"

  resp.message(resp_message)
  return str(resp)

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
  app.secret_key = "SECRET_KEY"
  app.run('localhost', 5000)