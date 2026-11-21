from datetime import date, timedelta
from decimal import Decimal

from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone

from goals.models import Goal, GoalActivity, GoalMilestone, GoalPlanProposal


class GoalService:
    TRANSITIONS = {
        Goal.Status.DRAFT: {Goal.Status.PLANNED, Goal.Status.ACTIVE, Goal.Status.CANCELLED, Goal.Status.ARCHIVED},
        Goal.Status.PLANNED: {Goal.Status.ACTIVE, Goal.Status.PAUSED, Goal.Status.CANCELLED, Goal.Status.ARCHIVED},
        Goal.Status.ACTIVE: {Goal.Status.PAUSED, Goal.Status.AT_RISK, Goal.Status.COMPLETED, Goal.Status.CANCELLED, Goal.Status.ARCHIVED},
        Goal.Status.PAUSED: {Goal.Status.ACTIVE, Goal.Status.AT_RISK, Goal.Status.CANCELLED, Goal.Status.ARCHIVED},
        Goal.Status.AT_RISK: {Goal.Status.ACTIVE, Goal.Status.PAUSED, Goal.Status.COMPLETED, Goal.Status.CANCELLED, Goal.Status.ARCHIVED},
        Goal.Status.COMPLETED: {Goal.Status.ACTIVE, Goal.Status.ARCHIVED},
        Goal.Status.CANCELLED: {Goal.Status.ARCHIVED},
        Goal.Status.ARCHIVED: set(),
    }

    @staticmethod
    def record(goal, user, event_type, description="", data=None):
        return GoalActivity.objects.create(goal=goal, user=user, event_type=event_type,
                                           description=description, data=data or {})

    @staticmethod
    def notify(user, title, message, obj, action_url="/goals"):
        try:
            from notification.models import Notification, NotificationService
            NotificationService.create(user, type=Notification.Type.GOAL, title=title,
                                       message=message, action_url=action_url, obj=obj)
        except Exception:
            # Notification delivery must not roll back the user's goal operation.
            import logging
            logging.getLogger(__name__).exception("Goal notification could not be created.")

    @classmethod
    @transaction.atomic
    def set_status(cls, goal, status, user, notes=""):
        if status not in Goal.Status.values:
            raise ValueError("Invalid goal status.")
        if status != goal.status and status not in cls.TRANSITIONS.get(goal.status, set()):
            raise ValueError(f"Transition from {goal.status} to {status} is not allowed.")
        previous_status = goal.status
        goal.status = status
        if previous_status == Goal.Status.COMPLETED and status == Goal.Status.ACTIVE and goal.progress_percent == 100:
            goal.progress_percent = 0
        if status == Goal.Status.COMPLETED:
            goal.progress_percent = 100
            goal.completed_at = goal.completed_at or timezone.now()
            if notes:
                goal.completion_notes = notes
        elif status != Goal.Status.COMPLETED and goal.completed_at:
            goal.completed_at = None
        goal.save(update_fields=["status", "progress_percent", "completed_at", "completion_notes", "updated_at"])
        cls.record(goal, user, "status_changed", f"Goal status changed to {status}.", {"status": status})
        if status == Goal.Status.COMPLETED and previous_status != Goal.Status.COMPLETED:
            cls.notify(user, "تم تحقيق هدف", f"اكتمل الهدف: {goal.title}", goal)
        return goal

    @classmethod
    @transaction.atomic
    def complete(cls, goal, user, notes=""):
        return cls.set_status(goal, Goal.Status.COMPLETED, user, notes)

    @classmethod
    @transaction.atomic
    def update_progress(cls, goal, progress, user, source="user"):
        try:
            progress = int(progress)
        except (TypeError, ValueError):
            raise ValueError("Progress must be an integer between 0 and 100.")
        if not 0 <= progress <= 100:
            raise ValueError("Progress must be between 0 and 100.")
        if goal.status in {Goal.Status.ARCHIVED, Goal.Status.CANCELLED}:
            raise ValueError("Archived or cancelled goals cannot be updated.")
        previous_status = goal.status
        goal.progress_percent = progress
        goal.metadata = {**(goal.metadata or {}), "progress_source": source}
        if progress == 100:
            goal.status = Goal.Status.COMPLETED
            goal.completed_at = goal.completed_at or timezone.now()
        elif goal.status == Goal.Status.COMPLETED:
            goal.status = Goal.Status.ACTIVE
            goal.completed_at = None
        goal.save(update_fields=["progress_percent", "status", "completed_at", "metadata", "updated_at"])
        cls.record(goal, user, "progress_updated", f"Progress updated to {progress}%.", {"progress": progress, "source": source})
        if goal.status == Goal.Status.COMPLETED and previous_status != Goal.Status.COMPLETED:
            cls.notify(user, "تم تحقيق هدف", f"اكتمل الهدف: {goal.title}", goal)
        return goal

    @classmethod
    @transaction.atomic
    def recalculate_goal(cls, goal):
        if goal.milestones.exists():
            return cls.recalculate_from_milestones(goal)
        if goal.initial_value is not None and goal.target_value is not None and goal.current_value is not None:
            return goal
        return cls.recalculate_from_tasks(goal)

    @classmethod
    @transaction.atomic
    def recalculate_from_tasks(cls, goal):
        tasks = goal.tasks.exclude(status__in=["cancelled"])
        total = tasks.count()
        if total:
            completed = tasks.filter(status="completed").count()
            progress = round((completed / total) * 100)
            cls._save_derived_progress(goal, progress, "tasks")
        elif (goal.metadata or {}).get("progress_source") in {"tasks", "milestones"}:
            cls._save_derived_progress(goal, 0, "tasks")
        return goal

    @classmethod
    @transaction.atomic
    def recalculate_milestone(cls, milestone):
        linked = milestone.tasks.exclude(status="cancelled")
        total = linked.count()
        if total:
            completed = linked.filter(status="completed").count()
            milestone.progress_percent = round((completed / total) * 100)
            if milestone.progress_percent == 100:
                milestone.status = GoalMilestone.Status.COMPLETED
                milestone.completed_at = milestone.completed_at or timezone.now()
            elif milestone.status == GoalMilestone.Status.COMPLETED:
                milestone.status = GoalMilestone.Status.ACTIVE
                milestone.completed_at = None
            milestone.save(update_fields=["progress_percent", "status", "completed_at", "updated_at"])
        return milestone

    @classmethod
    @transaction.atomic
    def recalculate_for_task(cls, task):
        if task.milestone_id:
            cls.recalculate_milestone(task.milestone)
        goal = task.goal if task.goal_id else (task.milestone.goal if task.milestone_id else None)
        if goal:
            cls.recalculate_goal(goal)

    @classmethod
    @transaction.atomic
    def recalculate_from_milestones(cls, goal):
        milestones = list(goal.milestones.all())
        if not milestones:
            if goal.initial_value is not None and goal.target_value is not None and goal.current_value is not None:
                return goal
            return cls.recalculate_from_tasks(goal)
        weighted = [(m, Decimal(m.weight)) for m in milestones if Decimal(m.weight) > 0]
        if weighted:
            denominator = sum((weight for _, weight in weighted), Decimal("0"))
            progress = round(sum((Decimal(m.progress_percent) * weight for m, weight in weighted), Decimal("0")) / denominator)
        else:
            progress = round(sum(m.progress_percent for m in milestones) / len(milestones))
        cls._save_derived_progress(goal, int(progress), "milestones")
        return goal

    @staticmethod
    def _save_derived_progress(goal, progress, source):
        if goal.status in {Goal.Status.CANCELLED, Goal.Status.ARCHIVED}:
            return
        previous_status = goal.status
        previous_progress = goal.progress_percent
        goal.progress_percent = max(0, min(100, progress))
        if progress == 100:
            goal.status = Goal.Status.COMPLETED
            goal.completed_at = goal.completed_at or timezone.now()
        elif goal.status == Goal.Status.COMPLETED:
            goal.status = Goal.Status.ACTIVE
            goal.completed_at = None
        goal.metadata = {**(goal.metadata or {}), "progress_source": source}
        goal.save(update_fields=["progress_percent", "status", "completed_at", "metadata", "updated_at"])
        if goal.progress_percent != previous_progress or goal.status != previous_status:
            GoalService.record(goal, goal.user, "progress_derived", f"Progress recalculated from {source}.",
                               {"progress": goal.progress_percent, "source": source})
        if goal.status == Goal.Status.COMPLETED and previous_status != Goal.Status.COMPLETED:
            GoalService.notify(goal.user, "تم تحقيق هدف", f"اكتمل الهدف: {goal.title}", goal)

    @classmethod
    @transaction.atomic
    def approve_plan(cls, proposal, user):
        proposal = GoalPlanProposal.objects.select_for_update().select_related("goal").get(pk=proposal.pk, user=user)
        if proposal.status != GoalPlanProposal.Status.PENDING:
            raise ValueError("This plan proposal has already been processed.")
        payload = proposal.payload or {}
        milestones_data = payload.get("milestones", [])
        if not isinstance(milestones_data, list) or not milestones_data:
            raise ValueError("The proposal must contain at least one milestone.")
        goal = Goal.objects.select_for_update().get(pk=proposal.goal_id, user=user)
        from django.db.models import Max, Sum
        existing_weight = goal.milestones.aggregate(total=Sum("weight"))["total"] or Decimal("0")
        total_weight = sum(Decimal(str(item.get("weight", 0) or 0)) for item in milestones_data if isinstance(item, dict))
        if existing_weight + total_weight > 100:
            raise ValueError("The combined milestone weights for this goal cannot exceed 100.")
        sequence_start = goal.milestones.aggregate(max_sequence=Max("sequence"))["max_sequence"]
        sequence_start = (sequence_start if sequence_start is not None else -1) + 1
        created_milestones = []
        from tasks.models import Task
        for index, item in enumerate(milestones_data):
            if not isinstance(item, dict) or not item.get("title"):
                raise ValueError("Each milestone must have a title.")
            milestone = GoalMilestone.objects.create(
                goal=goal, title=str(item["title"])[:255], description=item.get("description", ""),
                sequence=sequence_start + index, start_date=item.get("start_date") or None, target_date=item.get("target_date") or None,
                weight=item.get("weight", 0), completion_criteria=item.get("completion_criteria", ""),
            )
            created_milestones.append(milestone)
            for task_data in item.get("tasks", []):
                if not isinstance(task_data, dict) or not task_data.get("title"):
                    raise ValueError("Each proposed task must have a title.")
                priority = task_data.get("priority", Task.Priority.MEDIUM)
                if priority not in Task.Priority.values:
                    raise ValueError("A proposed task contains an invalid priority.")
                Task.objects.create(
                    user=user, goal=goal, milestone=milestone,
                    title=str(task_data["title"])[:255], description=task_data.get("description", ""),
                    scheduled_date=task_data.get("scheduled_date") or goal.start_date or timezone.localdate(),
                    due_at=task_data.get("due_at") or None,
                    priority=priority,
                    estimated_minutes=max(0, int(task_data.get("estimated_minutes", 0) or 0)),
                )
        proposal.status = GoalPlanProposal.Status.APPROVED
        proposal.approved_at = timezone.now()
        proposal.save(update_fields=["status", "approved_at"])
        cls.record(goal, user, "plan_approved", "AI goal plan approved and materialized.", {"proposal_id": proposal.id, "milestone_count": len(created_milestones)})
        return created_milestones


