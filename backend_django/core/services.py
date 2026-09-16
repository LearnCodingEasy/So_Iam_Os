from django.db import transaction
from django.utils import timezone

from knowledge.models import KnowledgeFile, KnowledgeItem


class BaseService:
    """
    Base service for shared application logic.
    """

    @staticmethod
    @transaction.atomic
    def save(instance):
        """
        Save an instance inside an atomic transaction.
        """
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def delete(instance):
        """
        Delete an instance inside an atomic transaction.
        """
        instance.delete()


class DashboardService:
    """
    Service responsible for aggregating data
    from different So_Iam_OS applications.

    Dashboard does not own application data.
    It only reads and aggregates it.
    """

    @staticmethod
    def get_data(*, user):
        """
        Build dashboard data for the authenticated user.
        """

        # -------------------------------------------------
        # KNOWLEDGE
        # -------------------------------------------------

        knowledge_items = (
            KnowledgeItem.objects
            .filter(
                user=user,
                is_archived=False,
            )
            .order_by("-updated_at")
        )

        knowledge_count = knowledge_items.count()

        knowledge_files_count = (
            KnowledgeFile.objects
            .filter(
                knowledge__user=user,
                knowledge__is_archived=False,
            )
            .count()
        )

        recent_knowledge = knowledge_items[:5]

        recent_knowledge_data = [
            {
                "id": item.id,
                "title": item.title,
                "type": item.knowledge_type,
                "updated_at": item.updated_at,
                "files_count": item.files.count(),
            }
            for item in recent_knowledge
        ]

        # -------------------------------------------------
        # USER
        # -------------------------------------------------

        user_name = (
            getattr(user, "first_name", "")
            or getattr(user, "username", "")
            or "User"
        )

        user_email = (
            getattr(user, "email", "")
            or ""
        )

        # -------------------------------------------------
        # CURRENT TIME
        # -------------------------------------------------

        now = timezone.now()

        # -------------------------------------------------
        # DASHBOARD RESPONSE
        # -------------------------------------------------

        return {
            "user": {
                "id": user.id,
                "name": user_name,
                "email": user_email,
            },

            "date": {
                "now": now,
            },

            "stats": {
                # Future application
                "projects": {
                    "total": 0,
                    "active": 0,
                    "completed": 0,
                },

                # Future application
                "tasks": {
                    "total": 0,
                    "pending": 0,
                    "completed": 0,
                },

                # Future application
                "goals": {
                    "total": 0,
                    "in_progress": 0,
                    "completed": 0,
                },

                # Future application
                "learning": {
                    "total": 0,
                    "in_progress": 0,
                    "completed": 0,
                },

                # Real data from Knowledge application
                "knowledge": {
                    "total": knowledge_count,
                    "files": knowledge_files_count,
                },

                # Future application
                "memory": {
                    "total": 0,
                    "important": 0,
                },
            },

            "recent": {
                "knowledge": recent_knowledge_data,
            },

            # Will become dynamic when Tasks app exists
            "tasks": [],

            # Will become dynamic when the related apps exist
            "progress": {
                "projects": [],
                "tasks": [],
                "learning": [],
            },

            "system": {
                "online": True,
                "generated_at": now,
            },
        }
