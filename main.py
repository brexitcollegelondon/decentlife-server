import json
import requests
from tinydb import TinyDB, Query
from flask_cors import CORS
from flask import Flask, request
app = Flask(__name__)
CORS(app)
db: TinyDB = TinyDB('challenges.json')
user_db: TinyDB = TinyDB('users.json')
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
    if not new_challenge['creator_bystander']:
        new_challenge['participants'] = [new_challenge['creator_id']]
        new_challenge['bystanders'] = []
    else:
        new_challenge['bystanders'] = [new_challenge['creator_id']]
        new_challenge['participants'] = []

    db.upsert(new_challenge, q.challenge_id == new_challenge['challenge_id'])
    return "ok"

@app.route("/join_challenge", methods=['POST'])
def join_challenge():
    join_data = request.json #challenge_id, user_id, is_bystander
    challenge = db.search(q.challenge_id == join_data["challenge_id"])[0]
    if not join_data['is_bystander']:
        participants = challenge['participants']
        participants.append(join_data["user_id"])
        challenge["participants"] = list(set(participants))
    else:
        bystanders = challenge['bystanders']
        bystanders.append(join_data["user_id"])
        challenge["bystanders"] = list(set(bystanders))

    db.upsert(challenge, q.challenge_id == challenge["challenge_id"])
    return "ok"
@app.route("/add_user", methods=['POST'])
def add_user():
    new_user = request.json
    user_db.upsert(new_user, q.user_id == new_user['user_id'])
    return "ok"

@app.route("/users/<user_id>")
def get_user(user_id):
    return json.dumps(user_db.search(q.user_id == user_id)[0])

@app.route("/users/<user_id>/update", methods=['POST'])
def update_data(user_id):
    user = user_db.search(q.user_id == user_id)[0]
    health_data = request.json
    for parameter in health_data:
        user[parameter] = health_data[parameter]
    return json.dumps(user)

@app.route("/challenges/<challenge_id>/end")
def end_challenge(challenge_id):
    challenge = db.search(q.challenge_id == challenge_id)[0]
    challenge_type = challenge["challenge_type"]
    users = challenge["participants"]
    for user_id in users:
        user = user_db.search(q.user_id == user_id)[0]
        print(user)
        user_quantity = user[challenge_type]
        if user_quantity < challenge["target_quantity"]:
            participants = challenge['participants']
            losers       = []
            participants.remove(user_id)
            losers.append(user_id)
            challenge['losers']       = losers
            challenge['participants'] = participants
    winners = participants
    return json.dumps(challenge['participants'])
