from flask import Blueprint, request
import pymongo

signup_api = Blueprint('signup_api', __name__)

client = pymongo.MongoClient("mongodb://dbadmin:xcdVRvVnykgGMeouDlTWEnVVh@69.55.55.54:27017/")
db = client["users"]

@signup_api.route("/signup")
def signup():
    for x in db.users.find():
        print(x)
    return request
