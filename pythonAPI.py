from flask import Flask, request
import simplejson as json
from flask_pymongo import PyMongo
from signup import signup_api
from login import login_api
from linkPlaid import linkPlaid_api
from getscores import getscores_api

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://dbadmin:xcdVRvVnykgGMeouDlTWEnVVh@69.55.55.54:27017/users"
app.mongo = PyMongo(app)
app.register_blueprint(signup_api)
app.register_blueprint(linkPlaid_api)
app.register_blueprint(login_api)
app.register_blueprint(getscores_api)

@app.route('/')
def index():
    return json.dumps("Hello World! " + app.mongo)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
