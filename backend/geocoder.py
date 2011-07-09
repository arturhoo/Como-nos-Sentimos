#coding=utf-8

import re
import string
from geopy import geocoders
import MySQLdb
import sys


try:
    from geocoder_local_settings import *
except ImportError:
    sys.exit("No Geocoder Local Settings found!")

def interpretGeolocation(c, geolocation):
    print geolocation
    t = re.split(',|-', geolocation)
    if len(t) == 2:
        state = defineState(c, t[0])
        result = (None, state)
    else:
        try:
            state = defineState(c, t[len(t)-2])
            result = (t[len(t)-3], state)
        except IndexError, err:
            return (None, None)

    return result

def defineState(c, state_long):
    try:
        t0 = re.split('^ ', state_long)
        if len(t0) > 1:
            t = (t0[1],)
        else:
            t = (t0[0],)
        string =  'state|' + state_long + '|'
        print string
        c.execute('''select state from states 
        where state_long = %s''', t)
    except Exception, err:
        print 'ERROR STATE: ', err
        return None
    else:
        for row in c:
            return row[0]

def searchLocation(c, location):
    t = (string.lower(location.decode('utf-8')),)
    try:
        c.execute('''select structured
        from locations
        where text = %s''', t)
    except Exception, err:
        print 'Erro no SELECT', err
        return None
    else:
        for row in c:
            print 'ACHEI NO BD'
            return row[0]

def insertLocation(c, location, geolocation):
    t = (string.lower(location), geolocation)
    try:
        c.execute('''insert into locations
        values (%s, %s)''', t)

    except Exception, err:
        print 'NAO INSERI LOCATION: ', err
        conn.rollback()
    else:
        conn.commit()

db_filename = 'twitter.db'
conn = MySQLdb.connect(host, user, passwd, db=db, init_command='SET NAMES utf8')
c1 = conn.cursor()
c2 = conn.cursor()
g = geocoders.Google()

c1.execute('''select screen_name, location from users
where location_status = 0
and location != ''
and location is not null''')
count1 = 0
count2 = 0
count3 = 0
for row in c1:
    cache = False
    location = row[1]
    print '%s %s' % ('location:', location)
    location += " brazil"

    place = searchLocation(c2, location)

    try:
        if place is None:
            print 'NAO ACHEI NO DB'
            places= g.geocode(location, exactly_one=False)
            place = places[0][0]
            cache = True
        else:
            count3 += 1
        if re.search("^bra+(s|z)i+l$", place, re.IGNORECASE):
            raise Exception

    except Exception, err:
        print 'ERROR GEOCODE: ', err
        t = (row[0],)
        c2.execute('''update users set
        city = NULL,
        state = NULL,
        location_status = 2
        where screen_name = %s''', t)
        conn.commit()
        count2 += 1

    else:
        if cache is True:
            insertLocation(c2, location, place)

        t = interpretGeolocation(c2, place)
        t2 = (t[0], t[1], row[0])
        print t2
        c2.execute('''update users set
        city = %s,
        state = %s,
        location_status = 1
        where screen_name = %s''', t2)
        conn.commit()
        count1 += 1


print 'Foram geocodificados:', count1
print 'Nao foram geocodificados:', count2
print 'Propria base de dados:', count3
print 'De um total de:', count1 + count2
conn.commit()
c1.close()
c2.close()
