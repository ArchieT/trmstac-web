# -*- coding: utf8 -*-

from flask import Flask
from flask_jsonpify import jsonify

import db

app = Flask(__name__)

__author__ = u"Michał Krzysztof Feiler <archiet@platinum.edu.pl>"


@app.route("/")
def mostrecent():
    return jsonify(db.najnowszy())


@app.route("/<int:fromtime>")
def getfrom(fromtime):
    return jsonify(db.dajod(fromtime))


@app.route("/<int:fromtime>/<int:totime>")
def getfromto(fromtime, totime):
    return jsonify(db.dajoddo(fromtime, totime))
