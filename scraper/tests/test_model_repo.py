from django.test import TestCase
from scraper.models import Repo, User


class RepoModelTests(TestCase):
    def setUp(self):
        # setup test user
        self.username = "testUser"
        self.user = User.objects.create(id=1, login=self.username, site_admin=False)
        # setup test repo
        self.name = "testRepo"
        self.repo = Repo.objects.create(
            id=1,
            name=self.name,
            full_name=f"{self.username}/{self.name}",
            owner_id=self.user.id,
            private=False,
            fork=False,
        )

    def test_read_repo(self):
        repo = Repo.objects.get(pk=1)
        self.assertTrue(repo)
        self.assertEqual(repo.id, 1)
        self.assertEqual(repo.name, self.name)

    def test_can_fetch_owner_repo(self):
        repo = Repo.objects.get(pk=1)
        self.assertTrue(repo)
        self.assertTrue(repo.owner)
        self.assertEqual(repo.owner.login, self.username)

    def test_update_repo(self):
        repo = Repo.objects.get(pk=1)
        repo.fork = True
        new_node_id = "abcde12345"
        repo.node_id = new_node_id
        repo.save()
        updated_repo = Repo.objects.get(pk=1)
        self.assertTrue(updated_repo)
        self.assertTrue(updated_repo.fork)
        self.assertEqual(updated_repo.node_id, new_node_id)

    def test_delete_repo(self):
        Repo.objects.get(pk=1).delete()
        with self.assertRaises(Repo.DoesNotExist):
            Repo.objects.get(pk=1)
