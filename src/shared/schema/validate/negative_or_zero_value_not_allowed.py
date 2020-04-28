from decimal import Decimal

from marshmallow import ValidationError


def negative_or_zero_value_not_allowed(value):
    if not isinstance(value, float) and not isinstance(value, int) and not isinstance(value, Decimal):
        raise ValidationError('invalid_type')
    if value <= 0:
        raise ValidationError('negative_or_zero_value_not_allowed')
    return value
