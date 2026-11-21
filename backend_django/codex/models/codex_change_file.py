from django.db import models
from codex.models.change_set import ChangeSet


class CodexChangeFile(models.Model):
    changeset = models.ForeignKey(
        ChangeSet, on_delete=models.CASCADE, related_name='file_changes')
    path = models.CharField(max_length=700)
    before_content = models.TextField(blank=True)
    after_content = models.TextField(blank=True)
    before_sha256 = models.CharField(max_length=64, blank=True)
    after_sha256 = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
