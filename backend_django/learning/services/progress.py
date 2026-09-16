from django.utils import timezone

from learning.models import (
    LearningProgress,
    LearningTopic,
)


class ProgressService:

    @staticmethod
    def update_progress(
        *,
        user,
        topic,
        progress_percent,
        practice_completed=None,
        notes=None,
    ):
        if topic.path.user_id != user.id:
            raise ValueError(
                "Topic does not belong to this user."
            )

        progress, _ = LearningProgress.objects.get_or_create(
            user=user,
            topic=topic,
        )

        progress.progress_percent = progress_percent

        if practice_completed is not None:
            progress.practice_completed = practice_completed

        if notes is not None:
            progress.notes = notes

        progress.last_activity_at = timezone.now()

        progress.save()

        if progress_percent >= 100:
            topic.status = LearningTopic.STATUS_COMPLETED

        elif progress_percent > 0:
            topic.status = LearningTopic.STATUS_IN_PROGRESS

        else:
            topic.status = LearningTopic.STATUS_PENDING

        topic.save(update_fields=["status", "updated_at"])

        return progress
