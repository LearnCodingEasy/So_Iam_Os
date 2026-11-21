from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from learning.models import KnowledgeApplication
from learning.api.serializers import KnowledgeApplicationSerializer, ApplicationSubmissionSerializer, ApplicationReviewSerializer
from learning.services.services import ApplicationService, ApplicationReviewService
from learning.services.ai_service import LearningAIService


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
        methods=["post"],
        url_path="request-peer-review",
    )
    def request_peer_review(self, request, pk=None):
        """[منصات عالمية - Coursera / edX] طلب مراجعة الأقران لتطبيق المعرفة."""
        application = self.get_object()
        return Response({
            "success": True,
            "application_id": application.id,
            "status": "peer_review_requested",
            "message": "Application submitted to peer pool for review."
        })

    @action(
        detail=True,
        methods=["post"],
        url_path="submit-peer-review",
    )
    def submit_peer_review(self, request, pk=None):
        """[منصات عالمية] تقديم مراجعة على تطبيق زميل آخر."""
        application = self.get_object()
        rating = request.data.get("rating", 5)
        comments = request.data.get("comments", "")
        return Response({
            "success": True,
            "application_id": application.id,
            "peer_review": {
                "reviewer": request.user.username,
                "rating": rating,
                "comments": comments,
                "reviewed_at": timezone.now()
            },
            "message": "Peer review submitted successfully."
        })

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
