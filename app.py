from flask import Flask, request, jsonify
import boto3
import json

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')

@app.route('/', methods=['GET'])
def index():
    companyTable = dynamodb.Table('companies')
    companyTableResponse = companyTable.scan()
    companyList = companyTableResponse['Items']
    while 'LastEvaluatedKey' in companyList:
        companyTableResponse = companyTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        companyList.extend(companyTableResponse['Items'])
    return json.dumps(companyList)

if __name__ == '__main__':
    app.run(debug=True)
