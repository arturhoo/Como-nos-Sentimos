# -*- coding: utf-8 -*-
from datetime import timedelta
from utils import prepare_string_for_javascript


class Author(object):
    def __init__(self, screen_name):
        self.screen_name = screen_name


class Location(object):
    def __init__(self, state):
        self.state = state


class Tweet(object):
    def __init__(self, tid, author, text, created_at, created_at_bsb, \
                 created_at_local, feelings):
        self.id = tid
        self.author = author
        self.text = text
        self.created_at = created_at
        self.created_at_bsb = created_at_bsb
        self.created_at_local = created_at_local
        self.feelings = feelings


def tweet_from_dict_to_object(tweet):
    author = Author(tweet['author']['screen_name'])
    if 'name' in tweet['author']:
        author.name = prepare_string_for_javascript(tweet['author']['name'])
    if 'location' in tweet['author']:
        author.location = prepare_string_for_javascript(tweet['author']['location'])

    location = None
    if 'location' in tweet and tweet['location'] != None:
        try:
            location = Location(tweet['location']['state'])
            if 'city' in tweet['location']:
                location.city = tweet['location']['city']
                if 'weather' in tweet['location']:
                    location.weather = tweet['location']['weather']['condition']

        except TypeError:
            print tweet['location']

    new_tweet = Tweet(tweet['_id'],
                      author,
                      prepare_string_for_javascript(tweet['text']),
                      tweet['created_at'],
                      tweet['created_at'] + timedelta(seconds=-10800),
                      tweet['created_at_local'],
                      tweet['feelings'])

    if location is not None:
        new_tweet.location = location

    return new_tweet
