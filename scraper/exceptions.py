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


class APIRateLimitError(BaseError):
    def __str__(self):
        return f"GitHub API rate limit was reached. API limit: {self.kwargs.get('limit')} - remaining: {self.kwargs.get('remaining')}. Limiter reset in {self.kwargs.get('reset')}"


class UpdateDBRecordError(BaseError):
    def __str__(self):
        return f"{self.kwargs.get('entity')} failed to update, error: {self.kwargs.get('error')}"


class CreateDBRecordError(BaseError):
    def __str__(self):
        return f"Failed to create a new record for {self.kwargs.get('entity')}, error: {self.kwargs.get('error')}"
