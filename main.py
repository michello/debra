import os
import Cookie

from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from flask import Flask, request, redirect, session, make_response
from google.cloud import firestore

app = Flask(__name__)
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
    number = request.values.get('from', None)
    
    if message_body == 'HI DEBRA':
    	resp_message = "Hello! I am DEBRA (Disaster Emergency Bot Relief Alert). First, please provide the address you currently are at by typing, 'I am currently at...'"
    elif 'I am currently at' in message_body:
    	C["cookie_location"] = message_body.replace('I am currently at ','')
    	resp_message = "Thanks! If you wish to receive supplies or help, please start your text either with 'I can provide...' or 'I need these supplies...'"
    elif 'I need these supplies' in message_body:
    	# save stuff into db
      item = message_body.split("I need these supplies")[-1].strip()
      C["cookie_request"] = message_body.replace('I am currently at ','')
      needer = {
          u'number': number,
          u'item': item,
          u'user_id': 1,
          u'location':C["cookie_request"],
          u'completion': False
      }
      needers_ref.document(number).set(needer)
      resp_message = "Thanks for your request! I'll update you when there's someone with your supplies ASAP. (:"
    elif 'I can provide' in message_body:
    	# save stuff into db
      item = message_body.split("I can provide")[-1].strip()
      C["cookie_request"] = message_body.replace('I am currently at ','')
      giver = {
          u'number': number,
          u'item': item,
          u'user_id': 1,
          u'location':C["cookie_request"],
          u'supply': True
      }
      givers_ref.document(number).set(giver)
      resp_message = "Thanks for your request! I'll update you."
    else:
    	resp_message = "Whoops, that is an invalid text! Feel free to text 'Help!' for a full list of commands. :)"

  resp.message(resp_message)
  return str(resp)

if __name__ == "__main__":
  app.secret_key = "SECRET_KEY"
  app.run('localhost', 5000)