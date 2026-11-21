from django.db import models
import uuid
from django.utils.text import slugify
from users_accounts.models import User
from automation.models.program import Program


# ==================================================
# 7️⃣ Task
# ==================================================
class Task(models.Model):

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

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="tasks",
        null=True, blank=True
    )

    # ====================== 💾 Auto Save Slug ======================
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Task.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
