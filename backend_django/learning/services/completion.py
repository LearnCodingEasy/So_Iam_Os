from django.db import transaction
from django.utils import timezone
from learning.models import LearningGoal, LearningPath, LearningProgress, LearningTopic

class LearningCompletionService:
    @classmethod
    @transaction.atomic
    def complete_topic(cls, *, user, topic):
        if topic.path.user_id != user.id:
            raise ValueError("Topic does not belong to this user.")
        now = timezone.now()
        progress, _ = LearningProgress.objects.get_or_create(user=user, topic=topic)
        progress.progress_percent = 100
        progress.lesson_completed = True
        progress.practice_completed = True
        progress.quick_check_completed = True
        progress.assessment_completed = True
        progress.completed_at = progress.completed_at or now
        progress.last_activity_at = now
        progress.save()
        topic.status = LearningTopic.Status.COMPLETED
        topic.save(update_fields=["status", "updated_at"])

        path = topic.path
        topics = list(path.topics.all())
        if topics and all(t.status == LearningTopic.Status.COMPLETED for t in topics):
            path.status = LearningPath.Status.COMPLETED
            path.completed_at = path.completed_at or now
            path.save(update_fields=["status", "completed_at", "updated_at"])
            goal = path.goal
            goal.status = LearningGoal.Status.COMPLETED
            goal.completed_at = goal.completed_at or now
            goal.save(update_fields=["status", "completed_at", "updated_at"])

        next_topic = path.topics.filter(order__gt=topic.order).exclude(status=LearningTopic.Status.SKIPPED).order_by("order", "id").first()
        if next_topic and next_topic.status == LearningTopic.Status.PENDING:
            next_topic.status = LearningTopic.Status.IN_PROGRESS
            next_topic.save(update_fields=["status", "updated_at"])
        return {"progress": progress, "topic": topic, "next_topic": next_topic, "path": path, "goal": path.goal}

    @staticmethod
    def progress_summary(user):
        goals = list(LearningGoal.objects.filter(user=user).prefetch_related("paths__topics"))
        topics = LearningTopic.objects.filter(path__user=user)
        total = topics.count()
        completed = topics.filter(status=LearningTopic.Status.COMPLETED).count()
        progress = LearningProgress.objects.filter(user=user)
        avg = sum(p.progress_percent for p in progress) / progress.count() if progress.exists() else (completed / total * 100 if total else 0)
        return {"overall_progress": round(avg), "topics_total": total, "topics_completed": completed, "goals": [{"id": g.id, "title": g.title, "status": g.status, "progress": round(_goal_progress(g))} for g in goals]}

def _goal_progress(goal):
    topics = LearningTopic.objects.filter(path__goal=goal)
    total = topics.count()
    return topics.filter(status=LearningTopic.Status.COMPLETED).count() / total * 100 if total else 0
