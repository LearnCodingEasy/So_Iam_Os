from django.db.models import Avg
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from learning.models import Assessment, AssessmentAttempt
from learning.api.serializers import AssessmentSerializer, AssessmentLearnerSerializer, AssessmentAttemptSerializer
from learning.services import AssessmentService


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
        methods=["get"],
        url_path="analytics",
    )
    def analytics(self, request, pk=None):
        """[تحليلات التقييمات] تحليل محاولات واختبارات المتعلم."""
        assessment = self.get_object()
        attempts = AssessmentAttempt.objects.filter(
            assessment=assessment, user=request.user)
        total_attempts = attempts.count()
        best_score = attempts.order_by(
            "-score").first().score if total_attempts > 0 else 0
        avg_score = attempts.aggregate(Avg("score"))["score__avg"] or 0

        return Response({
            "success": True,
            "assessment_id": assessment.id,
            "title": assessment.title,
            "total_attempts": total_attempts,
            "best_score": best_score,
            "average_score": round(avg_score, 2),
        })

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
