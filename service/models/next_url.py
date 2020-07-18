from django.db import models
from .user import User
from .repo import Repo


class NextUrl(models.Model):
    """ Hold Next Urls for paginating through a list of users or public repos"""

    class Entity(models.TextChoices):
        REPO = "REPO", "repo"
        USER = "USER", "user"

    url = models.URLField(null=True)
    entity = models.CharField(max_length=4, choices=Entity.choices, unique=True)


class UserRepoNextUrl(models.Model):
    url = models.URLField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
