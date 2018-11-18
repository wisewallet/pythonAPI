from flask import Blueprint

signup_api = Blueprint('signup_api', __name__)

@account_api.route("/signup")
def signup():
    return "list of accounts"
