# -*- coding: utf-8 -*-
from flask import Flask, render_template, g, request
from pymongo import Connection
from datetime import timedelta
import hashlib


try:
    from local_settings import *
except ImportError:
    sys.exit("No Flask Local Settings found!")

app = Flask(__name__)
app.debug = True


class Author(object):
    def __init__(self, screen_name):
        self.screen_name = screen_name


class Location(object):
    def __init__(self, state):
        self.state = state


class Tweet(object):
    def __init__(self, tid, author, text, created_at, created_at_bsb, created_at_local, feelings):
        self.id = tid
        self.author = author
        self.text = text
        self.created_at = created_at
        self.created_at_bsb = created_at_bsb
        self.created_at_local = created_at_local
        self.feelings = feelings


def prepareStringForJavaScript(string):
    new_string = string.replace('\n', '')
    new_string = new_string.replace('\\', '\\\\')
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


def load_feelings(file_name):
    feelings_dic = {}
    with open(file_name) as f:
        for line in f.readlines():
            line_list = line.split(';')
            feelings_dic[line_list[0].decode('utf-8')] = line_list[2].rstrip()
    return feelings_dic


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
    limit = 100
    feelings = load_feelings('../crawler/feelings.txt')
    weather_translations = load_weather_translations('../crawler/weather_translations.txt')
    states = load_states('../crawler/states.txt')
    if 'selected-feelings' in request.args:
        feelings_query_list = []
        for feeling in request.args.getlist('selected-feelings'):
            feelings_query_list.append({'feelings': feeling})
        db_tweets = g.coll.find({'$or': feelings_query_list,
                                'feelings_size': 1}, \
                                sort=[('created_at', -1)], \
                                limit=limit)

    else:
        db_tweets = g.coll.find(sort=[('created_at', -1)], limit=limit)
    tweets = []
    string_md5 = ''
    for db_tweet in db_tweets:
        string_md5 += str(db_tweet['_id'])
        tweets.append(tweetFromDictToObject(db_tweet))
    data_md5 = hashlib.md5(string_md5).hexdigest()
    return render_template('test.html',
                           tweets=tweets,
                           feelings=sorted(feelings.items()),
                           weather_translations=sorted(weather_translations.items()),
                           states=sorted(states),
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
