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
        self.user_api = UserAPI()

    def test_user_api_is_not_authenticated(self):
        self.assertFalse(self.user_api.is_authenticated())

    def test_request_user_list(self):
        users = self.user_api.get_users(per_page=10)
        self.assertIn("data", users)
        self.assertIn("next_url", users)
        self.assertIsInstance(users["data"], list)
        self.assertEqual(len(users["data"]), 10)


class RepoAPITest(TestCase):
    def setUp(self):
        self.repo_api = RepoAPI()

    def test_repo_api_is_not_authenticated(self):
        self.assertFalse(self.repo_api.is_authenticated())

    def test_request_repo_list(self):
        repos = self.repo_api.get_public_repos()
        self.assertIn("data", repos)
        self.assertIn("next_url", repos)
        self.assertIsInstance(repos["data"], list)

    def test_valid_request_user_repo(self):
        per_page = 2
        repos = self.repo_api.get_repos_of_user(username="asfourco", per_page=per_page)
        self.assertIn("data", repos)
        self.assertIn("next_url", repos)
        self.assertIsInstance(repos["data"], list)
        self.assertEqual(len(repos["data"]), per_page)

    def test_invalid_request_user_repo(self):
        with self.assertRaises(InvalidParameterError):
            self.repo_api.get_repos_of_user(username="asfourco", sort_by="asc")
