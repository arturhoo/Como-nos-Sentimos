# -*- coding: utf-8 -*-
from flask import Flask, render_template, g
from pymongo import Connection
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
    def __init__(self, tid, author, text, created_at, created_at_local, feelings):
        self.id = tid
        self.author = author
        self.text = text
        self.created_at = created_at
        self.created_at_local = created_at_local
        self.feelings = feelings


def prepareStringForJavaScript(string):
    new_string = string.replace('\n', '')
    new_string = new_string.replace('\\', '\\\\')
    return new_string


def tweetFromDictToObject(tweet):
    author = Author(tweet['author']['screen_name'])
    if 'name' in tweet['author']:
        author.name = tweet['author']['name']
    if 'location' in tweet['author']:
        author.location = tweet['author']['location']

    location = None
    if 'location' in tweet:
        location = Location(tweet['location']['state'])
        if 'city' in tweet['location']:
            location.city = tweet['location']['city']

    new_tweet = Tweet(tweet['_id'],
                      author,
                      prepareStringForJavaScript(tweet['text']),
                      tweet['created_at'],
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


@app.route("/")
def hello():
    feelings = load_feelings('../crawler/feelings.txt')
    db_tweets = g.coll.find(sort=[('created_at', -1)], limit=100)
    tweets = []
    string_md5 = ''
    for db_tweet in db_tweets:
        string_md5 += str(db_tweet['_id'])
        tweets.append(tweetFromDictToObject(db_tweet))
    # tweet = g.coll.find_one()
    # new_tweet = tweetFromDictToObject(tweet)
    data_md5 = hashlib.md5(string_md5).hexdigest()
    return render_template('test.html', tweets=tweets, feelings=feelings.items(), data_md5=data_md5)

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
