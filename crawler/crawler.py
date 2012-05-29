# -*- coding: utf-8 -*-

from tweepy import OAuthHandler, StreamListener
from tweepy.streaming import Stream
import sys
from pprint import pprint
from sentiment_filter import identify_feeling


try:
    from local_settings import *
except ImportError:
    sys.exit("No Crawler Local Settings found!")

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)


class CustomStreamListener(StreamListener):

    def on_status(self, status):
        try:
            # print "%s\n" % (status.created_at)

            # for att in status.__dict__.keys():
            #     print att + ': ' + unicode(status.__getattribute__(att)).encode('utf-8')

            # if status.author:
            #     user = status.author
            #     pprint(user.__dict__)

            # if status.geo:
            #     pprint(status.geo)

            feeling = identify_feeling('feelings.txt', status.text)
            if feeling:
                print feeling

                # sys.exit()

        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream

query = ['eu to', 'me sentindo', 'estou']

streaming_api = Stream(auth, CustomStreamListener(), timeout=60)
streaming_api.filter(track=query)
