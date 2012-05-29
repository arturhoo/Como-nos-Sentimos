# -*- coding: utf-8 -*-

from tweepy import OAuthHandler, StreamListener
from tweepy.streaming import Stream
import sys
from pprint import pprint
from sentiment_filter import identify_feeling
from pymongo import Connection
from datetime import datetime
from textwrap import TextWrapper
import re


try:
    from local_settings import *
except ImportError:
    sys.exit("No Crawler Local Settings found!")

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)

connection = Connection()
db = connection.cns
tweets = db.tweets

query = [u'eu to'.encode('utf-8'),
         u'eu tô'.encode('utf-8'),
         u'me sentindo'.encode('utf-8'),
         u'me sinto'.encode('utf-8'),
         u'estou'.encode('utf-8'),
         u'fico'.encode('utf-8')]


def check_full_query(query, text):
    regex_str = ur'.*' + '('
    for (idx, value) in enumerate(query):
        if idx + 1 != len(query):
            regex_str += value.decode('utf-8') + '|'
        else:
            regex_str += value.decode('utf-8')
    regex_str += ')' + r'.*'
    regex = re.compile(regex_str, re.UNICODE)
    return regex.match(text)


def insert_tweet(tweets_collection, status, feeling):
    tweet = {'feeling': feeling,
             'author': {
                'screen_name': status.author.screen_name
             },
             'text': status.text,
             'created_at': status.created_at}
    if status.author.location:
        tweet['author']['location'] = status.author.location
    if status.geo:
        tweet['geo'] = status.geo
    if status.place and status.place['full_name']:
        tweet['place'] = status.place
    try:
        tweets_collection.insert(tweet)
        return True

    except Exception, e:
        print >> sys.stderr, 'Encountered Exception:', e
        return false


class CustomStreamListener(StreamListener):
    def on_status(self, status):
        try:
            with open('stream.log', 'a') as f:
                pprint(status.__dict__, f)

            if check_full_query(query, status.text):
                feeling = identify_feeling('feelings.txt', status.text)
                if feeling:
                    text_wrapper = TextWrapper(width=60,
                                               initial_indent='    ',
                                               subsequent_indent='    ')
                    print str(datetime.now()) + ': ' + feeling
                    print text_wrapper.fill(status.text)
                    insert_tweet(tweets, status, feeling)

        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream


if __name__ == '__main__':
    streaming_api = Stream(auth, CustomStreamListener(), timeout=60)
    streaming_api.filter(track=query)
