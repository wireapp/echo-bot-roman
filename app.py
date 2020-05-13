import logging
import sys
from importlib import util as importing

import json_logging
from flask import Flask
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from api.RomanAPI import roman_api
from api.StatusApi import status_api
from api.VersionApi import version_api, get_version
from services.Metrics import init_metrics

# setup log level and set stdout
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

# enable JSON logging for non http context (this init)
json_logging.ENABLE_JSON_LOGGING = True
json_logging.init_non_web()

# create logger
logger = logging.getLogger(__name__)
# make logger print jsons
json_logging.config_root_logger()


def load_configuration(app):
    config_file = 'config'
    if importing.find_spec(config_file):
        app.config.from_object(config_file)


def configure_apis(app):
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
    api.add_namespace(roman_api, path='/')
    api.add_namespace(version_api, path='/')
    api.add_namespace(status_api, path='/')


def configure_metrics(app):
    logger.debug("Initialize metrics")
    init_metrics(app, get_version())


def configure_json_logging(app):
    # enable JSON logging for the Flask
    json_logging.ENABLE_JSON_LOGGING = True
    json_logging.init_flask(enable_json=True)
    json_logging.init_request_instrument(app)

    # configure root logger
    json_logging.config_root_logger()
    # disable printing of flask requests
    logging.getLogger('flask-request-logger').setLevel(logging.WARNING)


# Create app
app = Flask(__name__)
# fix for https swagger - see https://github.com/python-restx/flask-restx/issues/58
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)

with app.app_context():
    # load app configuration
    load_configuration(app)
    # configure APIs
    configure_apis(app)
    # configure prometheus metrics
    configure_metrics(app)
    # lastly initialize logging to jsons
    configure_json_logging(app)

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
