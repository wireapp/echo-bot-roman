import logging
import sys
from importlib import util as importing

from flask import Flask
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from api.RomanAPI import roman_api
from api.StatusApi import status_api
from api.VersionApi import version_api

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] - %(levelname)s - %(module)s: %(message)s',
                    stream=sys.stdout)
logger = logging.getLogger(__name__)

logger.debug("Building App.")
# Create app
app = Flask(__name__)
# fix for https swagger - see https://github.com/python-restx/flask-restx/issues/58
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)

logger.debug("Creating auth.")
# Set up Swagger and API
authorizations = {
    'bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

logger.debug("Creating API.")

api = Api(app, authorizations=authorizations)

logger.debug("Creating namespaces.")

# Register namespaces
api.add_namespace(roman_api, path='/')
api.add_namespace(version_api, path='/')
api.add_namespace(status_api, path='/')

logger.debug("Loading configs.")

config_file = 'config'
if importing.find_spec(config_file):
    app.config.from_object(config_file)

logger.info("Starting up.")

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
