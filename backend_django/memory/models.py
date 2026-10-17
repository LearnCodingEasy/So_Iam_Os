from django.conf import settings
from django.db import models

class MemoryItem(models.Model):
    class Type(models.TextChoices):
        PREFERENCE='preference','Preference'; CONTEXT='context','Context'; GOAL='goal','Goal'; PROJECT='project','Project'; LEARNING='learning','Learning'; CONVERSATION='conversation','Conversation'; FACT='fact','Fact'
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='memory_items')
    type=models.CharField(max_length=30,choices=Type.choices,default=Type.FACT)
    key=models.CharField(max_length=200)
    content=models.TextField()
    source=models.CharField(max_length=100,blank=True)
    importance=models.PositiveSmallIntegerField(default=50)
    is_active=models.BooleanField(default=True)
    metadata=models.JSONField(default=dict,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-importance','-updated_at']
        indexes=[models.Index(fields=['user','type','is_active']),models.Index(fields=['user','key'])]
