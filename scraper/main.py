import json
from .user import UserAPI
from service.models import User, Repo, NextUrl, License
from .logger import Log


class ScrapeUserRepos:
    def __init__(self, username=None, access_token=None):
        self.api = UserAPI(username=username, access_token=access_token)
        self.per_page = 10

    def get_or_create_license(self, license_obj):
        if not license_obj:
            return None

        obj, created = License.objects.get_or_create(license_obj)
        return obj.pk

    def transform_repo(self, repo):
        owner = repo.get("owner")
        repo["owner"] = int(owner.get("id"))
        repo["license"] = self.get_or_create_license(repo.get("license"))
        return repo

    def fetch_repos(self, username):
        repos = self.api.get_repos_of_user(username=username, per_page=self.per_page)
        for repo in repos:
            yield self.transform_repo(repo)

    @Log("ScrapeUserRepos")
    def scrape(self):
        next_url = NextUrl.objects.get(NextUrl.Entity.USER)
        users = self.api.get_users(next_url=next_url, per_page=self.per_page)

        for user in users:
            User.objects.update_or_create(user)
            self.process_user_repos(user)

    def process_user_repos(self, user):
        for repo in self.fetch_repos(username=user.get("login")):
            Repo.objects.update_or_create(repo)
