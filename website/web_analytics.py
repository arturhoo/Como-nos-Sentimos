# -*- coding: utf-8 -*-
from operator import itemgetter
from datetime import datetime, timedelta
from collections import deque

try:
    from local_settings import *
except ImportError:
    sys.exit("No Flask Local Settings found!")


def insert_zero_counts(l, FMT='%H'):
    l.reverse()
    current_time = l[0][0]
    for i in range(1, len(l)):
        td = datetime.strptime(str(current_time), FMT) - datetime.strptime(str(l[i][0]), FMT)
        current_time_f = datetime.strptime(str(l[i][0]), FMT)
        for j in range(1, td.seconds / 3600):
            one_time = timedelta(hours=datetime.strptime(str(j), '%H').hour)
            new_time = current_time_f + one_time
            l.insert(i, (new_time.hour, 0))
        current_time = l[i][0]
    return l


def last_hours_sparkline(mongo_db, hours=49):
    """executes a mongo query of the form and
    receives a series of documents of the form:
        {
            "_id" : ObjectId("4fe92b2b31f6b91c918577f5"),
            "count" : 3094,
            "hour" : 0
        }
    and the objective is to give coordinates for a charting library
    returned list example:
        [1583, 850, 476, (...), 422]
    """
    coll = mongo_db[MONGO_COLLECTION_ANALYTICS_HISTORY]
    results = coll.find({'type': 'hourly'},
                        {'count': 1, 'hour': 1},
                        sort=[('year', -1),
                              ('month', -1),
                              ('day', -1),
                              ('hour', -1)],
                        limit=hours)
    l = []
    for item in results:
        l.append(item['count'])
    del l[0]
    l.reverse()
    return l


def get_last_hour_top_feelings(mongo_db):
    """queries the db for the top feelings in the last hour
    this information can be used to get the most relevant feelings for example
    returned list example:

        [u'feliz', u'saudade', u'triste', (...) u'realizado', u'est\xfapido']
    """
    coll = mongo_db[MONGO_COLLECTION_ANALYTICS_HISTORY]
    results = coll.find({'type': 'hourly'},
                        {'feelings': 1},
                        sort=[('year', -1),
                              ('month', -1),
                              ('day', -1),
                              ('hour', -1)],
                        limit=2)
    result_dic = results[1]['feelings']
    result_sorted = sorted(result_dic.iteritems(),
                           key=lambda x: x[1]['count'],
                           reverse=True)
    last_hour_top_feelings_list = [item[0] for item in result_sorted]
    return last_hour_top_feelings_list


def get_today_top_feelings(mongo_db):
    coll = mongo_db[MONGO_COLLECTION_ANALYTICS_HISTORY]
    results = coll.find_one({'type': 'daily'},
                            {'feelings': 1},
                            sort=[('year', -1),
                                  ('month', -1),
                                  ('day', -1),
                                  ('hour', -1)])
    result_dic = results['feelings']
    result_sorted = sorted(result_dic.iteritems(),
                           key=lambda x: x[1]['count'],
                           reverse=True)
    today_top_feelings_list = [item[0] for item in result_sorted]
    return today_top_feelings_list


def get_feeling_percentages_last_hours(mongo_db, feeling, hours=25, date=None):
    """returns the percetange of a given feeling, in the total of the feelings
    identified, in the last hours. The percentage for the current hour is
    not considered.
    parameter date must be instance of datetime.datetime
    returned list example:
        [(12, 0.07079646017699115),
         (13, 0.0720679714762555),
         (14, 0.06841011430550745)]
    """
    coll = mongo_db[MONGO_COLLECTION_ANALYTICS_HISTORY]
    where_dic = {'type': 'hourly'}
    if date is not None:
        hour = datetime.strftime(date, '%H')
        where_dic['hour'] = {'$lte': int(hour)}
        day = datetime.strftime(date, '%d')
        where_dic['day'] = {'$lte': int(day)}
        month = datetime.strftime(date, '%m')
        where_dic['month'] = {'$lte': int(month)}
        year = datetime.strftime(date, '%Y')
        where_dic['year'] = {'$lte': int(year)}
    results = coll.find(where_dic,
                        {'feelings.' + feeling: 1,
                         'hour': 1,
                         'count': 1},
                        sort=[('year', -1),
                              ('month', -1),
                              ('day', -1),
                              ('hour', -1)],
                        limit=hours)
    feeling_percentage_list = []
    for result in results:
        hour = result['hour']
        total = result['count']
        try:
            feeling_count = result['feelings'][feeling]['count']
        # KeyError means it has changed hours but there is no feeling yet
        except KeyError:
            feeling_count = 0

        try:
            feeling_percentage_list.append((hour,
                                            float(feeling_count / \
                                                  float(total) * 100.0)))
        except ZeroDivisionError:
            feeling_percentage_list.append((hour, float(0)))
    del feeling_percentage_list[0]
    feeling_percentage_list.reverse()
    return feeling_percentage_list


