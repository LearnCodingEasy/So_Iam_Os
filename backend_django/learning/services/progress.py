from django.db import IntegrityError, OperationalError, transaction
from django.utils import timezone

from learning.models import LearningProgress, LearningTopic


class ProgressService:
    """Concurrency-safe, monotonic learning progress updates."""

    MAX_DB_RETRIES = 3

    @staticmethod
    def update_progress(*, user, topic, progress_percent, practice_completed=None,
                         notes=None, lesson_completed=None, quick_check_completed=None,
                         assessment_completed=None):
        if topic.path.user_id != user.id:
            raise ValueError("Topic does not belong to this user.")

        incoming_percent = max(0, min(100, int(progress_percent)))

        for attempt in range(ProgressService.MAX_DB_RETRIES):
            try:
                with transaction.atomic():
                    # Lock both the topic and existing progress row. On SQLite,
                    # the retry loop below is still useful during local concurrent
                    # development; production is required to use PostgreSQL.
                    locked_topic = (
                        LearningTopic.objects
                        .select_for_update()
                        .select_related("path")
                        .get(pk=topic.pk, path__user=user)
                    )
                    try:
                        progress = (
                            LearningProgress.objects
                            .select_for_update()
                            .get(user=user, topic=locked_topic)
                        )
                    except LearningProgress.DoesNotExist:
                        try:
                            progress = LearningProgress.objects.create(
                                user=user,
                                topic=locked_topic,
                                progress_percent=0,
                            )
                        except IntegrityError:
                            progress = (
                                LearningProgress.objects
                                .select_for_update()
                                .get(user=user, topic=locked_topic)
                            )

                    # Progress is monotonic: a stale/repeated request can never
                    # silently move a learner backwards.
                    progress.progress_percent = max(
                        int(progress.progress_percent or 0),
                        incoming_percent,
                    )

                    for field, value in (
                        ("practice_completed", practice_completed),
                        ("lesson_completed", lesson_completed),
                        ("quick_check_completed", quick_check_completed),
                        ("assessment_completed", assessment_completed),
                    ):
                        if value is not None:
                            # Completion flags are also monotonic.
                            setattr(
                                progress,
                                field,
                                bool(getattr(progress, field, False) or bool(value)),
                            )

                    if notes is not None:
                        progress.notes = notes

                    now = timezone.now()
                    progress.last_activity_at = now
                    if progress.progress_percent >= 100:
                        progress.completed_at = progress.completed_at or now

                    progress.save()

                    if (
                        progress.progress_percent >= 100
                        or (
                            progress.lesson_completed
                            and progress.practice_completed
                            and progress.assessment_completed
                        )
                    ):
                        locked_topic.status = LearningTopic.Status.COMPLETED
                    elif progress.progress_percent > 0:
                        locked_topic.status = LearningTopic.Status.IN_PROGRESS
                    else:
                        locked_topic.status = LearningTopic.Status.PENDING

                    locked_topic.save(update_fields=["status", "updated_at"])
                    return progress

            except OperationalError as exc:
                if "locked" not in str(exc).lower() or attempt >= ProgressService.MAX_DB_RETRIES - 1:
                    raise
                # SQLite is intentionally supported only for development. A
                # short bounded retry prevents transient local lock errors from
                # becoming HTTP 500s during rapid UI updates.
                import time
                time.sleep(0.05 * (2 ** attempt))

        raise RuntimeError("Learning progress update could not be committed.")
