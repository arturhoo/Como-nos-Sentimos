# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from pymongo import Connection
from pylibmc import Client
from hashlib import md5
from datetime import datetime
from web_analytics import last_hours_sparkline, \
                          get_feelings_percentages_for_state, \
                          get_last_hour_top_feelings, \
                          get_feeling_percentages_last_hours, \
                          get_today_top_feelings, \
                          get_weather_conditions_count_for_feeling, \
                          get_feeling_mean_percentages_for_hours, \
                          get_feeling_mean_percentages_for_every_two_hours
from tweet import tweet_from_dict_to_object
from filters import request_args_filter
from utils import get_feeling_color
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

    query_dict = request_args_filter(request.args, feelings, states)
    print query_dict
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

    feelings_percentages_last_hours = []
    weather_conditions_count_for_feelings = []
    feelings_percentages_and_mean_last_hours = []
    feelings_mean_percentages_every_two_hours = []
    if 'feeling' in request.args:
        for feeling in request.args.getlist('feeling'):
            feeling_color = get_feeling_color(feeling, feelings)
            # dt = datetime.strptime('2012-07-06 6', '%Y-%m-%d %H')
            # fplh = get_feeling_percentages_last_hours(db, feeling, date=dt)
            fplh = get_feeling_percentages_last_hours(db, feeling)
            if len(request.args.getlist('feeling')) > 1:
                feelings_percentages_last_hours.append((feeling, fplh, feeling_color))
            weather_conditions_count_for_feelings.append((feeling, get_weather_conditions_count_for_feeling(db, feeling, weather_translations)))
            # Chart with mean
            feelings_percentages_and_mean_last_hours.append((feeling, fplh, get_feeling_mean_percentages_for_hours(db, feeling, fplh[len(fplh) - 1][0]), feeling_color))

    if not 'state' in request.args and not 'feeling' in request.args:
        today_top_feelings = get_today_top_feelings(db)
        for feeling in today_top_feelings[:5]:
            feeling_color = get_feeling_color(feeling, feelings)
            # dt = datetime.strptime('2012-07-06 06', '%Y-%m-%d %H')
            feelings_percentages_last_hours.append((feeling, get_feeling_percentages_last_hours(db, feeling), feeling_color))
        for feeling in feelings:
            feeling_color = get_feeling_color(feeling[0], feelings)
            weather_conditions_count_for_feelings.append((feeling[0], get_weather_conditions_count_for_feeling(db, feeling[0], weather_translations)))
            feelings_mean_percentages_every_two_hours.append((feeling[0], get_feeling_mean_percentages_for_every_two_hours(db, feeling[0]), feeling_color))

    return render_template('test.html',
                           tweets=tweets,
                           feelings=feelings,
                           weather_translations=sorted(weather_translations.items()),
                           states=sorted(states),
                           states_unique=sorted(states_unique),
                           data_md5=data_md5,
                           sparkline_data=sparkline_data,
                           feelings_percentages_for_states=feelings_percentages_for_states,
                           feelings_percentages_last_hours=feelings_percentages_last_hours,
                           weather_conditions_count_for_feelings=weather_conditions_count_for_feelings,
                           feelings_percentages_and_mean_last_hours=feelings_percentages_and_mean_last_hours,
                           feelings_mean_percentages_every_two_hours=feelings_mean_percentages_every_two_hours)

if __name__ == "__main__":
    app.run()
