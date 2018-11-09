from flask import Flask, request, jsonify
import boto3

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
    return jsonify(companyList)

if __name__ == '__main__':
    app.run(debug=True)
