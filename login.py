from flask import Blueprint, request
import simplejson as json
import pymongo
import bcrypt

login_api = Blueprint('login_api', __name__)

client = pymongo.MongoClient(
    "mongodb://dbadmin:xcdVRvVnykgGMeouDlTWEnVVh@69.55.55.54:27017/")
db = client["users"]


@login_api.route("/login")
def login():
    data = json.loads(request.data)
    item = db.users.find_one({'email': data['email']})
    print(item)
    if bcrypt.checkpw(data["password"], "$2b$08$PUYZ/WHwG4lf2gLsp8O5R.XO96mvisnqbFmz39nFTfHkKbq2S1Emy"):
        return("It Matches!")
    else:
        return("It Does not Match")
