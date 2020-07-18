from rest_framework import serializers
from service.models import NextUrl


class NextUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextUrl
        fields = "__all__"
