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


def dajoddo(odtstamp, dotstamp):
    nasz = findoddo(
        datetime.datetime.fromtimestamp(
            odtstamp) if odtstamp is not None else None,
        datetime.datetime.fromtimestamp(
            dotstamp) if dotstamp is not None else None,
    )
    return [k for k in nasz]


def findoddo(start, stop):
    print start, stop
    nasz = c.find(przedzialczasowy(start, stop),
                  {"_id": 0}).sort("timestamp", 1)
    return nasz


def find_opening_closing(start, stop):
    przedzial = c.find(przedzialczasowy(start, stop),
                       {"_id": 0}).limit(1)
    pocz = przedzial.sort("timestamp", 1)
    konc = przedzial.sort("timestamp", -1)
    return {"pocz": pocz, "konc": konc, "przedzial": przedzial}


def find_stations(start, stop):
    stacje = c.find(przedzialczasowy(start, stop),
                    {"list.loc": 1, "list.info": 1})
    return set(
        tuple(
            [
                tuple([
                    j["loc"]["num"],
                    j["loc"]["location"]["lat"],
                    j["loc"]["location"]["lon"],
                    j["info"]["addr"],
                ]) for j in k["list"]]) for k in stacje)


def przedzialczasowy(start, stop):
    if start is None and stop is None:
        return {}
    ourdict = {}
    if start is not None:
        ourdict["$gte"] = start
    if stop is not None:
        ourdict["$lt"] = stop
    return {"timestamp": ourdict}

print find_stations(None, None)
