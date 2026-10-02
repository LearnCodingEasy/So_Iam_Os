# automation

## app

```cmd
python manage.py startapp automation
```

## 1️⃣ Program

### models

```python
"""
models.py
==========
الملف ده هو عقل الداتابيز كله
أي Automation – Workflow – Node – Action
لازم يعدي من هنا الأول

اقرأ التعليقات كويس 👇
"""

from django.db import models
from django.conf import settings
import uuid

# App User
from users_accounts.models import User

from django.utils.text import slugify

# ==================================================
# 1️⃣ Program
# ==================================================
class Program(models.Model):
    """
    🖥️ يمثل أي برنامج على جهازك
    (Photoshop – Chrome – Premiere – VSCode)

    الهدف:
    - السيستم يبقى فاهم البرنامج
    - يعرف يضغط فين
    - يعرف يستخدم الاختصارات
    """

    # ====================== 🆔 IDs ======================
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ====================== ℹ️ Basic Info ======================
    # اسم البرنامج اللي هيظهر في الواجهة
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)  # URL-friendly
    description = models.TextField(blank=True)  # وصف اختياري

    # ====================== ⚡ Execution ======================
    executable_path = models.CharField(max_length=500)  # مسار تشغيل البرنامج
    project_path = models.CharField(
        max_length=500, blank=True, null=True)  # مشروع مرتبط
    working_directory = models.CharField(
        max_length=500, blank=True, null=True)  # فولدر تشغيل
    window_title_pattern = models.CharField(
        max_length=255, blank=True)  # عنوان الشباك للتأكد
    global_shortcuts = models.JSONField(
        default=dict, blank=True)  # اختصارات عامة

    # ====================== 📊 State ======================
    is_running = models.BooleanField(default=False)  # هل البرنامج شغال
    last_run_at = models.DateTimeField(null=True, blank=True)
    last_status = models.CharField(
        max_length=50,
        choices=[
            ("success", "Success"),
            ("failed", "Failed"),
            ("running", "Running"),
            ("idle", "Idle"),
        ],
        default="idle",
    )

    # ====================== 🎨 UI / Visual ======================
    icon = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="programs", blank=True, null=True)
    is_installed = models.BooleanField(default=True)

    # ====================== ⚙️ Configuration ======================
    settings = models.JSONField(default=dict, blank=True)  # إعدادات مخصصة
    env_variables = models.JSONField(
        default=dict, blank=True)  # متغيرات البيئة

    # ====================== 🗂️ Meta ======================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

```

### serializers

```python
# backend_django\automation\serializers.py

from rest_framework import serializers
from .models import Program

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"

```

### views

```python
# backend_django\automation\views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from django.utils import timezone

from .models import Program
from .serializers import ProgramSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    """
    🖥️ ViewSet لإدارة البرامج وتشغيلها وتتبع حالتها
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

```

### urls

```python

# backend_django\automation\urls.py
from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet

router = DefaultRouter()

router.register("programs", ProgramViewSet, basename="programs")

urlpatterns = router.urls

```

### admin

```python
# backend_django\automation\admin.py

# 🛠️ Django استيراد أدوات إدارة
from django.contrib import admin

# 🌐 (Model) استيراد نموذج
from .models import Program

# 🖥️ في لوحة الإدارة Website تسجيل نموذج
admin.site.register(Program)

```

## app

## app

## app
