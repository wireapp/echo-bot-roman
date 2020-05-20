import json
import logging
import sys
import traceback
from datetime import datetime, timezone
from logging import Logger

from wire_flask.RequestId import request_id


def setup_logging(name: str, level=logging.DEBUG, json_logging=True) -> Logger:
    """
    Sets up root logger.
    """
    if json_logging:
        setup_json_logging(level)
    else:
        setup_plain_logging(level)

    # disable useless logging from flask
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

    return logging.getLogger(name)


def setup_plain_logging(level):
    logging.basicConfig(level=level,
                        format='[%(asctime)s] - %(levelname)s - %(module)s: %(message)s',
                        stream=sys.stdout)


def setup_json_logging(level):
    # create handler with JSON formatter
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    handler.setStream(sys.stdout)

    # set handler as main
    # noinspection PyArgumentList
    logging.basicConfig(level=level, handlers=[handler])


class JsonFormatter(logging.Formatter):
    def __init__(self, task_name=None):
        self.task_name = task_name
        # ignore useless values -> we must use blacklisting in order to allow extras
        self.ignored = {'args', 'created', 'exc_info', 'exc_text', 'filename', 'funcName', 'levelno', 'lineno',
                        'module', 'msecs', 'pathname', 'process', 'processName', 'relativeCreated', 'stack_info',
                        'thread'}
        # rename values to the Wire common names
        self.renaming = {'levelname': 'level', 'msg': 'message', 'name': 'logger', 'threadName': 'thread_name'}
        # transform some values for common usage
        self.transformations = {'level': lambda x: 'WARN' if x == 'WARNING' else x}
        super(JsonFormatter, self).__init__()

    @staticmethod
    def __prepare_log_data(record):
        data = {
            # we can't use isoformat as it is not really ISO, because it is missing Z
            # thus this strftime is real ISO
            '@timestamp': datetime.fromtimestamp(record.created, timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
        # try to insert call id - needs flask context
        try:
            request = request_id()
            if request.nginx_related:
                data['infra_request'] = request.nginx_related
            if request.app_related:
                data['app_request'] = request.app_related
        # ignore exception when this log is outside of the context
        except Exception:
            pass
        return data

    def __transform_value(self, k_renamed, v):
        return self.transformations[k_renamed](v) if k_renamed in self.transformations else v

    def __copy_valid_data(self, record, data):
        # copy only necessary data
        for k, v in vars(record).items():
            if k in self.ignored or not v:
                continue
            k_renamed = self.renaming.get(k)
            k = k_renamed if k_renamed else k
            data[k] = self.__transform_value(k, v)

    @staticmethod
    def __insert_exception(record, data):
        # copy exception if there's one
        if record.exc_info:
            data['exception'] = {
                'stacktrace': traceback.format_exception(record.exc_info[0], record.exc_info[1], record.exc_info[2])
            }

    def format(self, record):
        data = self.__prepare_log_data(record)
        self.__copy_valid_data(record, data)
        self.__insert_exception(record, data)
        return json.dumps(data)
