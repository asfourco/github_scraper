"""Base Module to connect to Github API"""

import warnings
import time
from requests import Request, Session, get, codes
from requests.auth import HTTPBasicAuth
from .exceptions import (
    InvalidAPIUrlError,
    InvalidAPIQueryError,
    InvalidParameterError,
    APIRateLimitError,
)


class BaseRequest:
    ROOT_API_URL = "https://api.github.com"
    PER_PAGE_LIMIT = 100

    def get_request_limit(self):
        url = f"{self.ROOT_API_URL}/rate_limit"
        data = self.execute_request(url)
        return data["data"]

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
            if response.status_code == codes.not_found:
                raise InvalidAPIUrlError({"url": response.url})
            remaining = int(response.headers["X-RateLimit-Remaining"])
            if response.status_code == codes.forbidden and remaining == 0:
                raise APIRateLimitError(
                    {
                        "limit": response.headers["X-RateLimit-Limit"],
                        "remaining": response.headers["X-RateLimit-Remaining"],
                    }
                )
            if response.status_code != codes.ok:
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
