from flask import Flask
from flask_ask import Ask, statement, question, session
import random
from predict import predict

app = Flask(__name__)
ask = Ask(app, "/true_news")


def _random(iterable):
    length = len(iterable)
    return iterable[random.randint(0, length-1)]


@app.route('/')
def homepage():
    return "This is the website for the 'Error Reapers' Alexa Skills."


@ask.launch
def start_skill():
    hi = ['Hi!', 'Hello!', 'Hey!', 'Hey there!']
    welcome_msg = _random(hi) + " Which news would you like to verify ?"
    return question(welcome_msg)


@ask.intent("NewsReceiveIntent")
def answer(news):
    percent_true = int(predict(news))
    if 0 <= percent_true <= 50:
        result = "This news is {} percent fake.".format(100 - percent_true)
    elif 50 < percent_true <= 100:
        result = "This news is {} percent true.".format(percent_true)
    else:
        result = "I am not sure, please try again using different keywords."
    return statement(result)


@ask.intent("AMAZON.CancelIntent")
def _cancel():
    bye = ['Bye!', 'See you!', 'Goodbye']
    return statement(_random(bye))


@ask.intent("AMAZON.StopIntent")
def _stop():
    bye = ['Bye!', 'See you!', 'Goodbye']
    return statement(_random(bye))


@ask.intent("AMAZON.HelpIntent")
def _help():
    return question("This Alexa Skill will predict if the news is true or not.\n"
                    " Just tell it the news item and it will give you a probability of the news item being true.\n"
                    "Which news would you like to verify ?")


if __name__ == '__main__':
    app.run()
