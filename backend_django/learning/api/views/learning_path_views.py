from django.db import transaction
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from learning.models import LearningPath, LearningTopic
from learning.api.serializers import LearningPathSerializer, LearningPathDetailSerializer


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
        methods=["get"],
        url_path="analytics",
    )
    def analytics(self, request, pk=None):
        """[ميزة تحليلات التعليم الحديث] إحصائيات شاملة للمسار ونسب الإنجاز."""
        path = self.get_object()
        topics = path.topics.all()
        total_topics = topics.count()
        completed_topics = topics.filter(
            status=LearningTopic.Status.COMPLETED).count()
        in_progress_topics = topics.filter(
            status=LearningTopic.Status.IN_PROGRESS).count()

        progress_percentage = int(
            (completed_topics / total_topics * 100) if total_topics > 0 else 0)

        return Response({
            "success": True,
            "path_id": path.id,
            "title": path.title,
            "total_topics": total_topics,
            "completed_topics": completed_topics,
            "in_progress_topics": in_progress_topics,
            "progress_percentage": progress_percentage,
            "status": path.status,
        })

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
