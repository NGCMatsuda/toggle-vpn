from marshmallow import ValidationError


def empty_array_not_allowed(value):
    if not isinstance(value, list):
        raise ValidationError('invalid_type')
    if len(value) == 0:
        raise ValidationError('empty_array_not_allowed')
    return value
