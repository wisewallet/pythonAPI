from flask import Blueprint, request
import simplejson as json
import pymongo
import bcrypt
import time as idk
import plaid
from datetime import datetime, date, time, timedelta
import boto3

linkPlaid_api = Blueprint('linkPlaid_api', __name__)

mongoClient = pymongo.MongoClient(
    "mongodb://dbadmin:xcdVRvVnykgGMeouDlTWEnVVh@69.55.55.54:27017/")
db = mongoClient["users"]

plaidClient = plaid.Client('5a9f59e5bdc6a4062cd4229b',
                           '0f2c037ebe121dfeffc15cd13bb5f7',
                           '06812b585d6f3b0ebde352a7759bb1',
                           'development')

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('companies')
companyDicionaryDB = dynamodb.Table('companyDictionary')
dictResponse = companyDicionaryDB.scan()
companyDictionary = dictResponse['Items']
while 'LastEvaluatedKey' in dictResponse:
    response = companyDicionaryDB.scan(
        ExclusiveStartKey=response['LastEvaluatedKey'])
    companyDictionary.extend(response['Items'])


@linkPlaid_api.route("/link")
def linkPlaid():
    start = idk.time()
    # print(companyDicionaryDB.scan())
    data = json.loads(request.data)
    access_token = "access-development-65c2bdad-21b0-47e5-b1c5-f1455b83c340"
    # public_token = data["public_token"]
    # exchange_response = plaidClient.Item.public_token.exchange(public_token)
    # print 'access token: ' + exchange_response['access_token']
    # print 'item ID: ' + exchange_response['item_id']
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
    end = idk.time()
    # print(transactions)
    for i in range(6):
        next_month = (datetime.now() + timedelta(-30 * (1 + i)).replace(
            day=28) + datetime.timedelta(days=4)  # this will never fail
        end_date=next_month - datetime.timedelta(days=next_month.day)
    return str(end - start)
