# -*- coding: utf-8 -*-

from tweepy import OAuthHandler, StreamListener
from tweepy.streaming import Stream
import sys
from pprint import pprint
from sentiment_filter import identify_feeling
from pymongo import Connection
from datetime import datetime


try:
    from local_settings import *
except ImportError:
    sys.exit("No Crawler Local Settings found!")

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)

connection = Connection()
db = connection.cns
tweets = db.tweets


class CustomStreamListener(StreamListener):
    def on_status(self, status):
        try:
            with open('stream.log', 'a') as f:
                pprint(status.__dict__, f)

            feeling = identify_feeling('feelings.txt', status.text)
            if feeling:
                print str(datetime.now()) + ': ' + feeling
                tweet = {'feeling': feeling,
                         'author': {
                            'screen_name': status.author.screen_name,
                            'location': status.author.location
                         },
                         'text': status.text,
                         'created_at': status.created_at}
                if status.geo:
                    tweet['geo'] = status.geo
                    tweet['place'] = status.place

                tweets.insert(tweet)

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
    query = ['eu to', 'me sentindo', 'estou']
    streaming_api = Stream(auth, CustomStreamListener(), timeout=60)
    streaming_api.filter(track=query)
