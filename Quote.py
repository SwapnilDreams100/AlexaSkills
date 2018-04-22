from flask import Flask
from flask_ask import Ask, statement, question, session
from requests import get
import random
import time

app = Flask(__name__)
ask = Ask(app, "/lift_my_mood")
start = 0


def _random(iterable):
    length = len(iterable)
    return iterable[random.randint(0, length - 1)]


def predict_mood(mood):
    global start
    waste = (
        'i', 'am', 'very', 'feeling', 'very', 'extremely', 'you', 'too', 'to', 'him', 'super', 'his', 'we', 'some',
        'bit', 'in', 'somewhat', 'quite', 'little', 'much', 'tiny', 'a', 'an')
    emotions = (
        'love', 'anger', 'happiness', 'sadness', 'hate', 'boredom', 'worry', 'relief', 'surprise', 'enthusiasm', 'fun',
        'neutral')
    words = mood.split()
    s = 0
    ans = 'neutral'
    for word in words:
        if word.lower() not in waste:
            for emotion in emotions:
                if time.time() - start < 7.0:
                    score = 0.0
                    url = 'http://swoogle.umbc.edu/SimService/GetSimilarity?operation=api&phrase1=' + emotion + '&phrase2=' + word + '&corpus=webbase&type=relation'
                    try:
                        response = get(url)
                        score = float(response.text.strip())
                    except:
                        score = 0.0
                    if score > s:
                        s = score
                        ans = emotion
                else:
                    break
    if s < 0.1:
        ans = 'neutral'
    return ans


def get_quote(mood):
    quotes = {
        'love': ['There is only one happiness in this life, to love and be loved.',
                 'Love is when the other person\'s happiness is more important than your own.',
                 'Being deeply loved by someone gives you strength, while loving someone deeply gives you courage.',
                 'The most important thing in the world is family and love.',
                 'Sometimes the heart sees what is invisible to the eye.'],
        'enthusiasm': ['Enthusiasm is everything. It must be taut and vibrating like a guitar string.',
                       'Protect your enthusiasm from the negativity of others.',
                       'Enthusiasm is excitement with inspiration, motivation, and a pinch of creativity.',
                       'There is a real magic in enthusiasm. It spells the difference between mediocrity and accomplishment.',
                       'Enthusiasm moves the world.'],
        'surprise': ['Surprise is the greatest gift which life can grant us.',
                     'Mystery is at the heart of creativity. That, and surprise.',
                     'Life\'s supposed to be an adventure, a surprise!',
                     'The big things happen unexpectedly...', ],
        'anger': ['You will not be punished for your anger, you will be punished by your anger.',
                  'People won\'t have time for you if you are always angry or complaining.',
                  'For every minute you remain angry, you give up sixty seconds of peace of mind.',
                  'Anger and intolerance are the enemies of correct understanding.',
                  'Bitterness is like cancer. It eats upon the host. But anger is like fire. It burns it all clean.'],
        'happiness': [
            'Happiness is not something you postpone for the future; it is something you design for the present.',
            'Be happy for this moment. This moment is your life.',
            'Happiness radiates like the fragrance from a flower and draws all good things towards you.',
            'Happiness lies in the joy of achievement and the thrill of creative effort.',
            'A smile is happiness you\'ll find right under your nose.'],
        'sadness': ['We are no longer happy so soon as we wish to be happier.',
                    'Every day is a new day, and you\'ll never be able to find happiness if you don\'t move on.',
                    'Some days are just bad days, that\'s all. You have to experience sadness to know happiness, and I remind myself that not every day is going to be a good day, that\'s just the way it is!',
                    'Sadness flies away on the wings of time.',
                    'Sadness is but a wall between two gardens.', ],
        'hate': [
            'Let\'s practice motivation and love, not discrimination and hate.',
            'Darkness cannot drive out darkness; only light can do that. Hate cannot drive out hate; only love can do that.',
            'I have decided to stick with love. Hate is too great a burden to bear.',
            'I shall allow no man to belittle my soul by making me hate him.',
            'If you hate a person, you hate something in him that is part of yourself. What isn\'t part of ourselves doesn\'t disturb us.'],
        'boredom': [
            'There\'s no excuse to be bored. Sad, yes. Angry, yes. Depressed, yes. Crazy, yes. But there\'s no excuse for boredom, ever.',
            'When you pay attention to boredom it gets unbelievably interesting.',
            'Boredom always precedes a period of great creativity.',
            'The two enemies of human happiness are pain and boredom.',
            'Perhaps the world\'s second-worst crime is boredom; the first is being a bore.'],
        'worry': [
            'Don\'t worry about the pressure or the responsibility. Just live in it, have fun, and when everything seems to be going right, just stay humble and remember your family.',
            'Don\'t worry what people say or what people think. Be yourself.',
            'Worry never robs tomorrow of its sorrow, it only saps today of its joy.',
            'Life is too short to worry about anything. You had better enjoy it because the next day promises nothing.',
            'Pray, and let God worry.'],
        'fun': ['Just play. Have fun. Enjoy the game.',
                'If you go around being afraid, you\'re never going to enjoy life. You have only one chance, so you\'ve got to have fun.',
                'Even though you\'re growing up, you should never stop having fun.',
                'Winning is only half of it. Having fun is the other half.',
                'When you have confidence, you can have a lot of fun. And when you have fun, you can do amazing things.'],
        'neutral': ['Laughter is the tonic, the relief, the surcease for pain.',
                    'Smile, it\'s free therapy.',
                    'No matter what people tell you, words and ideas can change the world.',
                    'A penny saved is a penny earned.',
                    'When you reach the end of your rope, tie a knot in it and hang on.',
                    'He who lives in harmony with himself lives in harmony with the universe.'],
        'relief': ['A person free to choose will always choose peace.',
                   'Smile, it\'s free therapy.',
                   'Those who are free of resentful thoughts surely find peace.',
                   'I hope for nothing. I fear nothing. I am free.',
                   'None but ourselves can free our minds.'],
    }
    return _random(quotes[mood])


@app.route('/')
def homepage():
    return "This is the website for the 'Error Reapers' Alexa Skills."


@ask.launch
def start_skill():
    hi = ['Hi!', 'Hello!', 'Hey!', 'Hey there!']
    welcome_msg = _random(hi) + " How are you feeling today ?"
    return question(welcome_msg)


@ask.intent("FeelingReceiveIntent")
def answer(feeling):
    global start
    start = time.time()
    mood = predict_mood(feeling)
    quote = get_quote(mood)
    return statement(quote)


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
    return statement("This Alexa Skill will tell you a quote based on your current mood.")


if __name__ == '__main__':
    app.run()
