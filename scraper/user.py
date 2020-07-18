from .base import BaseRequest
from .logger import Log


class UserAPI(BaseRequest):
    def __init__(self, access_token=None, username=None):
        self._access_token = access_token
        self._username = username

    @Log(name="User API")
    def get_users(self, next_url=None, per_page=None):
        params = {}
        if not next_url:
            next_url = f"{self.ROOT_API_URL}/users"
        if per_page:
            params = {"per_page": self.verify_per_page_limit(per_page)}

        return self.execute_request(next_url, params)

    @Log(name="User API")
    def get_repos_of_user(
        self, username, per_page=None, page=None, type=None, sort=None, direction=None,
    ):
        url = f"{self.ROOT_API_URL}/users/{username.lower()}/repos"
        params = {}
        if per_page:
            params["per_page"] = self.verify_per_page_limit(per_page)
        if page:
            params["page"] = page
        if type:
            params["type"] = self.verify_type(type)
        if sort:
            params["sort"] = self.verify_sort(sort)
        if direction:
            params["direction"] = self.verify_direction(direction)
        return self.execute_request(url, params)

    @Log(name="User API")
    def get_user(self, username):
        url = f"{self.ROOT_API_URL}/users/{username.lower()}"
        response = self.execute_request(url)
        return response.get("data")
