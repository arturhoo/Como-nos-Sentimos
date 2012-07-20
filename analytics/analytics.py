# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from ast import literal_eval
from beanstalkc import Connection as BSConnection
from pymongo import Connection as MongoConnection

from os.path import realpath, abspath, split, join
from inspect import getfile, currentframe as cf
from sys import path, exit, stdout, stderr

# realpath() with make your script run, even if you symlink it :)
cmd_folder = realpath(abspath(split(getfile(cf()))[0]))
if cmd_folder not in path:
    path.insert(0, cmd_folder)

# use this if you want to include modules from a subforder
cmd_subfolder = realpath(abspath(join(split(getfile(cf()))[0], "../")))
if cmd_subfolder not in path:
    path.insert(0, cmd_subfolder)

try:
    from local_settings import *
except ImportError:
    exit("No local settings found")

coll_hist = MongoConnection(host=MONGO_HOST)[MONGO_DB][MONGO_ANALYTICS_HISTORY_COLLECTION]
coll_general = MongoConnection(host=MONGO_HOST)[MONGO_DB][MONGO_ANALYTICS_GENERAL_COLLECTION]
bs = BSConnection(host=BEANSTALKD_HOST, port=BEANSTALKD_PORT)
bs.watch(BEANSTALKD_ANALYTICS_TUBE)
bs.ignore('default')


def load_states_abbreviations(file_name):
    states_dic = {}
    with open(file_name) as f:
        for line in f.readlines():
            line_list = line.split(';')
            states_dic[line_list[0].decode('utf-8')] = line_list[1]
    return states_dic


def fix_history_insert_date_field_when_missing():
    """insert date field in legacy documents
    """
    result_hourly = coll_hist.find({'type': 'hourly',
                                    'date': {'$exists': False}})
    for e in result_hourly:
        date = datetime.strptime(str(e['year']) + '-' + \
                                 str(e['month']) + '-' + \
                                 str(e['day']) + '-' + \
                                 str(e['hour']), '%Y-%m-%d-%H')
        e.update({'date': date})
        coll_hist.save(e)

    result_daily = coll_hist.find({'type': 'daily',
                                   'date': {'$exists': False}})
    for e in result_daily:
        date = datetime.strptime(str(e['year']) + '-' + \
                                 str(e['month']) + '-' + \
                                 str(e['day']), '%Y-%m-%d')
        e.update({'date': date})
        coll_hist.save(e)

    result_monthly = coll_hist.find({'type': 'monthly',
                                     'date': {'$exists': False}})
    for e in result_monthly:
        date = datetime.strptime(str(e['year']) + '-' + \
                                 str(e['month']), '%Y-%m')
        e.update({'date': date})
        coll_hist.save(e)
    print >> stdout, 'Finished fixing missing date field in analytics history collection'


def fix_history_hourly():
    """this method insert zero counts in the hours that no data was collected
    """
    result = coll_hist.find(
            {'type': 'hourly'},
            {'year': 1, 'month': 1, 'day': 1, 'hour': 1, 'count': 1},
            sort=[('year', -1),
                  ('month', -1),
                  ('day', -1),
                  ('hour', -1)
            ]
    )
    date_string = str(result[0]['year']) + ',' + \
                  str(result[0]['month']) + ',' + \
                  str(result[0]['day']) + ',' + \
                  str(result[0]['hour'])
    previous_dt = datetime.strptime(date_string, '%Y,%m,%d,%H')
    insertions_list = []
    for i in range(1, result.count()):
        date_string = str(result[i]['year']) + ',' + \
                      str(result[i]['month']) + ',' + \
                      str(result[i]['day']) + ',' + \
                      str(result[i]['hour'])
        dt = datetime.strptime(date_string, '%Y,%m,%d,%H')
        hour_diff = int((previous_dt - dt).total_seconds()) / 3600
        for j in range(1, hour_diff):
            new_dt = previous_dt - timedelta(seconds=3600 * j)
            hourly_doc = {
                'type': 'hourly',
                'year': int(datetime.strftime(new_dt, '%Y')),
                'month': int(datetime.strftime(new_dt, '%m')),
                'day': int(datetime.strftime(new_dt, '%d')),
                'hour': int(datetime.strftime(new_dt, '%H')),
                'count': 0
            }
            insertions_list.append(hourly_doc)
        previous_dt = dt
    for doc in insertions_list:
        coll_hist.insert(doc)
    print >> stdout, 'Finished fixing history hourly'


