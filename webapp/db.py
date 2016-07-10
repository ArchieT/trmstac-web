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
    nasz = giveinterval(
        datetime.datetime.utcfromtimestamp(
            odtstamp) if odtstamp is not None else None,
        datetime.datetime.utcfromtimestamp(
            dotstamp) if dotstamp is not None else None,
    )
    return [(k, nasz[k]) for k in nasz]
    # return nasz
    # return [k for k in nasz]


def findoddo(start, stop):
    print start, stop
    nasz = c.find(przedzialczasowy(start, stop),
                  {"_id": 0}).sort("timestamp", 1)
    return nasz


def simple_find_opening_closing(start, stop):
    def przedzial():
        return c.find(przedzialczasowy(start, stop),
                      {"_id": 0}).limit(1)
    pocz = przedzial().sort("timestamp", 1)
    konc = przedzial().sort("timestamp", -1)
    return {"pocz": pocz, "konc": konc}


def pie(x): return x[0] if len(x) > 0 else None


def giveinterval(start, stop):
    nasz = findoddo(start, stop)
    mozliwe = mozliwestacje(start, stop)
    interv = {}
    for moz in mozliwe:
        interv[moz] = []
    for w in nasz:
        for s in w["list"]:
            si = s["info"]
            loc = s["loc"]["location"]
            st = s["sta"]
            interv[
                (si["num"], loc["lat"], loc["lon"], si["addr"])
            ].append({
                "timestamp": w["timestamp"],
                "row": st["dostrow"],
                "wol": st["wolrow"]
            })
    return interv


def find_interval(start, stop):
    mozliwe = mozliwestacje(start, stop)
    interv = {}
    for moz in mozliwe:
        def ourinterv():
            return c.find(
                {
                    "timestamp": {"$gte": start, "$lt": stop},
                    "list.info.num": moz[0],
                    "list.loc.location.lat": moz[1],
                    "list.loc.location.lon": moz[2],
                    "list.info.addr": moz[3]},
                {
                    "_id": 0,
                    "list": {"$elemMatch": {"info.num": moz[0]}},
                    "list.info": 0, "list.loc": 0}
            ).limit(1)
        opening = [i for i in ourinterv().sort("timestamp", 1)]
        closing = [i for i in ourinterv().sort("timestamp", -1)]
        highrow = [i for i in ourinterv().sort("list.sta.row", -1)]
        highwol = [i for i in ourinterv().sort("list.sta.wol", -1)]
        lowrow = [i for i in ourinterv().sort("list.sta.row", 1)]
        lowwol = [i for i in ourinterv().sort("list.sta.wol", 1)]
        print opening, closing, highrow, highwol, lowrow, lowwol

        interv[moz] = {
            "opening": pie(pie(opening)['list']),
            "closing": pie(pie(closing)['list']),
            "highrow": pie(pie(highrow)['list']),
            "highwol": pie(pie(highwol)['list']),
            "lowrow": pie(pie(lowrow)['list']),
            "lowwol": pie(pie(lowwol)['list'])}
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
        datetime.datetime.utcfromtimestamp(
            fromts) if fromts is not None else None,
        datetime.datetime.utcfromtimestamp(tots) if tots is not None else None,
    ))


def daj_sets_of_stations(fromts, tots):
    return sorted(sets_of_stations(
        datetime.datetime.utcfromtimestamp(
            fromts) if fromts is not None else None,
        datetime.datetime.utcfromtimestamp(tots) if tots is not None else None,
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
