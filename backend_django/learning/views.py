

from rest_framework import (
    viewsets,
    status,
)

from rest_framework.permissions import (
    IsAuthenticated,
)

from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)

from rest_framework.decorators import (
    action,
)

from rest_framework.response import (
    Response,
)
from .models import (
    Skill,
    LearningGoal,
    LearningPath,
    LearningTopic,
    LearningProgress,
    Assessment,
    AssessmentAttempt,
)

from .serializers import (
    SkillSerializer,
    LearningGoalSerializer,
    LearningPathSerializer,
    LearningTopicSerializer,
    LearningProgressSerializer,
    AssessmentSerializer,
    AssessmentAttemptSerializer,
)

from .services import (
    ProgressService,
    AssessmentService,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone

from .models import (
    KnowledgeApplication,
    ApplicationReview,
)

from .serializers import (
    KnowledgeApplicationSerializer,
    ApplicationReviewSerializer,
    LearningTopicDetailSerializer,
)

from .services.services import (ApplicationService, ApplicationReviewService)

from .services.ai_service import LearningAIService


class UserOwnedQuerysetMixin:

    def get_queryset(self):
        queryset = super().get_queryset()

        if hasattr(self.queryset.model, "user"):
            return queryset.filter(user=self.request.user)

        return queryset


class SkillViewSet(viewsets.ModelViewSet):

    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    queryset = Skill.objects.all()


class LearningGoalViewSet(viewsets.ModelViewSet):

    serializer_class = LearningGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LearningGoal.objects.filter(
            user=self.request.user
        ).select_related("skill")

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class LearningPathViewSet(viewsets.ModelViewSet):

    serializer_class = LearningPathSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LearningPath.objects.filter(
            user=self.request.user
        ).select_related("goal")

    def perform_create(self, serializer):

        goal = serializer.validated_data["goal"]

        if goal.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "This learning goal does not belong to you."
            )

        serializer.save(
            user=self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="reorder-topics",
    )
    def reorder_topics(self, request, pk=None):

        path = self.get_object()

        topic_ids = request.data.get("topic_ids")

        if not isinstance(topic_ids, list):
            return Response(
                {
                    "detail": "topic_ids must be a list."
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
                "detail": "Topics reordered successfully.",
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


class LearningTopicViewSet(viewsets.ModelViewSet):

    serializer_class = LearningTopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LearningTopic.objects.filter(
            path__user=self.request.user
        ).select_related(
            "path",
            "skill",
        )

    def perform_create(self, serializer):

        path = serializer.validated_data["path"]

        if path.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this learning path."
            )

        order = serializer.validated_data.get("order")

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
        methods=["get"],
        url_path="detail",
    )
    def detail(self, request, pk=None):

        topic = self.get_object()

        topic = (
            self.get_queryset()
            .select_related(
                "path",
                "path__goal",
                "skill",
            )
            .prefetch_related(
                "knowledge_items",
                "applications",
                "assessments",
            )
            .get(
                pk=topic.pk
            )
        )

        return Response(
            LearningTopicDetailSerializer(
                topic,
                context={
                    "request": request
                },
            ).data
        )


class LearningProgressViewSet(viewsets.ModelViewSet):

    serializer_class = LearningProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LearningProgress.objects.filter(
            user=self.request.user
        ).select_related("topic")

    def perform_create(self, serializer):

        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "This topic does not belong to you."
            )

        serializer.save(
            user=self.request.user
        )

    def perform_update(self, serializer):

        topic = serializer.instance.topic

        if topic.path.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied

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
        progress_percent = request.data.get(
            "progress_percent"
        )

        if topic_id is None:
            return Response(
                {
                    "detail": "topic is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if progress_percent is None:
            return Response(
                {
                    "detail": "progress_percent is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            topic = LearningTopic.objects.get(
                id=topic_id,
                path__user=request.user,
            )

            progress = ProgressService.update_progress(
                user=request.user,
                topic=topic,
                progress_percent=int(progress_percent),
                practice_completed=request.data.get(
                    "practice_completed"
                ),
                notes=request.data.get("notes"),
            )

        except LearningTopic.DoesNotExist:
            return Response(
                {
                    "detail": "Topic not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValueError as exc:
            return Response(
                {
                    "detail": str(exc)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            LearningProgressSerializer(progress).data
        )


class AssessmentViewSet(viewsets.ModelViewSet):

    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Assessment.objects.filter(
            topic__path__user=self.request.user
        ).select_related("topic")

    def perform_create(self, serializer):

        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "This topic does not belong to you."
            )

        serializer.save()

    @action(
        detail=True,
        methods=["post"],
        url_path="submit",
    )
    def submit(self, request, pk=None):

        assessment = self.get_object()

        score = request.data.get("score")

        if score is None:
            return Response(
                {
                    "detail": "score is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            score = int(score)

            if score < 0 or score > 100:
                raise ValueError

        except ValueError:
            return Response(
                {
                    "detail": "score must be between 0 and 100."
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
            AssessmentAttemptSerializer(attempt).data,
            status=status.HTTP_201_CREATED,
        )


class AssessmentAttemptViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = AssessmentAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AssessmentAttempt.objects.filter(
            user=self.request.user
        ).select_related("assessment")


class KnowledgeApplicationViewSet(viewsets.ModelViewSet):

    serializer_class = KnowledgeApplicationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return (
            KnowledgeApplication.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "topic",
                "topic__path",
                "knowledge_item",
            )
            .prefetch_related(
                "review",
            )
        )

    def perform_create(self, serializer):

        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this topic."
            )

        knowledge_item = serializer.validated_data.get(
            "knowledge_item"
        )

        if knowledge_item:
            if knowledge_item.user_id != self.request.user.id:
                raise PermissionDenied(
                    "You do not own this knowledge item."
                )

            if (
                knowledge_item.learning_topic_id
                and knowledge_item.learning_topic_id != topic.id
            ):
                raise ValidationError(
                    "Knowledge item belongs to another topic."
                )

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

        return Response(
            KnowledgeApplicationSerializer(
                application,
                context={"request": request},
            ).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="review",
    )
    def review(self, request, pk=None):

        application = self.get_object()

        if application.status != "submitted":
            return Response(
                {
                    "detail": (
                        "Application must be submitted "
                        "before it can be reviewed."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ai_result = LearningAIService.analyze_application(
            topic=application.topic,
            application=application,
        )

        review = ApplicationReviewService.save_review(
            user=request.user,
            application=application,
            review_data=ai_result,
        )

        return Response(
            ApplicationReviewSerializer(
                review,
                context={"request": request},
            ).data
        )
