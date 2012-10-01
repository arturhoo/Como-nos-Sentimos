# -*- coding: utf-8 -*-
import unicodedata
from urllib import urlopen
from simplejson import load as json_load
from pymongo import Connection
from xml.dom import minidom

from os.path import realpath, abspath, split, join
from inspect import getfile, currentframe as cf
from sys import path, exit

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


def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


def search_db_woeid(city, state):
    """
    The woeid is stored in the oldest document for the pair (city, state) as
    there might be multiple user_locations for the pair
    """
    result = geo_collection.find_one({'city': city, 'state': state},
                                     sort=[('_id', 1)])
    if result:
        if 'woeid_miss' in result:
            raise Exception
        if 'woeid' in result:
            return result['woeid']


def insert_woeid_into_db(city, state, woeid):
    result = geo_collection.find_one({'city': city, 'state': state},
                                     sort=[('_id', 1)])
    obj_id = result['_id']
    if result:
        if woeid is None:
            geo_collection.update({'_id': obj_id}, {'$set':
                                                        {'woeid_miss': True}})
        else:
            geo_collection.update({'_id': obj_id}, {'$set': {'woeid': woeid}})


def get_location_woeid(city, state):
    """
    Gets the woeoid for a given location, based on Yahoo!'s information.
    This id will be used to fetch the weather condition
    """
    try:
        woeid = search_db_woeid(city, state)
    except:
        url = 'http://where.yahooapis.com/geocode?city=%s&state=%s&country=brazil&appid=PTOH375e&flags=J' % (city, state)
        json = json_load(urlopen(url))
        if 'Error' in json:
            raise Exception
        result_set = json['ResultSet']
        result = result_set['Result']
        if int(result['woetype']) == 8:
            # Inserting woeid miss
            insert_woeid_into_db(city, state, None)
            raise Exception
        woeid = result['woeid']
        insert_woeid_into_db(city, state, woeid)
    return woeid


def get_weather_from_yahoo(city, state):
    """
    Code adapted from the pywapi package
    http://code.google.com/p/python-weather-api/
    http://code.google.com/p/python-weather-api/source/browse/trunk/pywapi.py
    """
    YAHOO_WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
    woeid = get_location_woeid(city, state)
    url = 'http://weather.yahooapis.com/forecastrss?w=%d&u=c' % woeid
    handler = urlopen(url)
    dom = minidom.parse(handler)
    handler.close()

    weather_data = {}
    weather_data['title'] = dom.getElementsByTagName('title')[0].firstChild.data
    weather_data['link'] = dom.getElementsByTagName('link')[0].firstChild.data

    ns_data_structure = {
        'location': ('city', 'region', 'country'),
        'units': ('temperature', 'distance', 'pressure', 'speed'),
        'wind': ('chill', 'direction', 'speed'),
        'atmosphere': ('humidity', 'visibility', 'pressure', 'rising'),
        'astronomy': ('sunrise', 'sunset'),
        'condition': ('text', 'code', 'temp', 'date')
    }

    for (tag, attrs) in ns_data_structure.items():
        weather_data[tag] = \
            xml_get_ns_yahoo_tag(dom, YAHOO_WEATHER_NS, tag, attrs)

    weather_data['geo'] = {}
    weather_data['geo']['lat'] = \
        dom.getElementsByTagName('geo:lat')[0].firstChild.data
    weather_data['geo']['long'] = \
        dom.getElementsByTagName('geo:long')[0].firstChild.data

    temp_element = dom.getElementsByTagName('item')[0]
    weather_data['condition']['title'] = \
        temp_element.getElementsByTagName('title')[0].firstChild.data
    weather_data['html_description'] = \
        temp_element.getElementsByTagName('description')[0].firstChild.data

    forecasts = []
    for forecast in dom.getElementsByTagNameNS(YAHOO_WEATHER_NS, 'forecast'):
        forecasts.append(xml_get_attrs(forecast, \
            ('date', 'low', 'high', 'text', 'code')))
    weather_data['forecasts'] = forecasts

    dom.unlink()

    condition = weather_data['condition']
    temp = int(condition['temp'])
    text = condition['text']
    if text == 'Unknown':
        raise Exception
    return (text, temp)


def xml_get_ns_yahoo_tag(dom, ns, tag, attrs):
    """
    Parses the necessary tag and returns the dictionary with values
    Parameters:
    dom - DOM
    ns - namespace
    tag - necessary tag
    attrs - tuple of attributes
    Returns: a dictionary of elements
    """
    element = dom.getElementsByTagNameNS(ns, tag)[0]
    return xml_get_attrs(element, attrs)


def xml_get_attrs(xml_element, attrs):
    """
    Returns the list of necessary attributes
    Parameters:
    element: xml element
    attrs: tuple of attributes
    Return: a dictionary of elements
    """
    result = {}
    for attr in attrs:
        result[attr] = xml_element.getAttribute(attr)
    return result
