import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from service.models import User, Repo
from service.serializers import UserSerializer, RepoSerializer

client = Client()


class GetAllUsersTest(TestCase):
    def setUp(self):
        User.objects.create(id=1, login="johnnya", type="User", site_admin=False)
        User.objects.create(id=2, login="foobar", type="User", site_admin=False)
        User.objects.create(id=3, login="fizzbuzz", type="User", site_admin=True)

    def test_get_all_users(self):
        response = client.get(reverse("get_post_users"))
        users = User.objects.all()
        serialized = UserSerializer(users, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=1, login="bob", type="User", site_admin=False
        )

    def test_get_valid_single_user(self):
        response = client.get(
            reverse("get_delete_update_user", kwargs={"pk": self.user.id})
        )
        user = User.objects.get(pk=self.user.id)
        serialized = UserSerializer(user)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_user(self):
        response = client.get(reverse("get_delete_update_user", kwargs={"pk": 300}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewUserTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            "login": "nitay",
            "id": 34,
            "node_id": "MDQ6VXNlcjM0",
            "avatar_url": "https://avatars2.githubusercontent.com/u/34?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/nitay",
            "html_url": "https://github.com/nitay",
            "followers_url": "https://api.github.com/users/nitay/followers",
            "following_url": "https://api.github.com/users/nitay/following{/other_user}",
            "gists_url": "https://api.github.com/users/nitay/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/nitay/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/nitay/subscriptions",
            "organizations_url": "https://api.github.com/users/nitay/orgs",
            "repos_url": "https://api.github.com/users/nitay/repos",
            "events_url": "https://api.github.com/users/nitay/events{/privacy}",
            "received_events_url": "https://api.github.com/users/nitay/received_events",
            "type": "User",
            "site_admin": False,
        }

        self.invalid_payload = {"login": "", "id": 100}

    def test_create_valid_user(self):
        response = client.post(
            reverse("get_post_users"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = client.post(
            reverse("get_post_users"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(login="casper", id=100, node_id="abcde12334")
        self.valid_payload = {
            "login": "casper",
            "id": 100,
            "node_id": "abcde12334",
            "avatar_url": "https://avatars2.githubusercontent.com/u/100?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/casper",
            "html_url": "https://github.com/casper",
            "followers_url": "https://api.github.com/users/casper/followers",
            "following_url": "https://api.github.com/users/casper/following{/other_user}",
            "gists_url": "https://api.github.com/users/casper/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/casper/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/casper/subscriptions",
            "organizations_url": "https://api.github.com/users/casper/orgs",
            "repos_url": "https://api.github.com/users/casper/repos",
            "events_url": "https://api.github.com/users/casper/events{/privacy}",
            "received_events_url": "https://api.github.com/users/casper/received_events",
            "type": "User",
            "site_admin": False,
        }
        self.invalid_payload = {"login": "", "id": 100, "node_id": "nmjkl123AA"}

    def test_valid_update_user(self):
        response = client.put(
            reverse("get_delete_update_user", kwargs={"pk": self.user.id}),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_user(self):
        response = client.put(
            reverse("get_delete_update_user", kwargs={"pk": self.user.id}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(login="john", id=99, node_id="abcd1234")

    def test_valid_delete_user(self):
        response = client.delete(
            reverse("get_delete_update_user", kwargs={"pk": self.user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_user(self):
        response = client.delete(reverse("get_delete_update_user", kwargs={"pk": 300}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetReposOfSingleUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(login="ronda", id=10, node_id="abds1234")
        Repo.objects.create(
            id=1,
            name="funky",
            full_name=f"{self.user.login}/funky",
            owner_id=self.user.id,
            private=False,
            fork=False,
        )

    def test_get_repo_of_user(self):
        response = client.get(reverse("get_repos_of_user", kwargs={"pk": self.user.id}))
        user = User.objects.get(pk=self.user.id)
        serialized = RepoSerializer(user.repo_set, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
