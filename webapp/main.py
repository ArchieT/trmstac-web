from flask import Flask
from flask.ext.jsonpify import jsonify

app = Flask(__name__)


@app.route("/")
def mostrecent():
    return jsonify()


@app.route("/<int:fromtime>")
def getfrom(fromtime):
    return jsonify()


@app.route("/<int:fromtime>/<int:totime>")
def getfromto(fromtime, totime):
    return jsonify()
