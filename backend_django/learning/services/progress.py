from django.utils import timezone
from learning.models import LearningProgress, LearningTopic

class ProgressService:
    @staticmethod
    def update_progress(*, user, topic, progress_percent, practice_completed=None, notes=None, lesson_completed=None, quick_check_completed=None, assessment_completed=None):
        if topic.path.user_id != user.id:
            raise ValueError("Topic does not belong to this user.")
        progress, _ = LearningProgress.objects.get_or_create(user=user, topic=topic)
        progress.progress_percent = max(0, min(100, int(progress_percent)))
        for field, value in (("practice_completed", practice_completed), ("lesson_completed", lesson_completed), ("quick_check_completed", quick_check_completed), ("assessment_completed", assessment_completed)):
            if value is not None:
                setattr(progress, field, bool(value))
        if notes is not None:
            progress.notes = notes
        progress.last_activity_at = timezone.now()
        if progress.progress_percent >= 100:
            progress.completed_at = progress.completed_at or timezone.now()
        progress.save()
        if progress.progress_percent >= 100 or (progress.lesson_completed and progress.practice_completed and progress.assessment_completed):
            topic.status = LearningTopic.Status.COMPLETED
        elif progress.progress_percent > 0:
            topic.status = LearningTopic.Status.IN_PROGRESS
        else:
            topic.status = LearningTopic.Status.PENDING
        topic.save(update_fields=["status", "updated_at"])
        return progress
