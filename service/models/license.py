from django.db import models


class License(models.Model):
    key = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    spdx_id = models.CharField(max_length=200)
    url = models.URLField(null=True)
    node_id = models.CharField(max_length=200)
