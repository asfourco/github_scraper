from .base import BaseRequest
from .logger import Log


class RepoAPI(BaseRequest):
    def __init__(self, access_token=None, username=None):
        self._access_token = access_token
        self._username = username

    @Log(name="Repo API")
    def get_public_repos(self, next_url=None, since=None):
        params = {}
        if not next_url:
            next_url = f"{self.ROOT_API_URL}/repositories"
        if since:
            params = {"since": int(since)}
        return self.execute_request(next_url, params)
