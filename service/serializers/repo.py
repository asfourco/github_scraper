from rest_framework import serializers
from service.models import Repo


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = "__all__"
