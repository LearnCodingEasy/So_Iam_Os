# knowledge source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## knowledge/admin.py
- Type/area: Python module
- Definitions: class KnowledgeItemAdmin(admin.ModelAdmin):; class KnowledgeFileAdmin(admin.ModelAdmin):
- Imports (first four): from django.contrib import admin; from .models import KnowledgeFile, KnowledgeItem
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/apps.py
- Type/area: Python module
- Definitions: class KnowledgeConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from rest_framework.routers import DefaultRouter; from knowledge.api.views import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/api/serializers/knowledge_file_serializers.py
- Type/area: Python API source
- Definitions: class KnowledgeFileSerializer(serializers.ModelSerializer):; class Meta:; def get_file_url(self, obj):; def get_file_size_display(self, obj):; def validate_file(self, value):; def create(self, validated_data):; def update(self, instance, validated_data):
- Imports (first four): from django.contrib.auth import get_user_model; from rest_framework import serializers; from knowledge.models import KnowledgeFile; from knowledge.validators import validate_knowledge_upload
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/api/serializers/knowledge_item_serializers.py
- Type/area: Python API source
- Definitions: class KnowledgeItemSerializer(serializers.ModelSerializer):; class Meta:; def get_files_count(self, obj):; def get_learning_topics(self, obj):; def get_learning_topics_count(self, obj):; def get_learning_notes_count(self, obj):; def get_learning_applications_count(self, obj):; def validate(self, attrs):; class KnowledgeItemDetailSerializer(; class Meta(KnowledgeItemSerializer.Meta):
- Imports (first four): from django.contrib.auth import get_user_model; from rest_framework import serializers; from knowledge.models import KnowledgeItem; from .knowledge_file_serializers import KnowledgeFileSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .knowledge_file_serializers import KnowledgeFileSerializer; from .knowledge_item_serializers import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/api/views/knowledge_file_views.py
- Type/area: Python API source
- Definitions: class KnowledgeFileViewSet(viewsets.ModelViewSet):; def get_queryset(self):; def perform_create(self, serializer):; def perform_update(self, serializer):; def perform_destroy(self, instance):
- Imports (first four): from rest_framework import viewsets; from rest_framework.exceptions import (; from rest_framework.parsers import (; from rest_framework.permissions import IsAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/api/views/knowledge_item_views.py
- Type/area: Python API source
- Definitions: class KnowledgeItemViewSet(viewsets.ModelViewSet):; def get_queryset(self):; def get_serializer_class(self):; def perform_create(self, serializer):; def perform_update(self, serializer):; def perform_destroy(self, instance):; def extract_metadata_action(self, request, pk=None):; def archive(self, request, pk=None):; def restore(self, request, pk=None):; def connect_topic(self, request, pk=None):; def disconnect_topic(; def files(self, request, pk=None):; def upload_file(; def archive_all(
- Imports (first four): from rest_framework import status, viewsets; from rest_framework.decorators import action; from rest_framework.exceptions import (; from rest_framework.parsers import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .knowledge_item_views import KnowledgeItemViewSet; from .knowledge_file_views import KnowledgeFileViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/extractors/metadata_extractor.py
- Type/area: Python module
- Definitions: def extract_metadata(title="", description="", content=""):
- Imports (first four): import re; from collections import Counter
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/extractors/text_extractor.py
- Type/area: Python module
- Definitions: def extract_text(file_obj):
- Imports (first four): import pypdf; from docx import Document
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/extractors/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from .metadata_extractor import extract_metadata; from .text_extractor import extract_text
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/models/knowledge_file.py
- Type/area: Python model source
- Definitions: class KnowledgeFile(models.Model):; class FileType(models.TextChoices):; class ProcessingStatus(models.TextChoices):; class Meta:; def __str__(self):; def delete(self, *args, **kwargs):
- Imports (first four): from django.db import models; from .knowledge_item import KnowledgeItem
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/models/knowledge_item.py
- Type/area: Python model source
- Definitions: class KnowledgeItem(models.Model):; class KnowledgeType(models.TextChoices):; class Visibility(models.TextChoices):; class Meta:; def __str__(self):; def learning_topics_count(self):; def learning_notes_count(self):; def learning_applications_count(self):
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .knowledge_item import KnowledgeItem; from .knowledge_file import KnowledgeFile
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/services/file_service.py
- Type/area: Python service source
- Definitions: class KnowledgeFileService:; def add_file(; def delete_file(
- Imports (first four): from django.db import transaction; from knowledge.models import KnowledgeFile; from pathlib import Path; from knowledge.validators import validate_knowledge_upload
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/services/knowledge_service.py
- Type/area: Python service source
- Definitions: class KnowledgeService:; def get_user_knowledge(; def create_knowledge(; def update_knowledge(; def archive_knowledge(; def restore_knowledge(; def connect_to_topic(; def disconnect_from_topic(; def search(
- Imports (first four): from django.db import transaction; from django.db.models import Count; from knowledge.models import KnowledgeItem
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/services/__init__.py
- Type/area: Python service source
- Definitions: none matched
- Imports (first four): from .knowledge_service import KnowledgeService; from .file_service import KnowledgeFileService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/tasks/knowledge_file_tasks.py
- Type/area: Python task source
- Definitions: def process_knowledge_file(self, file_id):
- Imports (first four): from celery import shared_task; from django.db import transaction; from django.utils import timezone; from knowledge.extractors import extract_text
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/tasks/__init__.py
- Type/area: Python task source
- Definitions: none matched
- Imports (first four): from .knowledge_file_tasks import process_knowledge_file
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/tests/test_api.py
- Type/area: Python test source
- Definitions: def make_user(email):; class KnowledgeItemApiTests(APITestCase):; def setUp(self):; def test_requires_authentication(self):; def test_create_list_and_owner_scoping(self):; def test_archive_and_restore(self):; def test_extract_metadata_action_fills_empty_fields_only(self):; def test_upload_rejects_unsupported_file_and_missing_file(self):; def test_upload_valid_text_file_creates_record(self):; def test_cannot_touch_another_users_item(self):; class KnowledgeStructureContractTests(APITestCase):; def test_celery_task_keeps_legacy_name(self):; def test_public_import_surface(self):
- Imports (first four): import tempfile; from django.contrib.auth import get_user_model; from django.core.files.uploadedfile import SimpleUploadedFile; from django.test import override_settings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/tests/test_file_validation.py
- Type/area: Python test source
- Definitions: class Upload(io.BytesIO):; def __init__(self, name, content):; class KnowledgeFileValidationTests(unittest.TestCase):; def test_accepts_utf8_markdown_and_resets_stream(self):; def test_rejects_unsupported_extension(self):; def test_rejects_pdf_extension_with_wrong_signature(self):; def test_rejects_invalid_utf8_text(self):; def test_rejects_empty_file(self):; def test_rejects_corrupt_docx_container(self):
- Imports (first four): import io; import unittest; from knowledge.validators.file_validator import validate_knowledge_upload
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/tests/test_metadata_extractor.py
- Type/area: Python test source
- Definitions: class MetadataExtractionTests(unittest.TestCase):; def test_extracts_headings_summary_and_technology_tags(self):; def test_arabic_language_hint(self):; def test_empty_content_is_safe(self):
- Imports (first four): import unittest; from knowledge.extractors.metadata_extractor import extract_metadata
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/validators/file_validator.py
- Type/area: Python module
- Definitions: def _read_prefix(uploaded_file, length=8192):; def validate_knowledge_upload(uploaded_file):
- Imports (first four): from pathlib import Path; import zipfile
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## knowledge/validators/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from .file_validator import validate_knowledge_upload
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

