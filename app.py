from flask import Flask
import boto3

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')

@app.route('/')
def index():
    companyTable = dynamodb.Table('companies')
    companyTableResponse = companyTable.scan()
    companyList = companyTableResponse['Items']
    while 'LastEvaluatedKey' in companyList:
        companyTableResponse = companyTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        companyList.extend(companyTableResponse['Items'])
    return companyList

if __name__ == '__main__':
    app.run(debug=True)
