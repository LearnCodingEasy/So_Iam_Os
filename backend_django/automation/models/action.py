from django.db import models
import uuid
from django.utils.text import slugify
from users_accounts.models import User
from automation.models.workflow_node import WorkflowNode


# ==================================================
# 6️⃣ Action
# ==================================================
class Action(models.Model):
    """
    التنفيذ الحقيقي
    (Mouse – Keyboard – Screen)
    """

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

    node = models.ForeignKey(
        WorkflowNode,
        on_delete=models.CASCADE,
        related_name="actions",
    )
    action_type = models.CharField(max_length=50)
    # بيانات التنفيذ
    payload = models.JSONField(default=dict)

    # ====================== 💾 Auto Save Slug ======================

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.action_type)
            slug = base_slug
            counter = 1
            while Action.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.action_type
