from flask import Flask, request
import simplejson as json
from signup import signup_api
from login import login_api
from linkPlaid import linkPlaid_api
from getscores import getscores_api

application = Flask(__name__)

application.register_blueprint(signup_api)
application.register_blueprint(linkPlaid_api)
application.register_blueprint(login_api)
application.register_blueprint(getscores_api)

@application.route('/', methods=['GET'])
def index():
    return json.dumps("Hello World!")

@application.route('/hello')
def index():
    return json.dumps("Hello World!")


if __name__ == '__main__':
    application.run(debug=True)