def get_feelings_percentages_for_state(mongo_db, state, num_feelings=10):
    """returns the percetanges of the top X feelings for a given state
    returned list example:
        [(u'feliz', 15.743950348288271),
         (u'triste', 7.48737248687729),
         (u'saudade', 6.747878907926447)]
    """
    coll = mongo_db[MONGO_COLLECTION_ANALYTICS_GENERAL]
    result = coll.find_one({'type': 'alltime'},
                            {'states.' + state: 1})
    total = result['states'][state]['count']
    feelings_count = result['states'][state]['feelings']
    # Sort the dict by value, the result is a list of tuples
    feelings_count = sorted(feelings_count.iteritems(),
                            key=itemgetter(1),
                            reverse=True)
    feelings_percentage = [(feeling, float(count / float(total) * 100.0)) \
                           for (feeling, count) \
                           in feelings_count]
    return feelings_percentage[:num_feelings]


def get_weather_conditions_count_for_feeling(mongo_db, feeling,
                                                   weather_translations):
    """returns the count of each weather translation for a given feling
    returned list example:
        [(u'com c\xe9u aberto', 26006),
         (u'nublado', 15482),
         (u'chovendo', 4010),
         (u'com neblina', 915)]
    """
    coll = mongo_db[MONGO_COLLECTION_ANALYTICS_GENERAL]
    result_dic = {}
    for (condition, translation) in weather_translations.items():
        result = coll.find_one({'type': 'alltime'},
                               {'weather_conditions.' + condition + \
                                '.feelings.' + feeling: 1})
        try:
            fc = result['weather_conditions'][condition]['feelings'][feeling]
        except KeyError:
            fc = 0
        if translation in result_dic:
            result_dic[translation] += fc
        else:
            result_dic[translation] = fc
    weather_conditions_count_list = sorted(result_dic.iteritems(),
                                           key=itemgetter(0),
                                           reverse=False)
    return weather_conditions_count_list


def get_feeling_mean_percentage_for_hour(mongo_db, feeling, hour):
    """returns the mean occurrence of a feeling in a given hour
    returned value example:
        27.216047709406343
    """
    coll = mongo_db[MONGO_COLLECTION_ANALYTICS_GENERAL]
    result = coll.find_one({'type': 'hour',
                            'hour': hour},
                           {'count': 1,
                            'feelings.' + feeling + '.count': 1})
    mean = float(result['feelings'][feeling]['count'] / \
                float(result['count']) * 100.0)
    return mean


def get_feeling_mean_percentages_for_hours(mongo_db, feeling, base_hour=0):
    """returns a list with the mean occurrences for each hour of the day for
    a given feelings
    the base_hour parameter is responsible for rotating the list to a given
    hour
    return list example, for base_hour=10:
        [(11, 15.567399118225117),
         (12, 15.0861101761472),
         (...),
         (9, 16.51805708236635),
         (10, 16.832664261395397)]
    """
    mean_percentages_for_hours = []
    for hour in range(24):
        mean = get_feeling_mean_percentage_for_hour(mongo_db, feeling, hour)
        mean_percentages_for_hours.append((hour, mean))
    dq = deque(mean_percentages_for_hours)
    dq.rotate(-base_hour - 1)
    new_list = list(dq)
    return new_list


def get_feeling_mean_percentages_for_every_two_hours(mongo_db, feeling):
    fmpfh = get_feeling_mean_percentages_for_hours(mongo_db, feeling, 23)
    fmpfh_list = [x[1] for x in fmpfh]
    new_list = []
    for i, k in zip(fmpfh_list[0::2], fmpfh_list[1::2]):
        new_list.append(float((i + k) / 2))
    return new_list
