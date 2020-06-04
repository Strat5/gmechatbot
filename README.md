PURPOSE AND INTENDED USE:

Welcome to my chatbot development page!
The purpose of this project is to learn about creating and having fun with a chatbot. 
The hope is that the final product will be a function (and practical) addition to any normal groupchat.

FUNCTION:

At it's max capability, it can send: the verse of day, the weather forecast, today in history, today's top news, and most importantly, it can directly talk with the users in it's groupchat.

THE OVERALL CONFIGURATION OF THIS CHATBOT: 

This chatbot is designed to be implemented on GroupMe, but can be transfered to a different messaging service relatively easiliy.
Since this is not a professional project, this is designed to run on a free Heroku server that in turn runs gunicorn (a webserver infastructure) that is programmed by the app.py file. 
Heroku offers free 24/7 hosting, but with limited computer hours, so certain time-based features require an outside source sending a wake-up ping. Personally I use an Ubuntu server that runs cron to automatically activate python programs that do the pinging.
Flask is imported in the code to handle HTTP POST requests.
The files in this GitHub directory are uploaded to Heroku automatically.

OVERVIEW OF APP.PY:

The indivdual parts of the code should be clearly explained by comments. *If there is a space where this is not the case, please fix it.*
There are two bots detailed in the code. 

"The Journalist" is the chatbot that collects time-specific information. This information can be released by pinging one of it's endpoints.
"The Talker" is the chatbot that directly interacts and talks with the users. If no users ever send a message, it is entirely useless.

UNDERSTANDING THE CODE:

I will do my best to add comments that are helpful in the code, but sometimes that's not always enough. 
Questions about the logic flow of the bot are usually anwsered by a quick Google search. 
However, there are two main components that make this chatbot special.

The use of APIs: These allow the chatbot to fetch the daily update stuff from other websites, or even post messages to GroupMe itself!
Here is a great video explaining APIs: https://safeyoutube.net/w/DPXI.

The use of a already built NLP package: It allows the chatbot to sort through any given message and try to find the intent of the message, among other things.
Here is great resource: https://www.sas.com/en_us/insights/analytics/what-is-natural-language-processing-nlp.html

*If you have any questions please leave a message or message me directly.*

COLLABORATION GUIDELINES:

I would like to make it clear that I am in no way expert, nor necessarily experienced in any of the above catagories. 
The main goal is to learn while creating a workable model of that learning.

I would really like others to collaborate on this with others! Github is a very good method of doing so. 
You can look at all my files, and you can download them, look at them via text editor, change them, and ask me to incoporate it.
Also, if you don't have a special programming-specific text editor, try this: https://www.sublimetext.com. (It's free.)

GitHub can be a bit daunting a first, but after a little while, it's very effective. 
Here is a tutorial to Git and Github: https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners
More specifically, here is how you can edit my project: https://guides.github.com/activities/forking/

*Just please try to keep your code commenting simple but effective.*
Thank you!
