import webapp2
from google.appengine.api import urlfetch
from webapp2 import uri_for
import urllib
import logging
import json

API_BASE_URL = 'https://api.telegram.org/bot'
webhook_url = ''
MY_URL = ''

class MainPage(webapp2.RequestHandler):
	# Start the app with an initial get request
	def get(self):
		global API_BASE_URL
		output = startup()
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write(output + ' ' + MY_URL)
	def post(self):
		handle_update(self.request)

app = webapp2.WSGIApplication([
	webapp2.Route('/', handler=MainPage, name='webhook'),
], debug=True)

# Start up the app by loading the API key, local hostname, and checking into Telegram
def startup():
	global API_BASE_URL
	global MY_URL
	token = read_token()
	API_BASE_URL = API_BASE_URL + token + '/'
	MY_URL = read_my_url()
	return register_webhook(token)

# Load the API key from the 'TOKEN' file
def read_token():
	with open('TOKEN', 'r') as f:
		return f.read()

def read_my_url():
	with open('HOSTNAME', 'r') as f:
		return f.read()

# Register the webhook with Telegram
def register_webhook(token):
	global webhook_url
	global API_BASE_URL
	url_setWebhook = API_BASE_URL + 'setWebhook'
	form_fields = {
		'url': MY_URL
	}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url=url_setWebhook,
		payload=form_data,
		method=urlfetch.POST)
	return result.content

# Handle an update from Telegram's webhook
def handle_update(data):
	message = json.load(data.post('message'))
	user = message['from']
	user_id = user['id']
	user_username = user['username']
	#if user_username == '@AshleyJacobs':
	url_sendMessage = API_BASE_URL + 'sendMessage'
	form_fields = {
		'chat_id': user_id,
		'text': "Hello " + user_username + "!"
	}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url=url_setWebhook,
		payload=form_data,
		method=urlfetch.POST)