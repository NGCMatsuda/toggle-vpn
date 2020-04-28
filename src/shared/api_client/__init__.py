from shared.api_client.api_client import ApiClient
from shared.api.request import request_id


def api_client(tenant_id):
    return ApiClient(tenant_id, request_id())
