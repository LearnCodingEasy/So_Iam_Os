"""Build a bounded, user-scoped context bundle for Codex integrations.

Only records owned by the authenticated user are queried. Large knowledge bodies are
excluded by default and can be explicitly requested with include_content=true.
"""
from __future__ import annotations

from django.utils import timezone


def _limit(raw_value, default=25, maximum=100):
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        value = default
    return max(1, min(value, maximum))


def build_user_context(user, *, limit=25, include_content=False):
    from goals.models import Goal
    from tasks.models import Task
    from knowledge.models import KnowledgeItem
    from learning.models import LearningGoal, LearningPath, LearningTopic

    limit = _limit(limit)
    goals_qs = Goal.objects.filter(user=user).order_by("target_date", "-updated_at")
    tasks_qs = Task.objects.filter(user=user).select_related("goal", "learning_goal").order_by("scheduled_date", "sort_order", "-priority")
    knowledge_qs = KnowledgeItem.objects.filter(user=user, is_archived=False).order_by("-updated_at")
    learning_goals_qs = LearningGoal.objects.filter(user=user).select_related("skill").order_by("-updated_at")
    learning_paths_qs = LearningPath.objects.filter(user=user, goal__user=user).select_related("goal").order_by("-updated_at")
    learning_topics_qs = LearningTopic.objects.filter(path__user=user, path__goal__user=user).select_related("path", "skill")

    goals = [{
        "id": item.pk, "title": item.title, "description": item.description[:1200],
        "status": item.status, "priority": item.priority,
        "progress_percent": item.progress_percent,
        "target_date": item.target_date.isoformat() if item.target_date else None,
        "updated_at": item.updated_at.isoformat(),
    } for item in goals_qs[:limit]]

    tasks = [{
        "id": item.pk, "title": item.title, "description": item.description[:800],
        "status": item.status, "priority": item.priority,
        "scheduled_date": item.scheduled_date.isoformat() if item.scheduled_date else None,
        "due_at": item.due_at.isoformat() if item.due_at else None,
        "goal_id": item.goal_id, "learning_goal_id": item.learning_goal_id,
        "estimated_minutes": item.estimated_minutes,
    } for item in tasks_qs[:limit]]

    knowledge = []
    for item in knowledge_qs[:limit]:
        record = {
            "id": item.pk, "title": item.title,
            "description": item.description[:1000],
            "knowledge_type": item.knowledge_type,
            "tags": item.tags if isinstance(item.tags, list) else [],
            "source_url": item.source_url,
            "updated_at": item.updated_at.isoformat(),
            "metadata": (item.metadata.get("extracted", {}) if isinstance(item.metadata, dict) else {}),
        }
        if include_content:
            record["content"] = item.content[:4000]
            record["content_truncated"] = len(item.content) > 4000
        knowledge.append(record)

    learning_goals = [{
        "id": item.pk, "title": item.title, "description": item.description[:800],
        "status": item.status, "current_level": item.current_level,
        "target_level": item.target_level, "skill": item.skill.name if item.skill_id else None,
        "target_date": item.target_date.isoformat() if item.target_date else None,
    } for item in learning_goals_qs[:limit]]

    learning_paths = [{
        "id": item.pk, "title": item.title, "description": item.description[:800],
        "status": item.status, "learning_goal_id": item.goal_id,
        "learning_goal_title": item.goal.title,
    } for item in learning_paths_qs[:limit]]

    learning_topics = [{
        "id": item.pk, "title": item.title, "description": item.description[:600],
        "status": item.status, "difficulty": item.difficulty,
        "path_id": item.path_id, "skill": item.skill.name if item.skill_id else None,
        "knowledge_item_id": item.knowledge_item_id,
    } for item in learning_topics_qs.order_by("path_id", "order")[:limit]]

    all_goal_count = goals_qs.count()
    all_task_count = tasks_qs.count()
    all_knowledge_count = knowledge_qs.count()
    all_learning_goal_count = learning_goals_qs.count()
    all_learning_path_count = learning_paths_qs.count()

    return {
        "schema_version": "1.0",
        "generated_at": timezone.now().isoformat(),
        "scope": "authenticated_user_owned_records",
        "limits": {"per_collection": limit, "knowledge_content_included": bool(include_content)},
        "summary": {
            "goals_total": all_goal_count,
            "tasks_total": all_task_count,
            "knowledge_items_total": all_knowledge_count,
            "learning_goals_total": all_learning_goal_count,
            "learning_paths_total": all_learning_path_count,
            "active_goals": goals_qs.filter(status=Goal.Status.ACTIVE).count(),
            "open_tasks": tasks_qs.exclude(status__in=[Task.Status.COMPLETED, Task.Status.CANCELLED]).count(),
            "completed_tasks": tasks_qs.filter(status=Task.Status.COMPLETED).count(),
        },
        "goals": goals,
        "tasks": tasks,
        "knowledge": knowledge,
        "learning_goals": learning_goals,
        "learning_paths": learning_paths,
        "learning_topics": learning_topics,
        "truncated": {
            "goals": all_goal_count > len(goals),
            "tasks": all_task_count > len(tasks),
            "knowledge": all_knowledge_count > len(knowledge),
            "learning_goals": all_learning_goal_count > len(learning_goals),
            "learning_paths": all_learning_path_count > len(learning_paths),
        },
    }
