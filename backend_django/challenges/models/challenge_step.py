from django.db import models
from challenges.models.challenge import Challenge


class ChallengeStep(models.Model):
    challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE,related_name='steps'); title=models.CharField(max_length=255); instructions=models.TextField(blank=True); order=models.PositiveIntegerField(default=0); expected_output=models.TextField(blank=True); metadata=models.JSONField(default=dict,blank=True)
    class Meta: ordering=['order']
