import decimal

import simplejson
from marshmallow import fields, Schema, EXCLUDE

from shared.schema.field import Enum

default_error_messages = dict(
    required='required',
    null='required',
    invalid='invalid',
    too_large='too_long',
    by_name='invalid',  # for Enum
    by_value='invalid',  # for Enum
    must_be_string='invalid',  # for Enum,
    format='invalid'  # for Date
)

fields.Integer.default_error_messages = default_error_messages
fields.Decimal.default_error_messages = default_error_messages
fields.String.default_error_messages = default_error_messages
fields.Date.default_error_messages = default_error_messages
fields.Nested.default_error_messages = default_error_messages
fields.List.default_error_messages = default_error_messages
Enum.default_error_messages = default_error_messages


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        render_module = simplejson
        render_module_opts = dict(
            parse_float=decimal.Decimal
        )
