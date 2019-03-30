import json
from tinydb import TinyDB, Query

from flask import Flask, request
app = Flask(__name__)
db: TinyDB = TinyDB('challenges.json')
q: Query = Query()


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/challenges")
def get_all_challenges():
    return json.dumps(db.all())


@app.route("/challenge", methods=['POST'])
def add_challenge():
    new_challenge = request.json
    db.upsert(new_challenge, q.challenge_id == new_challenge['challenge_id'])
    return "ok"
