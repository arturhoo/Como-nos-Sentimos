# -*- coding: utf-8 -*-
from operator import itemgetter

try:
    from local_settings import *
except ImportError:
    sys.exit("No Flask Local Settings found!")


def last_hours_sparkline(mongo_db):
    """executes a mongo query of the form:
        db.stats_history01
            .find({type: 'hourly'}, {hour: 1, count: 1})
            .sort({'hour': -1, 'day': -1})
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
                        limit=48)
    l = []
    for item in results:
        l.append(item['count'])
    del l[0]
    l.reverse()
    return l


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
