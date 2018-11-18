from flask import Blueprint, request
import pymongo
import bcrypt

signup_api = Blueprint('signup_api', __name__)

client = pymongo.MongoClient("mongodb://dbadmin:xcdVRvVnykgGMeouDlTWEnVVh@69.55.55.54:27017/")
db = client["users"]

@signup_api.route("/signup")
def signup():
    user ={"email":request.data.email, "password": bcrypt.hashpw(request.data.password, bcrypt.gensalt())}
    db.users.insert_one(user)
    return request.data
