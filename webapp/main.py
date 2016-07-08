# -*- coding: utf8 -*-

from flask import Flask
from flask.ext.jsonpify import jsonify

app = Flask(__name__)

__author__ = u"Michał Krzysztof Feiler <archiet@platinum.edu.pl>"


@app.route("/")
def mostrecent():
    return jsonify()


@app.route("/<int:fromtime>")
def getfrom(fromtime):
    return jsonify()


@app.route("/<int:fromtime>/<int:totime>")
def getfromto(fromtime, totime):
    return jsonify()
