from flask import Blueprint

signup_api = Blueprint('signup_api', __name__)

@signup_api.route("/signup")
def signup():
    return "list of accounts"
