"""Base Module to connect to Github API"""

from requests import Request, Session, get
from requests.auth import HTTPBasicAuth
import warnings
from .logger import LogDecorator
from .exceptions import InvalidAPIUrlError, InvalidAPIQueryError


class BaseRequest:
    ROOT_API_URL = "https://api.github.com"
    PER_PAGE_LIMIT = 100

    @property
    def username(self):
        return self._username

    @property
    def access_token(self):
        return self._access_token

    def is_authenticated(self):
        return bool(self.username and self.access_token)

    @property
    def default_headers(self):
        headers = {"Accept": "application/vnd.github.v3+json"}
        return headers

    def get_http_auth(self):
        return HTTPBasicAuth(self._username, self._access_token)

    @LogDecorator(name="BaseRequest")
    def execute_request(self, url, params=None):
        data = {}
        session = Session()
        request = Request("GET", url=url, headers=self.default_headers, params=params)
        prepped = session.prepare_request(request)
        if self.is_authenticated():
            prepped.auth = self.get_http_auth()
        try:
            response = session.send(prepped)
        except Exception as e:
            raise e
        else:
            if response.status_code == 404:
                raise InvalidAPIUrlError({"url": response.url})
            if response.status_code != 200:
                raise InvalidAPIQueryError(
                    {"url": response.url, "code": response.status_code}
                )
            data = {
                "status_code": int(response.status_code),
                "data": response.json(),
                "next_url": response.links.get("next", {}).get("url"),
            }
        return data

    def verify_per_page_limit(self, value):
        if value > self.PER_PAGE_LIMIT:
            warnings.warn(
                f"parameter per_page value exceeds {self.PER_PAGE_LIMIT}, the maxium Github API will return"
            )
            value = self.PER_PAGE_LIMIT
        return value
