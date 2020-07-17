from unittest import TestCase
from scraper.base import BaseRequest
from scraper import UserAPI, RepoAPI
from scraper.exceptions import InvalidParameterError, InvalidAPIUrlError


class BaseRequestTest(TestCase):
    def setUp(self):
        self.base_request = BaseRequest()
        self.base_request._username = None
        self.base_request._access_token = None

    def test_verify_valid_page_limit(self):
        per_page = 50
        new_per_page = self.base_request.verify_per_page_limit(per_page)
        self.assertEqual(new_per_page, per_page)

    def test_verify_invalid_page_limit(self):
        per_page = 500
        with self.assertWarns(Warning):
            new_per_page = self.base_request.verify_per_page_limit(per_page)
            self.assertEqual(new_per_page, self.base_request.PER_PAGE_LIMIT)

    def test_valid_execute_request(self):
        url = f"{self.base_request.ROOT_API_URL}"
        response = self.base_request.execute_request(url)
        self.assertEqual(response["status_code"], 200)

    def test_invalid_execute_request(self):
        url = f"{self.base_request.ROOT_API_URL}/foobar"
        with self.assertRaises(InvalidAPIUrlError):
            self.base_request.execute_request(url)


class UserAPITest(TestCase):
    def setUp(self):
        self.api = UserAPI()

    def test_user_api_is_not_authenticated(self):
        self.assertFalse(self.api.is_authenticated())

    def test_request_user_list(self):
        users = self.api.get_users(per_page=10)
        self.assertIn("data", users)
        self.assertIn("next_url", users)
        self.assertIsInstance(users["data"], list)
        self.assertEqual(len(users["data"]), 10)

    def test_valid_request_user_repo(self):
        per_page = 2
        repos = self.api.get_repos_of_user(username="asfourco", per_page=per_page)
        self.assertIn("data", repos)
        self.assertIn("next_url", repos)
        self.assertIsInstance(repos["data"], list)
        self.assertEqual(len(repos["data"]), per_page)

    def test_valid_request_without_next_user_repo(self):
        per_page = 100
        repos = self.api.get_repos_of_user(username="asfourco", per_page=per_page)
        self.assertIn("data", repos)
        self.assertIn("next_url", repos)
        self.assertIsInstance(repos["data"], list)
        self.assertLess(len(repos["data"]), per_page)
        self.assertFalse(repos.get("next_url"))

    def test_invalid_sort_request_user_repo(self):
        with self.assertRaises(InvalidParameterError):
            self.api.get_repos_of_user(username="asfourco", sort="asc")

    def test_invalid_type_request_user_repo(self):
        with self.assertRaises(InvalidParameterError):
            self.api.get_repos_of_user(username="asfourco", type="asc")

    def test_invalid_direction_request_user_repo(self):
        with self.assertRaises(InvalidParameterError):
            self.api.get_repos_of_user(username="asfourco", direction="up_and_away")


class RepoAPITest(TestCase):
    def setUp(self):
        self.api = RepoAPI()

    def test_repo_api_is_not_authenticated(self):
        self.assertFalse(self.api.is_authenticated())

    def test_request_repo_list(self):
        repos = self.api.get_public_repos()
        self.assertIn("data", repos)
        self.assertIn("next_url", repos)
        self.assertIsInstance(repos["data"], list)
