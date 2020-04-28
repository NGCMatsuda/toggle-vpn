from shared.messaging.publisher import prefix_params


def test_prefix_all_meta_headers():
    params = dict(
        tenant_id="foo",
        id="bar"
    )
    prefixed_params = prefix_params(params)

    assert {
               "meta-tenant_id": "foo",
               "meta-id": "bar"
           } == prefixed_params
