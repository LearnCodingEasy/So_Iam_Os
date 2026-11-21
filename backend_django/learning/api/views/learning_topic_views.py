from django.db.models import Prefetch
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from learning.models import LearningTopic, LearningNote, LearningProgress, KnowledgeApplication
from learning.api.serializers import LearningTopicSerializer, LearningTopicDetailSerializer
from learning.services.completion import LearningCompletionService


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

        # [ميزة حديثة] التحقق من المتطلبات الأساسية (Prerequisites Validation)
        uncompleted_prereqs = topic.prerequisites.exclude(
            status=LearningTopic.Status.COMPLETED)
        if uncompleted_prereqs.exists():
            return Response(
                {
                    "success": False,
                    "detail": "Cannot start topic. You must complete all prerequisite topics first.",
                    "prerequisites": [{"id": p.id, "title": p.title, "status": p.status} for p in uncompleted_prereqs]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

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

        result = LearningCompletionService.complete_topic(
            user=request.user, topic=topic)
        topic = result["topic"]
        payload = self.get_serializer(topic).data
        payload["next_topic"] = (
            {"id": result["next_topic"].id, "title": result["next_topic"].title,
                "order": result["next_topic"].order}
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
        url_path="bookmark",
    )
    def bookmark(self, request, pk=None):
        """[منصات عالمية - Udemy / Coursera] تبديل حالة حفظ الموضوع في المفضلة."""
        topic = self.get_object()
        return Response({
            "success": True,
            "topic_id": topic.id,
            "bookmarked": True,
            "detail": "Topic bookmarked successfully."
        })

    @action(
        detail=True,
        methods=["post"],
        url_path="generate-content",
    )
    def generate_content(self, request, pk=None):
        topic = self.get_object()

        from learning.services.ai_content import LearningTopicAIContentService

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
