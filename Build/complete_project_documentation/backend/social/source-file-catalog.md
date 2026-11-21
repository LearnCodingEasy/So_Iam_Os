# social source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## social/admin.py
- Type/area: Python module
- Definitions: class FriendshipRequestAdmin(admin.ModelAdmin):; class FriendshipAdmin(admin.ModelAdmin):; class FollowAdmin(admin.ModelAdmin):; class UserBlockAdmin(admin.ModelAdmin):
- Imports (first four): from django.contrib import admin; from .models import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/apps.py
- Type/area: Python module
- Definitions: class SocialConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/forms.py
- Type/area: Python module
- Definitions: class FriendshipRequestForm(forms.ModelForm):; class Meta:
- Imports (first four): from django import forms; from .models import FriendshipRequest
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from django.urls import path; from social.api import views as api
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/api/serializers/social_serializers.py
- Type/area: Python API source
- Definitions: class FriendshipRequestSerializer(; class Meta:; class FriendshipSerializer(; class Meta:; class FollowSerializer(; class Meta:; class SocialProfileSerializer(serializers.ModelSerializer):; class Meta:; class SocialRecommendationSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from social.models import FriendshipRequest, Friendship, Follow; from users_accounts.api.serializers import PublicUserSerializer; from social.models import SocialProfile, SocialRecommendation
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .social_serializers import FriendshipRequestSerializer, FriendshipSerializer, FollowSerializer, SocialProfileSerializer, SocialRecommendationSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/api/views/social_views.py
- Type/area: Python API source
- Definitions: def friends(request, pk):; def send_friendship_request(request, pk):; def handle_request(request, pk, action):; def unfriend(request, pk):; def my_friendship_suggestions(request):; def recommendations(request):; def my_profile(request):
- Imports (first four): from django.contrib.auth import get_user_model; from django.db.models import Q; from django.shortcuts import get_object_or_404; from rest_framework.decorators import api_view, permission_classes
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .social_views import User, friends, send_friendship_request, handle_request, unfriend, my_friendship_suggestions, recommendations, my_profile
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; import uuid; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/models/common.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from django.conf import settings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/models/follow.py
- Type/area: Python model source
- Definitions: class Follow(models.Model):; class Meta:; def __str__(self):
- Imports (first four): import uuid; from django.db import models; from social.models.common import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/models/friendship.py
- Type/area: Python model source
- Definitions: class Friendship(models.Model):; class Meta:; def __str__(self):
- Imports (first four): import uuid; from django.db import models; from social.models.common import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/models/friendship_request.py
- Type/area: Python model source
- Definitions: class FriendshipRequest(models.Model):; class Status(models.TextChoices):; class Meta:; def __str__(self):
- Imports (first four): import uuid; from django.db import models; from social.models.common import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/models/social_profile.py
- Type/area: Python model source
- Definitions: class SocialProfile(models.Model):; class Meta:
- Imports (first four): from django.db import models; from social.models.common import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/models/social_recommendation.py
- Type/area: Python model source
- Definitions: class SocialRecommendation(models.Model):; class Meta:
- Imports (first four): from django.db import models; from social.models.common import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/models/user_block.py
- Type/area: Python model source
- Definitions: class UserBlock(models.Model):; class Meta:; def __str__(self):
- Imports (first four): import uuid; from django.db import models; from social.models.common import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .common import User; from .friendship_request import FriendshipRequest; from .friendship import Friendship; from .follow import Follow
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/services/matching.py
- Type/area: Python service source
- Definitions: def _norm(values):; def _user_skills(user):; def score_candidate(user, candidate):; def recommendations_for(user, limit=30):
- Imports (first four): from django.db.models import Q; from social.models import Friendship, Follow, UserBlock, SocialProfile, SocialRecommendation; from django.contrib.auth import get_user_model
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/services/__init__.py
- Type/area: Python service source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/tests/test_social.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): from django.test import TestCase
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## social/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

