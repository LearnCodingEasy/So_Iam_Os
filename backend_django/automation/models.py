"""
models.py
==========
الملف ده هو عقل الداتابيز كله
لازم يعدي من هنا الأول
"""
from django.db import models
from django.conf import settings
import uuid
from django.utils.text import slugify
# App User
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


# ==================================================
# 2️⃣ ProgramElement
# ==================================================
class ProgramElement(models.Model):

    ELEMENT_TYPES = [
        ("BUTTON",   "Button"),
        ("INPUT",    "Text Input"),
        ("CHECKBOX", "Checkbox"),
        ("RADIO",    "Radio Button"),
        ("MENU",     "Menu Item"),
        ("LISTBOX",  "List Box"),
        ("COMBOBOX", "Combo Box"),
        ("TAB",      "Tab Control"),
        ("LINK",     "Hyperlink"),
        ("TEXT",     "Static Text"),
        ("OTHER",    "Other"),
    ]

    SELECTOR_TYPES = [
        ("ui",     "UI Automation"),
        ("image",  "Image Recognition"),
        ("coords", "Screen Coordinates"),
        ("text",   "Text OCR"),
    ]

    # ── Identity ───────────────────────────────────────
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # ── Relations ─────────────────────────────────────
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="elements")
    parent_element = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    # ── Element Identity ──────────────────────────────
    name = models.CharField(max_length=255, db_index=True)
    display_text = models.CharField(max_length=500, blank=True)
    element_type = models.CharField(
        max_length=20, choices=ELEMENT_TYPES, default="OTHER")
    description = models.TextField(blank=True)

    # ── Automation Properties ─────────────────────────
    automation_id = models.CharField(max_length=500, blank=True, db_index=True)
    class_name = models.CharField(
        max_length=500, blank=True, default='default_value')
    selector_type = models.CharField(
        max_length=20, choices=SELECTOR_TYPES, default="ui")
    selector_value = models.TextField(blank=True)   # للـ xpath / image path
    keyboard_shortcut = models.CharField(
        max_length=100, blank=True, default="")
    help_text = models.TextField(blank=True)

    # ── Coordinates ───────────────────────────────────
    x_coordinate = models.IntegerField(null=True, blank=True)
    y_coordinate = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

    # ── Hierarchy ─────────────────────────────────────
    tree_path = models.CharField(max_length=1000, blank=True)
    depth_level = models.IntegerField(default=0)

    # ── State ─────────────────────────────────────────
    is_visible = models.BooleanField(default=True)
    is_enabled = models.BooleanField(default=True)
    is_clickable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    # ── Extra ─────────────────────────────────────────
    raw_properties = models.JSONField(default=dict)
    stability_score = models.FloatField(default=1.0)
    image = models.ImageField(
        upload_to="programs_element", blank=True, null=True)
    confidence = models.FloatField(default=0.8)

    class Meta:
        indexes = [
            models.Index(fields=['program', 'automation_id']),
            models.Index(fields=['program', 'name']),
        ]

    def get_image(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        return "https://placehold.co/400x400?text=Element"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) if self.name else "element"
            slug = base
            i = 1
            while ProgramElement.objects.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.element_type})"
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

# ==================================================
# 🔟 Delay
# ==================================================


class Delay(models.Model):

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
    seconds = models.IntegerField()

    # ====================== 💾 Auto Save Slug ======================

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Delay.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
