from flask import Flask, request
import simplejson as json
from signup import signup_api

app = Flask(__name__)

app.register_blueprint(signup_api)

@app.route('/', methods=['GET'])
def index():
    return json.dumps("Hello World")

if __name__ == '__main__':
    app.run(debug=True)
