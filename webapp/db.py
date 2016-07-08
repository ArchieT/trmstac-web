# -*- coding: utf8 -*-

from pymongo import MongoClient
import datetime

__author__ = u"Michał Krzysztof Feiler <archiet@platinum.edu.pl>"

client = MongoClient()

db = client['trmstac']

c = db['allsta']


def najnowszy():
    nasz = c.find().limit(1).sort("timestamp", -1)
    return [k for k in nasz]


def dajod(odtstamp):
    start = datetime.datetime.fromtimestamp(odtstamp)
    nasz = c.find({'time': {'$gte': start}}).sort("timestamp", 1)
    return [k for k in nasz]


def dajoddo(odtstamp, dotstamp):
    start = datetime.datetime.fromtimestamp(odtstamp)
    stop = datetime.datetime.fromtimestamp(dotstamp)
    nasz = c.find({'time': {'$gte': start, '$lt': stop}}
                  ).sort("timestamp", 1)
    return [k for k in nasz]
