import json
import logging
import sys
from datetime import datetime
from logging import Logger


def setup_logging(name: str) -> Logger:
    """
    Sets up root logger.
    """
    # create handler with JSON formatter
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    handler.setStream(sys.stdout)

    # set handler as main
    # noinspection PyArgumentList
    logging.basicConfig(level=logging.DEBUG, handlers=[handler])

    # disable useless logging from flask
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('flask-request-logger').setLevel(logging.WARNING)

    return logging.getLogger(name)


class JsonFormatter(logging.Formatter):
    def __init__(self, task_name=None):
        self.task_name = task_name
        super(JsonFormatter, self).__init__()

    def format(self, record):
        data = {'message': record.msg,
                'level': record.levelname,
                'logger': record.name,
                'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')}

        return json.dumps(data)
