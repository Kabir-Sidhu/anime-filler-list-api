from flask import Flask, jsonify
from fillers import getFillers

app = Flask(__name__)

fillers = getFillers()

@app.route('/')
def index():
    return jsonify(fillers)

@app.route('/<name>')
def anime(name):
    return jsonify(fillers[name])

app.run()