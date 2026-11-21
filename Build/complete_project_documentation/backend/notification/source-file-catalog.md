# notification source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## notification/admin.py
- Type/area: Python module
- Definitions: class NotificationAdmin(admin.ModelAdmin):
- Imports (first four): from django.contrib import admin; from .models import Notification
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/apps.py
- Type/area: Python module
- Definitions: class NotificationConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from django.urls import include, path; from rest_framework.routers import DefaultRouter; from notification.api.views import NotificationViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/api/serializers/notification_serializers.py
- Type/area: Python API source
- Definitions: class NotificationSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from notification.models import Notification
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .notification_serializers import NotificationSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/api/views/notification_views.py
- Type/area: Python API source
- Definitions: class NotificationViewSet(viewsets.ModelViewSet):; def get_queryset(self):; def read(self, request, pk=None):; def read_all(self, request):; def unread_count(self, request):; def archive(self, request, pk=None):
- Imports (first four): from django.utils import timezone; from rest_framework import status, viewsets; from rest_framework.decorators import action; from rest_framework.permissions import IsAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .notification_views import NotificationViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/models/notification.py
- Type/area: Python model source
- Definitions: class Notification(models.Model):; class Type(models.TextChoices):; class Meta:; def is_read(self):; def mark_read(self):
- Imports (first four): from django.conf import settings; from django.contrib.contenttypes.fields import GenericForeignKey; from django.contrib.contenttypes.models import ContentType; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/models/notification_service.py
- Type/area: Python model source
- Definitions: class NotificationService:; def create(user, *, type=Notification.Type.SYSTEM, title, message, action_url="", priority=50, obj=None, metadata=None):
- Imports (first four): from django.contrib.contenttypes.models import ContentType; from notification.models.notification import Notification
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .notification import Notification; from .notification_service import NotificationService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/tests/test_notification.py
- Type/area: Python test source
- Definitions: class NotificationTests(TestCase):; def test_user_isolation_and_read_flow(self):
- Imports (first four): from django.contrib.auth import get_user_model; from django.test import TestCase; from notification.models import Notification, NotificationService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## notification/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

