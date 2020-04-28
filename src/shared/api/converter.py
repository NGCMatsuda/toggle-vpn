from datetime import datetime

from werkzeug.routing import BaseConverter, ValidationError

DATE_FORMAT = '%Y-%m-%d'


class DateConverter(BaseConverter):
    """Extracts a ISO8601 date from the path and validates it."""

    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        try:
            return to_date(value)
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        return value.strftime(DATE_FORMAT)

def to_date(value):
    return datetime.strptime(value, DATE_FORMAT).date()
