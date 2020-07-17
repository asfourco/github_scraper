from .base import BaseRequest
from .logger import LogDecorator


class UserAPI(BaseRequest):
    def __init__(self, access_token=None, username=None):
        self._access_token = access_token
        self._username = username

    @LogDecorator(name="User API")
    def get_users(self, next_url=None, per_page=None):
        params = {}
        if not next_url:
            next_url = f"{self.ROOT_API_URL}/users"
        if per_page:
            params = {"per_page": self.verify_per_page_limit(per_page)}

        return self.execute_request(next_url, params)
