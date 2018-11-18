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
notFoundTable = dynamodb.Table('notFound')
dictResponse = companyDicionaryDB.scan()
companyDictionary = dictResponse['Items']
while 'LastEvaluatedKey' in dictResponse:
    response = companyDicionaryDB.scan(
        ExclusiveStartKey=response['LastEvaluatedKey'])
    companyDictionary.extend(response['Items'])


def get_first_day(dt, d_years=0, d_months=0):
    # d_years, d_months are "deltas" to apply to dt
    y, m = dt.year + d_years, dt.month + d_months
    a, m = divmod(m - 1, 12)
    return date(y + a, m + 1, 1)


def get_last_day(dt):
    return get_first_day(dt, 0, 1) + timedelta(-1)


def calculateScore(transactions):
    scores = {'environmental': 0, 'social': 0, 'governance': 0, "politics": 0}
    foundCount = 0
    foundTransactions = dict()
    found = False
    notFound = 0
    for i in range(len(transactions)):
        for attempt in companyDictionary:
            if attempt['transactionString'] in transactions[i]['name'].lower():
                found = True
                #print("Found: " + attempt['matchName'] + " as " + transactions[i]['name'])
                response = table.get_item(
                    Key={
                        'name': attempt['matchName']
                    }
                )
                try:
                    item = response['Item']
                except KeyError as e:
                    notFound += 1
                    #print("Not Found" + transactions[i]['name'])
                else:
                    # print(transactions[i])
                    foundCount += 1
                    scores['environmental'] += int(item['eScore'])
                    scores['social'] += int(item['sScore'])
                    scores['governance'] += int(item['gScore'])
                    if item['pScore'] == "liberal":
                        scores['politics'] += 100
                    if item['pScore'] == "neutral" or item['pScore'] == "na":
                        scores['politics'] += 50
                    if len(foundTransactions) < 9:
                        foundTransactions[transactions[i]['transaction_id']] = {'date': transactions[i]['date'], "eScore": int(item['eScore']), "sScore": int(
                            item['sScore']), "gScore": int(item['gScore']), "pScore": (item['pScore']), "name": attempt['matchName'], "amount": transactions[i]['amount']}
                break
        if not found:
            #print("Not Found: " + transactions[i]['name'])
            response = notFoundTable.update_item(
                Key={
                    'transactionName': transactions[i]['name']
                },
                UpdateExpression="SET countNumber = if_not_exists(countNumber, :start) + :increment",
                ExpressionAttributeValues={
                    ':start': 0,
                    ':increment': 1
                },
                ReturnValues="UPDATED_NEW"
            )
        found = False
    if foundCount == 0:
        return("No foundTransactions")
    scores['environmental'] /= foundCount
    scores['social'] /= foundCount
    scores['politics'] /= foundCount
    scores['governance'] /= foundCount
    scores['total'] = int(0.4 * scores['environmental'] +
                          0.4 * scores['social'] + 0.2 * scores['governance'])
    return scores


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
    for i in range(6):
        start_date = get_first_day(datetime.now(), 0, -(i + 1))
        end_date = get_last_day(start_date)
        print("Start: " + '{:%Y-%m-%d}'.format(start_date))
        print("End: " + '{:%Y-%m-%d}'.format(end_date))

        transactions_response = plaidClient.Transactions.get(access_token,
                                                             '{:%Y-%m-%d}'.format(
                                                                 start_date),
                                                             '{:%Y-%m-%d}'.format(end_date))
        transactions = transactions_response['transactions']
        while len(transactions) < transactions_response['total_transactions']:
            transactions_response = plaidClient.Transactions.get(access_token,
                                                                 '{:%Y-%m-%d}'.format(
                                                                     start_date),
                                                                 '{:%Y-%m-%d}'.format(
                                                                     end_date),
                                                                 offset=len(
                                                                     transactions)
                                                                 )
            transactions.extend(transactions_response['transactions'])
        print(calculateScore(transactions))
    end = idk.time()
    # print(transactions)
    return str(end - start)
