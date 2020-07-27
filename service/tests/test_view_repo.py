import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from service.models import User, Repo
from service.serializers import UserSerializer, RepoSerializer

client = Client()


class GetAllReposTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=1, login="johnnya", type="User", site_admin=False
        )
        Repo.objects.create(
            id=1,
            node_id="abscsd123",
            name="joy",
            owner_id=self.user.id,
            fork=False,
            private=False,
        )
        Repo.objects.create(
            id=10,
            node_id="ASC123ASD",
            name="fizzbuzz",
            owner_id=self.user.id,
            fork=False,
            private=True,
        )

    def test_get_all_repos(self):
        response = client.get(reverse("get_post_repos"))
        repos = Repo.objects.all()
        serialized = RepoSerializer(repos, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleRepoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=1, login="bob", type="User", site_admin=False
        )
        self.repo = Repo.objects.create(
            id=1,
            node_id="ASC123ASD",
            name="fizzbuzz",
            owner_id=self.user.id,
            fork=False,
            private=True,
        )

    def test_get_valid_single_repo(self):
        response = client.get(
            reverse("get_delete_update_repo", kwargs={"pk": self.repo.id})
        )
        repo = Repo.objects.get(pk=self.repo.id)
        serialized = RepoSerializer(repo)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_repo(self):
        response = client.get(reverse("get_delete_update_repo", kwargs={"pk": 300}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewRepoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=10, login="bob", type="User", site_admin=False
        )
        self.valid_payload = json.loads(
            """
        {"id": 128637300, "node_id": "MDEwOlJlcG9zaXRvcnkxMjg2MzczMDA=", "name": "amz", "full_name": "asfourco/amz", "private": false, "owner": 10, "html_url": "https://github.com/asfourco/amz", "description": "Apollo graphql client/server demo", "fork": false, "url": "https://api.github.com/repos/asfourco/amz", "forks_url": "https://api.github.com/repos/asfourco/amz/forks", "keys_url": "https://api.github.com/repos/asfourco/amz/keys{/key_id}", "collaborators_url": "https://api.github.com/repos/asfourco/amz/collaborators{/collaborator}", "teams_url": "https://api.github.com/repos/asfourco/amz/teams", "hooks_url": "https://api.github.com/repos/asfourco/amz/hooks", "issue_events_url": "https://api.github.com/repos/asfourco/amz/issues/events{/number}", "events_url": "https://api.github.com/repos/asfourco/amz/events", "assignees_url": "https://api.github.com/repos/asfourco/amz/assignees{/user}", "branches_url": "https://api.github.com/repos/asfourco/amz/branches{/branch}", "tags_url": "https://api.github.com/repos/asfourco/amz/tags", "blobs_url": "https://api.github.com/repos/asfourco/amz/git/blobs{/sha}", "git_tags_url": "https://api.github.com/repos/asfourco/amz/git/tags{/sha}", "git_refs_url": "https://api.github.com/repos/asfourco/amz/git/refs{/sha}", "trees_url": "https://api.github.com/repos/asfourco/amz/git/trees{/sha}", "statuses_url": "https://api.github.com/repos/asfourco/amz/statuses/{sha}", "languages_url": "https://api.github.com/repos/asfourco/amz/languages", "stargazers_url": "https://api.github.com/repos/asfourco/amz/stargazers", "contributors_url": "https://api.github.com/repos/asfourco/amz/contributors", "subscribers_url": "https://api.github.com/repos/asfourco/amz/subscribers", "subscription_url": "https://api.github.com/repos/asfourco/amz/subscription", "commits_url": "https://api.github.com/repos/asfourco/amz/commits{/sha}", "git_commits_url": "https://api.github.com/repos/asfourco/amz/git/commits{/sha}", "comments_url": "https://api.github.com/repos/asfourco/amz/comments{/number}", "issue_comment_url": "https://api.github.com/repos/asfourco/amz/issues/comments{/number}", "contents_url": "https://api.github.com/repos/asfourco/amz/contents/{+path}", "compare_url": "https://api.github.com/repos/asfourco/amz/compare/{base}...{head}", "merges_url": "https://api.github.com/repos/asfourco/amz/merges", "archive_url": "https://api.github.com/repos/asfourco/amz/{archive_format}{/ref}", "downloads_url": "https://api.github.com/repos/asfourco/amz/downloads", "issues_url": "https://api.github.com/repos/asfourco/amz/issues{/number}", "pulls_url": "https://api.github.com/repos/asfourco/amz/pulls{/number}", "milestones_url": "https://api.github.com/repos/asfourco/amz/milestones{/number}", "notifications_url": "https://api.github.com/repos/asfourco/amz/notifications{?since,all,participating}", "labels_url": "https://api.github.com/repos/asfourco/amz/labels{/name}", "releases_url": "https://api.github.com/repos/asfourco/amz/releases{/id}", "deployments_url": "https://api.github.com/repos/asfourco/amz/deployments", "created_at": "2018-04-08T12:08:46Z", "updated_at": "2020-06-02T20:02:25Z", "pushed_at": "2018-04-11T13:44:30Z", "git_url": "git://github.com/asfourco/amz.git", "ssh_url": "git@github.com:asfourco/amz.git", "clone_url": "https://github.com/asfourco/amz.git", "svn_url": "https://github.com/asfourco/amz", "homepage": "", "size": 497, "stargazers_count": 1, "watchers_count": 1, "language": "JavaScript", "has_issues": true, "has_projects": true, "has_downloads": true, "has_wiki": true, "has_pages": false, "forks_count": 1, "mirror_url": null, "archived": true, "disabled": false, "open_issues_count": 0, "forks": 1, "open_issues": 0, "watchers": 1, "default_branch": "master"}
        """
        )

        self.invalid_payload = {"name": "", "id": 100}

    def test_create_valid_repo(self):
        response = client.post(
            reverse("get_post_repos"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_repo(self):
        response = client.post(
            reverse("get_post_repos"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleRepoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(login="casper", id=100, node_id="abcde12334")
        self.repo = Repo.objects.create(
            id=100, name="foobar", owner_id=self.user.id, private=False, fork=False
        )
        self.valid_payload = json.loads(
            """
        {"id": 100, "node_id": "MDEwOlJlcG9zaXRvcnkxMjg2MzczMDA=", "name": "amz", "full_name": "asfourco/amz", "private": false, "owner": 100, "html_url": "https://github.com/asfourco/amz", "description": "Apollo graphql client/server demo", "fork": false, "url": "https://api.github.com/repos/asfourco/amz", "forks_url": "https://api.github.com/repos/asfourco/amz/forks", "keys_url": "https://api.github.com/repos/asfourco/amz/keys{/key_id}", "collaborators_url": "https://api.github.com/repos/asfourco/amz/collaborators{/collaborator}", "teams_url": "https://api.github.com/repos/asfourco/amz/teams", "hooks_url": "https://api.github.com/repos/asfourco/amz/hooks", "issue_events_url": "https://api.github.com/repos/asfourco/amz/issues/events{/number}", "events_url": "https://api.github.com/repos/asfourco/amz/events", "assignees_url": "https://api.github.com/repos/asfourco/amz/assignees{/user}", "branches_url": "https://api.github.com/repos/asfourco/amz/branches{/branch}", "tags_url": "https://api.github.com/repos/asfourco/amz/tags", "blobs_url": "https://api.github.com/repos/asfourco/amz/git/blobs{/sha}", "git_tags_url": "https://api.github.com/repos/asfourco/amz/git/tags{/sha}", "git_refs_url": "https://api.github.com/repos/asfourco/amz/git/refs{/sha}", "trees_url": "https://api.github.com/repos/asfourco/amz/git/trees{/sha}", "statuses_url": "https://api.github.com/repos/asfourco/amz/statuses/{sha}", "languages_url": "https://api.github.com/repos/asfourco/amz/languages", "stargazers_url": "https://api.github.com/repos/asfourco/amz/stargazers", "contributors_url": "https://api.github.com/repos/asfourco/amz/contributors", "subscribers_url": "https://api.github.com/repos/asfourco/amz/subscribers", "subscription_url": "https://api.github.com/repos/asfourco/amz/subscription", "commits_url": "https://api.github.com/repos/asfourco/amz/commits{/sha}", "git_commits_url": "https://api.github.com/repos/asfourco/amz/git/commits{/sha}", "comments_url": "https://api.github.com/repos/asfourco/amz/comments{/number}", "issue_comment_url": "https://api.github.com/repos/asfourco/amz/issues/comments{/number}", "contents_url": "https://api.github.com/repos/asfourco/amz/contents/{+path}", "compare_url": "https://api.github.com/repos/asfourco/amz/compare/{base}...{head}", "merges_url": "https://api.github.com/repos/asfourco/amz/merges", "archive_url": "https://api.github.com/repos/asfourco/amz/{archive_format}{/ref}", "downloads_url": "https://api.github.com/repos/asfourco/amz/downloads", "issues_url": "https://api.github.com/repos/asfourco/amz/issues{/number}", "pulls_url": "https://api.github.com/repos/asfourco/amz/pulls{/number}", "milestones_url": "https://api.github.com/repos/asfourco/amz/milestones{/number}", "notifications_url": "https://api.github.com/repos/asfourco/amz/notifications{?since,all,participating}", "labels_url": "https://api.github.com/repos/asfourco/amz/labels{/name}", "releases_url": "https://api.github.com/repos/asfourco/amz/releases{/id}", "deployments_url": "https://api.github.com/repos/asfourco/amz/deployments", "created_at": "2018-04-08T12:08:46Z", "updated_at": "2020-06-02T20:02:25Z", "pushed_at": "2018-04-11T13:44:30Z", "git_url": "git://github.com/asfourco/amz.git", "ssh_url": "git@github.com:asfourco/amz.git", "clone_url": "https://github.com/asfourco/amz.git", "svn_url": "https://github.com/asfourco/amz", "homepage": "", "size": 497, "stargazers_count": 1, "watchers_count": 1, "language": "JavaScript", "has_issues": true, "has_projects": true, "has_downloads": true, "has_wiki": true, "has_pages": false, "forks_count": 1, "mirror_url": null, "archived": true, "disabled": false, "open_issues_count": 0, "forks": 1, "open_issues": 0, "watchers": 1, "default_branch": "master"}
        """
        )

        self.invalid_payload = {"login": "", "id": 100, "node_id": "nmjkl123AA"}

    def test_valid_update_repo(self):
        response = client.put(
            reverse("get_delete_update_repo", kwargs={"pk": self.repo.id}),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_repo(self):
        response = client.put(
            reverse("get_delete_update_repo", kwargs={"pk": self.user.id}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleRepoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(login="john", id=99, node_id="abcd1234")
        self.repo = Repo.objects.create(id=10, owner_id=self.user.id, name="jazz")

    def test_valid_delete_repo(self):
        response = client.delete(
            reverse("get_delete_update_repo", kwargs={"pk": self.repo.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_repo(self):
        response = client.delete(reverse("get_delete_update_repo", kwargs={"pk": 300}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetOwnerOfSingleRepoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(login="ronda", id=10, node_id="abds1234")
        self.repo = Repo.objects.create(
            id=1,
            name="funky",
            full_name=f"{self.user.login}/funky",
            owner_id=self.user.id,
            private=False,
            fork=False,
        )

    def test_get_owner_of_repo(self):
        response = client.get(reverse("get_repo_owner", kwargs={"pk": self.repo.id}))
        user = User.objects.get(pk=self.user.id)
        serialized = UserSerializer(user)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
