# -*- coding: utf8 -*-

from pymongo import MongoClient
import datetime

__author__ = u"Michał Krzysztof Feiler <archiet@platinum.edu.pl>"

client = MongoClient()

db = client['trmstac']

c = db['allsta']


def findlatest():
    return c.find({}, {"_id": 0}).limit(1).sort("timestamp", -1)


def najnowszy():
    return [k for k in findlatest()]


def findall():
    nasz = c.find({}, {"_id": 0}).sort("timestamp", 1)
    return nasz


def findod(start):
    if start is None:
        return findall()
    print start
    nasz = c.find({'timestamp': {'$gte': start}},
                  {"_id": 0}).sort("timestamp", 1)
    return nasz


def dajoddo(odtstamp, dotstamp):
    nasz = findoddo(
        datetime.datetime.fromtimestamp(
            odtstamp) if odtstamp is not None else None,
        datetime.datetime.fromtimestamp(
            dotstamp) if dotstamp is not None else None,
    )
    return [k for k in nasz]


def findoddo(start, stop):
    if stop is None:
        return findod(start)
    print start, stop
    nasz = c.find({'timestamp': {'$gte': start, '$lt': stop}},
                  {"_id": 0}).sort("timestamp", 1)
    return nasz


def find_opening_closing(nasz, start, stop):
    przedzial = nasz.find({'timestamp': {'$gte': start, '$lt': stop}})
    pocz = przedzial.limit(1).sort("timestamp", 1)
    konc = przedzial.limit(1).sort("timestamp", -1)
    return {"pocz": pocz, "konc": konc, "przedzial": przedzial}


def find_stations(przedzial):
    stacje = przedzial.find({}, {"list.loc": 1, "list.info": 1,
                                 "list.sta": 0, "_id": 0, "timestamp": 0})
    return set(k for k in stacje)

wszystkie = findall()

print find_stations(wszystkie)
