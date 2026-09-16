from django.db import transaction

from learning.models import (
    LearningGoal,
    LearningPath,
    LearningTopic,
)

class LearningService:

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
            raise ValueError(
                "Learning goal does not belong to this user."
            )

        return LearningPath.objects.create(
            user=user,
            goal=goal,
            title=title,
            description=description,
        )

    @staticmethod
    @transaction.atomic
    def create_topic(
        *,
        user,
        path,
        title,
        description="",
        skill=None,
        order=0,
        estimated_minutes=0,
    ):
        if path.user_id != user.id:
            raise ValueError(
                "Learning path does not belong to this user."
            )

        return LearningTopic.objects.create(
            path=path,
            skill=skill,
            title=title,
            description=description,
            order=order,
            estimated_minutes=estimated_minutes,
        )

    @staticmethod
    def get_user_learning_overview(user):
        goals = LearningGoal.objects.filter(
            user=user
        ).select_related("skill")

        paths = LearningPath.objects.filter(
            user=user
        ).select_related("goal")

        return {
            "goals": goals,
            "paths": paths,
        }
