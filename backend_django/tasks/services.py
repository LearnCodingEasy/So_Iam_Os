
from datetime import date, datetime

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime

from .models import Task


class TaskService:
    @staticmethod
    @transaction.atomic
    def complete(task, actual_minutes=None):
        if actual_minutes is not None:
            try:
                actual_minutes = int(actual_minutes)
            except (TypeError, ValueError):
                raise ValidationError(
                    "Actual minutes must be an integer."
                )

            if actual_minutes < 0:
                raise ValidationError(
                    "Actual minutes cannot be negative."
                )

        task.status = Task.Status.COMPLETED
        task.completed_at = task.completed_at or timezone.now()

        if actual_minutes is not None:
            task.actual_minutes = actual_minutes

        task.save(update_fields=[
            "status",
            "completed_at",
            "actual_minutes",
            "updated_at",
        ])

        if task.goal_id:
            from goals.services import GoalService

            GoalService.recalculate_from_tasks(task.goal)

        return task

    @staticmethod
    @transaction.atomic
    def postpone(task, until):
        parsed_date = parse_date(until) if isinstance(until, str) else None
        parsed_datetime = (
            parse_datetime(until) if isinstance(until, str) else None
        )

        if isinstance(until, datetime):
            parsed_datetime = until
            parsed_date = until.date()
        elif isinstance(until, date):
            parsed_date = until

        if parsed_datetime is not None:
            if timezone.is_naive(parsed_datetime):
                parsed_datetime = timezone.make_aware(
                    parsed_datetime,
                    timezone.get_current_timezone(),
                )
            parsed_date = timezone.localtime(
                parsed_datetime
            ).date()

        if parsed_date is None:
            raise ValidationError(
                "until must be a valid ISO date or datetime."
            )

        if parsed_date < timezone.localdate():
            raise ValidationError(
                "A task cannot be postponed to a past date."
            )

        postponed_field = Task._meta.get_field("postponed_until")
        field_type = postponed_field.get_internal_type()

        if field_type == "DateTimeField":
            if parsed_datetime is None:
                parsed_datetime = timezone.make_aware(
                    datetime.combine(
                        parsed_date,
                        datetime.min.time(),
                    ),
                    timezone.get_current_timezone(),
                )
            postponed_value = parsed_datetime
        elif field_type == "DateField":
            postponed_value = parsed_date
        else:
            raise ValidationError(
                "Unsupported postponed_until field type."
            )

        task.status = Task.Status.POSTPONED
        task.postponed_until = postponed_value
        task.scheduled_date = parsed_date

        task.save(update_fields=[
            "status",
            "postponed_until",
            "scheduled_date",
            "updated_at",
        ])

        return task
