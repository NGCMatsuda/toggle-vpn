from decimal import Decimal
from unittest.mock import MagicMock

from pytest import raises

from shared.api_client.api_client import _raise_on_error, _deserialize_response
from shared.api_client.api_request_exception import NotFoundException, ApiRequestException


def test_json_deserializer_uses_decimal_function_for_floats():
    response = MagicMock()
    response.json.return_value = None

    _deserialize_response(response)

    response.json.assert_called_with(parse_float=Decimal)


def test_raises_not_found_exception_when_entity_not_found():
    response = MagicMock()
    response.status_code = 404

    with raises(NotFoundException):
        _raise_on_error(response)


def test_raises_default_exception_when_unhandled_status_code():
    response = MagicMock()
    response.status_code = 900

    with raises(ApiRequestException):
        _raise_on_error(response)