class GoalAnalyticsService:
    @staticmethod
    def dashboard(user):
        goals = Goal.objects.filter(user=user)
        totals = goals.aggregate(
            total=Count("id"),
            active=Count("id", filter=Q(status__in=[Goal.Status.ACTIVE, Goal.Status.PLANNED, Goal.Status.AT_RISK])),
            completed=Count("id", filter=Q(status=Goal.Status.COMPLETED)),
            at_risk=Count("id", filter=Q(status=Goal.Status.AT_RISK)),
        )
        today = timezone.localdate()
        overdue = goals.filter(target_date__lt=today).exclude(status__in=[Goal.Status.COMPLETED, Goal.Status.CANCELLED, Goal.Status.ARCHIVED]).count()
        active_goals = list(goals.exclude(status__in=[Goal.Status.COMPLETED, Goal.Status.CANCELLED, Goal.Status.ARCHIVED]).values("id", "progress_percent", "start_date", "target_date", "status"))
        average = round(sum(item["progress_percent"] for item in active_goals) / len(active_goals)) if active_goals else 0
        from tasks.models import Task
        from goals.models import GoalMilestone, GoalActivity
        goal_ids = goals.values_list("id", flat=True)
        task_qs = Task.objects.filter(goal_id__in=goal_ids)
        task_total = task_qs.exclude(status="cancelled").count()
        task_overdue = task_qs.filter(scheduled_date__lt=today).exclude(status__in=["completed", "cancelled"]).count()
        milestone_qs = GoalMilestone.objects.filter(goal_id__in=goal_ids)
        milestone_total = milestone_qs.count()
        milestone_completed = milestone_qs.filter(status=GoalMilestone.Status.COMPLETED).count()
        recent_activity = GoalActivity.objects.filter(goal_id__in=goal_ids, event_type__in=["progress_updated", "progress_derived"], created_at__date__gte=today - timedelta(days=30)).order_by("created_at").values("created_at", "data")
        weekly_progress = []
        monthly_progress = []
        for item in recent_activity:
            entry = {"date": item["created_at"].date().isoformat(), "progress": (item["data"] or {}).get("progress", 0)}
            monthly_progress.append(entry)
            if item["created_at"].date() >= today - timedelta(days=7):
                weekly_progress.append(entry)
        return {**totals, "overdue": overdue, "average_progress": average,
                "completion_rate": round((totals["completed"] / totals["total"]) * 100) if totals["total"] else 0,
                "category_distribution": list(goals.values("category").annotate(count=Count("id")).order_by("category")),
                "milestone_total": milestone_total, "milestone_completed": milestone_completed,
                "milestone_completion_rate": round(milestone_completed / milestone_total * 100) if milestone_total else 0,
                "task_total": task_total, "overdue_task_ratio": round(task_overdue / task_total * 100) if task_total else 0,
                "weekly_progress": weekly_progress, "monthly_progress": monthly_progress}


