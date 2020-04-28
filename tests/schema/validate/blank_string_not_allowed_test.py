from marshmallow import ValidationError
from pytest import raises

from shared.schema.validate.blank_string_not_allowed import blank_string_not_allowed


def test_valid_string_contains_non_whitespace_characters():
    assert blank_string_not_allowed('not a blank string') == 'not a blank string'


def test_non_string_value_is_invalid():
    with raises(ValidationError) as exception:
        blank_string_not_allowed(123)

    assert exception.value.messages == ['invalid_type']


def test_empty_string_value_is_invalid():
    with raises(ValidationError) as exception:
        blank_string_not_allowed('')

    assert exception.value.messages == ['blank_not_allowed']


def test_blank_string_value_is_invalid():
    with raises(ValidationError) as exception:
        blank_string_not_allowed('  \t \n \r  ')

    assert exception.value.messages == ['blank_not_allowed']
