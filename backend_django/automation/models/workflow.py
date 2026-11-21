from django.db import models
import uuid
from django.utils.text import slugify
from users_accounts.models import User


# ==================================================
# 3️⃣ Workflow
# ==================================================


class Workflow(models.Model):
    """
    ده السيناريو الكامل
    (زي n8n Workflow)
    """

    STATUS = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("paused", "Paused"),
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

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS, default="draft")
    permissions = models.JSONField(default=dict, blank=True)

    # ====================== 💾 Auto Save Slug ======================

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Workflow.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Workflow Name: {self.name}"
