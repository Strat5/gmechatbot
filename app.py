#~~~~~~~~~~~~~~~ Package imports.
import os
import sys
import json
from flask import Flask, request
import requests
from random import randint
import linecache
import datetime
import wget
import time
app = Flask(__name__)
message_count = 0

#~~~~~~~~~~~~~~~ General-use methods.
def post_message(bot_name, msg, image_url): #Sending a message to the group chat.
	if image_url == '': #Post message without photo.
		if bot_name == 'The Talker': #Post message from Talker.
			data = requests.post(
				url = 'https://api.groupme.com/v3/bots/post', 
				data = {
					'bot_id'  : os.getenv('TALKER_BOT_ID'),
					'text' : msg,
				}
			)
			log('The Talker Log: Message: "{}" was posted. {}'.format(msg, data))
		elif bot_name == 'The Digital Journalist': #Post message from The Digital Journalist.
			data = requests.post(
				url = 'https://api.groupme.com/v3/bots/post', 
				data = {
					'bot_id'  : os.getenv('JOURNALIST_BOT_ID'),
					'text' : msg,
				}
			)
			log('The Digital Journalist Log: Message: "{}" was posted. {}'.format(msg, data))
	else: #Post message with photo.
		if bot_name == 'The Talker': #Post message from The Talker.
			data = requests.post(
				url = 'https://api.groupme.com/v3/bots/post', 
				params = {
					'bot_id'  : os.getenv('Talker_BOT_ID'),
					'text' : msg,
					'attachments' : [
   						{
							'type' : 'image',
							'url'  : image_url
						}
					]
				},
				data = {
					'text' : 'Image',
					'picture_url' : image_url
				}
			)
			log('The Talker Log: Message: "{}" was posted along with the image at this link: {}. {}'.format(msg, image_url, data))
		elif bot_name == 'The Digital Journalist': #Post message from The Digital Journalist.
			data = requests.post(
				url = 'https://api.groupme.com/v3/bots/post', 
				params = {
					'bot_id'  : os.getenv('JOURNALIST_BOT_ID'),
					'text' : msg,
					'attachments' : [
   						{
							'type' : 'image',
							'url'  : image_url
						}
					]
				},
				data = {
					'text' : 'Image',
					'picture_url' : image_url
				}
			)
			log('The Digital Journalist Log: Message: "{}" was posted along with the image at this link: {}. {}'.format(msg, image_url, data))

def log(msg): #Printing log information.
	print(str(msg))
	sys.stdout.flush()


#----------------------------The Talker----------------------------#

#~~~~~~~~~~~~~~~ Endpoint for GroupMe messages.
@app.route('/', methods=['POST'])
def webhook():
	global message_count
	data = request.get_json()
	if data['name'] != 'The Talker' and data['name'] != 'The Assistant':
		log('The Talker Log: Received Message: "{}" from "{}".'.format(data['text'], data['name']))

		if data['text'][0] == '?': 
				post_message('The Talker', '?', '')
		for i in range(len(data['text'])): #Scan for keywords.
			if data['text'][i:i+4].lower() == 'joke': #laughs
				read_joke()
			if data['text'][i:i+5].lower() == 'quote': #motivation
				read_quote()
			if data['text'][i:i+4].lower() == 'The Talker': #laughs
				post_message('Hehehe', '?', '')

		message_count += 1 #Tracking messages sent.
		if message_count > 9:
			post_message('The Talker', "My oh my! We've already reached 10 messages! Since my last update, that is.", '')

	return "ok", 200

#~~~~~~~~~~~~~~~ Methods.
def read_quote(): #Reading a quote.
	x = randint(1, 81)
	quote = linecache.getline('quotes.txt', x)
	log('The Talker Log: Quote has been read.')
	post_message('The Talker', quote, '')

def read_joke(): #Telling a joke.
	x = randint(1, 61)
	joke = linecache.getline('jokes.txt', x)
	log('The Talker Log: Joke has been read.')
	post_message('The Talker', joke, '')


#----------------------------The Digital Journalist----------------------------#

#~~~~~~~~~~~~~~~ Endpoints for cron-scheduled pings. 
@app.route('/weather', endpoint = 'weather', methods=['POST'])
def webhook():
	read_weather()
	return "ok", 200
@app.route('/news', endpoint = 'news', methods=['POST'])
def webhook():
	read_news()
	return "ok", 200
@app.route('/history', endpoint = 'history', methods=['POST'])
def webhook():
	read_history()
	return "ok", 200
@app.route('/votd', endpoint = 'votd', methods=['POST'])
def webhook():
	read_votd()
	return "ok", 200

