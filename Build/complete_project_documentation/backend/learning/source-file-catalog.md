# learning source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## learning/admin.py
- Type/area: Python module
- Definitions: class SkillAdmin(admin.ModelAdmin):; class LearningGoalAdmin(admin.ModelAdmin):; class LearningPathAdmin(admin.ModelAdmin):; class LearningTopicAdmin(admin.ModelAdmin):; class LessonAdmin(admin.ModelAdmin):; class LearningResourceAdmin(admin.ModelAdmin):; class LearningNoteAdmin(admin.ModelAdmin):; class LearningProgressAdmin(admin.ModelAdmin):; class LearningSessionAdmin(admin.ModelAdmin):; class AssessmentAdmin(admin.ModelAdmin):; class AssessmentQuestionAdmin(admin.ModelAdmin):; class AssessmentChoiceAdmin(admin.ModelAdmin):; class AssessmentAttemptAdmin(admin.ModelAdmin):; class AssessmentResponseAdmin(admin.ModelAdmin):; class KnowledgeApplicationAdmin(admin.ModelAdmin):; class ApplicationSubmissionAdmin(admin.ModelAdmin):; class ApplicationReviewAdmin(admin.ModelAdmin):; class LearningRevisionAdmin(admin.ModelAdmin):
- Imports (first four): from django.contrib import admin; from .models import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/apps.py
- Type/area: Python module
- Definitions: class LearningConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from rest_framework.routers import DefaultRouter; from learning.api.views import SkillViewSet, LearningGoalViewSet, LearningPathViewSet, LearningTopicViewSet, LessonViewSet, LearningResourceViewSet, LearningNoteViewSet, LearningProgressViewSet, LearningSessionViewSet, AssessmentViewSet, AssessmentQuestionViewSet, AssessmentChoiceViewSet, AssessmentAttemptViewSet, AssessmentResponseViewSet, KnowledgeApplicationViewSet, ApplicationSubmissionViewSet, ApplicationReviewViewSet, LearningRevisionViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/application_review_serializers.py
- Type/area: Python API source
- Definitions: class ApplicationReviewSerializer(; class Meta:; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from learning.models import ApplicationReview; from learning.api.serializers.application_submission_serializers import ApplicationSubmissionSerializer; from learning.api.serializers.knowledge_application_serializers import KnowledgeApplicationSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/application_submission_serializers.py
- Type/area: Python API source
- Definitions: class ApplicationSubmissionSerializer(; class Meta:; def validate_application(self, application):; def create(self, validated_data):
- Imports (first four): from rest_framework import serializers; from learning.models import ApplicationSubmission; from learning.api.serializers.common import ensure_owner, get_request_user; from learning.api.serializers.knowledge_application_serializers import KnowledgeApplicationSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/assessment_attempt_serializers.py
- Type/area: Python API source
- Definitions: class AssessmentAttemptSerializer(serializers.ModelSerializer):; class Meta:; def validate_assessment(self, assessment):; def create(self, validated_data):
- Imports (first four): from rest_framework import serializers; from learning.models import AssessmentAttempt; from learning.api.serializers.assessment_serializers import AssessmentLearnerSerializer; from learning.api.serializers.common import ensure_owner, get_request_user
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/assessment_choice_serializers.py
- Type/area: Python API source
- Definitions: class AssessmentChoiceSerializer(serializers.ModelSerializer):; class Meta:; class AssessmentChoiceLearnerSerializer(; class Meta:
- Imports (first four): from rest_framework import serializers; from learning.models import AssessmentChoice
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/assessment_question_serializers.py
- Type/area: Python API source
- Definitions: class AssessmentQuestionSerializer(serializers.ModelSerializer):; class Meta:; def validate_assessment(self, assessment):; class AssessmentQuestionLearnerSerializer(; class Meta:
- Imports (first four): from rest_framework import serializers; from learning.models import AssessmentQuestion; from learning.api.serializers.assessment_choice_serializers import AssessmentChoiceLearnerSerializer, AssessmentChoiceSerializer; from learning.api.serializers.common import ensure_owner, get_request_user
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/assessment_response_serializers.py
- Type/area: Python API source
- Definitions: class AssessmentResponseSerializer(; class Meta:; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from learning.models import AssessmentChoice, AssessmentResponse; from learning.api.serializers.common import get_request_user
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/assessment_serializers.py
- Type/area: Python API source
- Definitions: class AssessmentSerializer(serializers.ModelSerializer):; class Meta:; def validate_topic(self, topic):; class AssessmentLearnerSerializer(; class Meta:
- Imports (first four): from rest_framework import serializers; from learning.models import Assessment; from learning.api.serializers.assessment_question_serializers import AssessmentQuestionLearnerSerializer, AssessmentQuestionSerializer; from learning.api.serializers.common import ensure_owner, get_request_user
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/common.py
- Type/area: Python API source
- Definitions: def get_request_user(serializer):; def ensure_owner(user, obj, field_name="object"):
- Imports (first four): from django.contrib.auth import get_user_model; from rest_framework import serializers
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/knowledge_application_serializers.py
- Type/area: Python API source
- Definitions: class KnowledgeApplicationSerializer(; class Meta:; def validate_topic(self, topic):; def validate(self, attrs):; def create(self, validated_data):
- Imports (first four): from rest_framework import serializers; from learning.models import KnowledgeApplication; from learning.api.serializers.common import ensure_owner, get_request_user
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/learning_dashboard_serializers.py
- Type/area: Python API source
- Definitions: class LearningDashboardSerializer(
- Imports (first four): from rest_framework import serializers; from learning.api.serializers.application_review_serializers import ApplicationReviewSerializer; from learning.api.serializers.learning_goal_serializers import LearningGoalSerializer; from learning.api.serializers.learning_path_serializers import LearningPathSerializer, LearningTopicMinimalSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/learning_goal_serializers.py
- Type/area: Python API source
- Definitions: class LearningGoalSerializer(serializers.ModelSerializer):; class Meta:; def validate_skill(self, skill):; def validate(self, attrs):; def create(self, validated_data):; class LearningGoalDetailSerializer(; def get_paths(self, obj):; class Meta(LearningGoalSerializer.Meta):
- Imports (first four): from rest_framework import serializers; from learning.models import LearningGoal; from learning.api.serializers.common import get_request_user; from learning.api.serializers.skill_serializers import SkillMinimalSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/learning_note_serializers.py
- Type/area: Python API source
- Definitions: class LearningNoteSerializer(serializers.ModelSerializer):; class Meta:; def validate_topic(self, topic):; def validate(self, attrs):; def create(self, validated_data):
- Imports (first four): from rest_framework import serializers; from learning.models import LearningNote; from learning.api.serializers.common import ensure_owner, get_request_user
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/learning_path_serializers.py
- Type/area: Python API source
- Definitions: class LearningPathSerializer(serializers.ModelSerializer):; class Meta:; def validate_goal(self, goal):; def validate(self, attrs):; def create(self, validated_data):; class LearningTopicMinimalSerializer(serializers.ModelSerializer):; class Meta:; class LearningTopicSerializer(serializers.ModelSerializer):; class Meta:; def get_path_detail(self, obj):; def validate_path(self, path):; def validate_skill(self, skill):; def validate_prerequisites(self, prerequisites):; class LearningPathTopicSummarySerializer(; class Meta:; def get_goal(self, obj):; class LearningTopicDetailSerializer(; class Meta:; def get_lesson(self, obj):; def get_references(self, obj):; def get_images(self, obj):; def get_knowledge_item(self, obj):; def get_reviews(self, obj):; def get_progress(self, obj):; def get_mastery(self, obj):; def get_next_topic(self, obj):; def get_ai(self, obj):; class LearningPathDetailSerializer(; class Meta(LearningPathSerializer.Meta):
- Imports (first four): from rest_framework import serializers; from learning.models import LearningPath, LearningTopic, LearningResource; from learning.api.serializers.application_review_serializers import ApplicationReviewSerializer; from learning.api.serializers.common import ensure_owner, get_request_user
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/learning_progress_serializers.py
- Type/area: Python API source
- Definitions: class LearningProgressSerializer(serializers.ModelSerializer):; class Meta:; def validate_topic(self, topic):; def create(self, validated_data):
- Imports (first four): from rest_framework import serializers; from learning.models import LearningProgress; from learning.api.serializers.common import ensure_owner, get_request_user
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/learning_resource_serializers.py
- Type/area: Python API source
- Definitions: class LearningResourceSerializer(serializers.ModelSerializer):; class Meta:; def get_file_url(self, obj):; def validate_topic(self, topic):; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from learning.models import LearningResource; from learning.api.serializers.common import ensure_owner, get_request_user
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/learning_revision_serializers.py
- Type/area: Python API source
- Definitions: class LearningRevisionSerializer(; class Meta:; def validate_topic(self, topic):; def validate_source_review(self, source_review):; def validate(self, attrs):; def create(self, validated_data):
- Imports (first four): from rest_framework import serializers; from learning.models import LearningRevision; from learning.api.serializers.application_review_serializers import ApplicationReviewSerializer; from learning.api.serializers.common import ensure_owner, get_request_user
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/learning_session_serializers.py
- Type/area: Python API source
- Definitions: class LearningSessionSerializer(serializers.ModelSerializer):; class Meta:; def validate_topic(self, topic):; def validate(self, attrs):; def create(self, validated_data):
- Imports (first four): from rest_framework import serializers; from learning.models import LearningSession; from learning.api.serializers.common import ensure_owner, get_request_user
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/lesson_serializers.py
- Type/area: Python API source
- Definitions: class LessonMinimalSerializer(serializers.ModelSerializer):; class Meta:; class LessonSerializer(serializers.ModelSerializer):; class Meta:; def validate_topic(self, topic):; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from learning.models import Lesson; from learning.api.serializers.common import ensure_owner, get_request_user
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/skill_serializers.py
- Type/area: Python API source
- Definitions: class SkillSerializer(serializers.ModelSerializer):; class Meta:; class SkillMinimalSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from learning.models import Skill
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .common import User, get_request_user, ensure_owner; from .skill_serializers import SkillSerializer, SkillMinimalSerializer; from .learning_goal_serializers import LearningGoalSerializer, LearningGoalDetailSerializer; from .learning_path_serializers import LearningPathSerializer, LearningTopicMinimalSerializer, LearningTopicSerializer, LearningPathTopicSummarySerializer, LearningTopicDetailSerializer, LearningPathDetailSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/application_review_views.py
- Type/area: Python API source
- Definitions: class ApplicationReviewViewSet(; def get_queryset(self):
- Imports (first four): from rest_framework import viewsets; from rest_framework.permissions import IsAuthenticated; from learning.models import ApplicationReview
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/application_submission_views.py
- Type/area: Python API source
- Definitions: class ApplicationSubmissionViewSet(; def get_queryset(self):; def get_serializer_class(self):; def perform_create(self, serializer):; def update(self, request, *args, **kwargs):; def partial_update(; def destroy(
- Imports (first four): from rest_framework import status, viewsets; from rest_framework.exceptions import PermissionDenied; from rest_framework.permissions import IsAuthenticated; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/assessment_attempt_views.py
- Type/area: Python API source
- Definitions: class AssessmentAttemptViewSet(; def get_queryset(self):
- Imports (first four): from rest_framework import viewsets; from rest_framework.permissions import IsAuthenticated; from learning.models import AssessmentAttempt; from learning.api.serializers import AssessmentAttemptSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/assessment_choice_views.py
- Type/area: Python API source
- Definitions: class AssessmentChoiceViewSet(; def get_queryset(self):; def perform_create(self, serializer):
- Imports (first four): from rest_framework import viewsets; from rest_framework.exceptions import PermissionDenied; from rest_framework.permissions import IsAuthenticated; from learning.models import AssessmentChoice
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/assessment_question_views.py
- Type/area: Python API source
- Definitions: class AssessmentQuestionViewSet(; def get_queryset(self):; def perform_create(self, serializer):
- Imports (first four): from rest_framework import viewsets; from rest_framework.exceptions import PermissionDenied; from rest_framework.permissions import IsAuthenticated; from learning.models import AssessmentQuestion
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/assessment_response_views.py
- Type/area: Python API source
- Definitions: class AssessmentResponseViewSet(; def get_queryset(self):; def perform_create(self, serializer):
- Imports (first four): from rest_framework import viewsets; from rest_framework.exceptions import PermissionDenied; from rest_framework.permissions import IsAuthenticated; from learning.models import AssessmentResponse
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/assessment_views.py
- Type/area: Python API source
- Definitions: class AssessmentViewSet(; def get_queryset(self):; def get_serializer_class(self):; def perform_create(self, serializer):; def learner(self, request, pk=None):; def analytics(self, request, pk=None):; def start(self, request, pk=None):; def submit(self, request, pk=None):
- Imports (first four): from django.db.models import Avg; from rest_framework import status, viewsets; from rest_framework.decorators import action; from rest_framework.exceptions import PermissionDenied
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/knowledge_application_views.py
- Type/area: Python API source
- Definitions: class KnowledgeApplicationViewSet(; def get_queryset(self):; def perform_create(self, serializer):; def submit(self, request, pk=None):; def review(self, request, pk=None):; def request_peer_review(self, request, pk=None):; def submit_peer_review(self, request, pk=None):; def history(self, request, pk=None):
- Imports (first four): from django.utils import timezone; from rest_framework import status, viewsets; from rest_framework.decorators import action; from rest_framework.exceptions import PermissionDenied
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/learning_goal_views.py
- Type/area: Python API source
- Definitions: class LearningGoalViewSet(; def get_queryset(self):; def get_serializer_class(self):; def perform_create(self, serializer):; def generate(self, request):; def dashboard(self, request):; def complete(self, request, pk=None):; def pause(self, request, pk=None):; def resume(self, request, pk=None):; def certificate(self, request, pk=None):; def export_plan(self, request, pk=None):
- Imports (first four): from django.db.models import Prefetch; from django.utils import timezone; from rest_framework import status, viewsets; from rest_framework.decorators import action
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/learning_note_views.py
- Type/area: Python API source
- Definitions: class LearningNoteViewSet(; def get_queryset(self):; def perform_create(self, serializer):
- Imports (first four): from rest_framework import viewsets; from rest_framework.exceptions import PermissionDenied; from rest_framework.permissions import IsAuthenticated; from learning.models import LearningNote
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/learning_path_views.py
- Type/area: Python API source
- Definitions: class LearningPathViewSet(; def get_queryset(self):; def get_serializer_class(self):; def perform_create(self, serializer):; def start(self, request, pk=None):; def complete(self, request, pk=None):; def pause(self, request, pk=None):; def analytics(self, request, pk=None):; def reorder_topics(self, request, pk=None):
- Imports (first four): from django.db import transaction; from django.utils import timezone; from rest_framework import status, viewsets; from rest_framework.decorators import action
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/learning_progress_views.py
- Type/area: Python API source
- Definitions: class LearningProgressViewSet(; def get_queryset(self):; def perform_create(self, serializer):; def perform_update(self, serializer):; def update_progress(self, request):; def summary(self, request):
- Imports (first four): from rest_framework import status, viewsets; from rest_framework.decorators import action; from rest_framework.exceptions import PermissionDenied; from rest_framework.permissions import IsAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/learning_resource_views.py
- Type/area: Python API source
- Definitions: class LearningResourceViewSet(; def get_queryset(self):; def perform_create(self, serializer):
- Imports (first four): from rest_framework import viewsets; from rest_framework.exceptions import PermissionDenied; from rest_framework.permissions import IsAuthenticated; from learning.models import LearningResource
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/learning_revision_views.py
- Type/area: Python API source
- Definitions: class LearningRevisionViewSet(; def get_queryset(self):; def perform_create(self, serializer):; def start(self, request, pk=None):; def complete(self, request, pk=None):; def snooze(self, request, pk=None):; def skip(self, request, pk=None):
- Imports (first four): from django.utils import timezone; from rest_framework import viewsets; from rest_framework.decorators import action; from rest_framework.exceptions import PermissionDenied
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/learning_session_views.py
- Type/area: Python API source
- Definitions: class LearningSessionViewSet(; def get_queryset(self):; def perform_create(self, serializer):; def finish(self, request, pk=None):
- Imports (first four): from django.utils import timezone; from rest_framework import viewsets; from rest_framework.decorators import action; from rest_framework.exceptions import PermissionDenied
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/learning_topic_views.py
- Type/area: Python API source
- Definitions: class LearningTopicViewSet(; def get_queryset(self):; def get_serializer_class(self):; def get_queryset_for_detail(self):; def get_object(self):; def perform_create(self, serializer):; def start(self, request, pk=None):; def complete(self, request, pk=None):; def skip(self, request, pk=None):; def bookmark(self, request, pk=None):; def generate_content(self, request, pk=None):
- Imports (first four): from django.db.models import Prefetch; from rest_framework import status, viewsets; from rest_framework.decorators import action; from rest_framework.exceptions import PermissionDenied, NotFound
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/lesson_views.py
- Type/area: Python API source
- Definitions: class LessonViewSet(; def get_queryset(self):; def perform_create(self, serializer):; def mark_complete(self, request, pk=None):
- Imports (first four): from rest_framework import viewsets; from rest_framework.decorators import action; from rest_framework.exceptions import PermissionDenied; from rest_framework.permissions import IsAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/skill_views.py
- Type/area: Python API source
- Definitions: class SkillViewSet(; def get_queryset(self):
- Imports (first four): from rest_framework import viewsets; from rest_framework.permissions import IsAuthenticated; from learning.models import Skill; from learning.api.serializers import SkillSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/user_owned_model_views.py
- Type/area: Python API source
- Definitions: class UserOwnedModelViewSet(
- Imports (first four): from rest_framework import viewsets; from rest_framework.permissions import IsAuthenticated; from learning.api.views.user_owned_queryset_mixin_views import UserOwnedQuerysetMixin
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/user_owned_queryset_mixin_views.py
- Type/area: Python API source
- Definitions: class UserOwnedQuerysetMixin:; def get_queryset(self):
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/user_owned_read_only_views.py
- Type/area: Python API source
- Definitions: class UserOwnedReadOnlyViewSet(
- Imports (first four): from rest_framework import viewsets; from rest_framework.permissions import IsAuthenticated; from learning.api.views.user_owned_queryset_mixin_views import UserOwnedQuerysetMixin
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .user_owned_queryset_mixin_views import UserOwnedQuerysetMixin; from .user_owned_model_views import UserOwnedModelViewSet; from .user_owned_read_only_views import UserOwnedReadOnlyViewSet; from .skill_views import SkillViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.core.validators; import django.db.models.deletion; import django.utils.timezone; from django.conf import settings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/application_review.py
- Type/area: Python model source
- Definitions: class ApplicationReview(models.Model):; class Mastery(models.TextChoices):; class Meta:; def clean(self):; def __str__(self):
- Imports (first four): from django.core.exceptions import ValidationError; from django.db import models; from django.utils import timezone; from learning.models.application_submission import ApplicationSubmission
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/application_submission.py
- Type/area: Python model source
- Definitions: class ApplicationSubmission(models.Model):; class Meta:; def __str__(self):
- Imports (first four): from django.db import models; from django.utils import timezone; from learning.models.knowledge_application import KnowledgeApplication
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/assessment.py
- Type/area: Python model source
- Definitions: class Assessment(models.Model):; class Type(models.TextChoices):; class Meta:; def __str__(self):
- Imports (first four): from django.db import models; from django.db.models import Q; from learning.models.common import MINUTES_VALIDATORS, SCORE_VALIDATORS; from learning.models.learning_topic import LearningTopic
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/assessment_attempt.py
- Type/area: Python model source
- Definitions: class AssessmentAttempt(models.Model):; class Meta:; def clean(self):; def __str__(self):
- Imports (first four): from django.conf import settings; from django.core.exceptions import ValidationError; from django.db import models; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/assessment_choice.py
- Type/area: Python model source
- Definitions: class AssessmentChoice(models.Model):; class Meta:; def __str__(self):
- Imports (first four): from django.db import models; from learning.models.assessment_question import AssessmentQuestion
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/assessment_question.py
- Type/area: Python model source
- Definitions: class AssessmentQuestion(models.Model):; class Type(models.TextChoices):; class Meta:; def __str__(self):
- Imports (first four): from django.db import models; from learning.models.assessment import Assessment
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/assessment_response.py
- Type/area: Python model source
- Definitions: class AssessmentResponse(models.Model):; class Meta:; def clean(self):; def __str__(self):
- Imports (first four): from django.core.exceptions import ValidationError; from django.db import models; from learning.models.assessment_attempt import AssessmentAttempt; from learning.models.assessment_choice import AssessmentChoice
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/common.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from django.core.validators import MinValueValidator, MaxValueValidator
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/knowledge_application.py
- Type/area: Python model source
- Definitions: class KnowledgeApplication(models.Model):; class Status(models.TextChoices):; class ApplicationType(models.TextChoices):; class Meta:; def clean(self):; def __str__(self):
- Imports (first four): from django.conf import settings; from django.core.exceptions import ValidationError; from django.db import models; from learning.models.learning_topic import LearningTopic
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/learning_goal.py
- Type/area: Python model source
- Definitions: class LearningGoal(models.Model):; class Status(models.TextChoices):; class Meta:; def __str__(self):
- Imports (first four): from django.conf import settings; from django.db import models; from learning.models.skill import Skill
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/learning_note.py
- Type/area: Python model source
- Definitions: class LearningNote(models.Model):; class NoteType(models.TextChoices):; class Meta:; def clean(self):; def __str__(self):
- Imports (first four): from django.conf import settings; from django.core.exceptions import ValidationError; from django.db import models; from learning.models.learning_topic import LearningTopic
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/learning_path.py
- Type/area: Python model source
- Definitions: class LearningPath(models.Model):; class Status(models.TextChoices):; class Meta:; def clean(self):; def __str__(self):
- Imports (first four): from django.conf import settings; from django.core.exceptions import ValidationError; from django.db import models; from learning.models.learning_goal import LearningGoal
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/learning_progress.py
- Type/area: Python model source
- Definitions: class LearningProgress(models.Model):; class Mastery(models.TextChoices):; class Meta:; def __str__(self):
- Imports (first four): from django.conf import settings; from django.core.validators import MinValueValidator, MaxValueValidator; from django.db import models; from django.db.models import Q
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/learning_resource.py
- Type/area: Python model source
- Definitions: class LearningResource(models.Model):; class ResourceType(models.TextChoices):; class Meta:; def clean(self):; def __str__(self):
- Imports (first four): from django.core.exceptions import ValidationError; from django.db import models; from learning.models.learning_topic import LearningTopic; from learning.models.lesson import Lesson
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/learning_revision.py
- Type/area: Python model source
- Definitions: class LearningRevision(models.Model):; class Status(models.TextChoices):; class Meta:; def clean(self):; def __str__(self):
- Imports (first four): from django.conf import settings; from django.core.exceptions import ValidationError; from django.db import models; from learning.models.application_review import ApplicationReview
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/learning_session.py
- Type/area: Python model source
- Definitions: class LearningSession(models.Model):; class ActivityType(models.TextChoices):; class Meta:; def clean(self):; def __str__(self):
- Imports (first four): from django.conf import settings; from django.core.exceptions import ValidationError; from django.db import models; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/learning_topic.py
- Type/area: Python model source
- Definitions: class LearningTopic(models.Model):; class Status(models.TextChoices):; class Difficulty(models.TextChoices):; class Meta:; def clean(self):; def __str__(self):
- Imports (first four): from django.core.exceptions import ValidationError; from django.db import models; from learning.models.common import MINUTES_VALIDATORS; from learning.models.learning_path import LearningPath
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/lesson.py
- Type/area: Python model source
- Definitions: class Lesson(models.Model):; class ContentFormat(models.TextChoices):; class Meta:; def clean(self):; def __str__(self):
- Imports (first four): from django.core.exceptions import ValidationError; from django.db import models; from learning.models.common import MINUTES_VALIDATORS; from learning.models.learning_topic import LearningTopic
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/skill.py
- Type/area: Python model source
- Definitions: class Skill(models.Model):; class Level(models.TextChoices):; class Meta:; def __str__(self):
- Imports (first four): from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .common import SCORE_VALIDATORS, MINUTES_VALIDATORS; from .learning_progress import PERCENT_VALIDATORS, LearningProgress; from .skill import Skill; from .learning_goal import LearningGoal
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/services/ai_content.py
- Type/area: Python service source
- Definitions: class LearningTopicAIContentService:; def __init__(; def generate(self, topic):; def _ensure_owner(self, topic):; def _system_prompt(self):; def _build_context(self, topic):; def _save_source_lesson(self, *, topic, knowledge):; def _save_lesson(self, *, topic, payload):; def _save_assessment(self, *, topic, payload):; def _parse_json(content):; def _validate_payload(payload):; def _truncate(value, limit):
- Imports (first four): import json; import re; from django.db import transaction; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/services/ai_service.py
- Type/area: Python service source
- Definitions: class LearningAIService:; def analyze_application(; def calculate_mastery(score):
- Imports (first four): from learning.models import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/services/assessment.py
- Type/area: Python service source
- Definitions: class AssessmentService:; def submit_attempt(
- Imports (first four): from learning.models import AssessmentAttempt
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/services/completion.py
- Type/area: Python service source
- Definitions: class LearningCompletionService:; def complete_topic(cls, *, user, topic):; def progress_summary(user):; def _goal_progress(goal):
- Imports (first four): from django.db import transaction; from django.utils import timezone; from learning.models import LearningGoal, LearningPath, LearningProgress, LearningTopic
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/services/learning.py
- Type/area: Python service source
- Definitions: class LearningService:; def create_path(; def create_topic(; def get_user_learning_overview(user):
- Imports (first four): from django.db import transaction; from learning.models import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/services/progress.py
- Type/area: Python service source
- Definitions: class ProgressService:; def update_progress(*, user, topic, progress_percent, practice_completed=None,
- Imports (first four): from django.db import IntegrityError, OperationalError, transaction; from django.utils import timezone; from learning.models import LearningProgress, LearningTopic; import time
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/services/services.py
- Type/area: Python service source
- Definitions: class ApplicationService:; def submit_application(; class ApplicationReviewService:; def save_review(; def update_learning_progress(; def create_revision_if_needed(; def calculate_mastery(score):; class AssessmentService:; def submit_attempt(; class LearningService:; def create_goal(; def create_path(; def create_topic(; def get_user_learning_overview(user):; class ProgressService:; def update_progress(
- Imports (first four): from django.db import transaction; from django.db.models import Max; from django.utils import timezone; from learning.models import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/services/__init__.py
- Type/area: Python service source
- Definitions: none matched
- Imports (first four): from .services import (; from .ai_service import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/tests/tests_completion_additions.py
- Type/area: Python test source
- Definitions: class TopicCompletionIntegrationTests(APITestCase):; def setUp(self):; def test_completion_returns_next_topic_and_persists(self):
- Imports (first four): from django.contrib.auth import get_user_model; from rest_framework.test import APITestCase; from learning.models import LearningGoal, LearningPath, LearningTopic, Skill
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/tests/test_learning.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): from django.test import TestCase
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## learning/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

