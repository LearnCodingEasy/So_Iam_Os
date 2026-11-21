# core source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## core/admin.py
- Type/area: Python module
- Definitions: class UserLearningSettingsAdmin(admin.ModelAdmin):
- Imports (first four): from django.contrib import admin; from .models import UserLearningSettings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/apps.py
- Type/area: Python module
- Definitions: class CoreConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/cache_utils.py
- Type/area: Python module
- Definitions: def invalidate_dashboard(user_id):
- Imports (first four): from django.core.cache import cache
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/constants.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/exceptions.py
- Type/area: Python module
- Definitions: class CoreAPIException(APIException):; class ResourceNotFoundException(CoreAPIException):; class InvalidOperationException(CoreAPIException):
- Imports (first four): from rest_framework.exceptions import APIException
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/managers.py
- Type/area: Python module
- Definitions: class ActiveManager(models.Manager):; def get_queryset(self):
- Imports (first four): from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/pagination.py
- Type/area: Python module
- Definitions: class CorePagination(PageNumberPagination):
- Imports (first four): from rest_framework.pagination import PageNumberPagination; from .constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/permissions.py
- Type/area: Python module
- Definitions: class IsAuthenticatedUser(BasePermission):; def has_permission(self, request, view):
- Imports (first four): from rest_framework.permissions import BasePermission
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/signals.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/utils.py
- Type/area: Python module
- Definitions: def generate_uuid():; def generate_uuid_string():; def is_valid_uuid(value):
- Imports (first four): import uuid
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from django.urls import path; from core.api.views import CoreHealthView, DashboardView, UserLearningSettingsView
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/api/serializers/core_serializers.py
- Type/area: Python API source
- Definitions: class UserLearningSettingsSerializer(serializers.ModelSerializer):; class Meta:; def validate_daily_learning_tasks(self, value):; def validate_current_learning_goal(self, value):; def get_current_learning_goal_detail(self, obj):
- Imports (first four): from rest_framework import serializers; from core.models import UserLearningSettings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .core_serializers import UserLearningSettingsSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/api/views/core_views.py
- Type/area: Python API source
- Definitions: class CoreHealthView(APIView):; def get(self, request):; class DashboardView(APIView):; def get(self, request):; class UserLearningSettingsView(APIView):; def get_object(self, request):; def get(self, request):; def patch(self, request):
- Imports (first four): from rest_framework.permissions import AllowAny, IsAuthenticated; from rest_framework.response import Response; from rest_framework.views import APIView; from core.constants import API_SUCCESS, APP_NAME, APP_VERSION
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .core_views import CoreHealthView, DashboardView, UserLearningSettingsView
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/debug_console/consumers.py
- Type/area: Python module
- Definitions: class DebugConsoleConsumer(AsyncWebsocketConsumer):; async def connect(self):; async def disconnect(self, close_code):; async def send_log(self, event):
- Imports (first four): import json; from urllib.parse import urlparse; from django.conf import settings; from channels.generic.websocket import AsyncWebsocketConsumer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/debug_console/handlers.py
- Type/area: Python module
- Definitions: class WebSocketLogHandler(logging.Handler):; def emit(self, record):; def get_level(level_name):
- Imports (first four): from channels.layers import get_channel_layer; from asgiref.sync import async_to_sync; import logging; import asyncio
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/debug_console/routing.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from django.urls import re_path; from .consumers import DebugConsoleConsumer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/debug_console/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/models/base_model.py
- Type/area: Python model source
- Definitions: class BaseModel(models.Model):; class Meta:; def __str__(self):
- Imports (first four): import uuid; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/models/user_learning_settings.py
- Type/area: Python model source
- Definitions: class UserLearningSettings(models.Model):; class Meta:; def clean(self):
- Imports (first four): from django.conf import settings; from django.db import models; from django.core.exceptions import ValidationError
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .base_model import BaseModel; from .user_learning_settings import UserLearningSettings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/services/core_services.py
- Type/area: Python service source
- Definitions: class BaseService:; def save(instance):; def delete(instance):; class DashboardService:; def get_data(*, user):
- Imports (first four): from django.core.cache import cache; from django.db import transaction; from django.db.models import Avg, Count, Q; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/services/__init__.py
- Type/area: Python service source
- Definitions: none matched
- Imports (first four): from .core_services import DASHBOARD_CACHE_TTL, BaseService, DashboardService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/tests/tests_learning_settings.py
- Type/area: Python test source
- Definitions: class LearningSettingsAPITests(APITestCase):; def setUp(self):; def test_learning_settings_persist(self):
- Imports (first four): from django.contrib.auth import get_user_model; from rest_framework.test import APITestCase; from learning.models import LearningGoal, LearningPath, LearningTopic, Skill; from core.models import UserLearningSettings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/tests/test_api_contract.py
- Type/area: Python test source
- Definitions: class ApiContractRoutingTests(SimpleTestCase):; def assert_route(self, path, expected_url_name=None):; def test_learning_topic_actions(self):; def test_learning_path_actions(self):; def test_learning_session_finish(self):; def test_assessment_actions(self):; def test_goal_and_task_actions(self):; def test_knowledge_actions(self):; def test_notification_routes(self):; def test_social_routes(self):; def test_jobs_routes(self):
- Imports (first four): from django.test import SimpleTestCase; from django.urls import resolve
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/tests/test_core.py
- Type/area: Python test source
- Definitions: class DashboardTests(APITestCase):; def test_dashboard_is_database_driven(self):; def test_dashboard_cache_is_isolated_per_user(self):
- Imports (first four): from django.contrib.auth import get_user_model; from rest_framework.test import APITestCase; from rest_framework_simplejwt.tokens import RefreshToken; from goals.models import Goal
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## core/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

