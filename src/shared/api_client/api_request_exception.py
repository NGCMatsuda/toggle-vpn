from requests import Response


class ApiRequestException(Exception):
    def __init__(self, response: Response):
        super().__init__(
            f'Api request failed: {response.request.url}, code: {response.status_code}, body: {response.text}'
        )

        self.url = response.request.url
        self.status_code = response.status_code
        self.response = response.text


class NotFoundException(ApiRequestException):
    pass
