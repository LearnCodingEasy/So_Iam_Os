# jobs_opportunity source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## jobs_opportunity/admin.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from django.contrib import admin; from .models import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/apps.py
- Type/area: Python module
- Definitions: class JobsOpportunityConfig(AppConfig):; def ready(self):
- Imports (first four): from django.apps import AppConfig; from . import signals  # noqa: F401
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/default_sources.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/feature_catalog.py
- Type/area: Python module
- Definitions: def get_feature_count():; def get_categories():; def get_features_by_category(category):; def get_feature_catalog():
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/scraper.py
- Type/area: Python module
- Definitions: class JobScraperService:; def run(self, source_id: int):; class ScraperPolicyError(ValueError):; def _validate_public_url(url: str) -> urllib.parse.ParseResult:; def check_robots(url: str, user_agent: str = "So-IAM-OS-JobScraper/1.0") -> bool:; def _load_bs4():; def _select(root, selector: str, selector_type: str):; def _value(element, rule: dict):; def extract_jobs(html_text: str, mapping: dict) -> list[dict]:; def fetch_and_extract(url: str, mapping: dict, *, user_agent: str, rate_limit_seconds: float = 1.0) -> tuple[list[dict], dict]:
- Imports (first four): from __future__ import annotations; import hashlib; import ipaddress; import socket
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/signals.py
- Type/area: Python module
- Definitions: def provision_default_job_sources(sender, instance, created, **kwargs):
- Imports (first four): from django.db.models.signals import post_save; from django.dispatch import receiver; from django.contrib.auth import get_user_model; from .default_sources import DEFAULT_JOB_SOURCES
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/tasks.py
- Type/area: Python module
- Definitions: def _safe_url(url):; def _json_path(data, path):; def _skill_names(item):; def _canonical_key(item):; def _safe_published_at(value):; def _safe_decimal(value):; def _safe_job_url(value):; def _upsert_job(source, item):; def _rss_items(content):; def child_text(node, *names):; def sync_job_source(self, source_id, sync_run_id=None):; def refresh_all_job_sources():; def refresh_all_job_matches():; def expire_old_jobs():
- Imports (first four): import ipaddress; import json; import re; from datetime import datetime, time
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from rest_framework.routers import DefaultRouter; from jobs_opportunity.api.views import CompanyProfileViewSet, JobAlertViewSet, JobAnalyticsSnapshotViewSet, JobApplicationViewSet, JobCoverLetterViewSet, JobInterviewViewSet, JobMatchViewSet, JobOpportunityViewSet, JobPreferenceViewSet, JobReadinessViewSet, JobRecommendationViewSet, JobResumeViewSet, JobSavedSearchViewSet, JobSkillGapViewSet, JobSourceViewSet, JobsWorkspaceViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/company_profile_serializers.py
- Type/area: Python API source
- Definitions: class CompanyProfileSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import CompanyProfile
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_alert_serializers.py
- Type/area: Python API source
- Definitions: class JobAlertSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobAlert
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_analytics_snapshot_serializers.py
- Type/area: Python API source
- Definitions: class JobAnalyticsSnapshotSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobAnalyticsSnapshot
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_application_event_serializers.py
- Type/area: Python API source
- Definitions: class JobApplicationEventSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobApplicationEvent
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_application_serializers.py
- Type/area: Python API source
- Definitions: class JobApplicationSerializer(serializers.ModelSerializer):; class Meta:; def validate_resume(self, resume):; def validate_cover_letter(self, cover_letter):; def validate_job(self, job):
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobApplication
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_cover_letter_serializers.py
- Type/area: Python API source
- Definitions: class JobCoverLetterSerializer(serializers.ModelSerializer):; class Meta:; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobCoverLetter
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_interview_serializers.py
- Type/area: Python API source
- Definitions: class JobInterviewSerializer(serializers.ModelSerializer):; class Meta:; def validate_application(self, application):
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobInterview
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_match_serializers.py
- Type/area: Python API source
- Definitions: class JobMatchSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobMatch; from jobs_opportunity.api.serializers.job_opportunity_serializers import JobOpportunitySerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_opportunity_serializers.py
- Type/area: Python API source
- Definitions: class JobOpportunitySerializer(serializers.ModelSerializer):; class Meta:; def validate_source(self, source):; def validate_company_profile(self, value):; def get_match(self, obj):; def get_readiness(self, obj):
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobOpportunity; from jobs_opportunity.api.serializers.job_skill_requirement_serializers import JobSkillRequirementSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_preference_serializers.py
- Type/area: Python API source
- Definitions: class JobPreferenceSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobPreference
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_readiness_serializers.py
- Type/area: Python API source
- Definitions: class JobReadinessSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobReadiness
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_recommendation_serializers.py
- Type/area: Python API source
- Definitions: class JobRecommendationSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobRecommendation; from jobs_opportunity.api.serializers.job_opportunity_serializers import JobOpportunitySerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_resume_serializers.py
- Type/area: Python API source
- Definitions: class JobResumeSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobResume
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_saved_search_serializers.py
- Type/area: Python API source
- Definitions: class JobSavedSearchSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobSavedSearch
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_skill_gap_serializers.py
- Type/area: Python API source
- Definitions: class JobSkillGapSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobSkillGap
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_skill_requirement_serializers.py
- Type/area: Python API source
- Definitions: class JobSkillRequirementSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobSkillRequirement
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/job_source_serializers.py
- Type/area: Python API source
- Definitions: class JobSourceSerializer(serializers.ModelSerializer):; class Meta:; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from jobs_opportunity.models import JobSource
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .job_source_serializers import JobSourceSerializer; from .job_skill_requirement_serializers import JobSkillRequirementSerializer; from .job_opportunity_serializers import JobOpportunitySerializer; from .job_match_serializers import JobMatchSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/company_profile_views.py
- Type/area: Python API source
- Definitions: class CompanyProfileViewSet(UserOwnedViewSet):; def get_queryset(self): return CompanyProfile.objects.filter(; def perform_create(self, serializer): serializer.save(; def toggle_follow(self, request, pk=None):; def toggle_blacklist(self, request, pk=None):
- Imports (first four): from rest_framework.decorators import action; from rest_framework.response import Response; from jobs_opportunity.models import CompanyProfile; from jobs_opportunity.api.serializers import CompanyProfileSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/jobs_workspace_views.py
- Type/area: Python API source
- Definitions: class JobsWorkspaceViewSet(viewsets.ViewSet):; def dashboard(self, request):; def features(self, request):; def refresh_all(self, request):; def compare(self, request):
- Imports (first four): from rest_framework import viewsets; from rest_framework.decorators import action; from rest_framework.permissions import IsAuthenticated; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_alert_views.py
- Type/area: Python API source
- Definitions: class JobAlertViewSet(UserOwnedViewSet):; def get_queryset(self): return JobAlert.objects.filter(; def perform_create(self, serializer): serializer.save(; def read(self, request, pk=None):
- Imports (first four): from rest_framework.decorators import action; from rest_framework.response import Response; from jobs_opportunity.models import JobAlert; from jobs_opportunity.api.serializers import JobAlertSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_analytics_snapshot_views.py
- Type/area: Python API source
- Definitions: class JobAnalyticsSnapshotViewSet(viewsets.ReadOnlyModelViewSet):; def get_queryset(self): return JobAnalyticsSnapshot.objects.filter(
- Imports (first four): from rest_framework import viewsets; from rest_framework.permissions import IsAuthenticated; from jobs_opportunity.models import JobAnalyticsSnapshot; from jobs_opportunity.api.serializers import JobAnalyticsSnapshotSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_application_views.py
- Type/area: Python API source
- Definitions: class JobApplicationViewSet(UserOwnedViewSet):; def get_queryset(self): return JobApplication.objects.filter(; def perform_create(self, serializer):; def timeline(self, request, pk=None):; def event(self, request, pk=None):
- Imports (first four): from rest_framework.decorators import action; from rest_framework.response import Response; from jobs_opportunity.models import JobApplication, JobApplicationEvent; from jobs_opportunity.api.serializers import JobApplicationEventSerializer, JobApplicationSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_cover_letter_views.py
- Type/area: Python API source
- Definitions: class JobCoverLetterViewSet(UserOwnedViewSet):; def get_queryset(self): return JobCoverLetter.objects.filter(; def perform_create(self, serializer): serializer.save(
- Imports (first four): from jobs_opportunity.models import JobCoverLetter; from jobs_opportunity.api.serializers import JobCoverLetterSerializer; from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_interview_views.py
- Type/area: Python API source
- Definitions: class JobInterviewViewSet(UserOwnedViewSet):; def get_queryset(self): return JobInterview.objects.filter(
- Imports (first four): from jobs_opportunity.models import JobInterview; from jobs_opportunity.api.serializers import JobInterviewSerializer; from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_match_views.py
- Type/area: Python API source
- Definitions: class JobMatchViewSet(viewsets.ReadOnlyModelViewSet):; def get_queryset(self):; def refresh(self, request):
- Imports (first four): from rest_framework import viewsets; from rest_framework.decorators import action; from rest_framework.response import Response; from jobs_opportunity.models import JobMatch
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_opportunity_views.py
- Type/area: Python API source
- Definitions: class JobOpportunityViewSet(UserOwnedViewSet):; def get_queryset(self):; def create(self, request, *args, **kwargs):; def refresh_match(self, request, pk=None):; def analyze(self, request, pk=None):; def readiness(self, request, pk=None):; def similar(self, request, pk=None):; def compare(self, request):; def generate_cover_letter(self, request, pk=None):; def apply(self, request, pk=None):
- Imports (first four): from django.db.models import Q; from rest_framework import status; from rest_framework.decorators import action; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_preference_views.py
- Type/area: Python API source
- Definitions: class JobPreferenceViewSet(viewsets.ViewSet):; def list(self, request):; def create(self, request):; def update_preferences(self, request):
- Imports (first four): from rest_framework import viewsets; from rest_framework.decorators import action; from rest_framework.permissions import IsAuthenticated; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_readiness_views.py
- Type/area: Python API source
- Definitions: class JobReadinessViewSet(viewsets.ReadOnlyModelViewSet):; def get_queryset(self): return JobReadiness.objects.filter(; def refresh(self, request):
- Imports (first four): from rest_framework import viewsets; from rest_framework.decorators import action; from rest_framework.permissions import IsAuthenticated; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_recommendation_views.py
- Type/area: Python API source
- Definitions: class JobRecommendationViewSet(UserOwnedViewSet):; def get_queryset(self): return JobRecommendation.objects.filter(; def refresh(self, request):; def seen(self, request, pk=None):; def save(self, request, pk=None):; def dismiss(self, request, pk=None):
- Imports (first four): from rest_framework.decorators import action; from rest_framework.response import Response; from jobs_opportunity.models import JobRecommendation; from jobs_opportunity.api.serializers import JobRecommendationSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_resume_views.py
- Type/area: Python API source
- Definitions: class JobResumeViewSet(UserOwnedViewSet):; def get_queryset(self): return JobResume.objects.filter(; def perform_create(self, serializer): serializer.save(; def make_default(self, request, pk=None):
- Imports (first four): from rest_framework.decorators import action; from rest_framework.response import Response; from jobs_opportunity.models import JobResume; from jobs_opportunity.api.serializers import JobResumeSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_saved_search_views.py
- Type/area: Python API source
- Definitions: class JobSavedSearchViewSet(UserOwnedViewSet):; def get_queryset(self): return JobSavedSearch.objects.filter(; def perform_create(self, serializer): serializer.save(; def run(self, request, pk=None):
- Imports (first four): from django.db.models import Q; from rest_framework.decorators import action; from rest_framework.response import Response; from jobs_opportunity.models import JobOpportunity, JobSavedSearch
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_skill_gap_views.py
- Type/area: Python API source
- Definitions: class JobSkillGapViewSet(UserOwnedViewSet):; def get_queryset(self): return JobSkillGap.objects.filter(; def start_learning(self, request, pk=None):
- Imports (first four): from rest_framework.decorators import action; from rest_framework.response import Response; from jobs_opportunity.models import JobSkillGap; from jobs_opportunity.api.serializers import JobSkillGapSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/job_source_views.py
- Type/area: Python API source
- Definitions: class JobSourceViewSet(UserOwnedViewSet):; def get_queryset(self): return JobSource.objects.filter(; def perform_create(self, serializer): serializer.save(; def sync_all(self, request):; def sync_runs(self, request):; def sync(self, request, pk=None):; def test(self, request, pk=None):; def preview(self, request, pk=None):
- Imports (first four): import requests; from django.utils import timezone; from rest_framework import status; from rest_framework.decorators import action
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/user_owned_views.py
- Type/area: Python API source
- Definitions: class UserOwnedViewSet(viewsets.ModelViewSet):
- Imports (first four): from rest_framework import viewsets; from rest_framework.permissions import IsAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .user_owned_views import UserOwnedViewSet; from .job_source_views import JobSourceViewSet; from .job_opportunity_views import JobOpportunityViewSet; from .job_match_views import JobMatchViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/management/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/management/commands/bootstrap_job_sources.py
- Type/area: Python module
- Definitions: class Command(BaseCommand):; def add_arguments(self, parser):; def handle(self, *args, **options):
- Imports (first four): from django.core.management.base import BaseCommand; from django.contrib.auth import get_user_model; from jobs_opportunity.default_sources import DEFAULT_JOB_SOURCES; from jobs_opportunity.models import JobSource
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/management/commands/scrape_jobs.py
- Type/area: Python module
- Definitions: class Command(BaseCommand):; def add_arguments(self, parser):; def handle(self, *args, **options):
- Imports (first four): from django.core.management.base import BaseCommand, CommandError; from jobs_opportunity.models import JobSource; from jobs_opportunity.scraper import JobScraperService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/management/commands/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.core.validators; import django.db.models.deletion; import django.utils.timezone; from django.conf import settings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/migrations/0002_normalize_source_types.py
- Type/area: Python migration source
- Definitions: def normalize_job_sources(apps, schema_editor):; def reverse_normalize_job_sources(apps, schema_editor):; class Migration(migrations.Migration):
- Imports (first four): from django.db import migrations
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/migrations/0003_expand_job_url_length.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/migrations/0004_job_source_sync_run.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.conf import settings; from django.db import migrations, models; import django.db.models.deletion
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/migrations/0005_rename_jobs_sync_user_created_idx_jobs_opport_user_id_9739b7_idx_and_more.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.db import migrations
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/common.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from django.core.validators import MaxValueValidator, MinValueValidator
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/company_profile.py
- Type/area: Python model source
- Definitions: class CompanyProfile(models.Model):; class Meta:; def save(self, *args, **kwargs):
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_alert.py
- Type/area: Python model source
- Definitions: class JobAlert(models.Model):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_analytics_snapshot.py
- Type/area: Python model source
- Definitions: class JobAnalyticsSnapshot(models.Model):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_application.py
- Type/area: Python model source
- Definitions: class JobApplication(models.Model):; class Status(models.TextChoices):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from jobs_opportunity.models.job_opportunity import JobOpportunity
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_application_event.py
- Type/area: Python model source
- Definitions: class JobApplicationEvent(models.Model):; class Meta:
- Imports (first four): from django.db import models; from django.utils import timezone; from jobs_opportunity.models.job_application import JobApplication
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_cover_letter.py
- Type/area: Python model source
- Definitions: class JobCoverLetter(models.Model):
- Imports (first four): from django.conf import settings; from django.db import models; from jobs_opportunity.models.job_opportunity import JobOpportunity; from jobs_opportunity.models.job_resume import JobResume
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_interview.py
- Type/area: Python model source
- Definitions: class JobInterview(models.Model):
- Imports (first four): from django.core.validators import MaxValueValidator, MinValueValidator; from django.db import models; from jobs_opportunity.models.job_application import JobApplication
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_match.py
- Type/area: Python model source
- Definitions: class JobMatch(models.Model):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from jobs_opportunity.models.common import PERCENT; from jobs_opportunity.models.job_opportunity import JobOpportunity
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_opportunity.py
- Type/area: Python model source
- Definitions: class JobOpportunity(models.Model):; class JobType(models.TextChoices):; class LocationType(models.TextChoices):; class ExperienceLevel(models.TextChoices):; class SalaryPeriod(models.TextChoices):; class Meta:; def save(self, *args, **kwargs):
- Imports (first four): from django.conf import settings; from django.db import models; from django.utils import timezone; from jobs_opportunity.models.common import PERCENT
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_preference.py
- Type/area: Python model source
- Definitions: class JobPreference(models.Model):; class RemotePreference(models.TextChoices):
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_readiness.py
- Type/area: Python model source
- Definitions: class JobReadiness(models.Model):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from jobs_opportunity.models.common import PERCENT; from jobs_opportunity.models.job_opportunity import JobOpportunity
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_recommendation.py
- Type/area: Python model source
- Definitions: class JobRecommendation(models.Model):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from jobs_opportunity.models.common import PERCENT; from jobs_opportunity.models.job_opportunity import JobOpportunity
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_resume.py
- Type/area: Python model source
- Definitions: class JobResume(models.Model):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_saved_search.py
- Type/area: Python model source
- Definitions: class JobSavedSearch(models.Model):
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_skill_gap.py
- Type/area: Python model source
- Definitions: class JobSkillGap(models.Model):; class Severity(models.TextChoices):; class Status(models.TextChoices):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from jobs_opportunity.models.job_opportunity import JobOpportunity
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_skill_requirement.py
- Type/area: Python model source
- Definitions: class JobSkillRequirement(models.Model):; class Meta:
- Imports (first four): from django.core.validators import MaxValueValidator, MinValueValidator; from django.db import models; from jobs_opportunity.models.job_opportunity import JobOpportunity
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_source.py
- Type/area: Python model source
- Definitions: class JobSource(models.Model):; class SourceType(models.TextChoices):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/job_source_sync_run.py
- Type/area: Python model source
- Definitions: class JobSourceSyncRun(models.Model):; class Status(models.TextChoices):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from jobs_opportunity.models.job_source import JobSource
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .common import PERCENT; from .job_source import JobSource; from .job_source_sync_run import JobSourceSyncRun; from .company_profile import CompanyProfile
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/services/jobs_opportunity_services.py
- Type/area: Python service source
- Definitions: class JobMatchingService:; def _user_skill_levels(cls, user):; def calculate(cls, user, job):; def refresh_for_user(cls, user):; class JobGapService:; def sync_from_match(user, match):; def create_learning_goal(user, gap):; class JobParserService:; def analyze(cls, job, user=None, use_ai=False):; def _clean_strings(value, limit=12, width=600):; class ReadinessService:; def calculate(user, job, match=None):; class JobRecommendationService:; def refresh(user, limit=50):; class JobAnalyticsService:; def dashboard(user, *, persist_snapshot=False):; def _persist_snapshot(user, snapshot, *, attempts=3):; class JobService:; def save_source(user, **data):; def create_job(user, **data):; def apply(user, job, **data):
- Imports (first four): import logging; import re; import time; from collections import Counter
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/services/__init__.py
- Type/area: Python service source
- Definitions: none matched
- Imports (first four): from .jobs_opportunity_services import logger, JobMatchingService, JobGapService, JobParserService, ReadinessService, JobRecommendationService, JobAnalyticsService, JobService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/tests/test_jobs_opportunity.py
- Type/area: Python test source
- Definitions: class JobsAPITests(APITestCase):; def setUp(self):; def test_user_isolation(self):; def test_match_endpoint(self):; def test_workspace_has_150_features(self):; def test_preferences_and_readiness(self):; def test_dashboard(self):; class XPathScraperExtractionTests(SimpleTestCase):; def test_extracts_title_and_absolute_job_url_from_xpath_card(self):; def test_xpath_text_extraction_handles_multiple_nested_text_nodes(self):
- Imports (first four): from django.contrib.auth import get_user_model; from rest_framework.test import APITestCase; from django.test import SimpleTestCase; from rest_framework_simplejwt.tokens import RefreshToken
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/tests/test_rss_parser.py
- Type/area: Python test source
- Definitions: class RSSParserTests(SimpleTestCase):; def test_job_url_validator_rejects_unsafe_schemes_and_credentials(self):; def test_json_path_reads_nested_items(self):; def test_rss_item_reads_leaf_elements(self):; def test_atom_entry_reads_alternate_href(self):; def test_invalid_xml_raises_actionable_error_for_string_input(self):
- Imports (first four): from django.test import SimpleTestCase; from jobs_opportunity.tasks import _rss_items, _safe_job_url, _json_path
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## jobs_opportunity/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

