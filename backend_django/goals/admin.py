from django.contrib import admin

from .models import Goal, GoalActivity, GoalMilestone, GoalPlanProposal


class GoalMilestoneInline(admin.TabularInline):
    model = GoalMilestone
    extra = 0
    fields = ("title", "sequence", "status", "progress_percent", "weight", "target_date")


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "status", "priority", "progress_percent", "target_date")
    list_filter = ("category", "status", "priority")
    search_fields = ("title", "description", "user__username", "user__email")
    readonly_fields = ("created_at", "updated_at", "completed_at")
    inlines = (GoalMilestoneInline,)


@admin.register(GoalPlanProposal)
class GoalPlanProposalAdmin(admin.ModelAdmin):
    list_display = ("id", "goal", "user", "provider", "status", "created_at", "approved_at")
    list_filter = ("status", "provider")
    readonly_fields = ("created_at", "approved_at", "payload")


@admin.register(GoalActivity)
class GoalActivityAdmin(admin.ModelAdmin):
    list_display = ("goal", "user", "event_type", "created_at")
    list_filter = ("event_type",)
    readonly_fields = ("goal", "user", "event_type", "description", "data", "created_at")
