class ServiceException(Exception):
    def __init__(self, message, messages):
        super().__init__(message)
        self.data = dict(messages=messages)


class TenantAuthorizationException(Exception):
    pass


class RequestValidationException(Exception):
    def __init__(self, message, messages):
        super().__init__(message)
        self.data = dict(messages=messages)


class BadRequestException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
