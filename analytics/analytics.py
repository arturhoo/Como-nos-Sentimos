# -*- coding: utf-8 -*-
from datetime import datetime
from ast import literal_eval
from beanstalkc import Connection as BSConnection
from pymongo import Connection as MongoConnection


try:
    from local_settings import *
except ImportError:
    sys.exit("No Crawler Local Settings found!")

coll_hist = MongoConnection(host=MONGO_HOST)[MONGO_DB][MONGO_COLLECTION_STATS_HISTORY]
coll_general = MongoConnection(host=MONGO_HOST)[MONGO_DB][MONGO_COLLECTION_STATS_GENERAL]
bs = BSConnection(host=BEANSTALKD_HOST, port=BEANSTALKD_PORT)
bs.watch(BEANSTALKD_TUBE)
bs.ignore('default')


def load_states_abbreviations(file_name):
    states_dic = {}
    with open(file_name) as f:
        for line in f.readlines():
            line_list = line.split(';')
            states_dic[line_list[0].decode('utf-8')] = line_list[1]
    return states_dic


def insert_history(feeling, date, state, weather):
    feeling_key = 'feelings.' + feeling
    inc_data = {feeling_key + '.count': 1, 'count': 1}
    if state is not None:
        inc_data[feeling_key + '.states.' + state] = 1
    if weather is not None:
        inc_data[feeling_key + '.weather.' + weather] = 1

    monthly_key = {
        'type': 'monthly',
        'year': int(datetime.strftime(date, '%Y')),
        'month': int(datetime.strftime(date, '%m'))
    }
    monthly_data = {'$inc': inc_data}
    coll_hist.update(monthly_key, monthly_data, True)

    daily_key = {
        'type': 'daily',
        'year': int(datetime.strftime(date, '%Y')),
        'month': int(datetime.strftime(date, '%m')),
        'day': int(datetime.strftime(date, '%d'))
    }
    daily_data = {'$inc': inc_data}
    coll_hist.update(daily_key, daily_data, True)

    hourly_key = {
        'type': 'hourly',
        'year': int(datetime.strftime(date, '%Y')),
        'month': int(datetime.strftime(date, '%m')),
        'day': int(datetime.strftime(date, '%d')),
        'hour': int(datetime.strftime(date, '%H'))
    }
    hourly_data = {'$inc': inc_data}
    coll_hist.update(hourly_key, hourly_data, True)


def insert_general(feeling, date, state, weather):
    feeling_key = 'feelings.' + feeling
    inc_data = {feeling_key + '.count': 1, 'count': 1}
    if state is not None:
        inc_data[feeling_key + '.states.' + state] = 1
    if weather is not None:
        inc_data[feeling_key + '.weather.' + weather] = 1

    month_key = {
        'type': 'month',
        'month': int(datetime.strftime(date, '%m'))
    }
    month_data = {'$inc': inc_data}
    coll_general.update(month_key, month_data, True)

    weekday_key = {
        'type': 'weekday',
        'weekday': int(datetime.strftime(date, '%w'))
    }
    weekday_data = {'$inc': inc_data}
    coll_general.update(weekday_key, weekday_data, True)

    day_key = {
        'type': 'day',
        'day': int(datetime.strftime(date, '%d'))
    }
    day_data = {'$inc': inc_data}
    coll_general.update(day_key, day_data, True)

    hour_key = {
        'type': 'hour',
        'hour': int(datetime.strftime(date, '%H'))
    }
    hour_data = {'$inc': inc_data}
    coll_general.update(hour_key, hour_data, True)

    # Adding extra alltime data
    if state is not None:
        inc_data['states.' + state + '.count'] = 1
        inc_data['states.' + state + '.feelings.' + feeling] = 1
    if weather is not None:
        inc_data['weather_conditions.' + weather + '.count'] = 1
        inc_data['weather_conditions.' + weather + '.feelings.' + feeling] = 1
    alltime_key = {
        'type': 'alltime'
    }
    alltime_data = {'$inc': inc_data}
    coll_general.update(alltime_key, alltime_data, True)


if __name__ == '__main__':
    states_dic = load_states_abbreviations('../crawler/states.txt')
    while(True):
        job = bs.reserve()
        job_object = literal_eval(job.body)
        feelings = job_object['feelings']
        date = datetime.strptime(job_object['created_at'], '%Y-%m-%d %H:%M:%S')
        state = None
        if 'state' in job_object:
            state = states_dic[job_object['state']]
        weather = None
        if 'weather' in job_object:
            weather = job_object['weather']

        for feeling in feelings:
            insert_history(feeling, date, state, weather)
            insert_general(feeling, date, state, weather)
        job.delete()
