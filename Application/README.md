## Explanation of each file in the application:

Procfile - This tells Heroku what basic service to run.

runtime.txt - This tells Heroku what code enviroment I am using in my code.

requirements.txt - This tells Heroku what additional--in this case we have python--packages to install.

app.py - The main application, where all the bot magic occurs.

jokes.txt - A list of jokes needed by the bot.

quotes.txt - A list of motivational quotes need by the bot.

## Overview of app.py:

The code is mainly seperated into two functions and likewise two different bots.

"The Journalist" is the chatbot that collects time-specific information. This information can be released by pinging one of it's endpoints.
"The Talker" is the chatbot that directly interacts and talks with the users. If no users ever send a message, it is entirely useless.

## Understanding the code:

The indivdual parts of the code should be clearly explained by the commenting. *If there is a space where this is not the case, please fix it.*

There are two special features that the bot incorporates:

- The use of APIs: These allow the chatbot to fetch the daily update stuff from other websites, or even post messages to GroupMe itself!
Here is a great video explaining APIs: https://safeyoutube.net/w/DPXI.

- The use of a NLP module: It allows the chatbot to sort through any given message and try to find the intent of the message, among other things.
Here is great resource: https://www.sas.com/en_us/insights/analytics/what-is-natural-language-processing-nlp.html.