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
    )), linkedPLaid: False, first_name: data['firstName'], last_name: data['lastName']}
    db.users.insert_one(user)
    return request.data
