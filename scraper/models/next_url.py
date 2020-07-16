from django.db import models


class NextUrl(models.Model):
    class Entity(models.TextChoices):
        REPO = "REPO", "repo"
        USER = "USER", "user"

    url = models.URLField()
    entity = models.CharField(max_length=4, choices=Entity.choices, unique=True)
