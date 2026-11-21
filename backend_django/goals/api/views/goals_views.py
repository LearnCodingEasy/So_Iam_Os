import logging
from django.db import transaction
from django.db.models import Count, Q, Sum
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from ai.exceptions import AIError
from core.cache_utils import invalidate_dashboard
from projects.models import Project, ProjectGoal
from goals.models import Goal, GoalMilestone, GoalPlanProposal
from goals.api.serializers import GoalActivitySerializer, GoalMilestoneSerializer, GoalPlanProposalSerializer, GoalSerializer
from goals.services import GoalAnalyticsService, GoalRiskService, GoalService


logger = logging.getLogger(__name__)


class GoalPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = GoalPagination

    def get_queryset(self):
        queryset = (Goal.objects.filter(user=self.request.user)
            .prefetch_related("skills", "learning_goals", "related_goals", "milestones", "tasks")
            .annotate(
                task_count=Count("tasks", distinct=True),
                completed_task_count=Count("tasks", filter=Q(tasks__status="completed"), distinct=True),
                milestone_count=Count("milestones", distinct=True),
                completed_milestone_count=Count("milestones", filter=Q(milestones__status=GoalMilestone.Status.COMPLETED), distinct=True),
            ))
        params = self.request.query_params
        if params.get("status"):
            queryset = queryset.filter(status=params["status"])
        if params.get("category"):
            queryset = queryset.filter(category=params["category"])
        if params.get("priority"):
            queryset = queryset.filter(priority=params["priority"])
        if params.get("search"):
            queryset = queryset.filter(Q(title__icontains=params["search"]) | Q(description__icontains=params["search"]))
        if params.get("overdue") in {"true", "1"}:
            from django.utils import timezone
            queryset = queryset.filter(target_date__lt=timezone.localdate()).exclude(status__in=[Goal.Status.COMPLETED, Goal.Status.CANCELLED, Goal.Status.ARCHIVED])
        ordering = params.get("ordering")
        if ordering in {"target_date", "-target_date", "created_at", "-created_at", "priority", "-priority", "progress_percent", "-progress_percent", "title", "-title"}:
            queryset = queryset.order_by(ordering)
        return queryset

    def perform_create(self, serializer):
        goal = serializer.save(user=self.request.user)
        if goal.progress_percent == 100 or goal.status == Goal.Status.COMPLETED:
            goal.progress_percent = 100
            goal.status = Goal.Status.COMPLETED
            from django.utils import timezone
            goal.completed_at = timezone.now()
            goal.save(update_fields=["status", "completed_at", "updated_at"])
        GoalService.record(goal, self.request.user, "created", "Goal created.")
        invalidate_dashboard(self.request.user.id)

    def perform_update(self, serializer):
        previous_status = serializer.instance.status
        goal = serializer.save()
        if goal.status == Goal.Status.COMPLETED:
            from django.utils import timezone
            goal.progress_percent = 100
            goal.completed_at = goal.completed_at or timezone.now()
            goal.save(update_fields=["progress_percent", "completed_at", "updated_at"])
        elif previous_status == Goal.Status.COMPLETED:
            goal.completed_at = None
            if goal.status == Goal.Status.ACTIVE and goal.progress_percent == 100:
                goal.progress_percent = 0
            goal.save(update_fields=["completed_at", "progress_percent", "updated_at"])
        GoalService.record(goal, self.request.user, "updated", "Goal details updated.")
        if goal.status == Goal.Status.COMPLETED and previous_status != Goal.Status.COMPLETED:
            GoalService.notify(self.request.user, "تم تحقيق هدف", f"اكتمل الهدف: {goal.title}", goal)
        invalidate_dashboard(self.request.user.id)

    def perform_destroy(self, instance):
        GoalService.record(instance, self.request.user, "deleted", "Goal deleted.")
        instance.delete()
        invalidate_dashboard(self.request.user.id)

    @action(detail=False, methods=["get"])
    def analytics(self, request):
        return Response(GoalAnalyticsService.dashboard(request.user))

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        goal = self.get_object()
        items = goal.activity.all()[:200]
        return Response(GoalActivitySerializer(items, many=True).data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        try:
            goal = GoalService.complete(self.get_object(), request.user, request.data.get("notes", ""))
        except ValueError as exc:
            raise ValidationError({"status": str(exc)}) from exc
        invalidate_dashboard(request.user.id)
        return Response(self.get_serializer(goal).data)

    @action(detail=True, methods=["post"])
    def pause(self, request, pk=None):
        return self._set_status(request, Goal.Status.PAUSED)

    @action(detail=True, methods=["post"])
    def resume(self, request, pk=None):
        return self._set_status(request, Goal.Status.ACTIVE)

    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        return self._set_status(request, Goal.Status.ARCHIVED)

    def _set_status(self, request, new_status):
        try:
            goal = GoalService.set_status(self.get_object(), new_status, request.user)
        except ValueError as exc:
            raise ValidationError({"status": str(exc)}) from exc
        invalidate_dashboard(request.user.id)
        return Response(self.get_serializer(goal).data)

    @action(detail=True, methods=["post"], url_path="progress")
    def progress(self, request, pk=None):
        if "progress_percent" not in request.data:
            raise ValidationError({"progress_percent": "This field is required."})
        try:
            goal = GoalService.update_progress(self.get_object(), request.data["progress_percent"], request.user)
        except ValueError as exc:
            raise ValidationError({"progress_percent": str(exc)}) from exc
        invalidate_dashboard(request.user.id)
        return Response(self.get_serializer(goal).data)

    @action(detail=True, methods=["post"])
    def duplicate(self, request, pk=None):
        source = self.get_object()
        with transaction.atomic():
            clone = Goal.objects.create(user=request.user, title=f"{source.title} (Copy)", description=source.description,
                category=source.category, priority=source.priority, status=Goal.Status.DRAFT,
                start_date=source.start_date, target_date=source.target_date, estimated_minutes=source.estimated_minutes,
                measurement_unit=source.measurement_unit, initial_value=source.initial_value, target_value=source.target_value,
                metadata={**(source.metadata or {}), "duplicated_from": source.id})
            clone.learning_goals.set(source.learning_goals.all())
            clone.skills.set(source.skills.all())
            GoalService.record(clone, request.user, "duplicated", "Goal duplicated.", {"source_goal_id": source.id})
        return Response(self.get_serializer(clone).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def coach(self, request, pk=None):
        goal = self.get_object()
        message = str(request.data.get("message", "")).strip()
        if not message:
            raise ValidationError({"message": "A question is required."})
        if len(message) > 4000:
            raise ValidationError({"message": "The question cannot exceed 4000 characters."})
        try:
            from goals.services.coach import GoalCoachService
            answer = GoalCoachService.answer(goal, request.user, message)
        except AIError as exc:
            logger.warning("Goal coach provider failure for user=%s goal=%s (%s)",
                           request.user.pk, goal.pk, exc.__class__.__name__)
            return Response({
                "success": False,
                "code": "ai_provider_unavailable",
                "error": str(exc),
            }, status=status.HTTP_502_BAD_GATEWAY)
        except (ValueError, TypeError) as exc:
            logger.warning("Goal coach returned invalid output for goal=%s (%s)",
                           goal.pk, exc.__class__.__name__)
            return Response({
                "success": False,
                "code": "ai_invalid_response",
                "error": "The AI provider returned an invalid response. Please retry.",
            }, status=status.HTTP_502_BAD_GATEWAY)
        except Exception:
            logger.exception("Unexpected goal coach failure for user=%s goal=%s",
                             request.user.pk, goal.pk)
            return Response({
                "success": False,
                "code": "ai_internal_error",
                "error": "The AI coach could not complete this request.",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        GoalService.record(goal, request.user, "coach_question", "Goal Coach answered a question.", {"provider": answer.get("provider", "")})
        return Response(answer)

    @action(detail=True, methods=["post"], url_path="plan")
    def plan(self, request, pk=None):
        goal = self.get_object()
        if goal.status in {Goal.Status.COMPLETED, Goal.Status.CANCELLED, Goal.Status.ARCHIVED}:
            raise ValidationError({"goal": "A new execution plan cannot be generated for a completed, cancelled or archived goal."})
        try:
            from goals.services.coach import GoalCoachService
            payload, provider = GoalCoachService.propose_plan(
                goal, request.user, request.data.get("instructions", "")
            )
        except AIError as exc:
            logger.warning("Goal plan provider failure for user=%s goal=%s (%s)",
                           request.user.pk, goal.pk, exc.__class__.__name__)
            return Response({
                "success": False,
                "code": "ai_provider_unavailable",
                "error": str(exc),
            }, status=status.HTTP_502_BAD_GATEWAY)
        except (ValueError, TypeError) as exc:
            logger.warning("Goal plan output invalid for goal=%s (%s)",
                           goal.pk, exc.__class__.__name__)
            return Response({
                "success": False,
                "code": "ai_invalid_response",
                "error": "The AI provider returned an invalid plan. Please retry.",
            }, status=status.HTTP_502_BAD_GATEWAY)
        except Exception:
            logger.exception("Unexpected goal plan failure for user=%s goal=%s",
                             request.user.pk, goal.pk)
            return Response({
                "success": False,
                "code": "ai_internal_error",
                "error": "The AI plan could not be generated.",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        proposal = GoalPlanProposal.objects.create(goal=goal, user=request.user, payload=payload, provider=provider)
        GoalService.record(goal, request.user, "plan_proposed", "AI generated a plan proposal. No tasks or milestones were created.", {"proposal_id": proposal.id, "provider": provider})
        return Response(GoalPlanProposalSerializer(proposal).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="reject-plan")
    def reject_plan(self, request, pk=None):
        goal = self.get_object()
        proposal_id = request.data.get("proposal_id")
        proposal = GoalPlanProposal.objects.filter(pk=proposal_id, goal=goal, user=request.user).first()
        if not proposal:
            raise ValidationError({"proposal_id": "Plan proposal not found."})
        if proposal.status != GoalPlanProposal.Status.PENDING:
            raise ValidationError({"proposal_id": "This proposal has already been processed."})
        proposal.status = GoalPlanProposal.Status.REJECTED
        proposal.save(update_fields=["status"])
        GoalService.record(goal, request.user, "plan_rejected", "AI plan proposal rejected.", {"proposal_id": proposal.id})
        return Response(GoalPlanProposalSerializer(proposal).data)

    @action(detail=True, methods=["get"])
    def plans(self, request, pk=None):
        goal = self.get_object()
        return Response(GoalPlanProposalSerializer(goal.plan_proposals.filter(user=request.user), many=True).data)

    @action(detail=True, methods=["post"], url_path="approve-plan")
    def approve_plan(self, request, pk=None):
        self.get_object()
        proposal_id = request.data.get("proposal_id")
        if not proposal_id:
            raise ValidationError({"proposal_id": "This field is required."})
        try:
            proposal = GoalPlanProposal.objects.get(pk=proposal_id, goal_id=pk, user=request.user)
            milestones = GoalService.approve_plan(proposal, request.user)
        except GoalPlanProposal.DoesNotExist as exc:
            raise ValidationError({"proposal_id": "Plan proposal not found."}) from exc
        except (ValueError, TypeError) as exc:
            raise ValidationError({"plan": str(exc)}) from exc
        proposal.refresh_from_db()
        invalidate_dashboard(request.user.id)
        return Response({"proposal": GoalPlanProposalSerializer(proposal).data,
                         "created_milestones": GoalMilestoneSerializer(milestones, many=True).data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def notes(self, request, pk=None):
        goal = self.get_object()
        note = str(request.data.get("note", "")).strip()
        if not note:
            raise ValidationError({"note": "A non-empty note is required."})
        if len(note) > 10000:
            raise ValidationError({"note": "Notes cannot exceed 10000 characters."})
        event = GoalService.record(goal, request.user, "note_added", note)
        return Response(GoalActivitySerializer(event).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="milestones/reorder")
    def reorder_milestones(self, request, pk=None):
        goal = self.get_object()
        ordered_ids = request.data.get("milestone_ids")
        if not isinstance(ordered_ids, list):
            raise ValidationError({"milestone_ids": "A list of milestone IDs is required."})
        current_ids = set(goal.milestones.values_list("id", flat=True))
        if len(ordered_ids) != len(set(ordered_ids)) or set(ordered_ids) != current_ids:
            raise ValidationError({"milestone_ids": "The list must contain every milestone for this goal exactly once."})
        with transaction.atomic():
            stages = list(goal.milestones.select_for_update())
            for index, stage in enumerate(stages):
                stage.sequence = 100000 + index
                stage.save(update_fields=["sequence", "updated_at"])
            by_id = {stage.id: stage for stage in stages}
            for index, milestone_id in enumerate(ordered_ids):
                stage = by_id[milestone_id]
                stage.sequence = index
                stage.save(update_fields=["sequence", "updated_at"])
        return Response(GoalMilestoneSerializer(goal.milestones.all(), many=True).data)

    @action(detail=True, methods=["get", "post"], url_path="projects")
    def projects(self, request, pk=None):
        goal = self.get_object()
        if request.method == "GET":
            links = ProjectGoal.objects.filter(goal=goal, project__user=request.user).select_related("project")
            return Response([{"id": link.project_id, "title": link.project.title, "status": link.project.status} for link in links])
        project_id = request.data.get("project_id")
        try:
            project = Project.objects.filter(pk=project_id, user=request.user).first()
        except (TypeError, ValueError):
            project = None
        if not project:
            raise ValidationError({"project_id": "Project not found for this user."})
        link, created = ProjectGoal.objects.get_or_create(project=project, goal=goal)
        if created:
            GoalService.record(goal, request.user, "project_linked", "Project linked to goal.", {"project_id": project.id})
        return Response({"project_id": project.id, "created": created}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def risk(self, request, pk=None):
        return Response(GoalRiskService.analyze(self.get_object()))


class GoalMilestoneViewSet(viewsets.ModelViewSet):
    serializer_class = GoalMilestoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = GoalMilestone.objects.filter(goal__user=self.request.user).select_related("goal").annotate(
            task_count=Count("tasks", distinct=True),
            completed_task_count=Count("tasks", filter=Q(tasks__status="completed"), distinct=True),
        )
        goal_id = self.request.query_params.get("goal")
        return queryset.filter(goal_id=goal_id) if goal_id else queryset

    def perform_create(self, serializer):
        goal = serializer.validated_data["goal"]
        with transaction.atomic():
            locked_goal = Goal.objects.select_for_update().get(pk=goal.pk, user=self.request.user)
            from django.db.models import Sum
            used = locked_goal.milestones.aggregate(total=Sum("weight"))["total"] or 0
            if used + (serializer.validated_data.get("weight") or 0) > 100:
                raise ValidationError({"weight": "The total milestone weight for a goal cannot exceed 100."})
            milestone = serializer.save()
            GoalService.record(milestone.goal, self.request.user, "milestone_created", "Milestone created.", {"milestone_id": milestone.id})
            GoalService.recalculate_from_milestones(milestone.goal)
            invalidate_dashboard(self.request.user.id)

    def perform_update(self, serializer):
        previous_status = serializer.instance.status
        milestone = serializer.save()
        if milestone.status == GoalMilestone.Status.COMPLETED:
            milestone.progress_percent = 100
            milestone.completed_at = milestone.completed_at or timezone.now()
            milestone.save(update_fields=["progress_percent", "completed_at", "updated_at"])
        elif milestone.progress_percent == 100:
            milestone.status = GoalMilestone.Status.COMPLETED
            milestone.completed_at = milestone.completed_at or timezone.now()
            milestone.save(update_fields=["status", "completed_at", "updated_at"])
        GoalService.record(milestone.goal, self.request.user, "milestone_updated", "Milestone updated.", {"milestone_id": milestone.id})
        if milestone.status == GoalMilestone.Status.COMPLETED and previous_status != GoalMilestone.Status.COMPLETED:
            GoalService.notify(self.request.user, "اكتملت مرحلة", f"اكتملت المرحلة {milestone.title} ضمن الهدف {milestone.goal.title}", milestone)
        GoalService.recalculate_from_milestones(milestone.goal)
        invalidate_dashboard(self.request.user.id)

    def perform_destroy(self, instance):
        goal = instance.goal
        GoalService.record(goal, self.request.user, "milestone_deleted", "Milestone deleted.", {"milestone_id": instance.id})
        instance.delete()
        if goal.milestones.exists():
            GoalService.recalculate_from_milestones(goal)
        else:
            GoalService.recalculate_goal(goal)
        invalidate_dashboard(self.request.user.id)
