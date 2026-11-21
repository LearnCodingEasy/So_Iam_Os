from django.db import models
from django.conf import settings
import uuid
from django.utils.text import slugify
from users_accounts.models import User
from automation.models.program import Program


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
