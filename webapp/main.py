# -*- coding: utf8 -*-

from flask import Flask, request
from flask_jsonpify import jsonify

import db

app = Flask(__name__)

__author__ = u"Michał Krzysztof Feiler <archiet@platinum.edu.pl>"


@app.route("/")
def mostrecent():
    vals = request.values
    fromtime = None
    totime = None
    if "fromtime" in vals:
        fromtime = int(vals.get("fromtime"))
    if "totime" in vals:
        totime = int(vals.get("totime"))
    if fromtime is None and totime is None \
            and "latest" in vals and vals["latest"]:
        return jsonify(db.najnowszy())
    return jsonify(
        data=db.dajoddo(fromtime, totime),
        mozliwestacje=db.dajmozliwestacje(fromtime, totime),
        setsofstations=db.daj_sets_of_stations(fromtime, totime),
    )

if __name__ == "__main__":
    app.run(debug=True)
