from rest_framework import serializers
from service.models import License


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ["id", "key", "node_id", "spdx_id", "name", "url"]
