from rest_framework import serializers
from .models import ProjectRegistry,Feature,FileRegistry,APIEndpoint,ProtectedFeature,ChangeSet,ProjectSnapshot

class ProjectSerializer(serializers.ModelSerializer):
    class Meta: model=ProjectRegistry; fields="__all__"
class FeatureSerializer(serializers.ModelSerializer):
    class Meta: model=Feature; fields="__all__"
class FileSerializer(serializers.ModelSerializer):
    class Meta: model=FileRegistry; fields="__all__"
class APIEndpointSerializer(serializers.ModelSerializer):
    class Meta: model=APIEndpoint; fields="__all__"
class ProtectedFeatureSerializer(serializers.ModelSerializer):
    class Meta: model=ProtectedFeature; fields="__all__"
class ChangeSetSerializer(serializers.ModelSerializer):
    class Meta: model=ChangeSet; fields="__all__"; read_only_fields=["created_by"]
class SnapshotSerializer(serializers.ModelSerializer):
    class Meta: model=ProjectSnapshot; fields="__all__"; read_only_fields=["created_by"]
