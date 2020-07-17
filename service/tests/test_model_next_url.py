from django.test import TestCase
from django.db import IntegrityError
from service.models import NextUrl


class nextUrlModelTests(TestCase):
    def setUp(self):
        self.repo_link = "https://api.github.com/repositories?since=369"
        self.repo_next_url = NextUrl(entity=NextUrl.Entity.REPO, url=self.repo_link)
        self.repo_next_url.save()
        self.user_link = "https://api.github.com/users?since=46"
        self.user_next_url = NextUrl(entity=NextUrl.Entity.USER, url=self.user_link)
        self.user_next_url.save()

    def test_read_repo_next_url(self):
        next_url = NextUrl.objects.filter(entity=NextUrl.Entity.REPO)
        self.assertEqual(next_url.count(), 1)
        self.assertEqual(next_url.first().url, self.repo_link)
        self.assertNotEqual(next_url.first().url, self.user_link)

    def test_cannot_add_repo_next_url(self):
        new_url = NextUrl(
            entity=NextUrl.Entity.REPO,
            url="https://api.github.com/repositories?since=1000",
        )
        with self.assertRaises(IntegrityError):
            new_url.save()
