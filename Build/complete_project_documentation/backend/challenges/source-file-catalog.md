# challenges source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## challenges/admin.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from django.contrib import admin
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/apps.py
- Type/area: Python module
- Definitions: class ChallengesConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from rest_framework.routers import DefaultRouter; from challenges.api.views import ChallengeViewSet, ChallengeStepViewSet, ChallengeAttemptViewSet, ChallengeProgressViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/api/serializers/challenges_serializers.py
- Type/area: Python API source
- Definitions: class ChallengeStepSerializer(serializers.ModelSerializer):; class Meta: model=ChallengeStep; fields='__all__'; class ChallengeSerializer(serializers.ModelSerializer):; class Meta: model=Challenge; fields='__all__'; read_only_fields=['user','created_at','updated_at']; class ChallengeAttemptSerializer(serializers.ModelSerializer):; class Meta: model=ChallengeAttempt; fields='__all__'; read_only_fields=['user','created_at']; class ChallengeProgressSerializer(serializers.ModelSerializer):; class Meta: model=ChallengeProgress; fields='__all__'; read_only_fields=['user','updated_at']
- Imports (first four): from rest_framework import serializers; from challenges.models import Challenge, ChallengeStep, ChallengeAttempt, ChallengeProgress
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .challenges_serializers import ChallengeStepSerializer, ChallengeSerializer, ChallengeAttemptSerializer, ChallengeProgressSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/api/views/challenges_views.py
- Type/area: Python API source
- Definitions: class Owned(viewsets.ModelViewSet): permission_classes=[IsAuthenticated]; class ChallengeViewSet(Owned):; def get_queryset(self): return Challenge.objects.filter(user=self.request.user).prefetch_related('steps'); def perform_create(self,s): s.save(user=self.request.user); class ChallengeStepViewSet(Owned):; def get_queryset(self): return ChallengeStep.objects.filter(challenge__user=self.request.user); class ChallengeAttemptViewSet(Owned):; def get_queryset(self): return ChallengeAttempt.objects.filter(user=self.request.user); def perform_create(self,s): s.save(user=self.request.user); class ChallengeProgressViewSet(viewsets.ModelViewSet):; def get_queryset(self): return ChallengeProgress.objects.filter(user=self.request.user); def perform_create(self,s): s.save(user=self.request.user)
- Imports (first four): from rest_framework import viewsets; from rest_framework.permissions import IsAuthenticated; from challenges.models import Challenge, ChallengeStep, ChallengeAttempt, ChallengeProgress; from challenges.api.serializers import ChallengeSerializer, ChallengeStepSerializer, ChallengeAttemptSerializer, ChallengeProgressSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .challenges_views import Owned, ChallengeViewSet, ChallengeStepViewSet, ChallengeAttemptViewSet, ChallengeProgressViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/models/challenge.py
- Type/area: Python model source
- Definitions: class Challenge(models.Model):; class Type(models.TextChoices): LEARNING='learning','Learning'; CODING='coding','Coding'; GOAL='goal','Goal'; PROJECT='project','Project'; class Status(models.TextChoices): DRAFT='draft','Draft'; ACTIVE='active','Active'; COMPLETED='completed','Completed'; ARCHIVED='archived','Archived'
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/models/challenge_attempt.py
- Type/area: Python model source
- Definitions: class ChallengeAttempt(models.Model):
- Imports (first four): from django.conf import settings; from django.db import models; from challenges.models.challenge import Challenge
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/models/challenge_progress.py
- Type/area: Python model source
- Definitions: class ChallengeProgress(models.Model):; class Meta: constraints=[models.UniqueConstraint(fields=['challenge','user'],name='challenge_user_unique')]
- Imports (first four): from django.conf import settings; from django.db import models; from challenges.models.challenge import Challenge
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/models/challenge_step.py
- Type/area: Python model source
- Definitions: class ChallengeStep(models.Model):; class Meta: ordering=['order']
- Imports (first four): from django.db import models; from challenges.models.challenge import Challenge
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .challenge import Challenge; from .challenge_step import ChallengeStep; from .challenge_attempt import ChallengeAttempt; from .challenge_progress import ChallengeProgress
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/tests/test_challenges.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): from django.test import TestCase
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## challenges/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

