import re
from marshmallow import ValidationError


def year_month_format(value):
    if not isinstance(value, str):
        raise ValidationError('invalid_type')
    if not re.search("^\d{4}(0[1-9]|1[0-2])$", value):
        raise ValidationError('invalid_format')
    return value
