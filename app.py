from flask import Flask, request
import simplejson as json
from signup import signup_api
from login import login_api
from linkPlaid import linkPlaid_api
from getscores import getscores_api

app = Flask(__name__)

app.register_blueprint(signup_api)
app.register_blueprint(linkPlaid_api)
app.register_blueprint(login_api)
app.register_blueprint(getscores_api)

@app.route('/', methods=['GET'])
def index():
    return json.dumps("Hello World")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
