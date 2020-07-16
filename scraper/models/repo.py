from django.db import models
from .user import User


class Repo(models.Model):
    id = models.IntegerField(primary_key=True)
    node_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    private = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="repos")
    html_url = models.URLField()
    description = models.TextField()
    fork = models.BooleanField()
    url = models.URLField()
    forks_url = models.URLField()
    keys_url = models.URLField()
    collaborators_url = models.URLField()
    teams_url = models.URLField()
    hooks_url = models.URLField()
    issue_events_url = models.URLField()
    events_url = models.URLField()
    assignees_url = models.URLField()
    branches_url = models.URLField()
    tags_url = models.URLField()
    blobs_url = models.URLField()
    git_tags_url = models.URLField()
    git_refs_url = models.URLField()
    trees_url = models.URLField()
    statuses_url = models.URLField()
    languages_url = models.URLField()
    stargazers_url = models.URLField()
    contributors_url = models.URLField()
    subscribers_url = models.URLField()
    subscription_url = models.URLField()
    commits_url = models.URLField()
    git_commits_url = models.URLField()
    comments_url = models.URLField()
    issue_comment_url = models.URLField()
    contents_url = models.URLField()
    compare_url = models.URLField()
    merges_url = models.URLField()
    archive_url = models.URLField()
    downloads_url = models.URLField()
    issues_url = models.URLField()
    pulls_url = models.URLField()
    milestones_url = models.URLField()
    notifications_url = models.URLField()
    labels_url = models.URLField()
    releases_url = models.URLField()
    deployments_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)