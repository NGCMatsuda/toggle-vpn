from marshmallow import ValidationError
from pytest import raises

from shared.schema.validate.empty_array_not_allowed import empty_array_not_allowed


def test_valid_array_contains_items():
    assert empty_array_not_allowed([1]) == [1]


def test_no_list_value_is_invalid():
    with raises(ValidationError) as exception:
        empty_array_not_allowed(123)

    assert exception.value.messages == ['invalid_type']


def test_empty_array_value_is_invalid():
    with raises(ValidationError) as exception:
        empty_array_not_allowed([])

    assert exception.value.messages == ['empty_array_not_allowed']
