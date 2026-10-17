from rest_framework import serializers
from .models import Project,ProjectMember,ProjectGoal,ProjectTask,ProjectContext
class ProjectSerializer(serializers.ModelSerializer):
    class Meta: model=Project; fields='__all__'; read_only_fields=['user','created_at','updated_at']
class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta: model=ProjectMember; fields='__all__'
class ProjectContextSerializer(serializers.ModelSerializer):
    class Meta: model=ProjectContext; fields='__all__'; read_only_fields=['updated_at']
