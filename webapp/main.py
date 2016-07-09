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
        return jsonify(db.dajoddo(int(fromtime), None))
    if "latest" in vals and vals["latest"]:
        return jsonify(db.najnowszy())
    return jsonify(db.dajoddo(None, None))

if __name__ == "__main__":
    app.run(debug=True)
