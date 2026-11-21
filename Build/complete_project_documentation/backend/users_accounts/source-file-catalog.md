# users_accounts source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## users_accounts/admin.py
- Type/area: Python module
- Definitions: class UserAdmin(admin.ModelAdmin):
- Imports (first four): from django.contrib import admin; from .models import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/apps.py
- Type/area: Python module
- Definitions: class UsersAccountsConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/forms.py
- Type/area: Python module
- Definitions: class SignupForm(UserCreationForm):; class Meta:; def clean_email(self):; class ProfileForm(forms.ModelForm):; class Meta:; def clean_email(self):
- Imports (first four): from django import forms; from django.contrib.auth.forms import (; from .models import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from django.urls import path; from rest_framework_simplejwt.views import (; from users_accounts.api import views as api
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/api/serializers/users_accounts_serializers.py
- Type/area: Python API source
- Definitions: class PublicUserSerializer(serializers.ModelSerializer):; class Meta:; class UserSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from users_accounts.models import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .users_accounts_serializers import PublicUserSerializer, UserSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/api/views/users_accounts_views.py
- Type/area: Python API source
- Definitions: def signup(request):; def me(request):; def profile(request, id):; def editprofile(request):; def editpassword(request):
- Imports (first four): from django.contrib.auth.forms import PasswordChangeForm; from django.contrib.auth import get_user_model; from django.shortcuts import get_object_or_404; from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .users_accounts_views import logger, User, signup, me, profile, editprofile, editpassword
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.utils.timezone; import users_accounts.models; import uuid; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/models/custom_user_manager.py
- Type/area: Python model source
- Definitions: class CustomUserManager(UserManager):; def _create_user(self, email, password, **extra_fields):; def create_user(self, email, password=None, **extra_fields):; def create_superuser(self, email, password=None, **extra_fields):
- Imports (first four): from django.contrib.auth.models import UserManager
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/models/user.py
- Type/area: Python model source
- Definitions: class User(AbstractBaseUser, PermissionsMixin):; def __str__(self):; def full_name(self):; def avatar_url(self):; def cover_url(self):
- Imports (first four): from django.db import models; from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin; from django.utils import timezone; import uuid
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .custom_user_manager import CustomUserManager; from .user import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/tests/test_users_accounts.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): from django.test import TestCase
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## users_accounts/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

