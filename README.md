## 📖 Purpose: 

The primary purpose of this project is to learn about and have fun while creating a chatbot. 
But the hope is that the final product will be a function (and practical) addition to any groupchat.

## 🗒 Features:
	
- A working chatbot that uses natural language processing (NLP) to talk to users.
- A seperate bot that can post to the chat daily information including:
	- The verse of the day.
	- The weather forecast.
	- This day in history.
	- Today's top news.

## 🔨 Installation: 

Installation guide coming soon.

Note: The bot is designed to be ran on Heroku with a gunicorn setup.

## ⌨️ Usage: 

The Talker (one of the two chatbots) will recognize the following keywords in any message:
- 'joke'
- 'quote'

The Talker will also try to use natural language processing to recognize a request for one of the following catagories of top news headlines:
- business
- entertainment
- general 
- health
- science
- sports
- technology

Using the automatic pings setup in the installation section, you can customize exactly what time you would like any of the daily information (the second part of the features section) sent to the groupchat.

## 🤝 Contributing:

Contributions, issues and feature requests are welcome!

The main purpose of this project is to learn; don't hesitate to ask questions!

To start, try adding a new joke or motovational quote to the bot.
If you are new to Github and want to contribute try reading these tutorials:

- Here is a tutorial to Git and Github: https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners.
- More specifically, here is how you can edit my project: https://guides.github.com/activities/forking/.

*Please see the contributing.md file for more info.*

## 👍 Acknowledgements:

A big thank you to all these free services!

- spaCy: Industrial-strength NLP; https://github.com/explosion/spaCy
- Youversion Verse of the Day API: https://developers.youversion.com
- WeatherBit API: https://www.weatherbit.io/api
- Today’s History API: https://history.muffinlabs.com/#api
- News API: https://newsapi.org/
