from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=200)
    node_id = models.CharField(max_length=200)
    avatar_url = models.URLField()
    gravatar_id = models.CharField(max_length=200)
    url = models.URLField()
    html_url = models.URLField()
    followers_url = models.URLField()
    following_url = models.URLField()
    gists_url = models.URLField()
    starred_url = models.URLField()
    subscriptions_url = models.URLField()
    organizations_url = models.URLField()
    repos_url = models.URLField()
    events_url = models.URLField()
    received_events_url = models.URLField()
    type = models.CharField(max_length=200)
    site_admin = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
