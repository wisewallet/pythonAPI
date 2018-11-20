from flask import Blueprint, request
import simplejson as json
import bcrypt
from flask_pymongo import PyMongo

signup_api = Blueprint('signup_api', __name__)


@signup_api.route("/signup")
def signup():
    data = json.loads(request.data)
    user = {"email": data['email'], "password": bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt(
    )), "linked_plaid": False,"initalizedCurrent": False,"initalizedHistory": False, "name": data['name']}
    toReturn = current_app.userDB.db.users.insert_one(user).inserted_id
    return str(toReturn)
