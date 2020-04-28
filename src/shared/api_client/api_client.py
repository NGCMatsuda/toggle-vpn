from decimal import Decimal

import requests

from shared.api_client.api_request_exception import ApiRequestException, NotFoundException


class ApiClient:

    def __init__(self, tenant_id, request_id):
        super().__init__()
        self.tenant_id = tenant_id
        self.request_id = request_id

    def get(self, url):
        headers = {
            'Content-Type': 'application/json',
            'x-tenant': str(self.tenant_id)
        }

        if self.request_id:
            headers['X-Request-ID'] = self.request_id

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return _deserialize_response(response)

        _raise_on_error(response)


def _deserialize_response(response):
    return response.json(
        parse_float=Decimal
    )


def _raise_on_error(response):
    if response.status_code == 404:
        raise NotFoundException(response)
    raise ApiRequestException(response)
