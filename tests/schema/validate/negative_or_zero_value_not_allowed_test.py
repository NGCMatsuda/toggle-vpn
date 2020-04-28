from marshmallow import ValidationError
from pytest import raises

from shared.schema.validate.negative_or_zero_value_not_allowed import negative_or_zero_value_not_allowed


def test_negative_or_zero_value_not_allowed_with_empty_value():
    value = None
    with raises(ValidationError) as exception:
        negative_or_zero_value_not_allowed(value)

    assert exception.value.messages == ['invalid_type']


def test_negative_or_zero_value_not_allowed_with_string():
    value = "string"

    with raises(ValidationError) as exception:
        negative_or_zero_value_not_allowed(value)

    assert exception.value.messages == ['invalid_type']


def test_negative_or_zero_value_not_allowed_with_zero():
    value = 0

    with raises(ValidationError) as exception:
        negative_or_zero_value_not_allowed(value)

    assert exception.value.messages == ['negative_or_zero_value_not_allowed']


def test_negative_or_zero_value_not_allowed_with_negative():
    value = -5

    with raises(ValidationError) as exception:
        negative_or_zero_value_not_allowed(value)

    assert exception.value.messages == ['negative_or_zero_value_not_allowed']


def test_negative_or_zero_value_not_allowed_with_positive_integer():
    value = 6

    assert negative_or_zero_value_not_allowed(value) == value


def test_negative_or_zero_value_not_allowed_with_positive_float():
    value = 6.6

    assert negative_or_zero_value_not_allowed(value) == value
