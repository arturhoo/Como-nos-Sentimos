# -*- coding: utf-8 -*-
from tweepy import OAuthHandler, StreamListener
from tweepy.streaming import Stream
from pymongo import Connection
from beanstalkc import Connection as BSConnection
from datetime import timedelta
from sentiment_filter import identify_feelings
from utils import load_terms
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

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)

collection = Connection(host=MONGO_HOST)[MONGO_DB][MONGO_CRAWLER_COLLECTION]
beanstalk = BSConnection(host=BEANSTALKD_HOST, port=BEANSTALKD_PORT)


def check_full_query(query, text):
    regex_str = r'.*' + '('
    for (idx, value) in enumerate(query):
        if idx + 1 != len(query):
            regex_str += value + '|'
        else:
            regex_str += value
    regex_str += ')' + r'.*'
    regex = re.compile(regex_str, re.UNICODE | re.IGNORECASE)
    return regex.match(text)


def structure_location(place):
    if place.country_code == 'BR':
        regex = re.compile(r'^(.+), (.+)$')
        match = regex.match(place.full_name)
        dic = {}
        if place.place_type == 'admin':
            dic['state'] = match.groups()[0]
            return dic
        elif place.place_type == 'city':
            dic['city'] = match.groups()[0]
            dic['state'] = match.groups()[1]
            return dic
        return None
    return None


def insert_tweet(collection, status, feelings):
    tweet_id = 0
    tweet = {
        'feelings': feelings,
        '_id': status.id,
        'feelings_size': len(feelings),
        'author': {
            'screen_name': status.author.screen_name
        },
        'text': status.text,
        'created_at': status.created_at
    }
    if status.author.utc_offset:
        offset = timedelta(seconds=status.author.utc_offset)
        tweet['created_at_local'] = status.created_at + offset
    else:
        offset = timedelta(seconds=-10800)
        tweet['created_at_local'] = status.created_at + offset
    if status.author.name:
        tweet['author']['name'] = status.author.name
    if status.author.location:
        tweet['author']['location'] = status.author.location
    if (status.place and status.place.full_name and
       status.place.country_code == u'BR'):
        tweet['location'] = structure_location(status.place)

    try:
        tweet_id = collection.insert(tweet)

    except Exception, e:
        print >> stderr, 'Encountered exception trying to insert tweet:', e

    # If it is not geotagged but has the user location field
    if (status.author.location) and ('location' not in tweet):
        try:
            beanstalk.use(BEANSTALKD_GEO_TUBE)
            beanstalk.put(str(tweet_id))
        except Exception, e:
            print >> stderr, 'Encountered exception ' + \
                             'trying to insert job:', e

    # If it is geotagged or has no location information at all
    else:
        analytics_dic = {
            'feelings': feelings,
            'created_at': str(tweet['created_at'] + timedelta(seconds=-10800))
        }
        # If it is geotagged
        if 'location' in tweet:
            analytics_dic['state'] = tweet['location']['state']
        beanstalk.use(BEANSTALKD_ANALYTICS_TUBE)
        beanstalk.put(str(analytics_dic))


class CustomStreamListener(StreamListener):
    def on_status(self, status):
        #try:
            if check_full_query(query, status.text):
                feelings = identify_feelings('feelings.txt', status.text)
                if feelings:
                    insert_tweet(collection, status, feelings)
        #except Exception, e:
        #    print >> stderr, 'Encountered Exception:', e
        #    pass

    def on_error(self, status_code):
        print >> stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> stderr, 'Timeout...'
        return True  # Don't kill the stream


if __name__ == '__main__':
    query = load_terms('query_terms.txt')
    streaming_api = Stream(auth, CustomStreamListener(), timeout=60)
    streaming_api.filter(track=query)
