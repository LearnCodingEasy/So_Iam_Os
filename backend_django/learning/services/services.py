from django.db import transaction
from django.utils import timezone

from learning.models import (
    LearningProgress,
    KnowledgeApplication,
    ApplicationReview,
)


class ApplicationService:

    @staticmethod
    @transaction.atomic
    def submit_application(
        *,
        user,
        application,
    ):

        if application.user_id != user.id:
            raise PermissionError(
                "You do not own this application."
            )

        application.status = "submitted"

        application.submitted_at = timezone.now()

        application.save(
            update_fields=[
                "status",
                "submitted_at",
                "updated_at",
            ]
        )

        return application


class ApplicationReviewService:

    @staticmethod
    @transaction.atomic
    def save_review(
        *,
        user,
        application,
        review_data,
    ):

        if application.user_id != user.id:
            raise PermissionError(
                "You do not own this application."
            )

        review, _ = ApplicationReview.objects.update_or_create(
            application=application,
            defaults=review_data,
        )

        application.status = "reviewed"

        application.reviewed_at = timezone.now()

        application.save(
            update_fields=[
                "status",
                "reviewed_at",
                "updated_at",
            ]
        )

        ApplicationReviewService.update_learning_progress(
            application=application,
            review=review,
        )

        return review

    @staticmethod
    def update_learning_progress(
        *,
        application,
        review,
    ):

        user = application.user

        progress, _ = LearningProgress.objects.get_or_create(
            topic=application.topic,
            user=user,
        )

        score = review.score

        progress.last_ai_score = score

        progress.mastery_level = (
            ApplicationReviewService.calculate_mastery(
                score
            )
        )

        progress.needs_review = bool(
            review.needs_review
        )

        # Don't destroy manually higher progress.
        calculated_progress = min(
            100,
            max(
                progress.progress_percent,
                int(score),
            ),
        )

        progress.progress_percent = calculated_progress

        progress.last_activity_at = timezone.now()

        if score >= 70:
            progress.practice_completed = True

        progress.save()

        return progress

    @staticmethod
    def calculate_mastery(score):

        if score < 30:
            return "beginner"

        if score < 50:
            return "developing"

        if score < 70:
            return "competent"

        if score < 90:
            return "advanced"

        return "mastered"
