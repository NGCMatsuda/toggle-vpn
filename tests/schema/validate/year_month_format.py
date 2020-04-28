from marshmallow import ValidationError
from pytest import raises

from shared.schema.validate.year_month_format import year_month_format


def test_year_month_format_correct_format():
    assert year_month_format('201701') == '201701'


def test_year_month_format_error_if_not_string():
    with raises(ValidationError) as exception:
        year_month_format(201792)

    assert exception.value.messages == ['invalid']


def test_year_month_format_error_if_not_digits_in_string():
    with raises(ValidationError) as exception:
        year_month_format('20160A')

    assert exception.value.messages == ['invalid']


def test_year_month_format_error_if_wrong_length():
    with raises(ValidationError) as exception:
        year_month_format('2016011')

    assert exception.value.messages == ['invalid']


def test_year_month_format_error_if_wrong_month_number():
    with raises(ValidationError) as exception:
        year_month_format('201614')

    assert exception.value.messages == ['invalid']
