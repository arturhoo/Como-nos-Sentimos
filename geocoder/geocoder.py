# -*- coding: utf-8 -*-
from geopy import geocoders
from pymongo import Connection
from utils import remove_accents
from bson import ObjectId
from pywapi import get_weather_from_google
import beanstalkc
import re
import sys


try:
    from local_settings import *
except ImportError:
    sys.exit("No Crawler Local Settings found!")


geo_collection = Connection(host=MONGO_HOST)[MONGO_DB][MONGO_GEO_COLLECTION]
crawler_collection = Connection(host=MONGO_HOST)[MONGO_DB][MONGO_CRAWLER_COLLECTION]
beanstalk = beanstalkc.Connection(host=BEANSTALKD_HOST, port=BEANSTALKD_PORT)
beanstalk.watch(BEANSTALKD_TUBE)
beanstalk.ignore('default')


def insert_into_db(user_location, location_dic):
    clean_user_location = remove_accents(user_location).lower()
    dic = {'user_location': clean_user_location}
    for key, value in location_dic.items():
        dic[key] = value
    try:
        geo_collection.insert(dic)
        return True

    except Exception, e:
        print >> sys.stderr, 'Encountered Exception:', e
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
    g = geocoders.Google()
    query = user_location.encode('utf-8') + ' brasil'

    try:
        places = g.geocode(query, exactly_one=False)
    except Exception, e:
        # print >> sys.stderr, 'Encountered Exception:', e
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
        item = crawler_collection.find_one({'_id': ObjectId(job.body)})
        if not item:
            continue
        user_location = item['author']['location']
        search_db_result = search_db(user_location)
        if search_db_result:
            # print 'Hit DB: ' + user_location
            crawler_collection.update({'_id': ObjectId(job.body)},
                                      {'$set': {'location': search_db_result}})
            location = search_db_result
        else:
            result_dic = search_geocoder(user_location)
            if result_dic:
                # print 'Hit GEO: ' + user_location
                insert_into_db(user_location, result_dic)
                crawler_collection.update({'_id': ObjectId(job.body)},
                                          {'$set': {'location': result_dic}})
                location = result_dic

        if 'city' in location:
            query = location['city'] + ' - ' + location['state'] + ', brasil'
            query = query.encode('utf-8')
            google_result = get_weather_from_google(query)
            if google_result['current_conditions'] and \
               google_result['current_conditions']['condition'] and \
               google_result['current_conditions']['temp_c']:
                condition = google_result['current_conditions']['condition']
                temp = int(google_result['current_conditions']['temp_c'])
                weather = {'condition': condition, 'temp': temp}
                crawler_collection.update({'_id': ObjectId(job.body)},
                                          {'$set': {'location.weather': weather}})
        job.delete()
