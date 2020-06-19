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
import spacy
from spacy.matcher import Matcher
import en_core_web_sm

app = Flask(__name__)
nlp = en_core_web_sm.load()
matcher = Matcher(nlp.vocab)


#----------------------------The Talker----------------------------#

#~~~~~~~~~~~~~~~ Endpoints.
@app.route('/', methods=['POST']) 
def webhook():				
	data = request.get_json()
	if data['sender_type'] == 'user': #did the user send the message?
		log('The Talker Log: Received Message: "{}" from "{}".'.format(data['text'], data['name']))
		scan_message(data['text'])
	return "ok", 200
@app.route('/quote', endpoint = 'quote', methods=['POST'])
def webhook():
	log('The Talker Log: Received a ping to the /quote endpoint.')
	read_quote()
	return "ok", 200
@app.route('/joke', endpoint = 'joke', methods=['POST'])
def webhook():
	log('The Talker Log: Received a ping to the /joke endpoint.')
	read_joke()
	return "ok", 200

#~~~~~~~~~~~~~~~ Methods.
def read_quote():
	x = randint(1, 80)
	quote = linecache.getline('quotes.txt', x) #reading a random line in the file
	log('The Talker Log: Quote has been read.')
	post_message('The Talker', quote, '')

def read_joke():
	x = randint(1, 61)
	joke = linecache.getline('jokes.txt', x) #reading a random line in the file
	log('The Talker Log: Joke has been read.')
	post_message('The Talker', joke, '')

def scan_message(msg):
	doc = nlp(msg)
	for token in doc: #iterate over each token (a word or punctuation)
		#Keywords.
		if token.text.lower()[0:4] == 'joke':
			read_joke()
		if token.text.lower()[0:5] == 'quote':
			read_quote()
		if token.text.lower()[0:7] == 'weather':
			read_weather()
		if token.text.lower()[0:7] == 'holiday':
			read_holiday()
		if token.text.lower()[0:4] == 'news':
			read_news('')
		if token.text.lower()[0:7] == 'history':
			read_history()
		if token.text.lower()[0:5] == 'verse':
			read_verse()

	#Spacy matching patterns for custom news 
	matcher.add("CUSTOM_NEWS_PATTERN1", None, [{"POS":"NOUN"}, {"LOWER":"news"}])   
	matcher.add("CUSTOM_NEWS_PATTERN2", None, [{'LOWER': 'news'}, {'POS': 'ADP'}, {'POS': 'NOUN'}])
	matcher.add("CUSTOM_NEWS_PATTERN3", None, [{"POS":"PROPN"}, {"LOWER":"news"}])   
	matcher.add("CUSTOM_NEWS_PATTERN4", None, [{'LOWER': 'news'}, {'POS': 'ADP'}, {'POS': 'PROPN'}])
	matches = matcher(doc)

	# Iterate over the matches and tokens to find the category
	found_news_category = False
	for match_id, start, end in matches:
		for token in doc[start:end]:
			if token.text.lower() != 'news' and token.pos_ != 'ADP':
				possible_catagories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
				for i in possible_catagories:
					if token.text.lower() == i:
						found_news_category = True
						log('The Talker Log: Asking The Journalist for news about {}.'.format(token.text))
						read_news(token.text)
						break

				if found_news_category == False:
					log('The Talker Log: Received an unacceptable news request.')
					post_message("The Talker", "It appears that you requested news, but you did not provide an acceptable category. Try asking for news about: business, entertainment, general, health, science, sports, or technology.", '')


#----------------------------The Digital Journalist----------------------------#

#~~~~~~~~~~~~~~~ Endpoints. 
@app.route('/weather', endpoint = 'weather', methods=['POST'])
def webhook():
	log('The Digital Journalist Log: Received a ping to the /weather endpoint.')
	read_weather()
	return "ok", 200
@app.route('/holiday', endpoint = 'holiday', methods=['POST'])
def webhook():
	log('The Digital Journalist Log: Received a ping to the /holiday endpoint.')
	read_holiday()
	return "ok", 200
@app.route('/news', endpoint = 'news', methods=['POST'])
def webhook():
	log('The Digital Journalist Log: Received a ping to the /news endpoint.')
	read_news('')
	return "ok", 200
@app.route('/history', endpoint = 'history', methods=['POST'])
def webhook():
	log('The Digital Journalist Log: Received a ping to the /history endpoint.')
	read_history()
	return "ok", 200
@app.route('/verse', endpoint = 'verse', methods=['POST'])
def webhook():
	log('The Digital Journalist Log: Received a ping to the /verse endpoint.')
	read_verse()
	return "ok", 200

