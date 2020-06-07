## 📖 Purpose: 

The primary purpose of this project is to learn about and have fun while creating a chatbot. 
But the hope is that the final product will be a function (and practical) addition to any GroupMe groupchat.

## 🗒 Features (as of the last published version):
	
- Using keywords, the bots (there are two programmed into one app, each with different functions) recognize requests for the following information:
	- A joke.
	- A (motivational) quote
	- The verse of the day.
	- The weather forecast.
	- This day in history.
	- Today's top news--with an additional feature allowing many news catagories.
- All of the above features also have an server endpoint attached to them, which any machine can ping to activate their respective functions.

## 🔨 Installation: 
This is the recommended and tested setup, feel free to switch out server hosting providers, for example, but we can not guarantee any results. Contact us with any questions!

The following guide is only for those who know how to navigate their computer well; a more complex guide will come out soon.
Step 1: Install Git from here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.
Step 2: Install Heroku CLI from here: https://devcenter.heroku.com/articles/heroku-cli.
Step 3: Go to heroku.com and signup (or log in).
Step 4: Click "New" in the top left corner, click "Create new app."
Step 5: Go to https://github.com/Strat5/gmechatbot, and click "Clone or download," then "Download ZIP"
Step 6: In your downloads, folder unzip the gmechatbot-master file, and move the file to your preferred directory
Step 6: Open cmd if you are in Windows, or terminal on MacOS or Linux.
Step 7: Navigate using the cd command to the gmechatbot-master file.
Step 8: Enter the following commands
	- "heroku login"
		- you will need to provide your heroku account login details
	- cd server_application
	- git init .
	- heroku git:remote -a {name of your heroku app here... without the curly braces}
	- git add -A
	- git commit 
	- git push heroku master
Step 9: Go to dev.groupme.com and log in with your GroupMe account.
	- You will need to provide a verification code that is texted or emailed to you.
Step 10: Click "Bots" at the top of the screen.
Step 11: Click the orange "Create Bot" button.
Step 12: Select the groupchat you want to the bot to live in, fill in the name of bot #1, the callback url with this: "https://{name of your heroku app here... without the curly braces}.herokuapp.com/", and then click "Submit."
Step 13: Repeat steps 12 and 13 but with a different name for the second bot, and don't include a callback url.
Step 14: Test it in GroupMe! If it doesn't work, try to see if you missed a step. If you can't figure it out, ask a question in Github.

For those who know what they are doing, try setting up cron--or some other alternative--on a server to automatically ping the provided endpoints: 
	- /joke
	- /quote
	- /verse
	- /weather
	- /history
	- /news

## ⌨️ Usage: 

The Talker (one of the two chatbots) will recognize the following keywords in any message:
- 'joke'
- 'quote'
- 'verse'
- 'weather'
- 'history'
- 'news'

For those who know what they are doing, try setting up cron--or some other alternative--on a server to automatically ping the provided endpoints: 
	- /joke
	- /quote
	- /verse
	- /weather
	- /history
	- /news

## 🤝 Contributing:

Contributions, issues and feature requests are welcome!

The main purpose of this project is to learn; don't hesitate to ask questions!

To start, try adding a new joke or motovational quote to the bot.
If you are new to Github and want to contribute try reading these tutorials:

- Here is a tutorial to Git and Github: https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners.
- More specifically, here is how you can edit my project: https://guides.github.com/activities/forking/.

*Please see the contributing.md file for more info.*

## 👍 Acknowledgements:
Thank you to this article which got this project started!
http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/

A big thank you to all these free services!

- spaCy: Industrial-strength NLP; https://github.com/explosion/spaCy
- Youversion Verse of the Day API: https://developers.youversion.com
- WeatherBit API: https://www.weatherbit.io/api
- Today’s History API: https://history.muffinlabs.com/#api
- News API: https://newsapi.org/
