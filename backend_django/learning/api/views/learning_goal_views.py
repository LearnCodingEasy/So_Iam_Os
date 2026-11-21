from django.db.models import Prefetch
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from learning.models import LearningGoal, LearningPath
from learning.api.serializers import LearningGoalSerializer, LearningGoalDetailSerializer, LearningPathDetailSerializer


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
                user=request.user,
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

    @action(
        detail=True,
        methods=["get"],
        url_path="certificate",
    )
    def certificate(self, request, pk=None):
        """[منصات عالمية - Coursera / edX] إصدار شهادة إتمام الهدف التعليمي."""
        goal = self.get_object()
        if goal.status != LearningGoal.Status.COMPLETED:
            return Response(
                {"success": False,
                    "detail": "Goal is not completed yet. Certificate is locked."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({
            "success": True,
            "certificate": {
                "recipient": request.user.get_full_name() or request.user.username,
                "goal_title": goal.title,
                "skill": goal.skill.name if goal.skill else "General Learning",
                "issued_at": goal.completed_at or timezone.now(),
                "verification_code": f"CERT-{request.user.id}-{goal.id}-{timezone.now().strftime('%Y%m%d')}",
                "issuer": "Modern Learning Management System"
            }
        })

    @action(
        detail=True,
        methods=["post"],
        url_path="export-plan",
    )
    def export_plan(self, request, pk=None):
        """[ميزة تعليمية عالمية] تصدير المسار والهدف بصيغة هيكلية قابلة للمشاركة."""
        goal = self.get_object()
        serializer = LearningGoalDetailSerializer(
            goal, context={"request": request})
        return Response({
            "success": True,
            "exported_at": timezone.now(),
            "data": serializer.data
        })