class GoalRiskService:
    @staticmethod
    def analyze(goal):
        today = timezone.localdate()
        reasons = []
        milestones = list(goal.milestones.all())
        tasks = list(goal.tasks.all())
        overdue_milestones = sum(1 for item in milestones if item.target_date and item.target_date < today and item.status != GoalMilestone.Status.COMPLETED)
        overdue_tasks = sum(1 for item in tasks if item.scheduled_date < today and item.status not in ["completed", "cancelled"])
        days_left = (goal.target_date - today).days if goal.target_date else None
        if overdue_milestones:
            reasons.append({"code": "overdue_milestones", "count": overdue_milestones, "message": "Milestones are past their target date."})
        if overdue_tasks:
            reasons.append({"code": "overdue_tasks", "count": overdue_tasks, "message": "Linked tasks are overdue."})
        if days_left is not None and days_left < 14 and goal.progress_percent < 80 and goal.status not in [Goal.Status.COMPLETED, Goal.Status.CANCELLED, Goal.Status.ARCHIVED]:
            reasons.append({"code": "deadline_near", "days_left": days_left, "progress": goal.progress_percent, "message": "The deadline is near relative to recorded progress."})
        if goal.updated_at.date() < today and (today - goal.updated_at.date()).days >= 14 and goal.status not in [Goal.Status.COMPLETED, Goal.Status.CANCELLED, Goal.Status.ARCHIVED]:
            reasons.append({"code": "stale_goal", "days_since_update": (today - goal.updated_at.date()).days, "message": "This goal has not been updated for at least 14 days."})
        recommendations = []
        for reason in reasons:
            if reason["code"] == "overdue_milestones":
                recommendations.append({"action": "review_milestones", "reason": reason["message"], "suggestion": "Review milestone scope and propose revised target dates."})
            elif reason["code"] == "overdue_tasks":
                recommendations.append({"action": "reprioritize_tasks", "reason": reason["message"], "suggestion": "Reprioritize overdue tasks and split large tasks into smaller steps."})
            elif reason["code"] == "deadline_near":
                recommendations.append({"action": "review_scope", "reason": reason["message"], "suggestion": "Review remaining scope and agree whether to adjust scope or deadline."})
            elif reason["code"] == "stale_goal":
                recommendations.append({"action": "update_goal", "reason": reason["message"], "suggestion": "Record the latest progress and any blockers."})
        return {"risk_level": "high" if len(reasons) >= 2 else "medium" if reasons else "low", "reasons": reasons, "recommendations": recommendations}


# 
"""

"""
