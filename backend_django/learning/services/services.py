from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from learning.models import (
    LearningGoal,
    LearningPath,
    LearningTopic,
    LearningProgress,
    KnowledgeApplication,
    ApplicationSubmission,
    ApplicationReview,
    LearningRevision,
    Assessment,
    AssessmentAttempt,
)


# ============================================================
# 🧠 Application Service
# ============================================================

class ApplicationService:
    """
    Handles the lifecycle of KnowledgeApplication.

    Flow:

        Draft
          ↓
        Submit
          ↓
        ApplicationSubmission
          ↓
        AI / Human Review
          ↓
        LearningProgress
    """

    @staticmethod
    @transaction.atomic
    def submit_application(
        *,
        user,
        application,
    ):
        """
        Submit a knowledge application and create an immutable
        ApplicationSubmission snapshot.

        Every submission creates a new version.
        """

        if application.user_id != user.id:
            raise PermissionError(
                "You do not own this application."
            )

        # ----------------------------------------------------
        # Find the latest submission version
        # ----------------------------------------------------

        latest_version = (
            ApplicationSubmission.objects
            .filter(application=application)
            .aggregate(
                max_version=Max("version")
            )
            .get("max_version")
            or 0
        )

        next_version = latest_version + 1

        now = timezone.now()

        # ----------------------------------------------------
        # Create immutable snapshot
        # ----------------------------------------------------

        submission = ApplicationSubmission.objects.create(
            application=application,
            version=next_version,
            title=application.title,
            content=application.content,
            submitted_at=now,
        )

        # ----------------------------------------------------
        # Update application state
        # ----------------------------------------------------

        application.status = "submitted"
        application.submitted_at = now

        application.save(
            update_fields=[
                "status",
                "submitted_at",
                "updated_at",
            ]
        )

        return submission


# ============================================================
# 🤖 Application Review Service
# ============================================================

class ApplicationReviewService:
    """
    Handles application reviews and synchronization with
    LearningProgress.

    A review belongs to a specific immutable submission.
    """

    @staticmethod
    @transaction.atomic
    def save_review(
        *,
        user,
        application,
        review_data,
        submission=None,
    ):
        """
        Save an AI/human review for a specific submission.

        Backward compatible:
        If submission is not provided, the latest submission
        is automatically selected.
        """

        if application.user_id != user.id:
            raise PermissionError(
                "You do not own this application."
            )

        # ----------------------------------------------------
        # Resolve submission
        # ----------------------------------------------------

        if submission is None:
            submission = (
                ApplicationSubmission.objects
                .filter(
                    application=application,
                )
                .order_by("-version")
                .first()
            )

        if submission is None:
            raise ValueError(
                "Application must be submitted before it can be reviewed."
            )

        # ----------------------------------------------------
        # Security / consistency check
        # ----------------------------------------------------

        if submission.application_id != application.id:
            raise ValueError(
                "Submission does not belong to this application."
            )

        # ----------------------------------------------------
        # Prepare review data
        # ----------------------------------------------------

        review_data = dict(review_data or {})

        # These fields are managed by the service.
        review_data.pop("application", None)
        review_data.pop("submission", None)

        review_data["application"] = application
        review_data["submission"] = submission

        # ----------------------------------------------------
        # Save / update review for this submission
        # ----------------------------------------------------

        review, _ = (
            ApplicationReview.objects
            .update_or_create(
                submission=submission,
                defaults=review_data,
            )
        )

        # ----------------------------------------------------
        # Update application status
        # ----------------------------------------------------

        now = timezone.now()

        application.status = "reviewed"
        application.reviewed_at = now

        application.save(
            update_fields=[
                "status",
                "reviewed_at",
                "updated_at",
            ]
        )

        # ----------------------------------------------------
        # Update learning progress
        # ----------------------------------------------------

        ApplicationReviewService.update_learning_progress(
            application=application,
            review=review,
        )

        # ----------------------------------------------------
        # Create revision when needed
        # ----------------------------------------------------

        ApplicationReviewService.create_revision_if_needed(
            application=application,
            review=review,
        )

        return review

    # ========================================================
    # 📊 Update Learning Progress
    # ========================================================

    @staticmethod
    def update_learning_progress(
        *,
        application,
        review,
    ):
        """
        Synchronize application review with LearningProgress.
        """

        user = application.user

        progress, _ = (
            LearningProgress.objects
            .get_or_create(
                topic=application.topic,
                user=user,
            )
        )

        score = review.score or 0

        # ----------------------------------------------------
        # AI score
        # ----------------------------------------------------

        progress.last_ai_score = score

        # ----------------------------------------------------
        # Mastery
        # ----------------------------------------------------

        progress.mastery_level = (
            ApplicationReviewService.calculate_mastery(
                score
            )
        )

        # ----------------------------------------------------
        # Review requirement
        # ----------------------------------------------------

        progress.needs_review = bool(
            review.needs_review
        )

        # ----------------------------------------------------
        # Never destroy higher manual progress
        # ----------------------------------------------------

        calculated_progress = min(
            100,
            max(
                progress.progress_percent or 0,
                int(score),
            ),
        )

        progress.progress_percent = calculated_progress

        progress.last_activity_at = timezone.now()

        # ----------------------------------------------------
        # Practical application completion
        # ----------------------------------------------------

        if score >= 70:
            progress.practice_completed = True

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        progress.save()

        return progress

    # ========================================================
    # 🔄 Create Revision
    # ========================================================

    @staticmethod
    @transaction.atomic
    def create_revision_if_needed(
        *,
        application,
        review,
    ):
        """
        If the review identifies knowledge gaps or requests
        another review, create a LearningRevision.
        """

        needs_review = bool(
            review.needs_review
        )

        knowledge_gaps = (
            review.knowledge_gaps
            or []
        )

        recommendations = (
            review.recommendations
            or []
        )

        if not needs_review and not knowledge_gaps:
            return None

        concepts = []

        if isinstance(knowledge_gaps, list):
            concepts.extend(
                str(item)
                for item in knowledge_gaps
                if item
            )

        if isinstance(recommendations, list):
            concepts.extend(
                str(item)
                for item in recommendations
                if item
            )

        # Avoid unnecessary duplicates
        concepts = list(
            dict.fromkeys(concepts)
        )

        revision = (
            LearningRevision.objects
            .create(
                user=application.user,
                topic=application.topic,
                source_review=review,
                concepts=concepts,
                recommendation=recommendations,
                status="pending",
            )
        )

        return revision

    # ========================================================
    # 🧠 Calculate Mastery
    # ========================================================

    @staticmethod
    def calculate_mastery(score):
        """
        Convert score into the learning mastery scale.
        """

        score = float(score or 0)

        if score < 30:
            return "beginner"

        if score < 50:
            return "developing"

        if score < 70:
            return "competent"

        if score < 90:
            return "advanced"

        return "mastered"


