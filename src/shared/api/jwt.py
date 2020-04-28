import os

from flask_jwt_extended import verify_jwt_in_request, JWTManager


def setup_jwt(app):
    if os.getenv('JWT_SECRET_KEY', None):
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', None)

    JWTManager(app)


def setup_authorization(blueprint):
    @blueprint.before_request
    def authorize():
        verify_jwt_in_request()
