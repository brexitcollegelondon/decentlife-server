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

@app.route("/challenges/<challenge_id>")
def get_challenge(challenge_id):
    return json.dumps(db.search(q.challenge_id == challenge_id)[0])


@app.route("/challenge", methods=['POST'])
def add_challenge():
    new_challenge = request.json
    new_challenge['participants_list'] = [{
        new_challenge['creator_id']: new_challenge['is_bystander']
    }]
    db.upsert(new_challenge, q.challenge_id == new_challenge['challenge_id'])
    return "ok"

@app.route("/join_challenge", methods=['POST'])
def join_challenge():
    join_data = request.json #challenge_id, user_id, is_bystander
    challenge = db.search(q.challenge_id == join_data["challenge_id"])[0]
    participants_list = challenge['participants_list']
    unique = True
    for dict in participants_list:
        if join_data["user_id"] in dict:
            unique = False
    if unique:
        participants_list.append({join_data["user_id"]: join_data["is_bystander"]})
    challenge["participants_list"] = participants_list
    db.upsert(challenge, q.challenge_id == challenge["challenge_id"])
    return "ok"