# ============================================================
# 🧪 Assessment Service
# ============================================================

class AssessmentService:
    """
    Handles assessment attempts.
    """

    @staticmethod
    @transaction.atomic
    def submit_attempt(
        *,
        user,
        assessment,
        score,
        feedback="",
    ):
        """
        Create a new assessment attempt.

        Attempt numbers are generated server-side.
        """

        # ----------------------------------------------------
        # Ownership
        # ----------------------------------------------------

        if assessment.topic.path.user_id != user.id:
            raise PermissionError(
                "Assessment does not belong to this user."
            )

        # ----------------------------------------------------
        # Validate score
        # ----------------------------------------------------

        try:
            score = float(score)
        except (
            TypeError,
            ValueError,
        ):
            raise ValueError(
                "Score must be a valid number."
            )

        if score < 0 or score > 100:
            raise ValueError(
                "Score must be between 0 and 100."
            )

        # ----------------------------------------------------
        # Next attempt number
        # ----------------------------------------------------

        latest_attempt = (
            AssessmentAttempt.objects
            .filter(
                assessment=assessment,
                user=user,
            )
            .aggregate(
                max_attempt=Max(
                    "attempt_number"
                )
            )
            .get("max_attempt")
            or 0
        )

        attempt_number = (
            latest_attempt + 1
        )

        now = timezone.now()

        passed = (
            score >= assessment.passing_score
        )

        # ----------------------------------------------------
        # Create attempt
        # ----------------------------------------------------

        attempt = (
            AssessmentAttempt.objects
            .create(
                user=user,
                assessment=assessment,
                score=score,
                passed=passed,
                feedback=feedback or "",
                attempt_number=attempt_number,
                started_at=now,
                completed_at=now,
            )
        )

        return attempt


# ============================================================
# 🛣️ Learning Service
# ============================================================

