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


def simple_find_opening_closing(start, stop):
    przedzial = c.find(przedzialczasowy(start, stop),
                       {"_id": 0}).limit(1)
    pocz = przedzial.sort("timestamp", 1)
    konc = przedzial.sort("timestamp", -1)
    return {"pocz": pocz, "konc": konc, "przedzial": przedzial}


def find_interval(start, stop):
    mozliwe = mozliwestacje(start, stop)
    interv = {}
    for moz in mozliwe:
        interv[moz] = c.find(
            {
                "timestamp": {"$gte": start, "$lt": stop},
                "list.sta.num": moz[0],
                "$or": [
                    {"list.loc.location.lat": moz[1]},
                    {"list.loc.location.lon": moz[2]},
                    {"list.info.addr": moz[3]}]},
            {
                "_id": 0,
                "list": {"$elemMatch": {"sta.num": moz[0]}}}
        )
    return interv


def sets_of_stations(start, stop):
    stacje = c.find(przedzialczasowy(start, stop),
                    {"list.loc": 1, "list.info": 1})
    return set(
        tuple(
            [
                (
                    j["loc"]["num"],
                    j["loc"]["location"]["lat"],
                    j["loc"]["location"]["lon"],
                    j["info"]["addr"],
                ) for j in k["list"]]) for k in stacje)


def mozliwestacje(start, stop):
    nasze = sets_of_stations(start, stop)
    dozw = set()
    for i in nasze:
        dozw.update(set(i))
    return dozw


def dajmozliwestacje(fromts, tots):
    return sorted(mozliwestacje(
        datetime.datetime.fromtimestamp(fromts) if fromts is not None else None,
        datetime.datetime.fromtimestamp(tots) if tots is not None else None,
    ))


def daj_sets_of_stations(fromts, tots):
    return sorted(sets_of_stations(
        datetime.datetime.fromtimestamp(fromts) if fromts is not None else None,
        datetime.datetime.fromtimestamp(tots) if tots is not None else None,
    ))


def przedzialczasowy(start, stop):
    if start is None and stop is None:
        return {}
    ourdict = {}
    if start is not None:
        ourdict["$gte"] = start
    if stop is not None:
        ourdict["$lt"] = stop
    return {"timestamp": ourdict}
