import uuid
from functools import wraps

from flask import request, has_request_context
from marshmallow import ValidationError

from shared.exception import RequestValidationException


def parse_request(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                request_body = request.get_data(as_text=True)
                parsed_parameters = schema.loads(request_body, **schema.Meta.render_module_opts)
                return func(*args, **kwargs, **parsed_parameters)
            except ValidationError as error:
                raise RequestValidationException('Invalid request data', error.messages)

        return wrapper

    return decorator


def serialize_response(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response, status, headers = __unpack(func(*args, **kwargs))
            return schema.dump(response), status, headers

        return wrapper

    return decorator


def request_id():
    return request.headers.get('X-Request-ID') if has_request_context() else None


def __unpack(response):
    response = response if isinstance(response, tuple) else (response,)
    return response + (None,) * (3 - len(response))
