from django.db import models
import uuid
from django.utils.text import slugify
from users_accounts.models import User
from automation.models.program import Program
from automation.models.program_element import ProgramElement
from automation.models.workflow import Workflow


# ==================================================
# 4️⃣ WorkflowNode (VueFlow Node)
# ==================================================
class WorkflowNode(models.Model):
    """
    كل مربع في VueFlow = Node هنا
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
        related_name="nodes",
    )

    # نوع النود (click – wait – open_program)
    node_type = models.CharField(max_length=50)

    label = models.CharField(max_length=100)

    # ربط اختياري ببرنامج / عنصر
    program = models.ForeignKey(
        Program, null=True, blank=True, on_delete=models.SET_NULL)
    element = models.ForeignKey(
        ProgramElement, null=True, blank=True, on_delete=models.SET_NULL)

    # مكانه في VueFlow
    position_x = models.FloatField()
    position_y = models.FloatField()

    # إعدادات النود (JSON)
    config = models.JSONField(default=dict, blank=True)

    # ====================== 💾 Auto Save Slug ======================
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.label)
            slug = base_slug
            counter = 1
            while WorkflowNode.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Node: {self.label} | Workflow: {self.workflow}"