#~~~~~~~~~~~~~~~ Methods.
def read_weather(): #Explaining the weather forecast.
	data = requests.get(
		url = 'https://api.weatherbit.io/v2.0/forecast/daily?city=Oakdale,MN&units=I&days=1&key={}'.format(os.getenv('WEATHERBIT_API_KEY'))
	)
	log('The Digital Journalist Log: Recieved Weather. {}'.format(data))
	post_message('The Digital Journalist', "Today's high temp is {}°F, the low temp {}°F, and there is {}% predicted chance of precipitation. Clouds will cover the sky around {}% of sky today.".format(data.json()['data'][0]['high_temp'], data.json()['data'][0]['low_temp'], data.json()['data'][0]['pop'], data.json()['data'][0]['clouds']),'')	

def read_news(): #Detailing top headlines.
	data = requests.get(
		url = 'https://newsapi.org/v2/top-headlines?country=us&pageSize=30&apiKey={}'.format(os.getenv('NEWS_API_KEY'))
	)
	log("The Digital Journalist Log: Recieved Today's News. {}".format(data))
	
	#Determine three random events to display.
	story1 = randint(0, 30)
	story2 = randint(0, 30)
	story3 = randint(0, 30)

	if(story2 == story1):	#Check once to see if there is a duplicate event in the list.
		story2 = randint(0, 30)
	if(story3 == story1 or story3 == story2):
		story3 = randint(0, 30)

	post_message('The Digital Journalist', "Today's Top News: \n\n{}\n{}, \n\n{}\n{}, \n\n{}\n{}".format(data.json()['articles'][story1]['description'], data.json()['articles'][story1]['url'], data.json()['articles'][story2]['description'], data.json()['articles'][story2]['url'], data.json()['articles'][story3]['description'], data.json()['articles'][story3]['url']),'')

def read_history(): #Recalling the events of the past.
	data = requests.get(
		url = 'http://history.muffinlabs.com/date'
		)
	log("The Digital Journalist Log: Recieved Today's History. {}".format(data))

	limit = len(data.json()['data']['Events']) #Determine three random events to display.
	story1 = randint(0, limit + 1)
	story2 = randint(0, limit + 1)
	story3 = randint(0, limit + 1)

	if(story2 == story1):	#Check once to see if there is a duplicate event in the list.
		story2 = randint(0, limit + 1)
	if(story3 == story1 or story3 == story1):
		story3 = randint(0, limit + 1)

	for i in range(2): #Scan the events twice to make sure the dates are in order.
		if(data.json()['data']['Events'][story1]['year'] > data.json()['data']['Events'][story2]['year']):
			x = story1
			story1 = story2
			story2 = x
		if(data.json()['data']['Events'][story2]['year'] > data.json()['data']['Events'][story3]['year']):
			x = story3
			story3 = story2
			story2 = x
	date = data.json()['date']
	post_message('The Digital Journalist', 'Today in History, {}: \n\n{}, {}\n\n{}, {}\n\n{}, {}'.format(date, data.json()['data']['Events'][story1]['year'], data.json()['data']['Events'][story1]['text'], data.json()['data']['Events'][story2]['year'], data.json()['data']['Events'][story2]['text'], data.json()['data']['Events'][story3]['year'], data.json()['data']['Events'][story3]['text']), '')

def read_votd(): #Downloading and uploading verse of tbe day picture.
	dayNumber = (datetime.date.today() - datetime.date(2020, 1, 1)).days
	data = requests.get( #Request verse and picture url from YouVersion. 
		url ='https://developers.youversionapi.com/1.0/verse_of_the_day/{}?version_id=1'.format(dayNumber), 
		headers = {
			'accept' : 'application/json',
			'x-youversion-developer-token' : '{}'.format(os.getenv('YOUVERSION_DEVELOPER_TOKEN')),
			'accept-language' : 'en'
		}
	)
	verse = data.json()['verse']['text'] + '\n-' + data.json()['verse']['human_reference'] 
	log('The Digital Journalist Log: Recieved VOTD. {}'.format(data))


	data = wget.download(data.json()['image']['url'][56:]) #Download the picture from Youversion.
	log('The Digital Journalist Log: Image Download from YouVersion Complete.')
  

	data = requests.post( #Upload the picture to GroupMe's image service.
		url = 'https://image.groupme.com/pictures', 
		data = open('./1280x1280.jpg', 'rb').read(), 
		headers = {'Content-Type': 'image/jpeg','X-Access-Token':'{}'.format(os.getenv('GROUPME_DEVELOPER_TOKEN'))}
	)
	log('The Digital Journalist Log: Image Upload to GroupMe Complete. {}'.format(data))


	msg = '', #Post the image to the chat.
	image_url = (data.json()['payload']['url'])
	post_message('The Digital Journalist', msg, image_url)
	post_message('The Digital Journalist', verse, '')
