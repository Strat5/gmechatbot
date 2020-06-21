## Simple Guidelines:
- On your first pull request, try adding a joke or two. Don't add any material that would only be appropiate for a higher age groups.
- Got a new idea for the bot? Make a feature request! Also, if you want to personally program it into the bot, anwser yes to the last question.
- Please try to add commenting where you deem necessary, refer to [this article](https://www.elegantthemes.com/blog/wordpress/how-to-comment-your-code-like-a-pro-best-practices-and-good-habits) for some tips.

Note: The master branch on this repositiory auto deploys to a Heroku for testing; please do not submit a pull request from a fork with a known bug.

## Resources: 

API Documentation Links:
	- GroupMe API Documentation: https://dev.groupme.com
	- WeatherBit API Documentation: https://www.weatherbit.io/api
	- Today’s History API Documentation: https://history.muffinlabs.com/#api
	- News API Documentation: https://newsapi.org/docs/

Spacy NLP Documentation: 
	https://spacy.io/api/doc 

Spacy Online Course: 
	https://course.spacy.io/en <-- At least do Chapter 1. 

Chatbot Online Course:
	https://campus.datacamp.com/courses/building-chatbots-in-python/chatbots-101?ex=1

The Community! Don't understand something about the bot? Create a new issue, and make sure to give the label 'question' to it.

## Explanation of each file in the application:

Procfile - This tells Heroku what basic service to run.

runtime.txt - This tells Heroku what code enviroment I am using in my code.

requirements.txt - This tells Heroku what additional--in this case we have python--packages to install.

app.py - The main application, where all the bot magic occurs.

config.py - The on/off switches for each keyword the bot reads in chat messages.

jokes.txt - A list of jokes used by the bot.

quotes.txt - A list of motivational quotes used by the bot.

## Overview of app.py:

The code is mainly seperated into two functions and likewise two different bots.

"The Journalist" is the chatbot that collects research-like information, like the weather forecast. 
"The Talker" is the chatbot that directly interacts and talks with the users. 

## Understanding the code:

The indivdual parts of the code should be explained by the commenting. *If there is a space where this is not the case, please fix it.*

There are two special features that the bot incorporates:

- The use of APIs: These allow the chatbot to fetch the daily update stuff from other websites, or even post messages to GroupMe itself!
Here is a great video explaining APIs: https://safeyoutube.net/w/DPXI.

- The use of a NLP module: It allows the chatbot to sort through any given message and try to find the intent of the message, among other things.
Here is great resource: https://www.sas.com/en_us/insights/analytics/what-is-natural-language-processing-nlp.html.