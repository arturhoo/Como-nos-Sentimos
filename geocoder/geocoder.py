# -*- coding: utf-8 -*-
from geopy import geocoders
from pymongo import Connection
from utils import remove_accents
import re


try:
    from local_settings import *
except ImportError:
    sys.exit("No Crawler Local Settings found!")


geo_collection = Connection()[MONGO_DB][MONGO_GEO_COLLECTION]
crawler_collection = Connection()[MONGO_DB][MONGO_CRAWLER_COLLECTION]


def get_relevant_items():
    return crawler_collection.find({'cns_location': {'$exists': False},
                                    'no_location': {'$exists': False},
                                    'author.location': {'$exists': True},
                                    'place': {'$exists': False}})


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
            if (key != 'user_location') & (key != '_id'):
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
    except Exception:
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
    relevant_items = get_relevant_items()
    for item in relevant_items:
        item_id = item['_id']
        user_location = item['author']['location']
        search_db_result = search_db(user_location)
        if search_db_result:
            crawler_collection.update({'_id': item_id},
                                      {'$set': {'user_location': search_db_result}})
        else:
            result_dic = search_geocoder(user_location)
            if result_dic:
                insert_into_db(user_location, result_dic)
                crawler_collection.update({'_id': item_id},
                                          {'$set': {'user_location': result_dic}})
            else:
                crawler_collection.update({'_id': item_id},
                                           {'$set': {'no_location': True}})
