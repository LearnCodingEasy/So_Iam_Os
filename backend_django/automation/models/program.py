from django.db import models
from django.conf import settings
import uuid
from django.utils.text import slugify
from users_accounts.models import User


# ==================================================
# 1️⃣ Program
# ==================================================


class Program(models.Model):

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

    # ====================== ℹ️ Basic Info ======================
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # ====================== ⚡ Execution ======================
    # مسار تشغيل البرنامج
    executable_path = models.CharField(max_length=500)
    project_path = models.CharField(max_length=500, blank=True, null=True)
    # فولدر تشغيل
    working_directory = models.CharField(max_length=500, blank=True, null=True)
    # عنوان الشباك للتأكد
    window_title_pattern = models.CharField(max_length=255, blank=True)
    # اختصارات عامة
    # global_shortcuts = models.JSONField(default=dict, blank=True)

    # ====================== 📊 State ======================
    # هل البرنامج شغال
    # is_running = models.BooleanField(default=False)
    # last_run_at = models.DateTimeField(null=True, blank=True)
    # last_status = models.CharField(
    #     max_length=50,
    #     choices=[
    #         ("success", "Success"),
    #         ("failed", "Failed"),
    #         ("running", "Running"),
    #         ("idle", "Idle"),
    #     ],
    #     default="idle",
    # )

    # ====================== 🎨 UI / Visual ======================
    # icon = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="programs", blank=True, null=True)
    # is_installed = models.BooleanField(default=True)

    # ====================== ⚙️ Configuration ======================
    # إعدادات مخصصة
    # settings = models.JSONField(default=dict, blank=True)
    # متغيرات البيئة
    # env_variables = models.JSONField(default=dict, blank=True)
    # ==========================================
    # Property جاهزة لاستخدام عنوان النافذة
    # ==========================================
    @property
    def window_title(self):
        # لو فيه pattern، رجعها، لو لأ رجع اسم البرنامج
        return self.window_title_pattern or self.name

    # ====================== 🖼️ Helper ======================

    def get_image(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        return "https://placehold.co/400x400?text=Program"

    # ====================== 💾 Auto Save Slug ======================
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Program.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
