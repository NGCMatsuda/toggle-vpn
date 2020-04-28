import json
import os
import uuid
from datetime import datetime, timedelta

import jwt


def _create_authenticated_request_headers(username, headers):
    return {
        **(headers or {}),
        "Authorization": f'Bearer {access_token(username)}'
    }


def get_request_authenticated(client, url, tenant_id, headers=None, username='admin'):
    return get_request(client, url, tenant_id, headers=_create_authenticated_request_headers(username, headers))


def post_request_authenticated(client, url, data, tenant_id, headers=None, username='admin'):
    return post_request(client, url, data, tenant_id, _create_authenticated_request_headers(username, headers))


def patch_request_authenticated(client, url, data, tenant_id, headers=None, username='admin'):
    return patch_request(client, url, data, tenant_id, _create_authenticated_request_headers(username, headers))


def delete_request_authenticated(client, url, tenant_id, headers=None, username='admin'):
    return delete_request(client, url, tenant_id, _create_authenticated_request_headers(username, headers))


def get_request(client, url, tenant_id, headers=None):
    return client.get(url, headers={'x-tenant': tenant_id, **(headers or {})})


def post_request(client, url, data, tenant_id, headers=None):
    return client.post(url, data=json.dumps(data), content_type='application/json', headers={'x-tenant': tenant_id, **(headers or {})})


def patch_request(client, url, data, tenant_id, headers=None):
    return client.patch(url, data=json.dumps(data), content_type='application/json', headers={'x-tenant': tenant_id, **(headers or {})})


def delete_request(client, url, tenant_id, headers=None):
    return client.delete(url, content_type='application/json', headers={'x-tenant': tenant_id, **(headers or {})})


def json_of_response(response):
    return json.loads(response.data.decode('utf8'))


def access_token(username):
    users = dict(
        admin=dict(role='cis', id=1, username='admin')
    )
    user = users.get(username)

    now = datetime.timestamp(datetime.now())
    expires = datetime.timestamp(datetime.now() + timedelta(days=1))
    token_data = {
        'iat': now,
        'nbf': now,
        'jti': str(uuid.uuid4()),
        'exp': expires,
        'identity': user.get('username'),
        'fresh': False,
        'type': 'access',
        'user_claims': {'role': user.get('role')}
    }

    return jwt.encode(token_data, os.getenv('JWT_SECRET_KEY')).decode('utf-8')
