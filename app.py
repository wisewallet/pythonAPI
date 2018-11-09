from flask import Flask, request
import boto3
import simplejson as json

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')

def totalScore(company):
    return company['eScore'] + company['sScore'] + company['gScore']

@app.route('/', methods=['GET'])
def index():
    companyTable = dynamodb.Table('companies')
    companyTableResponse = companyTable.scan()
    companyList = companyTableResponse['Items']
    while 'LastEvaluatedKey' in companyList:
        companyTableResponse = companyTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        companyList.extend(companyTableResponse['Items'])
    companyList.sort(key=totalScore, reverse=True)
    return json.dumps(companyList[:10])

if __name__ == '__main__':
    app.run(debug=True)
