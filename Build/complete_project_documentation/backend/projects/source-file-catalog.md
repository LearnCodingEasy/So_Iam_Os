# projects source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## projects/admin.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from django.contrib import admin
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/apps.py
- Type/area: Python module
- Definitions: class ProjectsConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from rest_framework.routers import DefaultRouter; from projects.api.views import ProjectViewSet, ProjectMemberViewSet, ProjectContextViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/api/serializers/projects_serializers.py
- Type/area: Python API source
- Definitions: class ProjectSerializer(serializers.ModelSerializer):; class Meta: model=Project; fields='__all__'; read_only_fields=['user','created_at','updated_at']; class ProjectMemberSerializer(serializers.ModelSerializer):; class Meta: model=ProjectMember; fields='__all__'; class ProjectContextSerializer(serializers.ModelSerializer):; class Meta: model=ProjectContext; fields='__all__'; read_only_fields=['updated_at']
- Imports (first four): from rest_framework import serializers; from projects.models import Project, ProjectMember, ProjectContext
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .projects_serializers import ProjectSerializer, ProjectMemberSerializer, ProjectContextSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/api/views/projects_views.py
- Type/area: Python API source
- Definitions: class ProjectViewSet(viewsets.ModelViewSet):; def get_queryset(self): return Project.objects.filter(user=self.request.user).prefetch_related('members'); def perform_create(self,s): s.save(user=self.request.user); def context(self,request,pk=None):; class ProjectMemberViewSet(viewsets.ModelViewSet):; def get_queryset(self): return ProjectMember.objects.filter(project__user=self.request.user); class ProjectContextViewSet(viewsets.ReadOnlyModelViewSet):; def get_queryset(self): return ProjectContext.objects.filter(project__user=self.request.user)
- Imports (first four): from rest_framework import viewsets; from rest_framework.decorators import action; from rest_framework.permissions import IsAuthenticated; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .projects_views import ProjectViewSet, ProjectMemberViewSet, ProjectContextViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/models/project.py
- Type/area: Python model source
- Definitions: class Project(models.Model):; class Status(models.TextChoices): PLANNING='planning','Planning'; ACTIVE='active','Active'; PAUSED='paused','Paused'; COMPLETED='completed','Completed'; ARCHIVED='archived','Archived'; class Meta: ordering=['-updated_at']
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/models/project_context.py
- Type/area: Python model source
- Definitions: class ProjectContext(models.Model):
- Imports (first four): from django.db import models; from projects.models.project import Project
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/models/project_goal.py
- Type/area: Python model source
- Definitions: class ProjectGoal(models.Model):; class Meta: constraints=[models.UniqueConstraint(fields=['project','goal'],name='projects_project_goal_unique')]
- Imports (first four): from django.db import models; from projects.models.project import Project
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/models/project_member.py
- Type/area: Python model source
- Definitions: class ProjectMember(models.Model):; class Meta: constraints=[models.UniqueConstraint(fields=['project','user'],name='projects_project_user_unique')]
- Imports (first four): from django.conf import settings; from django.db import models; from projects.models.project import Project
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/models/project_task.py
- Type/area: Python model source
- Definitions: class ProjectTask(models.Model):; class Meta: constraints=[models.UniqueConstraint(fields=['project','task'],name='projects_project_task_unique')]
- Imports (first four): from django.db import models; from projects.models.project import Project
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .project import Project; from .project_member import ProjectMember; from .project_goal import ProjectGoal; from .project_task import ProjectTask
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/tests/test_projects.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): from django.test import TestCase
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## projects/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

