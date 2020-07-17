import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from service.models import NextUrl
from service.serializers import NextUrlSerializer

client = Client()


class GetAllNextUrlsTest(TestCase):
    def setUp(self):
        NextUrl.objects.create(
            entity=NextUrl.Entity.REPO,
            url="https://api.github.com/repositories?since=100",
        )
        NextUrl.objects.create(
            entity=NextUrl.Entity.USER, url="https://api.github.com/users?since=100"
        )

    def test_get_all_links(self):
        response = client.get(reverse("get_post_next_links"))
        links = NextUrl.objects.all()
        serialized = NextUrlSerializer(links, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleNextUrlTest(TestCase):
    def setUp(self):
        NextUrl.objects.create(
            entity=NextUrl.Entity.REPO,
            url="https://api.github.com/repositories?since=100",
        )
        NextUrl.objects.create(
            entity=NextUrl.Entity.USER, url="https://api.github.com/users?since=100"
        )

    def test_get_valid_single_repo_next_link(self):
        response = client.get(
            reverse("get_delete_update_next_link", kwargs={"entity": "REPO"})
        )
        link = NextUrl.objects.get(entity="REPO")
        serialized = NextUrlSerializer(link)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_user_next_link(self):
        response = client.get(
            reverse("get_delete_update_next_link", kwargs={"entity": "USER"})
        )
        link = NextUrl.objects.get(entity="USER")
        serialized = NextUrlSerializer(link)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_next_link(self):
        response = client.get(
            reverse("get_delete_update_next_link", kwargs={"entity": "FOOBAR"})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateNewNextUrlTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            "url": "https://api.github.com/repositories?since=100",
            "entity": "REPO",
        }

        self.invalid_payload = {"url": "", "entity": "REPO"}

    def test_create_valid_next_link(self):
        response = client.post(
            reverse("get_post_next_links"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_next_link(self):
        response = client.post(
            reverse("get_post_next_links"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleNextUrlTest(TestCase):
    def setUp(self):
        self.next_url = NextUrl.objects.create(
            entity=NextUrl.Entity.REPO,
            url="https://api.github.com/repositories?since=100",
        )

        self.valid_payload = {
            "url": "https://api.github.com/repositories?since=130",
            "entity": "REPO",
        }
        self.invalid_payload = {
            "url": "https://api.github.com/repositories?since=130",
            "entity": "",
        }

    def test_valid_update_next_link(self):
        response = client.put(
            reverse(
                "get_delete_update_next_link", kwargs={"entity": self.next_url.entity}
            ),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_next_link(self):
        response = client.put(
            reverse(
                "get_delete_update_next_link", kwargs={"entity": self.next_url.entity}
            ),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleNextLinkTest(TestCase):
    def setUp(self):
        self.next_url = NextUrl.objects.create(
            entity=NextUrl.Entity.REPO,
            url="https://api.github.com/repositories?since=100",
        )

    def test_valid_delete_next_link(self):
        response = client.delete(
            reverse(
                "get_delete_update_next_link", kwargs={"entity": self.next_url.entity}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_next_link(self):
        NextUrl.objects.get(entity="REPO").delete()
        response = client.delete(
            reverse("get_delete_update_next_link", kwargs={"entity": "REPO"})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
