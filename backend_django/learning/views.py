# learning/views.py

from django.db import transaction
from django.db.models import Prefetch

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Skill,
    LearningGoal,
    LearningPath,
    LearningTopic,
    Lesson,
    LearningResource,
    LearningNote,
    LearningProgress,
    LearningSession,
    Assessment,
    AssessmentQuestion,
    AssessmentChoice,
    AssessmentAttempt,
    AssessmentResponse,
    KnowledgeApplication,
    ApplicationSubmission,
    ApplicationReview,
    LearningRevision,
)

from .serializers import (
    SkillSerializer,
    LearningGoalSerializer,
    LearningGoalDetailSerializer,
    LearningPathSerializer,
    LearningPathDetailSerializer,
    LearningTopicSerializer,
    LearningTopicDetailSerializer,
    LessonSerializer,
    LearningResourceSerializer,
    LearningNoteSerializer,
    LearningProgressSerializer,
    LearningSessionSerializer,
    AssessmentSerializer,
    AssessmentLearnerSerializer,
    AssessmentQuestionSerializer,
    AssessmentChoiceSerializer,
    AssessmentAttemptSerializer,
    AssessmentResponseSerializer,
    KnowledgeApplicationSerializer,
    ApplicationSubmissionSerializer,
    ApplicationReviewSerializer,
    LearningRevisionSerializer,
)

from .services import (
    ProgressService,
    AssessmentService,
)
from .services.completion import LearningCompletionService

from .services.services import (
    ApplicationService,
    ApplicationReviewService,
)

from .services.ai_service import (
    LearningAIService,
)


# ===================================================
# Base Mixins
# ===================================================


class UserOwnedQuerysetMixin:
    """
    Base queryset protection.

    Models that directly contain a `user` ForeignKey
    can use this mixin.
    """

    def get_queryset(self):
        queryset = super().get_queryset()

        model = queryset.model

        if hasattr(model, "user"):
            return queryset.filter(
                user=self.request.user
            )

        return queryset


class UserOwnedModelViewSet(
    UserOwnedQuerysetMixin,
    viewsets.ModelViewSet,
):
    permission_classes = [IsAuthenticated]


class UserOwnedReadOnlyViewSet(
    UserOwnedQuerysetMixin,
    viewsets.ReadOnlyModelViewSet,
):
    permission_classes = [IsAuthenticated]


# ===================================================
# Skill
# ===================================================


class SkillViewSet(
    viewsets.ReadOnlyModelViewSet
):
    """
    Skills are global system entities.

    Learners can read them but should not create,
    modify, or delete global skills.
    """

    queryset = Skill.objects.filter(
        is_active=True
    )

    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get(
            "category"
        )

        if category:
            queryset = queryset.filter(
                category=category
            )

        return queryset


# ===================================================
# Learning Goal
# ===================================================


class LearningGoalViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            LearningGoal.objects
            .filter(
                user=self.request.user
            )
            .select_related("skill")
            .prefetch_related(
                Prefetch(
                    "paths",
                    queryset=(
                        LearningPath.objects
                        .filter(user=self.request.user)
                        .select_related("goal", "goal__skill")
                        .prefetch_related("topics")
                        .order_by("-created_at")
                    ),
                )
            )
        )

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LearningGoalDetailSerializer

        return LearningGoalSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="generate",
    )
    def generate(self, request):
        """Generate a real AI learning plan and persist it atomically."""
        message = (
            request.data.get("message")
            or request.data.get("prompt")
            or ""
        ).strip()

        if not message:
            return Response(
                {"success": False, "error": "message is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from ai.learning_actions import (
            AILearningActionService,
            looks_like_learning_request,
        )
        from ai.services import AIService

        if not looks_like_learning_request(message):
            return Response(
                {
                    "success": False,
                    "error": "Please describe what you want to learn.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        provider = request.data.get("provider") or "ollama"
        model = request.data.get("model") or ""

        try:
            plan = AILearningActionService.generate_ai_plan(
                message=message,
                provider=provider,
                model=model,
            )

            result = AILearningActionService(
                user=request.user
            ).create_learning_plan(
                skill_name=plan["skill"],
                level=plan.get("level", "beginner"),
                target_level=plan.get("target_level", "advanced"),
                goal_title=plan.get("goal_title") or None,
                goal_description=plan.get("goal_description", ""),
                reason=plan.get("reason", ""),
                path_title=plan.get("path_title") or None,
                path_description=plan.get("path_description", ""),
                topics=plan.get("topics") or [],
            )

            data = AIService(request.user).serialize_learning_result(result)

            return Response(
                {
                    "success": True,
                    "learning": data,
                    "learning_action": {
                        "type": "create_learning_plan",
                        "status": (
                            "created" if result["created"] else "already_exists"
                        ),
                        "provider": plan.get("provider"),
                        "model": plan.get("model"),
                    },
                },
                status=status.HTTP_201_CREATED if result["created"] else status.HTTP_200_OK,
            )
        except Exception as exc:
            return Response(
                {
                    "success": False,
                    "error": str(exc),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

    @action(
        detail=False,
        methods=["get"],
        url_path="dashboard",
    )
    def dashboard(self, request):
        """Return the complete persisted learning tree for the Learning page."""
        goals = self.get_queryset().order_by("-created_at")

        payload = []
        for goal in goals:
            goal_data = LearningGoalSerializer(
                goal, context={"request": request}
            ).data

            paths = []
            for path in goal.paths.all():
                path_data = LearningPathDetailSerializer(
                    path, context={"request": request}
                ).data
                paths.append(path_data)

            goal_data["paths"] = paths
            payload.append(goal_data)

        return Response(
            {
                "success": True,
                "count": len(payload),
                "goals": payload,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="complete",
    )
    def complete(self, request, pk=None):
        goal = self.get_object()

        goal.status = LearningGoal.Status.COMPLETED

        if not goal.completed_at:
            from django.utils import timezone

            goal.completed_at = timezone.now()

        goal.save(
            update_fields=[
                "status",
                "completed_at",
                "updated_at",
            ]
        )

        return Response(
            self.get_serializer(goal).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="pause",
    )
    def pause(self, request, pk=None):
        goal = self.get_object()

        goal.status = LearningGoal.Status.PAUSED

        goal.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return Response(
            self.get_serializer(goal).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="resume",
    )
    def resume(self, request, pk=None):
        goal = self.get_object()

        goal.status = LearningGoal.Status.ACTIVE

        goal.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return Response(
            self.get_serializer(goal).data
        )


# ===================================================
# Learning Path
# ===================================================


class LearningPathViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            LearningPath.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "goal",
                "goal__skill",
            )
            .prefetch_related(
                "topics",
            )
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LearningPathDetailSerializer

        return LearningPathSerializer

    def perform_create(self, serializer):
        goal = serializer.validated_data["goal"]

        if goal.user_id != self.request.user.id:
            raise PermissionDenied(
                "This learning goal does not belong to you."
            )

        serializer.save(
            user=self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="start",
    )
    def start(self, request, pk=None):
        path = self.get_object()

        from django.utils import timezone

        path.status = LearningPath.Status.ACTIVE

        if not path.started_at:
            path.started_at = timezone.now()

        path.save(
            update_fields=[
                "status",
                "started_at",
                "updated_at",
            ]
        )

        return Response(
            self.get_serializer(path).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="complete",
    )
    def complete(self, request, pk=None):
        path = self.get_object()

        from django.utils import timezone

        path.status = LearningPath.Status.COMPLETED
        path.completed_at = timezone.now()

        path.save(
            update_fields=[
                "status",
                "completed_at",
                "updated_at",
            ]
        )

        return Response(
            self.get_serializer(path).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="pause",
    )
    def pause(self, request, pk=None):
        path = self.get_object()

        path.status = LearningPath.Status.PAUSED

        path.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return Response(
            self.get_serializer(path).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="reorder-topics",
    )
    def reorder_topics(self, request, pk=None):
        """
        Reorder all topics in a learning path.

        Expected:

        {
            "topic_ids": [12, 15, 13, 20]
        }
        """

        path = self.get_object()

        topic_ids = request.data.get(
            "topic_ids"
        )

        if not isinstance(topic_ids, list):
            return Response(
                {
                    "detail": (
                        "topic_ids must be a list."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not topic_ids:
            return Response(
                {
                    "detail": (
                        "topic_ids cannot be empty."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # Remove duplicates
        # ----------------------------------------------------

        if len(topic_ids) != len(set(topic_ids)):
            return Response(
                {
                    "detail": (
                        "topic_ids must not contain duplicates."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        topics = list(
            path.topics.filter(
                id__in=topic_ids
            )
        )

        if len(topics) != len(topic_ids):
            return Response(
                {
                    "detail": (
                        "All topic_ids must belong "
                        "to this learning path."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        topic_map = {
            topic.id: topic
            for topic in topics
        }

        # ----------------------------------------------------
        # Important:
        #
        # path + order is UNIQUE.
        #
        # So we cannot directly swap:
        #
        # A = 1
        # B = 2
        #
        # into:
        #
        # A = 2
        # B = 1
        #
        # because the DB can reject the intermediate state.
        #
        # First move everything to temporary negative orders.
        # ----------------------------------------------------

        with transaction.atomic():

            for index, topic_id in enumerate(topic_ids):
                topic = topic_map[topic_id]

                topic.order = -(
                    index + 1
                )

                topic.save(
                    update_fields=[
                        "order",
                        "updated_at",
                    ]
                )

            for index, topic_id in enumerate(topic_ids):
                topic = topic_map[topic_id]

                topic.order = index + 1

                topic.save(
                    update_fields=[
                        "order",
                        "updated_at",
                    ]
                )

        return Response(
            {
                "detail": (
                    "Topics reordered successfully."
                ),
                "topics": [
                    {
                        "id": topic_id,
                        "order": index + 1,
                    }
                    for index, topic_id
                    in enumerate(topic_ids)
                ],
            }
        )


# ===================================================
# Learning Topic
# ===================================================


class LearningTopicViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            LearningTopic.objects
            .filter(
                path__user=self.request.user
            )
            .select_related(
                "path",
                "path__goal",
                "skill",
                "knowledge_item",
            )
        )

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LearningTopicDetailSerializer

        return LearningTopicSerializer

    def get_queryset_for_detail(self):
        current_user = self.request.user

        current_progress = (
            LearningProgress.objects
            .filter(
                user=current_user,
            )
            .order_by("-updated_at")
        )

        current_applications = (
            KnowledgeApplication.objects
            .filter(
                user=current_user,
            )
            .prefetch_related(
                "reviews",
                "submissions",
            )
            .order_by("-updated_at")
        )

        current_notes = (
            LearningNote.objects
            .filter(
                user=current_user,
            )
            .order_by("-updated_at")
        )

        return (
            self.get_queryset()

            .select_related(
                "path",
                "path__goal",
                "path__goal__skill",
                "skill",
                "knowledge_item",
            )

            .prefetch_related(
                "prerequisites",

                "lessons",

                "resources",

                "assessments",

                Prefetch(
                    "progress_records",
                    queryset=current_progress,
                    to_attr="_current_user_progress",
                ),

                Prefetch(
                    "applications",
                    queryset=current_applications,
                ),

                Prefetch(
                    "notes",
                    queryset=current_notes,
                ),
            )
        )

    def get_object(self):
        if self.action == "retrieve":
            queryset = self.get_queryset_for_detail()

            obj = queryset.filter(
                pk=self.kwargs["pk"]
            ).first()

            if obj is None:
                from rest_framework.exceptions import NotFound

                raise NotFound(
                    "Learning topic not found."
                )

            self.check_object_permissions(
                self.request,
                obj,
            )

            return obj

        return super().get_object()

    def perform_create(self, serializer):
        path = serializer.validated_data["path"]

        if path.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this learning path."
            )

        order = serializer.validated_data.get(
            "order"
        )

        if order is None:
            last_topic = (
                LearningTopic.objects
                .filter(path=path)
                .order_by("-order")
                .first()
            )

            order = (
                last_topic.order + 1
                if last_topic
                else 1
            )

        serializer.save(
            order=order
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="start",
    )
    def start(self, request, pk=None):
        topic = self.get_object()

        topic.status = LearningTopic.Status.IN_PROGRESS

        topic.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return Response(
            self.get_serializer(topic).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="complete",
    )
    def complete(self, request, pk=None):
        topic = self.get_object()

        result = LearningCompletionService.complete_topic(user=request.user, topic=topic)
        topic = result["topic"]
        payload = self.get_serializer(topic).data
        payload["next_topic"] = (
            {"id": result["next_topic"].id, "title": result["next_topic"].title, "order": result["next_topic"].order}
            if result["next_topic"] else None
        )
        return Response(payload)

    @action(
        detail=True,
        methods=["post"],
        url_path="skip",
    )
    def skip(self, request, pk=None):
        topic = self.get_object()

        topic.status = LearningTopic.Status.SKIPPED

        topic.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return Response(
            self.get_serializer(topic).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="generate-content",
    )
    def generate_content(self, request, pk=None):
        topic = self.get_object()

        from .services.ai_content import (
            LearningTopicAIContentService,
        )

        provider = (
            request.data.get("provider")
            or "ollama"
        )

        model = (
            request.data.get("model")
            or ""
        )

        try:
            result = LearningTopicAIContentService(
                user=request.user,
                provider=provider,
                model=model,
            ).generate(topic)

            topic.refresh_from_db()

            return Response(
                {
                    "success": True,
                    "topic": LearningTopicDetailSerializer(
                        topic,
                        context={
                            "request": request,
                        },
                    ).data,
                    "ai": {
                        "provider": result["provider"],
                        "model": result["model"],
                        "generated_at": result["generated_at"],
                        "status": "ready",
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as exc:
            return Response(
                {
                    "success": False,
                    "error": str(exc),
                    "ai": {
                        "status": "failed",
                    },
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

# ===================================================
# Lesson
# ===================================================


class LessonViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Lesson.objects
            .filter(
                topic__path__user=self.request.user
            )
            .select_related(
                "topic",
                "topic__path",
            )
            .prefetch_related(
                "resources",
            )
        )

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this learning topic."
            )

        serializer.save()


# ===================================================
# Learning Resource
# ===================================================


class LearningResourceViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            LearningResource.objects
            .filter(
                topic__path__user=self.request.user
            )
            .select_related(
                "topic",
                "lesson",
            )
        )

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this learning topic."
            )

        lesson = serializer.validated_data.get(
            "lesson"
        )

        if lesson and lesson.topic_id != topic.id:
            raise PermissionDenied(
                "Lesson does not belong to this topic."
            )

        serializer.save()


# ===================================================
# Learning Notes
# ===================================================


class LearningNoteViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = LearningNoteSerializer

    def get_queryset(self):
        return (
            LearningNote.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "topic",
                "lesson",
                "knowledge_item",
            )
        )

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this learning topic."
            )

        serializer.save(
            user=self.request.user
        )


# ===================================================
# Learning Progress
# ===================================================


class LearningProgressViewSet(
    viewsets.ModelViewSet
):
    serializer_class = LearningProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            LearningProgress.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "topic",
                "topic__path",
            )
        )

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "This topic does not belong to you."
            )

        serializer.save(
            user=self.request.user
        )

    def perform_update(self, serializer):
        topic = serializer.instance.topic

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "This topic does not belong to you."
            )

        serializer.save()

    @action(
        detail=False,
        methods=["post"],
        url_path="update-progress",
    )
    def update_progress(self, request):
        topic_id = request.data.get("topic")

        if topic_id is None:
            return Response(
                {
                    "detail": "topic is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        progress_percent = request.data.get(
            "progress_percent"
        )

        if progress_percent is None:
            return Response(
                {
                    "detail": (
                        "progress_percent is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            progress_percent = int(
                progress_percent
            )

            if not 0 <= progress_percent <= 100:
                raise ValueError

        except (TypeError, ValueError):
            return Response(
                {
                    "detail": (
                        "progress_percent must be "
                        "between 0 and 100."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            topic = (
                LearningTopic.objects
                .select_related("path")
                .get(
                    id=topic_id,
                    path__user=request.user,
                )
            )

        except LearningTopic.DoesNotExist:
            return Response(
                {
                    "detail": "Topic not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            progress = (
                ProgressService.update_progress(
                    user=request.user,
                    topic=topic,
                    progress_percent=progress_percent,
                    practice_completed=request.data.get("practice_completed"),
                    notes=request.data.get("notes"),
                    lesson_completed=request.data.get("lesson_completed"),
                    quick_check_completed=request.data.get("quick_check_completed"),
                    assessment_completed=request.data.get("assessment_completed"),
                )
            )

        except ValueError as exc:
            return Response(
                {
                    "detail": str(exc)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            LearningProgressSerializer(
                progress,
                context={
                    "request": request
                },
            ).data
        )

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        from .services.completion import LearningCompletionService
        return Response(LearningCompletionService.progress_summary(request.user))

# ===================================================
# Learning Sessions
# ===================================================


class LearningSessionViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            LearningSession.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "topic",
                "lesson",
            )
        )

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this topic."
            )

        serializer.save(
            user=self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="finish",
    )
    def finish(self, request, pk=None):
        session = self.get_object()

        from django.utils import timezone

        ended_at = timezone.now()

        session.ended_at = ended_at
        session.completed = True

        if session.started_at:
            session.duration_seconds = max(
                0,
                int(
                    (
                        ended_at
                        - session.started_at
                    ).total_seconds()
                ),
            )

        session.save(
            update_fields=[
                "ended_at",
                "completed",
                "duration_seconds",
            ]
        )

        return Response(
            self.get_serializer(session).data
        )


# ===================================================
# Assessment
# ===================================================


class AssessmentViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Assessment.objects
            .filter(
                topic__path__user=self.request.user
            )
            .select_related(
                "topic",
                "topic__path",
            )
            .prefetch_related(
                "questions",
                "questions__choices",
            )
        )

    def get_serializer_class(self):
        if self.action in [
            "list",
            "retrieve",
            "start",
        ]:
            return AssessmentLearnerSerializer

        return AssessmentSerializer

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "This topic does not belong to you."
            )

        serializer.save()

    @action(
        detail=True,
        methods=["get"],
        url_path="learner",
    )
    def learner(self, request, pk=None):
        assessment = self.get_object()

        serializer = AssessmentLearnerSerializer(
            assessment,
            context={
                "request": request
            },
        )

        return Response(
            serializer.data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="start",
    )
    def start(self, request, pk=None):
        assessment = self.get_object()

        attempt = AssessmentAttempt.objects.create(
            assessment=assessment,
            user=request.user,
            attempt_number=(
                AssessmentAttempt.objects.filter(
                    assessment=assessment,
                    user=request.user,
                ).count()
                + 1
            ),
        )

        return Response(
            AssessmentAttemptSerializer(
                attempt,
                context={
                    "request": request
                },
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="submit",
    )
    def submit(self, request, pk=None):
        assessment = self.get_object()

        score = request.data.get(
            "score"
        )

        if score is None:
            return Response(
                {
                    "detail": (
                        "score is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            score = int(score)

        except (TypeError, ValueError):
            return Response(
                {
                    "detail": (
                        "score must be a number."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not 0 <= score <= 100:
            return Response(
                {
                    "detail": (
                        "score must be between "
                        "0 and 100."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        attempt = AssessmentService.submit_attempt(
            user=request.user,
            assessment=assessment,
            score=score,
            feedback=request.data.get(
                "feedback",
                "",
            ),
        )

        return Response(
            AssessmentAttemptSerializer(
                attempt,
                context={
                    "request": request
                },
            ).data,
            status=status.HTTP_201_CREATED,
        )


# ===================================================
# Assessment Questions
# ===================================================


class AssessmentQuestionViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            AssessmentQuestion.objects
            .filter(
                assessment__topic__path__user=(
                    self.request.user
                )
            )
            .select_related(
                "assessment",
            )
            .prefetch_related(
                "choices",
            )
        )

    def perform_create(self, serializer):
        assessment = serializer.validated_data[
            "assessment"
        ]

        if (
            assessment.topic.path.user_id
            != self.request.user.id
        ):
            raise PermissionDenied(
                "You do not own this assessment."
            )

        serializer.save()


# ===================================================
# Assessment Choices
# ===================================================


class AssessmentChoiceViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            AssessmentChoice.objects
            .filter(
                question__assessment__topic__path__user=(
                    self.request.user
                )
            )
            .select_related(
                "question",
                "question__assessment",
            )
        )

    def perform_create(self, serializer):
        question = serializer.validated_data[
            "question"
        ]

        if (
            question.assessment.topic.path.user_id
            != self.request.user.id
        ):
            raise PermissionDenied(
                "You do not own this assessment."
            )

        serializer.save()


# ===================================================
# Assessment Attempts
# ===================================================


class AssessmentAttemptViewSet(
    viewsets.ReadOnlyModelViewSet
):
    serializer_class = AssessmentAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            AssessmentAttempt.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "assessment",
                "assessment__topic",
            )
            .prefetch_related(
                "responses",
                "responses__question",
                "responses__selected_choices",
            )
        )

# ===================================================
# Assessment Responses
# ===================================================


class AssessmentResponseViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            AssessmentResponse.objects
            .filter(
                attempt__user=self.request.user
            )
            .select_related(
                "attempt",
                "question",
            )
            .prefetch_related(
                "selected_choices",
            )
        )

    def perform_create(self, serializer):
        attempt = serializer.validated_data[
            "attempt"
        ]

        if attempt.user_id != self.request.user.id:
            raise PermissionDenied(
                "This attempt does not belong to you."
            )

        serializer.save()


# ===================================================
# Knowledge Application
# ===================================================


class KnowledgeApplicationViewSet(
    viewsets.ModelViewSet
):
    serializer_class = KnowledgeApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            KnowledgeApplication.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "topic",
                "topic__path",
                "lesson",
                "knowledge_item",
            )
            .prefetch_related(
                "submissions",
                "reviews",
            )
        )

    def perform_create(self, serializer):
        topic = serializer.validated_data[
            "topic"
        ]

        if (
            topic.path.user_id
            != self.request.user.id
        ):
            raise PermissionDenied(
                "You do not own this topic."
            )

        lesson = serializer.validated_data.get(
            "lesson"
        )

        if lesson and lesson.topic_id != topic.id:
            raise PermissionDenied(
                "Lesson does not belong to this topic."
            )

        knowledge_item = (
            serializer.validated_data.get(
                "knowledge_item"
            )
        )

        if knowledge_item:

            if (
                knowledge_item.user_id
                != self.request.user.id
            ):
                raise PermissionDenied(
                    "You do not own this knowledge item."
                )

            serializer_topic_id = topic.id

            # The KnowledgeItem model may or may not
            # contain a direct learning_topic field.
            #
            # We intentionally do not assume a field
            # that does not exist in the current model.
            #
            # Relationship validation should be handled
            # by the knowledge application service when
            # needed.

        serializer.save(
            user=self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="submit",
    )
    def submit(self, request, pk=None):
        application = self.get_object()

        ApplicationService.submit_application(
            user=request.user,
            application=application,
        )

        application.refresh_from_db()

        return Response(
            KnowledgeApplicationSerializer(
                application,
                context={
                    "request": request
                },
            ).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="review",
    )
    def review(self, request, pk=None):
        """
        Run AI analysis against the submitted application.

        Flow:

        Application
              ↓
        AI Service
              ↓
        ApplicationReview
              ↓
        LearningRevision
        """

        application = self.get_object()

        if (
            application.status
            != KnowledgeApplication.Status.SUBMITTED
        ):
            return Response(
                {
                    "detail": (
                        "Application must be submitted "
                        "before it can be reviewed."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ai_result = (
            LearningAIService.analyze_application(
                topic=application.topic,
                application=application,
            )
        )

        review = (
            ApplicationReviewService.save_review(
                user=request.user,
                application=application,
                review_data=ai_result,
            )
        )

        return Response(
            ApplicationReviewSerializer(
                review,
                context={
                    "request": request
                },
            ).data
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="history",
    )
    def history(self, request, pk=None):
        application = self.get_object()

        submissions = (
            application.submissions.all()
        )

        reviews = (
            application.reviews.all()
        )

        return Response(
            {
                "application": (
                    KnowledgeApplicationSerializer(
                        application,
                        context={
                            "request": request
                        },
                    ).data
                ),
                "submissions": (
                    ApplicationSubmissionSerializer(
                        submissions,
                        many=True,
                        context={
                            "request": request
                        },
                    ).data
                ),
                "reviews": (
                    ApplicationReviewSerializer(
                        reviews,
                        many=True,
                        context={
                            "request": request
                        },
                    ).data
                ),
            }
        )


# ===================================================
# Application Submissions
# ===================================================


class ApplicationSubmissionViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            ApplicationSubmission.objects
            .filter(
                application__user=self.request.user
            )
            .select_related(
                "application",
            )
        )

    def get_serializer_class(self):
        return ApplicationSubmissionSerializer

    def perform_create(self, serializer):
        application = serializer.validated_data[
            "application"
        ]

        if application.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this application."
            )

        serializer.save()

    def update(self, request, *args, **kwargs):
        return Response(
            {
                "detail": (
                    "Application submissions are immutable."
                )
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(
        self,
        request,
        *args,
        **kwargs,
    ):
        return Response(
            {
                "detail": (
                    "Application submissions are immutable."
                )
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(
        self,
        request,
        *args,
        **kwargs,
    ):
        return Response(
            {
                "detail": (
                    "Application submissions are immutable."
                )
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


# ===================================================
# Application Reviews
# ===================================================


class ApplicationReviewViewSet(
    viewsets.ReadOnlyModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            ApplicationReview.objects
            .filter(
                application__user=self.request.user
            )
            .select_related(
                "application",
                "submission",
                "submission__application",
            )
        )


# ===================================================
# Learning Revisions
# ===================================================


class LearningRevisionViewSet(
    viewsets.ModelViewSet
):
    serializer_class = LearningRevisionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            LearningRevision.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "topic",
                "source_review",
                "source_review__application",
                "source_review__submission",
            )
        )

    def perform_create(self, serializer):
        topic = serializer.validated_data[
            "topic"
        ]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this topic."
            )

        source_review = (
            serializer.validated_data.get(
                "source_review"
            )
        )

        if source_review:
            if (
                source_review.application.user_id
                != self.request.user.id
            ):
                raise PermissionDenied(
                    "You do not own this review."
                )

        serializer.save(
            user=self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="start",
    )
    def start(self, request, pk=None):
        revision = self.get_object()

        from django.utils import timezone

        revision.status = (
            LearningRevision.Status.IN_PROGRESS
        )
        revision.started_at = timezone.now()

        revision.save(
            update_fields=[
                "status",
                "started_at",
                "updated_at",
            ]
        )

        return Response(
            self.get_serializer(
                revision
            ).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="complete",
    )
    def complete(self, request, pk=None):
        revision = self.get_object()

        from django.utils import timezone

        revision.status = (
            LearningRevision.Status.COMPLETED
        )
        revision.completed_at = timezone.now()

        outcome = request.data.get(
            "outcome"
        )

        if outcome is not None:
            revision.outcome = outcome

        update_fields = [
            "status",
            "completed_at",
            "updated_at",
        ]

        if outcome is not None:
            update_fields.append(
                "outcome"
            )

        revision.save(
            update_fields=update_fields
        )

        return Response(
            self.get_serializer(
                revision
            ).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="skip",
    )
    def skip(self, request, pk=None):
        revision = self.get_object()

        revision.status = (
            LearningRevision.Status.SKIPPED
        )

        revision.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return Response(
            self.get_serializer(
                revision
            ).data
        )
