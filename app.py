from flask import Flask, request
from flask_pymongo import PyMongo
import simplejson as json
from signup import signup_api

app = Flask(__name__)
app.config['MONGO_HOST'] = '69.55.55.54'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DBNAME'] = 'users'
app.config['MONGO_USERNAME'] = 'dbadmin'
app.config['MONGO_PASSWORD'] = 'xcdVRvVnykgGMeouDlTWEnVVh'
app.config['MONGO_AUTH_SOURCE'] = 'admin'
mongo = PyMongo(app)

app.register_blueprint(signup_api)

@app.route('/', methods=['GET'])
def index():
    mongo.db.users.insert_one({"email": "main"})
    return json.dumps("Hello World")

if __name__ == '__main__':
    app.run(debug=True)
