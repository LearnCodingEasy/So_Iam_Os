from django.conf import settings
from django.db import models
from challenges.models.challenge import Challenge


class ChallengeAttempt(models.Model):
    challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE,related_name='attempts'); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='challenge_attempts'); answer=models.TextField(blank=True); score=models.PositiveSmallIntegerField(default=0); feedback=models.TextField(blank=True); status=models.CharField(max_length=20,default='submitted'); created_at=models.DateTimeField(auto_now_add=True)
