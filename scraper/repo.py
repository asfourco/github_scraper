from .base import BaseRequest
from .exceptions import InvalidParameterError
from .logger import LogDecorator


class RepoAPI(BaseRequest):
    def __init__(self, access_token=None, username=None):
        self._access_token = access_token
        self._username = username

    @LogDecorator(name="Repo API")
    def get_public_repos(self, next_url=None, since=None):
        params = {}
        if not next_url:
            next_url = f"{self.ROOT_API_URL}/repositories"
        if since:
            params = {"since": int(since)}
        return self.execute_request(next_url, params)

    @LogDecorator(name="Repo API")
    def get_repos_of_user(
        self,
        username,
        per_page=None,
        page=None,
        repo_user_type="all",
        sort_by=None,
        direction=None,
    ):
        url = f"{self.ROOT_API_URL}/users/{username}/repos"
        params = {}
        if per_page:
            params["per_page"] = self.verify_per_page_limit(per_page)
        if page:
            params["page"] = page
        if repo_user_type:
            params["type"] = self.verify_type(repo_user_type)
        if sort_by:
            params["sort"] = self.verify_sort(sort_by)
        if direction:
            params["direction"] = self.verify_direction(direction)
        return self.execute_request(url, params)

    def verify_type(self, value):
        valid_values = ["all", "member", "owner"]
        return self._verify(value, valid_values, "Repository user type")

    def verify_sort(self, value):
        valid_values = ["created", "updated", "pushed", "full_name"]
        return self._verify(value, valid_values, "Sort")

    def verify_direction(self, value):
        valid_values = ["asc", "desc"]
        return self._verify(value, valid_values, "Direction")

    def _verify(self, value, valid_values, entity):
        if value.lower() in valid_values:
            return value.lower()
        else:
            raise InvalidParameterError({"entity": entity})
