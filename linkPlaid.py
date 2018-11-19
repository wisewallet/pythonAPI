from flask import Blueprint, request
import simplejson as json
import pymongo
import time as clock
import plaid
from datetime import datetime, time, date, timedelta
from bson.objectid import ObjectId

linkPlaid_api = Blueprint('linkPlaid_api', __name__)

mongoURI = "mongodb://dbadmin:xcdVRvVnykgGMeouDlTWEnVVh@69.55.55.54:27017/"
mongoClient = pymongo.MongoClient(mongoURI)
db = mongoClient["users"]
companyDB = mongoClient["companies"]
client_id = '5a9f59e5bdc6a4062cd4229b'
secret = '0f2c037ebe121dfeffc15cd13bb5f7'
public_key = '06812b585d6f3b0ebde352a7759bb1'
environment = 'development'
plaidClient = plaid.Client(client_id, secret, public_key, environment)


def get_first_day(dt, d_years=0, d_months=0):
    y, m = dt.year + d_years, dt.month + d_months
    a, m = divmod(m - 1, 12)
    return date(y + a, m + 1, 1)


def get_last_day(dt):
    return get_first_day(dt, 0, 1) + timedelta(-1)


def calculateScore(transactions):
    scores = {'environmental': 0, 'social': 0, 'governance': 0, "politics": 0}
    foundCount = 0
    found = False
    foundCompanies = dict()
    for i in range(len(transactions)):
        if transactions[i]['name'] in foundCompanies:
            item = foundCompanies[transactions[i]['name']]
        else:
            item = companyDB.companies.find_one({'transactionMatch': transactions[i]['name']},{ 'eScore' : 1 , 'gScore' : 1 , 'sScore' : 1 , 'pScore' : 1})
            foundCompanies[transactions[i]['name']] = item
        if item != None:
            found = True
            foundCount += 1
            scores['environmental'] += item['eScore']
            scores['social'] += item['sScore']
            scores['governance'] += item['gScore']
            companyPScore = item['pScore']
            if companyPScore == "liberal":
                scores['politics'] += 100
            if companyPScore == "neutral" or companyPScore == "na":
                scores['politics'] += 50
        if not found:
            companyDB.not_found.update_one({"name": transactions[i]['name']}, {'$inc': {"count": 1}}, upsert=True)
            foundCompanies[transactions[i]['name']] = None
        found = False
    if foundCount == 0:
        return("No Transactions Found")
    scores['environmental'] /= foundCount
    scores['social'] /= foundCount
    scores['politics'] /= foundCount
    scores['governance'] /= foundCount
    scores['total'] = int(0.4 * scores['environmental'] + 0.4 * scores['social'] + 0.2 * scores['governance'])
    return scores


@linkPlaid_api.route("/link")
def linkPlaid():
    start = clock.time()
    # print(companyDicionaryDB.scan())
    data = json.loads(request.data)
    access_token = None
    # public_token = data["public_token"]
    # exchange_response = plaidClient.Item.public_token.exchange(public_token)
    # print 'access token: ' + exchange_response['access_token']
    # print 'item ID: ' + exchange_response['item_id']
    user = db.users.find_one({'_id': ObjectId(data['id'])})
    access_token = user['plaid']['access_token']
    start_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-30))
    end_date = '{:%Y-%m-%d}'.format(datetime.now())

    transactions_response = plaidClient.Transactions.get(access_token, start_date, end_date)
    transactions = transactions_response['transactions']
    while len(transactions) < transactions_response['total_transactions']:
        transactions_response = plaidClient.Transactions.get(access_token, start_date, end_date, offset=len(transactions))
        transactions.extend(transactions_response['transactions'])
    scores = calculateScore(transactions)
    db.users.update({"_id": user['_id']}, {'$set': {"scores": scores, "initalizedCurrent": True}}, upsert=False)

    for i in range(6):
        start_date_unformatted = get_first_day(datetime.now(), 0, -(i + 1))
        start_date = '{:%Y-%m-%d}'.format(start_date_unformatted)
        end_date = '{:%Y-%m-%d}'.format(get_last_day(start_date_unformatted))
        # print("Start: " + '{:%Y-%m-%d}'.format(start_date))
        # print("End: " + '{:%Y-%m-%d}'.format(end_date))
        transactions_response = plaidClient.Transactions.get(access_token, start_date, end_date)
        transactions = transactions_response['transactions']
        while len(transactions) < transactions_response['total_transactions']:
            transactions_response = plaidClient.Transactions.get(access_token, start_date, end_date, offset=len(transactions))
            transactions.extend(transactions_response['transactions'])
        scores = calculateScore(transactions)
        updateQuery = "scoreHistory." + str(start_date)
        db.users.update({"_id": user['_id']}, {'$set': {updateQuery: scores, "initalizedHistory": True}}, upsert=False)
    end = clock.time()
    return str(end - start)
