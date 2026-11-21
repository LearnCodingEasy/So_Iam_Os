from django.conf import settings
from django.db import models
from challenges.models.challenge import Challenge


class ChallengeProgress(models.Model):
    challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE,related_name='progress_rows'); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='challenge_progress'); progress_percent=models.PositiveSmallIntegerField(default=0); completed_steps=models.PositiveIntegerField(default=0); updated_at=models.DateTimeField(auto_now=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['challenge','user'],name='challenge_user_unique')]
