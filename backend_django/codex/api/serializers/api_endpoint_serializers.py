from rest_framework import serializers
from codex.models import APIEndpoint


class APIEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIEndpoint
        fields = "__all__"
