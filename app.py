from flask import Flask, request
from flask_pymongo import PyMongo
import simplejson as json
from signup import signup_api

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://dbadmin:xcdVRvVnykgGMeouDlTWEnVVh@69.55.55.54:27017/"
mongo = PyMongo(app)

app.register_blueprint(signup_api)

@app.route('/', methods=['GET'])
def index():
    mongo.db.users.insert({"email": "main"})
    return json.dumps("Hello World")

if __name__ == '__main__':
    app.run(debug=True)
