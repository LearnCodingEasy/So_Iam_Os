# scraper source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## scraper/admin.py
- Type/area: Python module
- Definitions: class ScrapingConfigInline(admin.StackedInline):; class WebsiteAdmin(admin.ModelAdmin):; class ParentSelectorAdmin(admin.ModelAdmin):; class ScrapingJobAdmin(admin.ModelAdmin):; class ScrapedDataAdmin(admin.ModelAdmin):
- Imports (first four): from django.contrib import admin; from .models import Website, ParentSelector, ScrapingConfig, ScrapingJob, ScrapedData
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/apps.py
- Type/area: Python module
- Definitions: class ScraperConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/tasks.py
- Type/area: Python module
- Definitions: def run_scraping_job(self, job_id):
- Imports (first four): from celery import shared_task; from .services import ScrapingService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from rest_framework.routers import DefaultRouter; from scraper.api.views import WebsiteViewSet, ParentSelectorViewSet, ScrapingConfigViewSet, ScrapingJobViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/api/serializers/scraper_serializers.py
- Type/area: Python API source
- Definitions: class WebsiteSerializer(serializers.ModelSerializer):; class Meta:; def get_last_run_id(self, obj):; def validate_base_url(self, value):; def validate_config(self, value):; def validate(self, attrs):; class ParentSelectorSerializer(serializers.ModelSerializer):; class Meta:; class ScrapingConfigSerializer(serializers.ModelSerializer):; class Meta:; class ScrapedDataSerializer(serializers.ModelSerializer):; class Meta:; class ScrapingJobSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from scraper.models import Website, ParentSelector, ScrapingConfig, ScrapingJob, ScrapedData; from scraper.services import validate_public_url
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .scraper_serializers import WebsiteSerializer, ParentSelectorSerializer, ScrapingConfigSerializer, ScrapedDataSerializer, ScrapingJobSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/api/views/scraper_views.py
- Type/area: Python API source
- Definitions: class OwnedQuerysetMixin:; def get_queryset(self):; class WebsiteViewSet(viewsets.ModelViewSet):; def get_queryset(self):; def perform_create(self, serializer):; def perform_update(self, serializer):; def perform_destroy(self, instance):; def test_connection(self, request, pk=None):; def run(self, request, pk=None):; def stats(self, request):; class ParentSelectorViewSet(viewsets.ModelViewSet):; def perform_create(self, serializer):; def perform_update(self, serializer):; def get_queryset(self):; class ScrapingConfigViewSet(viewsets.ModelViewSet):; def perform_create(self, serializer):; def perform_update(self, serializer):; def get_queryset(self):; class ScrapingJobViewSet(viewsets.ReadOnlyModelViewSet):; def get_queryset(self):; def results(self, request, pk=None):
- Imports (first four): from django.db.models import Count; from django.utils import timezone; from rest_framework import status, viewsets; from rest_framework.decorators import action
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .scraper_views import OwnedQuerysetMixin, WebsiteViewSet, ParentSelectorViewSet, ScrapingConfigViewSet, ScrapingJobViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; import uuid; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/migrations/0002_source_connectors_and_run_metrics.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.conf import settings; from django.db import migrations, models; import django.db.models.deletion
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/models/parent_selector.py
- Type/area: Python model source
- Definitions: class ParentSelector(models.Model):; class Meta:; def created_at_formatted(self):; def __str__(self):
- Imports (first four): import uuid; from django.db import models; from django.utils.timesince import timesince; from scraper.models.website import Website
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/models/scraped_data.py
- Type/area: Python model source
- Definitions: class ScrapedData(models.Model):; def __str__(self):
- Imports (first four): import uuid; from django.db import models; from scraper.models.scraping_job import ScrapingJob
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/models/scraping_config.py
- Type/area: Python model source
- Definitions: class ScrapingConfig(models.Model):; class Meta:; def __str__(self):
- Imports (first four): import uuid; from django.db import models; from scraper.models.parent_selector import ParentSelector
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/models/scraping_job.py
- Type/area: Python model source
- Definitions: class ScrapingJob(models.Model):; def __str__(self):
- Imports (first four): import uuid; from django.db import models; from scraper.models.website import Website
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/models/website.py
- Type/area: Python model source
- Definitions: class Website(models.Model):; class Meta:; def created_at_formatted(self):; def __str__(self):
- Imports (first four): import uuid; from django.db import models; from django.conf import settings; from django.utils.timesince import timesince
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .website import Website; from .parent_selector import ParentSelector; from .scraping_config import ScrapingConfig; from .scraping_job import ScrapingJob
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/services/scraper_services.py
- Type/area: Python service source
- Definitions: def validate_public_url(url):; def fetch_public(url, timeout=15):; def _text(value):; def _json_path(data, path):; def parse_source(website, content, content_type=""):; def normalize_item(item, base_url=""):; def first(*keys):; class ScrapingService:; def test_connection(website):; def start_scraping_job(job_id, use_playwright=False, show_browser=False):; def _job_field_rule(field_name):
- Imports (first four): import ipaddress; import json; import logging; import socket
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/services/__init__.py
- Type/area: Python service source
- Definitions: none matched
- Imports (first four): from .scraper_services import logger, USER_AGENT, validate_public_url, fetch_public, _text, _json_path, parse_source, normalize_item, ScrapingService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/tests/test_scraper.py
- Type/area: Python test source
- Definitions: class ScraperSafetyTests(SimpleTestCase):; def test_rejects_localhost(self):; def test_rejects_non_http_scheme(self):; def test_normalize_json_job(self):; def test_normalize_greenhouse_style_job(self):; def test_normalize_does_not_treat_id_as_a_url(self):; def test_parse_json_items_path(self):; def test_html_requires_explicit_selector(self):
- Imports (first four): from django.test import SimpleTestCase; from types import SimpleNamespace; from scraper.services import normalize_item, parse_source, validate_public_url
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## scraper/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

