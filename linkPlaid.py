from flask import Blueprint, request
import simplejson as json
import pymongo
import bcrypt
import time
import plaid

linkPlaid_api = Blueprint('linkPlaid_api', __name__)

mongoClient = pymongo.MongoClient(
    "mongodb://dbadmin:xcdVRvVnykgGMeouDlTWEnVVh@69.55.55.54:27017/")
db = mongoClient["users"]

plaidClient = plaid.Client('5a9f59e5bdc6a4062cd4229b',
                           '0f2c037ebe121dfeffc15cd13bb5f7',
                           '06812b585d6f3b0ebde352a7759bb1',
                           'development')


@linkPlaid_api.route("/link")
def linkPlaid():
    start = time.time()
    data = json.loads(request.data)
    access_token = "access-development-65c2bdad-21b0-47e5-b1c5-f1455b83c340"
    #public_token = data["public_token"]
    #exchange_response = plaidClient.Item.public_token.exchange(public_token)
    #print 'access token: ' + exchange_response['access_token']
    #print 'item ID: ' + exchange_response['item_id']
    transactions_response = plaidClient.Transactions.get(access_token,
                                                         start_date='2018-01-01',
                                                         end_date='2018-02-01')
    transactions = transactions_response['transactions']
    while len(transactions) < transactions_response['total_transactions']:
        transactions_response = plaidClient.Transactions.get(access_token,
                                                             start_date='2018-01-01',
                                                             end_date='2018-02-01',
                                                             offset=len(
                                                                 transactions)
                                                             )
        transactions.extend(transactions_response['transactions'])
    end = time.time()
    print(transactions)
    return str(end - start)
