from shared.messaging.consumer import extract_metadata
from shared.messaging.metadata import Metadata


def test_collect_and_remove_prefix_from_all_meta_headers():
    prefixed_params = {
        "meta-tenant_id": "foo",
        "meta-id": "bar",
        "x-death": 1
    }
    metadata = extract_metadata(prefixed_params)

    assert Metadata(
        tenant_id='foo',
        id='bar'
    ) == metadata
    assert metadata.__class__ == Metadata
