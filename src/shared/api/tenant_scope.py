from flask import request


def request_tenant_id():
    return int(request.headers.get('x-tenant', None))


def request_accessible_tenants():
    return list(request.headers.get('tenants', []))