#~~~~~~~~~~~~~~~ Methods.
def read_weather():
	data = requests.get( #get the weather at Oakdale, Minnesota, in imperial units
		url = 'https://api.weatherbit.io/v2.0/forecast/daily?city=Oakdale,MN&units=I&days=1&key={}'.format(os.getenv('WEATHERBIT_API_KEY'))
	)
	log('The Digital Journalist Log: Received Weather. {}'.format(data))
	post_message('The Digital Journalist', "Today's high temp is {}°F, the low temp {}°F, and there is {}% predicted chance of precipitation. Clouds will cover the sky around {}% of sky today.".format(data.json()['data'][0]['high_temp'], data.json()['data'][0]['low_temp'], data.json()['data'][0]['pop'], data.json()['data'][0]['clouds']),'')	

def read_holiday():
	month = datetime.date.today().month
	day = datetime.date.today().day
	data = requests.get(
    url='https://calendarific.com/api/v2/holidays?api_key={}&country=US&year=2020&month={}&day={}&location=us-mn'.format(os.getenv('CALENDARIFIC_API_KEY'), month, day)
	)
	log("The Digital Journalist Log: Received The Holidays. {}".format(data))

	if(len(data.json()['response']['holidays']) == 0):
		post_message('The Digital Journalist', 'There are no state or national holidays today.', '')
	else:
		message = "Today's National Holidays:"
		for i in range(len(data.json()['response']['holidays'])):
			message = message + '\n\n' + data.json()['response']['holidays'][i]['name'] + '\n' + data.json()['response']['holidays'][i]['description']
		post_message('The Digital Journalist', message, '')

def read_news(category):
	if category == '':
		category = 'general'
		log("The Digital Journalist Log: Asking for today's top news.")
	else:
		log('The Digital Journalist Log: Asking for news about "{}."'.format(category))

	url_category = 'category=' + category + '&' #add the url format to custom news request
	data = requests.get(#get the top twenty US headlines, with an optional custom query
		url = 'http://newsapi.org/v2/top-headlines?country=us&{}apiKey={}'.format(url_category, os.getenv('NEWS_API_KEY'))
	)
	log("The Digital Journalist Log: Received The News. {}".format(data))
	
	limit = data.json()['totalResults']
	story1 = randint(0, 19)
	story2 = randint(0, 19)
	story3 = randint(0, 19)

	#Check once to try to fix a duplicate event in the list.
	if(story2 == story1): 
		story2 = randint(0, 19)
	if(story3 == story1 or story3 == story2):
		story3 = randint(0, 19)

	story1_title = data.json()['articles'][story1]['title']
	story2_title = data.json()['articles'][story2]['title']
	story3_title = data.json()['articles'][story3]['title']
	story1_url = data.json()['articles'][story1]['url']
	story2_url = data.json()['articles'][story2]['url']
	story3_url = data.json()['articles'][story3]['url']
	better_title = category[0].upper() + category[1:]

	post_message('The Digital Journalist', "Top {} Headlines: \n\n{}\n{}, \n\n{}\n{}, \n\n{}\n{}".format(better_title, story1_title, story1_url, story2_title, story2_url, story3_title, story3_url),'')

def read_history():
	data = requests.get(
		url = 'http://history.muffinlabs.com/date'
		)
	log("The Digital Journalist Log: Received Today's History. {}".format(data))

	#Determine three random events to display.
	limit = len(data.json()['data']['Events']) 
	story1 = randint(0, limit - 1)
	story2 = randint(0, limit - 1)
	story3 = randint(0, limit - 1)

	#Check once to see if there is a duplicate event in the list.
	if(story2 == story1):	
		story2 = randint(0, limit - 1)
	if(story3 == story1 or story3 == story1):
		story3 = randint(0, limit - 1)

	#Scan the events twice to make sure the dates are in order.
	for i in range(2): 
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

def read_verse():
	dayNumber = (datetime.date.today() - datetime.date(2020, 1, 1)).days
	data = requests.get( #Request verse and picture url from YouVersion. 
		url ='https://developers.youversionapi.com/1.0/verse_of_the_day/{}?version_id=1'.format(dayNumber), 
		headers = {
			'accept' : 'application/json',
			'x-youversion-developer-token' : '{}'.format(os.getenv('YOUVERSION_DEVELOPER_TOKEN')),
			'accept-language' : 'en'
		}
	)
	log('The Digital Journalist Log: Received the verse of the day. {}'.format(data))
	
	verse = data.json()['verse']['text'] + '\n- ' + data.json()['verse']['human_reference'] 
	data = wget.download(data.json()['image']['url'][56:]) #Download the picture from Youversion.
	log('The Digital Journalist Log: Image Download from YouVersion Complete.')
  

	data = requests.post( #Upload the picture to GroupMe's image service.
		url = 'https://image.groupme.com/pictures', 
		data = open('./1280x1280.jpg', 'rb').read(), 
		headers = {'Content-Type': 'image/jpeg','X-Access-Token':'{}'.format(os.getenv('GROUPME_DEVELOPER_TOKEN'))}
	)
	log('The Digital Journalist Log: Image Upload to GroupMe Complete. {}'.format(data))

	#Post the image to the chat.
	image_url = (data.json()['payload']['url'])
	post_message('The Digital Journalist', '', image_url)
	post_message('The Digital Journalist', verse, '')


#----------------------------General-use Methods
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
