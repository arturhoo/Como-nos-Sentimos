from datetime import datetime
from ast import literal_eval
from beanstalkc import Connection as BSConnection
from pymongo import Connection as MongoConnection


try:
    from local_settings import *
except ImportError:
    sys.exit("No Crawler Local Settings found!")

coll_hist = MongoConnection(host=MONGO_HOST)[MONGO_DB][MONGO_COLLECTION_STATS_HISTORY]
bs = BSConnection(host=BEANSTALKD_HOST, port=BEANSTALKD_PORT)
bs.watch(BEANSTALKD_TUBE)
bs.ignore('default')


def insert_history(feeling, date):
    feeling_key = 'feelings.' + feeling
    print feeling_key
    monthly_key = {
        'type': 'monthly',
        'month': int(datetime.strftime(date, '%m'))
    }
    monthly_data = {'$inc': {feeling_key: 1, 'count': 1}}
    coll_hist.update(monthly_key, monthly_data, True)

    daily_key = {
        'type': 'daily',
        'month': int(datetime.strftime(date, '%m')),
        'day': int(datetime.strftime(date, '%d'))
    }
    daily_data = {'$inc': {feeling_key: 1, 'count': 1}}
    coll_hist.update(daily_key, daily_data, True)

    hourly_key = {
        'type': 'hourly',
        'month': int(datetime.strftime(date, '%m')),
        'day': int(datetime.strftime(date, '%d')),
        'hour': int(datetime.strftime(date, '%H'))
    }
    hourly_data = {'$inc': {feeling_key: 1, 'count': 1}}
    coll_hist.update(hourly_key, hourly_data, True)


if __name__ == '__main__':
    while(True):
        job = bs.reserve()
        job_object = literal_eval(job.body)
        feelings = job_object[0]
        date = datetime.strptime(job_object[1], '%Y-%m-%d %H:%M:%S')
        for feeling in feelings:
            insert_history(feeling, date)
        job.delete()


