from django.db import models
import uuid
from django.utils.text import slugify
from users_accounts.models import User
from automation.models.workflow import Workflow
from automation.models.workflow_node import WorkflowNode


# ==================================================
# 5️⃣ WorkflowEdge
# ==================================================
class WorkflowEdge(models.Model):
    """
    الخط اللي بيربط نود بنود
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

    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE,
        related_name="edges",
    )

    source_node = models.ForeignKey(
        WorkflowNode,
        related_name="out_edges",
        on_delete=models.CASCADE,
    )

    target_node = models.ForeignKey(
        WorkflowNode,
        related_name="in_edges",
        on_delete=models.CASCADE,
    )

    # success / fail / true / false
    condition = models.CharField(
        max_length=100, blank=True, null=True, default="success")
    edge_type = models.CharField(max_length=50, default="default")

    # ====================== 💾 Auto Save Slug ======================

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.condition)
            slug = base_slug
            counter = 1
            while WorkflowEdge.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.condition
