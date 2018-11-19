from flask import Blueprint, request
import simplejson as json
import pymongo
import bcrypt

login_api = Blueprint('login_api', __name__)

client = pymongo.MongoClient(
    "mongodb://dbadmin:xcdVRvVnykgGMeouDlTWEnVVh@69.55.55.54:27017/")
db = client["users"]


@signup_api.route("/login")
def signup():
    data = json.loads(request.data)
    item = companyDB.companies.find_one({'email': data['email']})
    if bcrypt.checkpw(item['password'], data['password']):
        return("It Matches!")
    else:
        return("It Does not Match")
