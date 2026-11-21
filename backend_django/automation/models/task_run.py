from django.db import models
import uuid
from django.utils.text import slugify
from users_accounts.models import User
from automation.models.workflow import Workflow


# ==================================================
# 8️⃣ TaskRun
# ==================================================


class TaskRun(models.Model):
    """
    سجل تشغيل الـ Workflow
    """

    STATUS = [
        ("running", "Running"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    # ___________________
    # حقل يتم تعبئة تلقائي
    # ___________________
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(
        max_length=255, editable=False, unique=True, blank=True)
    # ====================== 🗂️ Meta ======================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS)

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    logs = models.TextField(blank=True)

    # ====================== 💾 Auto Save Slug ======================
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.status)
            slug = base_slug
            counter = 1
            while TaskRun.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.status
