import json
from .user import UserAPI
from service.models import User, Repo, NextUrl, UserRepoNextUrl, License
from service.serializers import UserSerializer, RepoSerializer
from .logger import Log
from .exceptions import UpdateDBRecordError, CreateDBRecordError


class Scraper:
    def __init__(
        self,
        username=None,
        access_token=None,
        per_page=10,
        page=None,
        type=None,
        sort=None,
        direction=None,
        reset=False,
    ):
        self.api = UserAPI(username=username, access_token=access_token)
        self.per_page = per_page
        self.page = page
        self.type = type
        self.sort = sort
        self.direction = direction
        self.reset = reset

    def get_user_next_url(self):
        try:
            next_url = NextUrl.objects.get(entity=NextUrl.Entity.USER)
        except NextUrl.DoesNotExist:
            return None
        else:
            return next_url.url

    def write_user_next_url(self, url):
        obj, create = NextUrl.objects.update_or_create(
            {"entity": NextUrl.Entity.USER, "url": url}
        )
        return obj

    def get_or_create_license(self, license_obj):
        if not license_obj:
            return None

        obj, created = License.objects.get_or_create(license_obj)
        return obj.pk

    def transform_repo(self, repo):
        """ Remove dicts of owner and license and replace with foreign keys """
        repo["owner"] = repo.get("owner", {}).get("id")
        repo["license"] = self.get_or_create_license(repo.get("license"))
        return repo

    def fetch_repos(self, user_id, username):
        repos = self.api.get_repos_of_user(
            username=username,
            per_page=self.per_page,
            page=self.page,
            type=self.type,
            sort=self.sort,
            direction=self.direction,
        )
        # write next_url
        UserRepoNextUrl.objects.update_or_create(
            {"user_id": user_id, "url": repos.get("next_url")}
        )
        for repo in repos.get("data"):
            yield self.transform_repo(repo)

    def scrape(self):
        next_url = None if self.reset else self.get_user_next_url()
        users = self.api.get_users(next_url=next_url, per_page=self.per_page)
        self.write_user_next_url(users.get("next_url"))
        for raw_user in users.get("data"):
            user = self.update_or_create_user(data=raw_user)
            self.process_user_repos(user=user)

    def process_user_repos(self, user):
        for repo in self.fetch_repos(
            user_id=user.get("id"), username=user.get("login")
        ):
            self.update_or_create_repo(data=repo)

    ####
    # Workarounds for model.objects.update_or_create
    # reason: Models cannot find unique records when called
    ####

    def update_or_create_repo(self, data):
        pk = data.get("id")
        try:
            repo = Repo.objects.get(id=pk)
        except Repo.DoesNotExist:
            serialized_repo = RepoSerializer(data=data)
            if serialized_repo.is_valid():
                serialized_repo.save()
                return serialized_repo.data
            else:
                raise CreateDBRecordError(
                    {"entity": Repo.__name__, "error": serialized_repo.errors}
                )
        else:
            serialized_repo = RepoSerializer(repo, data=data)
            if serialized_repo.is_valid():
                serialized_repo.save()
                return serialized_repo.data
            else:
                raise UpdateDBRecordError(
                    {"entity": Repo.__name__, "error": serialized_repo.errors}
                )

    def update_or_create_user(self, data):
        pk = data.get("id")
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            serialized_user = UserSerializer(data=data)
            if serialized_user.is_valid():
                serialized_user.save()
                return serialized_user.data
            else:
                raise CreateDBRecordError(
                    {"entity": User.__name__, "error": serialized_user.errors}
                )
        else:
            serialized_user = UserSerializer(user, data=data)
            if serialized_user.is_valid():
                serialized_user.save()
                return serialized_user.data
            else:
                raise UpdateDBRecordError(
                    {"entity": User.__name__, "error": serialized_user.errors}
                )
