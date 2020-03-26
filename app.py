from importlib import util as importing

from flask import Flask
from flask_restx import Api

from api.RomanAPI import roman_api
from api.StatusApi import status_api
from api.VersionApi import version_api

app = Flask(__name__)

# Set up Swagger and API
authorizations = {
    'bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(app, authorizations=authorizations)

api.add_namespace(roman_api, path='/')
api.add_namespace(version_api, path='/')
api.add_namespace(status_api, path='/')

config_file = 'config'

if importing.find_spec(config_file):
    app.config.from_object(config_file)

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
