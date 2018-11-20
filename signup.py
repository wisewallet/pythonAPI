from flask import Blueprint, request
import simplejson as json
import pymongo
import bcrypt

signup_api = Blueprint('signup_api', __name__)

client = pymongo.MongoClient(
    "mongodb://dbadmin:xcdVRvVnykgGMeouDlTWEnVVh@69.55.55.54:27017/")
db = client["users"]


@signup_api.route("/signup")
def signup():
    data = json.loads(request.data)
    user = {"email": data['email'], "password": bcrypt.hashpw(data['password'], bcrypt.gensalt(
    )), "linked_plaid": False,"initalizedCurrent": False,"initalizedHistory": False, "name": data['name']}
    toReturn = db.users.insert_one(user).inserted_id
    return str(toReturn)
