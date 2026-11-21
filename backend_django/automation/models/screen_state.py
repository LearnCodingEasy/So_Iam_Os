from django.db import models
import uuid
from django.utils.text import slugify
from users_accounts.models import User
from automation.models.task_run import TaskRun


# ==================================================
# 9️⃣ ScreenState
# ==================================================


class ScreenState(models.Model):
    """
    حالة الشاشة أثناء التنفيذ
    (مهم للـ AI & Vision)
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

    task_run = models.ForeignKey(
        TaskRun, related_name="screen_states", on_delete=models.CASCADE)

    screenshot = models.ImageField(upload_to="screens")

    detected_elements = models.JSONField(default=dict)

    active_program = models.CharField(max_length=100)
    action_id = models.UUIDField()
    screenshot_path = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    # ====================== 💾 Auto Save Slug ======================

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.active_program)
            slug = base_slug
            counter = 1
            while ScreenState.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.status
