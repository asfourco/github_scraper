class BaseError(Exception):
    def __init__(self, kwargs):
        self.kwargs = kwargs


class InvalidParameterError(BaseError):
    def __str__(self):
        return f"Invalid value for {self.kwargs.get('entity')}"


class InvalidAPIQueryError(BaseError):
    def __str__(self):
        return f"Invalid url: {self.kwargs.get('url')}, status code: {self.kwargs.get('status_code')}"


class InvalidAPIUrlError(BaseError):
    def __str__(self):
        return f"{self.kwargs.get('url')} is not a valid Github API endpoint"
