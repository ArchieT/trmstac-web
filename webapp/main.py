# -*- coding: utf8 -*-

from flask import Flask, request
from flask_jsonpify import jsonify

import db

app = Flask(__name__)

__author__ = u"Michał Krzysztof Feiler <archiet@platinum.edu.pl>"


@app.route("/")
def mostrecent():
    vals = request.values
    if "fromtime" in vals:
        fromtime = vals.get("fromtime")
        if "totime" in vals:
            return jsonify(db.dajoddo(int(fromtime), int(vals.get("totime"))))
        return jsonify(db.dajod(int(fromtime)))
    return jsonify(db.najnowszy())

if __name__ == "__main__":
    app.run(debug=True)
