from flask import Blueprint, request
import simplejson as json
import pymongo
import bcrypt
from bson.objectid import ObjectId

getscores_api = Blueprint('getscores_api', __name__)

client = pymongo.MongoClient(
    "mongodb://dbadmin:xcdVRvVnykgGMeouDlTWEnVVh@69.55.55.54:27017/")
db = client["users"]


@getscores_api.route("/getscores")
def getscores():
    data = json.loads(request.data)
    item = db.users.find_one({'_id': ObjectId(data['id'])})
    if item == None:
        return("Invalid User")
    else:
        return({eScore: item['eScore'], sScore: item['sScore']})
