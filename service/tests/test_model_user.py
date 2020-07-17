from django.test import TestCase
from service.models import User, Repo


class UserModelTests(TestCase):
    def setUp(self):
        self.username = "testuser"
        User.objects.create(
            login=self.username,
            id=1,
            node_id="abcde1233",
            type="User",
            site_admin=False,
        )

    def test_read_user(self):
        user = User.objects.get(pk=1)
        self.assertTrue(user)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.login, self.username)
        self.assertEqual(user.type, "User")

    def test_read_user_repo(self):
        name = "testRepo"
        Repo.objects.create(
            id=1,
            name=name,
            full_name=f"{self.username}/{name}",
            owner_id=1,
            private=False,
            fork=False,
        )
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
