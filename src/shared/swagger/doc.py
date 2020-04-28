from flask_apispec import doc as apispec_doc

from shared.swagger.access import Access


def doc(params=dict(), request_body=dict(), responses=dict(),
        access=Access.PROTECTED, roles=[], tenant_required=True,
        tags=[], **kwargs):
    return apispec_doc(
        inherit=None,
        responses=responses,
        requestBody=request_body,
        params=params,
        access=access,
        roles=roles,
        tenant_required=tenant_required,
        tags=tags,
        **kwargs)
