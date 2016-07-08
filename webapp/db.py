# -*- coding: utf8 -*-

from pymongo import MongoClient
import datetime

__author__ = u"Michał Krzysztof Feiler <archiet@platinum.edu.pl>"

client = MongoClient()

db = client['trmstac']

c = db['allsta']


def najnowszy():
    nasz = c.find({}, {"_id": 0}).limit(1).sort("timestamp", -1)
    return [k for k in nasz]


def dajod(odtstamp):
    start = datetime.datetime.fromtimestamp(odtstamp)
    print start
    nasz = c.find({'timestamp': {'$gte': start}},
                  {"_id": 0}).sort("timestamp", 1)
    return [k for k in nasz]


def dajoddo(odtstamp, dotstamp):
    start = datetime.datetime.fromtimestamp(odtstamp)
    stop = datetime.datetime.fromtimestamp(dotstamp)
    print start, stop
    nasz = c.find({'timestamp': {'$gte': start, '$lt': stop}},
                  {"_id": 0}).sort("timestamp", 1)
    return [k for k in nasz]
