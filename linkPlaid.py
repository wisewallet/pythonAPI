from flask import Blueprint, request
import simplejson as json
import pymongo
import bcrypt
import time

linkPlaid_api = Blueprint('linkPlaid_api', __name__)

client = pymongo.MongoClient(
    "mongodb://dbadmin:xcdVRvVnykgGMeouDlTWEnVVh@69.55.55.54:27017/")
db = client["users"]


@linkPlaid_api.route("/signup")
def linkPlaid():
    start = time.time()
    data = json.loads(request.data)
    user = {"email": data['email'], "password": bcrypt.hashpw(data['password'], bcrypt.gensalt(
    )), "linked_plaid": False, "first_name": data['firstName'], "last_name": data['lastName']}
    toReturn = db.users.insert_one(user).inserted_id
    end = time.time()
    return end - start
