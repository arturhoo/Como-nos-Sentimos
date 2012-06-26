# -*- coding: utf-8 -*-
from flask import Flask, render_template, g, request
from pymongo import Connection
from datetime import timedelta
from pylibmc import Client
from hashlib import md5
from htmlentitydefs import name2codepoint
from re import sub
import locale


try:
    from local_settings import *
except ImportError:
    sys.exit("No Flask Local Settings found!")

app = Flask(__name__)
app.debug = True
mc = Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True,
                                                   "ketama": True})
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


class Author(object):
    def __init__(self, screen_name):
        self.screen_name = screen_name


class Location(object):
    def __init__(self, state):
        self.state = state


class Tweet(object):
    def __init__(self, tid, author, text, created_at, created_at_bsb, \
                 created_at_local, feelings):
        self.id = tid
        self.author = author
        self.text = text
        self.created_at = created_at
        self.created_at_bsb = created_at_bsb
        self.created_at_local = created_at_local
        self.feelings = feelings


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return sub("&#?\w+;", fixup, text)


def prepareStringForJavaScript(string):
    new_string = string.replace('\n', '')
    new_string = new_string.replace('\\', '\\\\')
    new_string = unescape(new_string)
    return new_string


def tweetFromDictToObject(tweet):
    author = Author(tweet['author']['screen_name'])
    if 'name' in tweet['author']:
        author.name = prepareStringForJavaScript(tweet['author']['name'])
    if 'location' in tweet['author']:
        author.location = prepareStringForJavaScript(tweet['author']['location'])

    location = None
    if 'location' in tweet and tweet['location'] != None:
        try:
            location = Location(tweet['location']['state'])
            if 'city' in tweet['location']:
                location.city = tweet['location']['city']
                if 'weather' in tweet['location']:
                    location.weather = tweet['location']['weather']['condition']

        except TypeError, e:
            print tweet['location']
            print >> sys.stderr, e

    new_tweet = Tweet(tweet['_id'],
                      author,
                      prepareStringForJavaScript(tweet['text']),
                      tweet['created_at'],
                      tweet['created_at'] + timedelta(seconds=-10800),
                      tweet['created_at_local'],
                      tweet['feelings'])

    if location is not None:
        new_tweet.location = location

    return new_tweet


def tweet_list_from_cursor(db_tweets):
    tweets = []
    string_md5 = ''
    for db_tweet in db_tweets:
        string_md5 += str(db_tweet['_id'])
        tweets.append(tweetFromDictToObject(db_tweet))
    return (tweets, string_md5)


def load_feelings(file_name):
    feelings_dic = {}
    with open(file_name) as f:
        for line in f.readlines():
            line_list = line.split(';')
            feelings_dic[line_list[0].decode('utf-8')] = line_list[2].rstrip()
    feelings_list = []
    for key in sorted(feelings_dic.iterkeys(), cmp=locale.strcoll):
        feelings_list.append((key, feelings_dic[key]))
    return feelings_list


def load_weather_translations(file_name):
    weather_translations_dic = {}
    with open(file_name) as f:
        for line in f.readlines():
            line_list = line.split(';')
            weather_translations_dic[line_list[0]] = line_list[1].decode('utf-8').rstrip()
    return weather_translations_dic


def load_states(file_name):
    states_list = []
    with open(file_name) as f:
        for line in f.readlines():
            line_list = line.split(';')
            states_list.append((line_list[1],
                                line_list[0].decode('utf-8'),
                                line_list[2].rstrip()))
    return states_list


@app.route("/")
def hello():
    limit = NUM_PARTICLES
    feelings = mc.get('feelings')
    if not feelings:
        feelings = load_feelings('../crawler/feelings.txt')
        mc.set('feelings', feelings, 0)
    states = mc.get('states')
    if not states:
        states = load_states('../crawler/states.txt')
        mc.set('states', states, 0)
    states_unique = mc.get('states_unique')
    if not states_unique:
        states_unique = load_states('../crawler/states_unique.txt')
        mc.set('states_unique', states_unique, 0)
    weather_translations = mc.get('weather_translations')
    if not weather_translations:
        weather_translations = load_weather_translations('../crawler/weather_translations.txt')
        mc.set('weather_translations', weather_translations, 0)
    tweets = None
    string_md5 = None

    if 'selected-feelings' in request.args:
        feelings_query_list = []
        for feeling in request.args.getlist('selected-feelings'):
            feelings_query_list.append({'feelings': feeling})
        db_tweets = g.coll.find({'$or': feelings_query_list,
                                'feelings_size': 1}, \
                                sort=[('created_at', -1)], \
                                limit=limit)
        tweet_tuple = tweet_list_from_cursor(db_tweets)
        tweets = tweet_tuple[0]
        string_md5 = tweet_tuple[1]

    elif 'selected-states' in request.args:
        states_query_list = []
        for state in request.args.getlist('selected-states'):
            state_full_name = states_unique[[x[0] for x in states_unique].index(state)][1]
            states_query_list.append({'location.state': state_full_name})
        db_tweets = g.coll.find({'$or': states_query_list}, \
                                sort=[('created_at', -1)], \
                                limit=limit)
        tweet_tuple = tweet_list_from_cursor(db_tweets)
        tweets = tweet_tuple[0]
        string_md5 = tweet_tuple[1]

    else:
        tweet_tuple = mc.get('no_kw')
        if not tweet_tuple:
            db_tweets = g.coll.find(sort=[('created_at', -1)], limit=limit)
            tweet_tuple = tweet_list_from_cursor(db_tweets)
            mc.set('no_kw', tweet_tuple, 2)
        tweets = tweet_tuple[0]
        string_md5 = tweet_tuple[1]

    data_md5 = md5(string_md5).hexdigest()
    return render_template('test.html',
                           tweets=tweets,
                           feelings=feelings,
                           weather_translations=sorted(weather_translations.items()),
                           states=sorted(states),
                           states_unique=sorted(states_unique),
                           data_md5=data_md5)

if __name__ == "__main__":
    app.run()


@app.before_request
def before_request():
    g.conn = Connection(MONGO_HOST)
    g.db = g.conn[MONGO_DB]
    g.coll = g.db[MONGO_COLLECTION]


@app.teardown_request
def teardown_request(exception):
    g.conn.disconnect()
