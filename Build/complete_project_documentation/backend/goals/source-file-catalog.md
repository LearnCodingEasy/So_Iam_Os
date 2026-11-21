# goals source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## goals/admin.py
- Type/area: Python module
- Definitions: class GoalMilestoneInline(admin.TabularInline):; class GoalAdmin(admin.ModelAdmin):; class GoalPlanProposalAdmin(admin.ModelAdmin):; class GoalActivityAdmin(admin.ModelAdmin):
- Imports (first four): from django.contrib import admin; from .models import Goal, GoalActivity, GoalMilestone, GoalPlanProposal
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/apps.py
- Type/area: Python module
- Definitions: class GoalsConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from rest_framework.routers import DefaultRouter; from goals.api.views import GoalMilestoneViewSet, GoalViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/api/serializers/goals_serializers.py
- Type/area: Python API source
- Definitions: class GoalSerializer(serializers.ModelSerializer):; class Meta:; def get_overdue(self, obj):; def get_risk(self, obj):; def validate(self, attrs):; class GoalMilestoneSerializer(serializers.ModelSerializer):; class Meta:; def get_overdue(self, obj):; def validate(self, attrs):; class GoalPlanProposalSerializer(serializers.ModelSerializer):; class Meta:; class GoalActivitySerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from django.utils import timezone; from rest_framework import serializers; from goals.models import Goal, GoalActivity, GoalMilestone, GoalPlanProposal; from goals.services import GoalRiskService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .goals_serializers import GoalSerializer, GoalMilestoneSerializer, GoalPlanProposalSerializer, GoalActivitySerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/api/views/goals_views.py
- Type/area: Python API source
- Definitions: class GoalPagination(PageNumberPagination):; class GoalViewSet(viewsets.ModelViewSet):; def get_queryset(self):; def perform_create(self, serializer):; def perform_update(self, serializer):; def perform_destroy(self, instance):; def analytics(self, request):; def history(self, request, pk=None):; def complete(self, request, pk=None):; def pause(self, request, pk=None):; def resume(self, request, pk=None):; def archive(self, request, pk=None):; def _set_status(self, request, new_status):; def progress(self, request, pk=None):; def duplicate(self, request, pk=None):; def coach(self, request, pk=None):; def plan(self, request, pk=None):; def reject_plan(self, request, pk=None):; def plans(self, request, pk=None):; def approve_plan(self, request, pk=None):; def notes(self, request, pk=None):; def reorder_milestones(self, request, pk=None):; def projects(self, request, pk=None):; def risk(self, request, pk=None):; class GoalMilestoneViewSet(viewsets.ModelViewSet):; def get_queryset(self):; def perform_create(self, serializer):; def perform_update(self, serializer):; def perform_destroy(self, instance):
- Imports (first four): import logging; from django.db import transaction; from django.db.models import Count, Q, Sum; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .goals_views import logger, GoalPagination, GoalViewSet, GoalMilestoneViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.core.validators; import django.db.models.deletion; import django.utils.timezone; from django.conf import settings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/migrations/0002_goal_intelligence.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.core.validators; import django.db.models.deletion; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/migrations/0003_rename_goals_goal_user_cat_status_idx_goals_goal_user_id_500d12_idx_and_more.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.db import migrations
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/models/goal.py
- Type/area: Python model source
- Definitions: class Goal(models.Model):; class Status(models.TextChoices):; class Priority(models.TextChoices):; class Category(models.TextChoices):; class Meta:; def __str__(self):; def mark_completed(self):
- Imports (first four): from django.conf import settings; from django.core.validators import MaxValueValidator, MinValueValidator; from django.db import models; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/models/goal_activity.py
- Type/area: Python model source
- Definitions: class GoalActivity(models.Model):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from goals.models.goal import Goal
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/models/goal_milestone.py
- Type/area: Python model source
- Definitions: class GoalMilestone(models.Model):; class Status(models.TextChoices):; class Meta:; def __str__(self):
- Imports (first four): from django.core.validators import MaxValueValidator, MinValueValidator; from django.db import models; from goals.models.goal import Goal
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/models/goal_plan_proposal.py
- Type/area: Python model source
- Definitions: class GoalPlanProposal(models.Model):; class Status(models.TextChoices):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from goals.models.goal import Goal
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .goal import Goal; from .goal_milestone import GoalMilestone; from .goal_plan_proposal import GoalPlanProposal; from .goal_activity import GoalActivity
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/services/coach.py
- Type/area: Python service source
- Definitions: class GoalCoachService:; def propose_plan(goal, user, instructions=""):; def answer(goal, user, message):
- Imports (first four): import json; import re; from django.utils.dateparse import parse_date, parse_datetime; from ai.services import AIFallbackChainService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/services/goals_services.py
- Type/area: Python service source
- Definitions: class GoalService:; def record(goal, user, event_type, description="", data=None):; def notify(user, title, message, obj, action_url="/goals"):; def set_status(cls, goal, status, user, notes=""):; def complete(cls, goal, user, notes=""):; def update_progress(cls, goal, progress, user, source="user"):; def recalculate_goal(cls, goal):; def recalculate_from_tasks(cls, goal):; def recalculate_milestone(cls, milestone):; def recalculate_for_task(cls, task):; def recalculate_from_milestones(cls, goal):; def _save_derived_progress(goal, progress, source):; def approve_plan(cls, proposal, user):; class GoalAnalyticsService:; def dashboard(user):; class GoalRiskService:; def analyze(goal):
- Imports (first four): from datetime import date, timedelta; from decimal import Decimal; from django.db import transaction; from django.db.models import Count, Q
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/services/__init__.py
- Type/area: Python service source
- Definitions: none matched
- Imports (first four): from .goals_services import GoalService, GoalAnalyticsService, GoalRiskService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/tests/test_goals.py
- Type/area: Python test source
- Definitions: class GoalServiceTests(TestCase):; def setUp(self):; def test_progress_validation_and_completion(self):; def test_invalid_status_transition_is_rejected(self):; def test_weighted_milestone_progress(self):; def test_task_completion_updates_goal_progress(self):; def test_milestone_dependency_cycle_is_rejected(self):; def test_numeric_measurement_is_not_double_counted_with_task_progress(self):; def test_analytics_are_user_scoped(self):; def test_activity_is_recorded(self):; def test_approved_plan_creates_milestones_and_tasks_once(self):; def test_milestone_task_completion_updates_weighted_goal_progress(self):; def test_goal_coach_uses_existing_fallback_service_and_returns_proposal(self, generate):; def test_goal_coach_answers_without_mutating_goal(self, generate):; class GoalAPITests(TestCase):; def setUp(self):; def test_list_is_scoped_to_authenticated_user(self):; def test_other_users_goal_is_not_accessible(self):; def test_analytics_endpoint(self):; def test_invalid_progress_is_rejected(self):
- Imports (first four): from datetime import timedelta; from decimal import Decimal; from unittest.mock import patch; from types import SimpleNamespace
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## goals/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

