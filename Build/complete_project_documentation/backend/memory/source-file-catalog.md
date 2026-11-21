# memory source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## memory/admin.py
- Type/area: Python module
- Definitions: class MemoryItemAdmin(admin.ModelAdmin):
- Imports (first four): from django.contrib import admin; from .models import MemoryItem
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/apps.py
- Type/area: Python module
- Definitions: class MemoryConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from rest_framework.routers import DefaultRouter; from memory.api.views import MemoryItemViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/api/serializers/memory_serializers.py
- Type/area: Python API source
- Definitions: class MemoryItemSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from memory.models import MemoryItem
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .memory_serializers import MemoryItemSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/api/views/memory_views.py
- Type/area: Python API source
- Definitions: class MemoryItemViewSet(viewsets.ModelViewSet):; def get_queryset(self): return MemoryItem.objects.filter(user=self.request.user); def perform_create(self,serializer): serializer.save(user=self.request.user)
- Imports (first four): from rest_framework import viewsets; from rest_framework.permissions import IsAuthenticated; from memory.models import MemoryItem; from memory.api.serializers import MemoryItemSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .memory_views import MemoryItemViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/models/memory_item.py
- Type/area: Python model source
- Definitions: class MemoryItem(models.Model):; class Type(models.TextChoices):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .memory_item import MemoryItem
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/tests/test_memory.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): from django.test import TestCase
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## memory/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

