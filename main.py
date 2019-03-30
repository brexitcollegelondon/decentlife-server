import json
from tinydb import TinyDB, Query

from flask import Flask
app = Flask(__name__)
db = TinyDB('challenges.json')

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/challenges")
def get_all_challenges():
    return json.dumps(db.all())
