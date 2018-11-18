from flask import Flask, request
import simplejson as json

app = Flask(__name__)

@app.route('/getSuggestions', methods=['GET'])
def index():
    return json.dumps("Hello World")

if __name__ == '__main__':
    app.run(debug=True)
