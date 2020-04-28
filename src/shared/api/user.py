from flask import request


def get_username():
    return request.headers.get('username')
