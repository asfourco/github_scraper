from rest_framework import serializers
from scraper.models import NextUrl


class NextUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextUrl
        fields = ["entity", "url"]
