# -*- coding: utf-8 -*-
from operator import itemgetter

try:
    from local_settings import *
except ImportError:
    sys.exit("No Flask Local Settings found!")


def last_hours_sparkline(mongo_db, hours=48):
    """executes a mongo query of the form and
    receives a series of documents of the form:
        {
            "_id" : ObjectId("4fe92b2b31f6b91c918577f5"),
            "count" : 3094,
            "hour" : 0
        }
    and the objective is to give coordinates for a charting library
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


def get_feeling_percentage_last_hours(mongo_db, feeling, hours=24):
    """returns the percetange of a given feeling, in the total of the feelings
    identified, in the last hours. The percentage for the current hour is
    not considered.
    returned list example:
        [(12, 0.07079646017699115),
         (13, 0.0720679714762555),
         (14, 0.06841011430550745)]
    """
    coll = mongo_db[MONGO_COLLECTION_ANALYTICS_HISTORY]
    results = coll.find({'type': 'hourly'},
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
        feeling_count = result['feelings'][feeling]['count']
        feeling_percentage_list.append((hour,
                                        float(feeling_count / float(total) * 100.0)))
    del feeling_percentage_list[0]
    feeling_percentage_list.reverse()
    return feeling_percentage_list


def get_feelings_percentages_for_state(mongo_db, state, num_feelings=10):
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
