from django.test import TestCase
from scraper.models import User, Repo


class userModelTests(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.user = User(
            login=self.username,
            id=1,
            node_id="abcde1233",
            type="User",
            site_admin=False,
        )
        self.user.save()

    def test_read_user(self):
        user = User.objects.get(pk=1)
        self.assertTrue(user)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.login, self.username)
        self.assertEqual(user.type, "User")

    def test_read_user_repo(self):
        name = "testRepo"
        repo = Repo(
            id=1,
            name=name,
            full_name=f"{self.username}/{name}",
            owner_id=self.user.id,
            private=False,
            fork=False,
        )
        repo.save()
        user = User.objects.get(pk=1)
        self.assertTrue(user.repos)
        self.assertEqual(user.repos.count(), 1)
        self.assertEqual(user.repos.first().name, name)

    def test_update_user(self):
        user = User.objects.get(id=1)
        new_node_id = "zxcmnrjlASDj"
        user.node_id = new_node_id
        user.save()
        updated_user = User.objects.get(id=1)
        self.assertTrue(updated_user)
        self.assertEqual(updated_user.node_id, new_node_id)

    def test_delete_user(self):
        User.objects.get(id=1).delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=1)
