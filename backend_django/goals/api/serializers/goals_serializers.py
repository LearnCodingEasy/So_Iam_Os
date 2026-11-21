from django.utils import timezone
from rest_framework import serializers
from goals.models import Goal, GoalActivity, GoalMilestone, GoalPlanProposal


class GoalSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    priority_display = serializers.CharField(source="get_priority_display", read_only=True)
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    task_count = serializers.IntegerField(read_only=True)
    completed_task_count = serializers.IntegerField(read_only=True)
    milestone_count = serializers.IntegerField(read_only=True)
    completed_milestone_count = serializers.IntegerField(read_only=True)
    overdue = serializers.SerializerMethodField()
    risk = serializers.SerializerMethodField()
    related_goals = serializers.PrimaryKeyRelatedField(many=True, queryset=Goal.objects.all(), required=False)

    class Meta:
        model = Goal
        fields = [
            "id", "title", "description", "category", "category_display", "priority", "priority_display",
            "status", "status_display", "start_date", "target_date", "estimated_minutes", "actual_minutes",
            "progress_percent", "measurement_unit", "initial_value", "target_value", "current_value",
            "completion_notes", "completed_at", "metadata", "learning_goals", "skills", "related_goals",
            "task_count", "completed_task_count", "milestone_count", "completed_milestone_count", "overdue", "risk",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "status_display", "priority_display", "category_display", "task_count",
                            "completed_task_count", "milestone_count", "completed_milestone_count", "overdue",
                            "risk", "completed_at", "created_at", "updated_at"]

    def get_overdue(self, obj):
        return bool(obj.target_date and obj.target_date < timezone.localdate() and obj.status not in {
            Goal.Status.COMPLETED, Goal.Status.CANCELLED, Goal.Status.ARCHIVED})

    def get_risk(self, obj):
        from goals.services import GoalRiskService
        return GoalRiskService.analyze(obj)

    def validate(self, attrs):
        if self.instance and "status" in attrs and attrs["status"] != self.instance.status:
            from goals.services import GoalService
            if attrs["status"] not in GoalService.TRANSITIONS.get(self.instance.status, set()):
                raise serializers.ValidationError({"status": f"Transition from {self.instance.status} to {attrs['status']} is not allowed."})
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        target = attrs.get("target_date", getattr(self.instance, "target_date", None))
        if start and target and target < start:
            raise serializers.ValidationError({"target_date": "Target date cannot be before start date."})
        initial = attrs.get("initial_value", getattr(self.instance, "initial_value", None))
        target_value = attrs.get("target_value", getattr(self.instance, "target_value", None))
        current = attrs.get("current_value", getattr(self.instance, "current_value", None))
        if initial is not None and target_value is not None and initial == target_value:
            raise serializers.ValidationError({"target_value": "Target value must differ from initial value."})
        request = self.context.get("request")
        user = getattr(request, "user", None)
        for field in ("learning_goals", "skills", "related_goals"):
            values = attrs.get(field)
            if values is None:
                continue
            for item in values:
                owner_id = getattr(item, "user_id", None)
                if owner_id is not None and owner_id != user.id:
                    raise serializers.ValidationError({field: "All linked records must belong to the current user."})
                if field == "related_goals" and item.user_id != user.id:
                    raise serializers.ValidationError({field: "Related goals must belong to the current user."})
        related = attrs.get("related_goals")
        if self.instance and related is not None and any(item.pk == self.instance.pk for item in related):
            raise serializers.ValidationError({"related_goals": "A goal cannot be related to itself."})
        if initial is not None and target_value is not None and current is not None and initial != target_value:
            measured = round(float((current - initial) / (target_value - initial) * 100))
            attrs["progress_percent"] = max(0, min(100, measured))
            metadata = attrs.get("metadata", getattr(self.instance, "metadata", {}) or {})
            attrs["metadata"] = {**metadata, "progress_source": "measurement"}
        return attrs


class GoalMilestoneSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(read_only=True)
    completed_task_count = serializers.IntegerField(read_only=True)
    overdue = serializers.SerializerMethodField()

    class Meta:
        model = GoalMilestone
        fields = ["id", "goal", "depends_on", "title", "description", "sequence", "start_date", "target_date", "status",
                  "progress_percent", "weight", "completion_criteria", "completion_evidence", "completed_at",
                  "task_count", "completed_task_count", "overdue", "created_at", "updated_at"]
        read_only_fields = ["id", "completed_at", "task_count", "completed_task_count", "overdue", "created_at", "updated_at"]

    def get_overdue(self, obj):
        return bool(obj.target_date and obj.target_date < timezone.localdate() and obj.status != GoalMilestone.Status.COMPLETED)

    def validate(self, attrs):
        goal = attrs.get("goal", getattr(self.instance, "goal", None))
        if self.instance and "goal" in attrs and attrs["goal"].id != self.instance.goal_id:
            raise serializers.ValidationError({"goal": "A milestone cannot be moved to another goal."})
        request = self.context.get("request")
        if goal and request and goal.user_id != request.user.id:
            raise serializers.ValidationError({"goal": "Goal does not belong to the current user."})
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        target = attrs.get("target_date", getattr(self.instance, "target_date", None))
        if start and target and target < start:
            raise serializers.ValidationError({"target_date": "Milestone deadline cannot precede its start date."})
        if self.instance and "status" in attrs and attrs["status"] != self.instance.status:
            allowed = {
                GoalMilestone.Status.PLANNED: {GoalMilestone.Status.ACTIVE, GoalMilestone.Status.BLOCKED, GoalMilestone.Status.COMPLETED},
                GoalMilestone.Status.ACTIVE: {GoalMilestone.Status.PLANNED, GoalMilestone.Status.BLOCKED, GoalMilestone.Status.COMPLETED},
                GoalMilestone.Status.BLOCKED: {GoalMilestone.Status.ACTIVE, GoalMilestone.Status.COMPLETED},
                GoalMilestone.Status.COMPLETED: {GoalMilestone.Status.ACTIVE},
            }
            if attrs["status"] not in allowed.get(self.instance.status, set()):
                raise serializers.ValidationError({"status": "This milestone status transition is not allowed."})
        dependencies = attrs.get("depends_on")
        if dependencies is not None:
            for dependency in dependencies:
                if dependency.goal_id != goal.id:
                    raise serializers.ValidationError({"depends_on": "Milestone dependencies must belong to the same goal."})
                if self.instance and dependency.id == self.instance.id:
                    raise serializers.ValidationError({"depends_on": "A milestone cannot depend on itself."})
                if self.instance:
                    pending = list(dependency.depends_on.all())
                    visited = set()
                    while pending:
                        node = pending.pop()
                        if node.id == self.instance.id:
                            raise serializers.ValidationError({"depends_on": "This dependency would create a cycle."})
                        if node.id not in visited:
                            visited.add(node.id)
                            pending.extend(node.depends_on.all())
        if goal:
            weight = attrs.get("weight", getattr(self.instance, "weight", 0)) or 0
            from django.db.models import Sum
            used = goal.milestones.exclude(pk=getattr(self.instance, "pk", None)).aggregate(total=Sum("weight"))["total"] or 0
            if used + weight > 100:
                raise serializers.ValidationError({"weight": "The total milestone weight for a goal cannot exceed 100."})
        return attrs


class GoalPlanProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalPlanProposal
        fields = ["id", "goal", "payload", "provider", "status", "approved_at", "created_at"]
        read_only_fields = fields


class GoalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalActivity
        fields = ["id", "event_type", "description", "data", "created_at"]
        read_only_fields = fields