class LearningService:
    """
    High-level learning operations.
    """

    # ================================================
    # 🎯 Create Goal
    # ================================================

    @staticmethod
    @transaction.atomic
    def create_goal(
        *,
        user,
        **data,
    ):
        """
        Create a LearningGoal for the current user.
        """

        return LearningGoal.objects.create(
            user=user,
            **data,
        )

    # ================================================
    # 🛣️ Create Path
    # ================================================

    @staticmethod
    @transaction.atomic
    def create_path(
        *,
        user,
        goal,
        title,
        description="",
    ):
        if goal.user_id != user.id:
            raise PermissionError(
                "Learning goal does not belong to this user."
            )

        return LearningPath.objects.create(
            user=user,
            goal=goal,
            title=title,
            description=description,
        )

    # ================================================
    # 📚 Create Topic
    # ================================================

    @staticmethod
    @transaction.atomic
    def create_topic(
        *,
        user,
        path,
        title,
        description="",
        skill=None,
        order=None,
        estimated_minutes=0,
        difficulty="beginner",
        status="pending",
    ):
        if path.user_id != user.id:
            raise PermissionError(
                "Learning path does not belong to this user."
            )

        # ----------------------------------------------------
        # Automatically calculate order
        # ----------------------------------------------------

        if order is None or order <= 0:
            last_order = (
                LearningTopic.objects
                .filter(path=path)
                .aggregate(
                    max_order=Max("order")
                )
                .get("max_order")
                or 0
            )

            order = last_order + 1

        return LearningTopic.objects.create(
            path=path,
            skill=skill,
            title=title,
            description=description,
            order=order,
            estimated_minutes=estimated_minutes,
            difficulty=difficulty,
            status=status,
        )

    # ================================================
    # 📊 Learning Overview
    # ================================================

    @staticmethod
    def get_user_learning_overview(user):
        goals = (
            LearningGoal.objects
            .filter(
                user=user,
            )
            .select_related(
                "skill",
            )
        )

        paths = (
            LearningPath.objects
            .filter(
                user=user,
            )
            .select_related(
                "goal",
                "goal__skill",
            )
            .prefetch_related(
                "topics",
            )
        )

        progress = (
            LearningProgress.objects
            .filter(
                user=user,
            )
            .select_related(
                "topic",
                "topic__path",
            )
        )

        applications = (
            KnowledgeApplication.objects
            .filter(
                user=user,
            )
            .select_related(
                "topic",
                "lesson",
                "knowledge_item",
            )
            .prefetch_related(
                "submissions",
                "reviews",
            )
        )

        revisions = (
            LearningRevision.objects
            .filter(
                user=user,
            )
            .select_related(
                "topic",
                "source_review",
            )
        )

        return {
            "goals": goals,
            "paths": paths,
            "progress": progress,
            "applications": applications,
            "revisions": revisions,
        }


# ====================================================
# 📈 Progress Service
# ====================================================

class ProgressService:
    """
    Handles LearningProgress updates.
    """

    @staticmethod
    @transaction.atomic
    def update_progress(
        *,
        user,
        topic,
        progress_percent,
        practice_completed=None,
        notes=None,
        lesson_completed=None,
        quick_check_completed=None,
        assessment_completed=None,
    ):
        # ----------------------------------------------------
        # Ownership
        # ----------------------------------------------------

        if topic.path.user_id != user.id:
            raise PermissionError(
                "Topic does not belong to this user."
            )

        # ----------------------------------------------------
        # Validate progress
        # ----------------------------------------------------

        try:
            progress_percent = float(
                progress_percent
            )
        except (
            TypeError,
            ValueError,
        ):
            raise ValueError(
                "Progress percent must be a valid number."
            )

        progress_percent = max(
            0,
            min(
                100,
                progress_percent,
            ),
        )

        # ----------------------------------------------------
        # Get / create progress
        # ----------------------------------------------------

        progress, _ = (
            LearningProgress.objects
            .get_or_create(
                user=user,
                topic=topic,
            )
        )

        # ----------------------------------------------------
        # Update core progress
        # ----------------------------------------------------

        progress.progress_percent = (
            progress_percent
        )

        # ----------------------------------------------------
        # Optional fields
        # ----------------------------------------------------

        if practice_completed is not None:
            progress.practice_completed = (
                bool(practice_completed)
            )

        if lesson_completed is not None:
            progress.lesson_completed = (
                bool(lesson_completed)
            )

        if quick_check_completed is not None:
            progress.quick_check_completed = (
                bool(quick_check_completed)
            )

        if assessment_completed is not None:
            progress.assessment_completed = (
                bool(assessment_completed)
            )

        if notes is not None:
            progress.notes = notes

        # ----------------------------------------------------
        # Activity timestamp
        # ----------------------------------------------------

        progress.last_activity_at = timezone.now()

        # ----------------------------------------------------
        # Completion
        # ----------------------------------------------------

        if progress_percent >= 100:
            progress.completed_at = (
                progress.completed_at
                or timezone.now()
            )

        else:
            progress.completed_at = None

        progress.save()

        # ----------------------------------------------------
        # Update topic status
        # ----------------------------------------------------

        if progress_percent >= 100:
            topic.status = (
                LearningTopic.STATUS_COMPLETED
            )

        elif progress_percent > 0:
            topic.status = (
                LearningTopic.STATUS_IN_PROGRESS
            )

        else:
            topic.status = (
                LearningTopic.STATUS_PENDING
            )

        topic.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return progress
