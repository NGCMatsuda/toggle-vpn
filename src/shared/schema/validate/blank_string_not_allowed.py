from marshmallow import ValidationError


def blank_string_not_allowed(value):
    if not isinstance(value, str):
        raise ValidationError('invalid_type')
    if value.strip() == '':
        raise ValidationError('blank_not_allowed')
    return value
