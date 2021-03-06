# -*- coding: utf-8 -*-
from utils import remove_accents, get_weather_from_yahoo
from geopy import geocoders
from pymongo import Connection
from pylibmc import Client
from datetime import timedelta
from hashlib import md5
from beanstalkc import Connection as BSConnection
import re

from os.path import realpath, abspath, split, join
from inspect import getfile, currentframe as cf
from sys import path, exit, stderr

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

geo_collection = Connection(host=MONGO_HOST)[MONGO_DB][MONGO_GEO_COLLECTION]
crawler_collection = Connection(host=MONGO_HOST)[MONGO_DB][MONGO_CRAWLER_COLLECTION]
beanstalk = BSConnection(host=BEANSTALKD_HOST, port=BEANSTALKD_PORT)
beanstalk.watch(BEANSTALKD_GEO_TUBE)
beanstalk.use(BEANSTALKD_ANALYTICS_TUBE)
beanstalk.ignore('default')
mc = Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True,
                                                   "ketama": True})


def insert_into_db_hit(user_location, location_dic):
    clean_user_location = remove_accents(user_location).lower()
    dic = {'user_location': clean_user_location}
    for key, value in location_dic.items():
        dic[key] = value
    try:
        geo_collection.insert(dic)
        return True
    except Exception, e:
        print >> stderr, 'Encountered Exception:', e
        return false


def insert_into_db_miss(user_location):
    clean_user_location = remove_accents(user_location).lower()
    dic = {'user_location': clean_user_location, 'miss': True}
    try:
        geo_collection.insert(dic)
        return True
    except Exception, e:
        print >> stderr, 'Encountered Exception:', e
        return false


def search_db(user_location):
    clean_user_location = remove_accents(user_location).lower()
    result = geo_collection.find({'user_location': clean_user_location})
    if result.count() > 0:
        dic = {}
        for key, value in result[0].items():
            if (key != 'user_location') and (key != '_id'):
                dic[key] = value
        return dic


def validate_returned_location(place):
    regex = re.compile(r'^([^-,]+) - ([^-,]+), Brazil$', re.UNICODE | re.IGNORECASE)
    match = regex.match(place)
    if match:
        return match
    else:
        regex = re.compile(r'^([^-,]+), Brazil$', re.UNICODE | re.IGNORECASE)
        return regex.match(place)


def search_geocoder(user_location):
    g = geocoders.GoogleV3()
    query = user_location.encode('utf-8') + ' brasil'

    try:
        places = g.geocode(query, exactly_one=False)
    except Exception:
        return None

    # Sometimes google returns no result, an empty list
    if places is None or len(places) == 0:
        return None

    place = places[0][0]
    match = validate_returned_location(place)
    if match:
        dic = {}
        if len(match.groups()) == 1:
            dic['state'] = match.groups()[0]
        if len(match.groups()) == 2:
            dic['city'] = match.groups()[0]
            dic['state'] = match.groups()[1]
        return dic


if __name__ == '__main__':
    while True:
        location = {}
        job = beanstalk.reserve()
        item = crawler_collection.find_one({'_id': int(job.body)})
        if not item:
            job.delete()
            continue

        analytics_dic = {
            'feelings': item['feelings'],
            'created_at': str(item['created_at'] + timedelta(seconds=-10800))
        }

        user_location = item['author']['location']
        clean_user_location = remove_accents(user_location).lower()
        search_db_result = search_db(clean_user_location)
        if search_db_result:
            if 'miss' in search_db_result:
                job.delete()
                beanstalk.put(str(analytics_dic))
                continue
            else:
                crawler_collection.update({'_id': int(job.body)},
                                          {'$set': {'location':
                                                    search_db_result}})
                location = search_db_result
        else:
            result_dic = search_geocoder(user_location)
            if result_dic:
                insert_into_db_hit(user_location, result_dic)
                crawler_collection.update({'_id': int(job.body)},
                                          {'$set': {'location': result_dic}})
                location = result_dic
            else:
                insert_into_db_miss(user_location)

        if 'state' in location:
            analytics_dic['state'] = location['state']

        if 'city' in location:
            city = location['city']
            state = location['state']
            m = md5()
            m.update(remove_accents(city + state))
            identifier = 'weather_' + m.hexdigest()

            city = city.encode('utf-8')
            state = state.encode('utf-8')
            yahoo_result = mc.get(identifier)
            if not yahoo_result:
                try:
                    yahoo_result = get_weather_from_yahoo(city, state)
                    mc.set(identifier, yahoo_result, 1800)
                except Exception:
                    pass
            if yahoo_result:
                weather = {'condition': yahoo_result[0],
                           'temp': yahoo_result[1]}
                crawler_collection.update({'_id': int(job.body)},
                                          {'$set':
                                          {'location.weather': weather}})
                analytics_dic['weather'] = yahoo_result[0]

        job.delete()
        beanstalk.put(str(analytics_dic))
