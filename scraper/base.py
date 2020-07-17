"""Base Module to connect to Github API"""

from requests import Request, Session, get
from requests.auth import HTTPBasicAuth
import warnings


class BaseRequest:
    ROOT_API_URL = "https://api.github.com"

    def get_request_limit(self, access_token):
        url = f"{self.ROOT_API_URL}/rate_limit?access_token={access_token}"
        response = get(url)
        data = response.json()
        return data["resources"]["core"].get("remaining")

    def get_default_access_token(self):
        return self.default_access_token

    def get_default_username(self):
        return self.default_username

    def is_authenticated(self):
        return bool(self.get_default_username() and self.get_default_access_token())

    def get_default_headers(self):
        headers = {"Accept": "application/vnd.github.v3+json"}
        return headers

    def _get(self, url, params=None):
        data = {}
        session = Session()
        req = Request("GET", url=url, headers=self.get_default_headers(), params=params)
        prepped = session.prepare_request(req)
        if self.is_authenticated:
            prepped.auth = HTTPBasicAuth(
                self.get_default_username, self.get_default_access_token
            )

        response = session.send(prepped)
        data = {"data": response.json(), "next_url": response.links["next"]["url"]}
        return data

    def check_per_page_limit(self, value):
        limit = 100
        if value > limit:
            warnings.warn(
                f"parameter per_page value exceeds {limit}, the maxium Github API will return"
            )
            value = 100
        return value
