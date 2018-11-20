from flask import Blueprint, request, current_app
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
    item = current_app.userDB.db.users.find_one({'email': data['email']})
    if item == None:
        return("Invalid Email")
    if bcrypt.checkpw(data["password"], item["password"]):
        return(str(item["_id"]))
    else:
        return("Invalid Password")
