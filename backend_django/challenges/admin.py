from django.contrib import admin

from challenges.models import Challenge, ChallengeAttempt, ChallengeProgress, ChallengeStep


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'type', 'status', 'difficulty', 'created_at')
    list_filter = ('type', 'status')
    search_fields = ('title', 'description')


@admin.register(ChallengeStep)
class ChallengeStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'challenge', 'order')


@admin.register(ChallengeAttempt)
class ChallengeAttemptAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'user', 'score', 'status', 'created_at')


@admin.register(ChallengeProgress)
class ChallengeProgressAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'user', 'progress_percent', 'completed_steps', 'updated_at')
