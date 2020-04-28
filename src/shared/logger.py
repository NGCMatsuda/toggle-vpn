import json
import logging
import os
import time
import traceback
from json import JSONDecodeError

import json_log_formatter
import simplejson
from flask import g, request, current_app, has_request_context
from flask.logging import default_handler

BLACKLIST_FIELDS = ['password']
LOG_FIELDS = [
    'method',
    'path',
    'status',
    'duration',
    'ip',
    'host',
    'params',
    'body',
    'username',
    'request_id'
]


def setup_server_application_logger(app):
    setup_json_log_formatter()
    __remove_default_flask_logger(app)
    __prepare_logger_levels()

    @app.before_request
    def before_request():
        __start_request_timer()

    @app.after_request
    def after_request(response):
        __log_request(response)
        return response

    @app.errorhandler(Exception)
    def unknown_exception(exception):
        logging.exception("Unknown exception:", exc_info=exception)
        return dict(error=str(exception)), 500


def setup_json_log_formatter():
    logging.basicConfig(level=logging.INFO, handlers=[__json_log_handler()])


def __json_log_handler():
    json_formatter = ApplicationJSONLogFormatter()
    json_formatter.json_lib = simplejson
    json_handler = logging.StreamHandler()
    json_handler.setFormatter(json_formatter)

    return json_handler


def __remove_default_flask_logger(app):
    app.logger.removeHandler(default_handler)


def __prepare_logger_levels():
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('pika').setLevel(logging.WARNING)


def __start_request_timer():
    g.start = time.time()


def __log_request(response):
    log_builder = LogBuilder(request, response)

    log_data = dict()

    for field in LOG_FIELDS:
        try:
            value = getattr(log_builder, field)()
            if value is not None:
                log_data[field] = value
        except Exception:
            pass

    current_app.logger.info('API Request', extra=log_data)


class ApplicationJSONLogFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        if os.getenv('FLASK_ENV') == 'development' and record.exc_info is not None:
            _, exception, _ = record.exc_info
            print(str(exception))
            traceback.print_tb(exception.__traceback__)

        result = super(ApplicationJSONLogFormatter, self).json_record(message, extra, record)
        result['logger'] = record.name
        return result


class LogBuilder:
    def __init__(self, req, res):
        self.request = req
        self.response = res
        self.now = time.time()

    def method(self):
        return self.request.method

    def path(self):
        return self.request.path

    def status(self):
        return self.response.status_code

    def duration(self):
        if hasattr(g, 'start') and g.start:
            return round(self.now - g.start, 2)

    def ip(self):
        return self.request.headers.get('X-Forwarded-For', self.request.remote_addr)

    def host(self):
        return self.request.host.split(':', 1)[0]

    def request_id(self):
        if has_request_context() and self.request.headers.get('X-Request-ID'):
            return self.request.headers.get('X-Request-ID')

    def username(self):
        return self.request.headers.get('username')

    def params(self):
        args = dict(self.request.args)
        return self.__whitelisted_dict(args) if args else None

    def body(self):
        return self.__whitelisted_body(self.request.data) if self.request.data else None

    def __whitelisted_body(self, body):
        try:
            parsed_json = json.loads(body)
            return self.__whitelisted_dict(parsed_json)
        except JSONDecodeError:
            return body

    def __whitelisted_dict(self, params):
        return {key: value.lower() if (key not in BLACKLIST_FIELDS) else '********' for key, value in params.items()}
