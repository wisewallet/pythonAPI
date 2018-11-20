from flask import Blueprint, request, current_app
import simplejson as json
import bcrypt
from flask_pymongo import PyMongo
from datetime import datetime, time, date

signup_api = Blueprint('signup_api', __name__)

@signup_api.route("/signup")
def signup():
    data = json.loads(request.data)
    created = datetime.now()
    #start_date = '{:%Y-%m-%d}'.format(start_date_unformatted)
    user = {"email": data['email'], "password": bcrypt.hashpw(data['password'].encode("UTF-8"), bcrypt.gensalt(
    )), "linked_plaid": False,"initalizedCurrent": False,"initalizedHistory": False, "name": data['name'], "created": created}
    toReturn = current_app.userDB.db.users.update_one(user)._id
    return str(toReturn)
