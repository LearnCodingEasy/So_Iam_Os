"""Shared transactional services and user-scoped dashboard aggregation."""

from django.core.cache import cache
from django.db import transaction
from django.db.models import Avg, Count, Q
from django.utils import timezone

from goals.models import Goal
from jobs_opportunity.models import JobApplication, JobMatch, JobOpportunity
from knowledge.models import KnowledgeFile, KnowledgeItem
from learning.models import (
    LearningGoal,
    LearningPath,
    LearningProgress,
    LearningTopic,
    Skill,
)
from tasks.models import Task


DASHBOARD_CACHE_TTL = 60


class BaseService:
    @staticmethod
    @transaction.atomic
    def save(instance):
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def delete(instance):
        instance.delete()


class DashboardService:
    """Build a compact dashboard with user-isolated caching and aggregate queries."""

    @staticmethod
    def get_data(*, user):
        cache_key = f"dashboard:{user.pk}"
        try:
            cached = cache.get(cache_key)
            if cached is not None:
                return cached
        except Exception:
            # The dashboard remains available when Redis/cache is temporarily down.
            pass

        today = timezone.localdate()
        generated_at = timezone.now()

        goals = Goal.objects.filter(user=user)
        tasks = Task.objects.filter(user=user)
        learning_goals = LearningGoal.objects.filter(user=user)
        paths = LearningPath.objects.filter(user=user)
        knowledge = KnowledgeItem.objects.filter(user=user, is_archived=False)
        jobs = JobOpportunity.objects.filter(user=user, is_active=True)
        matches = JobMatch.objects.filter(user=user)
        applications = JobApplication.objects.filter(user=user)
        learning_topics = LearningTopic.objects.filter(path__user=user)

        # Aggregate related counters in SQL instead of issuing a count query for
        # every metric. This keeps dashboard query volume predictable as data grows.
        task_stats = tasks.aggregate(
            total=Count("pk"),
            today=Count("pk", filter=Q(scheduled_date=today)),
            pending=Count("pk", filter=Q(status__in=("pending", "in_progress"))),
            completed=Count("pk", filter=Q(status="completed")),
        )
        goal_stats = goals.aggregate(
            total=Count("pk"),
            active=Count("pk", filter=Q(status="active")),
            completed=Count("pk", filter=Q(status="completed")),
        )
        learning_goal_stats = learning_goals.aggregate(total=Count("pk"))
        path_stats = paths.aggregate(
            total=Count("pk"),
            active=Count("pk", filter=Q(status="active")),
        )
        topic_stats = learning_topics.aggregate(
            total=Count("pk"),
            completed=Count(
                "pk", filter=Q(status=LearningTopic.Status.COMPLETED)
            ),
        )
        progress_stats = LearningProgress.objects.filter(user=user).aggregate(
            average=Avg("progress_percent"),
        )
        progress_avg = progress_stats["average"]
        if progress_avg is None:
            topic_total = topic_stats["total"] or 0
            progress_avg = (
                (topic_stats["completed"] or 0) / topic_total * 100
                if topic_total
                else 0
            )

        knowledge_stats = knowledge.aggregate(total=Count("pk"))
        knowledge_file_stats = KnowledgeFile.objects.filter(
            knowledge__user=user,
            knowledge__is_archived=False,
        ).aggregate(total=Count("pk"))
        job_stats = jobs.aggregate(total=Count("pk"))
        match_stats = matches.aggregate(
            qualified=Count("pk", filter=Q(score__gte=70))
        )
        application_stats = applications.aggregate(total=Count("pk"))
        skill_stats = Skill.objects.filter(
            learning_goals__user=user,
        ).aggregate(total=Count("pk", distinct=True))

        recent_tasks = list(
            tasks.filter(scheduled_date=today)
            .order_by("sort_order", "-priority")[:8]
            .values(
                "id",
                "title",
                "status",
                "priority",
                "scheduled_date",
                "due_at",
            )
        )

        data = {
            "user": {
                "id": str(user.id),
                "name": user.full_name,
                "email": user.email,
            },
            "date": {"now": generated_at, "local_date": today},
            "stats": {
                "tasks": task_stats,
                "goals": {
                    "total": goal_stats["total"],
                    "in_progress": goal_stats["active"],
                    "completed": goal_stats["completed"],
                },
                "learning": {
                    "goals": learning_goal_stats["total"],
                    "paths": path_stats["total"],
                    "active_paths": path_stats["active"],
                    "topics_total": topic_stats["total"],
                    "topics_completed": topic_stats["completed"],
                    "progress": round(float(progress_avg or 0)),
                },
                "knowledge": {
                    "total": knowledge_stats["total"],
                    "files": knowledge_file_stats["total"],
                },
                "jobs": {
                    "total": job_stats["total"],
                    "matches": match_stats["qualified"],
                    "applications": application_stats["total"],
                },
                "skills": {"total": skill_stats["total"]},
            },
            "tasks": recent_tasks,
            "recent": {
                "knowledge": list(
                    knowledge.order_by("-updated_at")[:5].values(
                        "id", "title", "knowledge_type", "updated_at"
                    )
                ),
                "jobs": list(
                    jobs.order_by("-published_at", "-discovered_at")[:5].values(
                        "id", "title", "company", "is_remote", "url"
                    )
                ),
            },
            "system": {"online": True, "generated_at": generated_at},
        }

        try:
            cache.set(cache_key, data, DASHBOARD_CACHE_TTL)
        except Exception:
            # Cache failure must never turn a successful database read into a 500.
            pass
        return data
