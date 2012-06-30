# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from pymongo import Connection
from pylibmc import Client
from hashlib import md5
from web_analytics import last_hours_sparkline, \
                          get_feelings_percentages_for_state
from tweet import tweet_from_dict_to_object
from filters import request_args_filter
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
db = Connection(MONGO_HOST)[MONGO_DB]
coll = db[MONGO_COLLECTION_TWEETS]


def tweet_list_from_cursor(db_tweets):
    tweets = []
    string_md5 = ''
    for db_tweet in db_tweets:
        string_md5 += str(db_tweet['_id'])
        tweets.append(tweet_from_dict_to_object(db_tweet))
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

    query_dict = request_args_filter(request.args, feelings, states_unique)
    db_tweets = coll.find(query_dict, \
                          sort=[('created_at', -1)], \
                          limit=limit)
    tweet_tuple = tweet_list_from_cursor(db_tweets)
    tweets = tweet_tuple[0]
    string_md5 = tweet_tuple[1]

    data_md5 = md5(string_md5).hexdigest()
    sparkline_data = last_hours_sparkline(db)
    feelings_percentages_for_states = {}
    if 'state' in request.args:
        for state in request.args.getlist('state'):
            feelings_percentages_for_states[state] = get_feelings_percentages_for_state(db, state)
    # feelings_percentages_for_states = {
    #     'mg': get_feelings_percentages_for_state(db, 'mg'),
    #     'sp': get_feelings_percentages_for_state(db, 'sp')
    # }
    return render_template('test.html',
                           tweets=tweets,
                           feelings=feelings,
                           weather_translations=sorted(weather_translations.items()),
                           states=sorted(states),
                           states_unique=sorted(states_unique),
                           data_md5=data_md5,
                           sparkline_data=sparkline_data,
                           feelings_percentages_for_states=feelings_percentages_for_states)

if __name__ == "__main__":
    app.run()
