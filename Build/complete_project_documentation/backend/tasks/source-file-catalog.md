# tasks source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## tasks/admin.py
- Type/area: Python module
- Definitions: class TaskAdmin(admin.ModelAdmin):
- Imports (first four): from django.contrib import admin; from .models import Task
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/apps.py
- Type/area: Python module
- Definitions: class TasksConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/tasks.py
- Type/area: Python module
- Definitions: def generate_daily_learning_tasks(self, user_id, count=None, provider=None, model=None):; def generate_daily_learning_tasks_for_all_users():
- Imports (first four): from celery import shared_task; from django.contrib.auth import get_user_model; from tasks.services.daily_generation import DailyTaskGenerationService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from rest_framework.routers import DefaultRouter; from tasks.api.views import TaskViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/api/serializers/tasks_serializers.py
- Type/area: Python API source
- Definitions: class TaskSerializer(serializers.ModelSerializer):; class Meta:; def get_overdue(self, obj):; def validate_actual_minutes(self, value):; def validate_estimated_minutes(self, value):; def validate_sort_order(self, value):; def validate(self, attrs):; def final_value(field):
- Imports (first four): from django.utils import timezone; from rest_framework import serializers; from tasks.models import Task
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .tasks_serializers import TaskSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/api/views/tasks_views.py
- Type/area: Python API source
- Definitions: class TaskPagination(PageNumberPagination):; class TaskViewSet(viewsets.ModelViewSet):; def has_field(self, name):; def invalidate_cache(self):; def get_queryset(self):; def completed_status_values(self):; def _recalculate_goal(self, task):; def perform_create(self, serializer):; def perform_update(self, serializer):; def perform_destroy(self, instance):; def list(self, request, *args, **kwargs):; def today(self, request):; def generate(self, request):; def complete(self, request, pk=None):; def postpone(self, request, pk=None):; def start(self, request, pk=None):; def cancel(self, request, pk=None):; def reopen(self, request, pk=None):; def change_status(self, request, target):; def stats(self, request):; def progress(self, request):; def calendar(self, request):; def overdue(self, request):; def generation_status(self, request, task_id=None):
- Imports (first four): import logging; from datetime import timedelta; from django.core.exceptions import FieldDoesNotExist, ValidationError; from django.db import transaction
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .tasks_views import logger, TaskPagination, TaskViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; import django.utils.timezone; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/migrations/0002_task_milestone.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/models/task.py
- Type/area: Python model source
- Definitions: class Task(models.Model):; class Status(models.TextChoices):; class Priority(models.TextChoices):; class Meta:; def __str__(self):; def mark_completed(self):
- Imports (first four): from django.conf import settings; from django.db import models; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .task import Task
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/services/daily_generation.py
- Type/area: Python service source
- Definitions: class DailyTaskGenerationService:; def __init__(self, user):; def context(self):; def generate(self, count=None, provider=None, model=None):; def _ai_tasks(self, goal, topics, existing, recent, count, provider, model):; def _fallback_tasks(self, goal, topics, count):; def _norm(value):
- Imports (first four): import json; import re; from django.db import transaction; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/services/tasks_services.py
- Type/area: Python service source
- Definitions: class TaskService:; def complete(task, actual_minutes=None):; def postpone(task, until):
- Imports (first four): from datetime import date, datetime; from django.core.exceptions import ValidationError; from django.db import transaction; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/services/__init__.py
- Type/area: Python service source
- Definitions: none matched
- Imports (first four): from .tasks_services import TaskService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/tests/test_tasks.py
- Type/area: Python test source
- Definitions: class TaskIntegrationTests(TestCase):; def setUp(self):; def test_completing_tasks_recalculates_goal_progress_from_real_tasks(self):; def test_task_serializer_rejects_learning_topic_owned_by_another_user(self):
- Imports (first four): from types import SimpleNamespace; from django.test import TestCase; from goals.models import Goal; from goals.services import GoalService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## tasks/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