def fix_history_daily():
    """this method insert zero counts in the days that no data was collected
    """
    result = coll_hist.find(
            {'type': 'daily'},
            {'year': 1, 'month': 1, 'day': 1, 'count': 1},
            sort=[('year', -1),
                  ('month', -1),
                  ('day', -1)
            ]
    )
    date_string = str(result[0]['year']) + ',' + \
                  str(result[0]['month']) + ',' + \
                  str(result[0]['day'])
    previous_dt = datetime.strptime(date_string, '%Y,%m,%d')
    insertions_list = []
    for i in range(1, result.count()):
        date_string = str(result[i]['year']) + ',' + \
                      str(result[i]['month']) + ',' + \
                      str(result[i]['day'])
        dt = datetime.strptime(date_string, '%Y,%m,%d')
        day_diff = (previous_dt - dt).days
        for j in range(1, day_diff):
            new_dt = previous_dt - timedelta(days=1 * j)
            daily_doc = {
                'type': 'daily',
                'year': int(datetime.strftime(new_dt, '%Y')),
                'month': int(datetime.strftime(new_dt, '%m')),
                'day': int(datetime.strftime(new_dt, '%d')),
                'count': 0
            }
            insertions_list.append(daily_doc)
        previous_dt = dt
    for doc in insertions_list:
        coll_hist.insert(doc)
    print >> stdout, 'Finished fixing history hourly'


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
        'month': int(datetime.strftime(date, '%m')),
        'date': datetime.strptime( \
            str(date.year) + '-' + str(date.month), '%Y-%m' \
        )
    }
    monthly_data = {'$inc': inc_data}
    coll_hist.update(monthly_key, monthly_data, True)

    daily_key = {
        'type': 'daily',
        'year': int(datetime.strftime(date, '%Y')),
        'month': int(datetime.strftime(date, '%m')),
        'day': int(datetime.strftime(date, '%d')),
        'date': datetime.strptime( \
            str(date.year) + '-' + str(date.month) + '-' + \
            str(date.day), '%Y-%m-%d' \
        )
    }
    daily_data = {'$inc': inc_data}
    coll_hist.update(daily_key, daily_data, True)

    hourly_key = {
        'type': 'hourly',
        'year': int(datetime.strftime(date, '%Y')),
        'month': int(datetime.strftime(date, '%m')),
        'day': int(datetime.strftime(date, '%d')),
        'hour': int(datetime.strftime(date, '%H')),
        'date': datetime.strptime( \
            str(date.year) + '-' + str(date.month) + '-' + \
            str(date.day) + '-' + str(date.hour), '%Y-%m-%d-%H' \
        )
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
    fix_history_insert_date_field_when_missing()
    fix_history_daily()
    fix_history_hourly()
    while(True):
        job = bs.reserve()
        job_object = literal_eval(job.body)
        feelings = job_object['feelings']
        date = datetime.strptime(job_object['created_at'], '%Y-%m-%d %H:%M:%S')
        state = None
        if 'state' in job_object:
            try:
                state = states_dic[job_object['state']]
            except KeyError, e:
                print >> stderr, 'No state named ', e
                job.delete()
                continue
        weather = None
        if 'weather' in job_object:
            weather = job_object['weather']

        for feeling in feelings:
            insert_history(feeling, date, state, weather)
            insert_general(feeling, date, state, weather)
        job.delete()
