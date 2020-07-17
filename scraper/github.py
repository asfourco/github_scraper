from .base import BaseRequest


class GithubAPI(BaseRequest):
    def __init__(self, access_token=None, username=None):
        self.default_access_token = access_token
        self.default_username = username

    def get_users(self, next_url=None, per_page=None):
        params = {}
        if not next_url:
            next_url = f"{self.ROOT_API_URL}/users"
        if per_page:
            params = {"per_page": self.check_per_page_limit(per_page)}

        return self._get(next_url, params)

    def get_repos(self, next_url=None, per_page=None):
        params = {}
        if not next_url:
            next_url = f"{self.ROOT_API_URL}/repositories"
        if per_page:
            params = {"per_page": self.check_per_page_limit(per_page)}

        return self._get(next_url, params)
