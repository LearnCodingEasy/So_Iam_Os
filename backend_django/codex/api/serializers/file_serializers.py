from rest_framework import serializers
from codex.models import FileRegistry


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileRegistry
        fields = "__all__"
