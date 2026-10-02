# automation/services/program_service.py


from __future__ import annotations
import logging
from collections import defaultdict
from django.db import transaction
from django.utils.text import slugify
from automation.engine.scanner_engine import scan_window_elements
from automation.models import ProgramElement

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC FUNCTION
# ══════════════════════════════════════════════════════════════════════════════

def scan_and_store_elements(program, user, custom_pattern: str = None) -> int:
    """
    يُستدعى من الـ view.
    يرجع عدد العناصر الجديدة اللي اتحفظت.
    """
    pattern = custom_pattern or program.window_title_pattern or program.name
    logger.info(f"🔍 Pattern: '{pattern}'")

    raw_items = scan_window_elements(pattern)
    logger.info(f"📦 Raw count: {len(raw_items)}")

    if not raw_items:
        return 0

    # ── تحميل الـ existing data مرة واحدة (أسرع من N queries) ────────
    existing_auto_ids: set[str] = set(
        ProgramElement.objects
        .filter(program=program)
        .exclude(automation_id="")
        .values_list("automation_id", flat=True)
    )
    existing_names: set[str] = set(
        ProgramElement.objects
        .filter(program=program)
        .values_list("name", flat=True)
    )
    existing_slugs: set[str] = set(
        ProgramElement.objects.values_list("slug", flat=True)
    )

    # ── تصفية المكررات ────────────────────────────────────────────────
    new_items = _filter_duplicates(
        raw_items, existing_auto_ids, existing_names)
    logger.info(f"🆕 New items after dedup: {len(new_items)}")

    if not new_items:
        return 0

    # ── Hierarchical insert ───────────────────────────────────────────
    return _hierarchical_bulk_insert(new_items, program, user, existing_slugs)


# ══════════════════════════════════════════════════════════════════════════════
# DEDUPLICATION
# ══════════════════════════════════════════════════════════════════════════════

def _filter_duplicates(
    items: list[dict],
    existing_auto_ids: set[str],
    existing_names: set[str],
) -> list[dict]:
    """يشيل العناصر اللي موجودة مسبقاً."""
    result = []
    seen_keys: set[str] = set()  # لتجنب التكرار داخل الـ batch نفسه

    for item in items:
        auto_id = item.get("automation_id", "")
        name = item.get("name", "")
        ukey = item.get("_unique_key", name)

        if ukey in seen_keys:
            continue
        if auto_id and auto_id in existing_auto_ids:
            continue
        if not auto_id and name in existing_names:
            continue

        seen_keys.add(ukey)
        result.append(item)

    return result


# ══════════════════════════════════════════════════════════════════════════════
# HIERARCHICAL BULK INSERT
# ══════════════════════════════════════════════════════════════════════════════

def _hierarchical_bulk_insert(
    items: list[dict],
    program,
    user,
    existing_slugs: set[str],
) -> int:
    """
    الخوارزمية:
    1. نرتب حسب depth_level (الأجداد الأول)
    2. نحفظ batch واحد في المرة
    3. نبني map من unique_key → DB id عشان نحل الـ parent FK
    """
    # ── ترتيب topological: depth أصغر = يتحفظ أول ────────────────────
    items_sorted = sorted(items, key=lambda x: x.get("depth_level", 0))

    # map من unique_key → ProgramElement instance (بعد ما يتحفظ)
    key_to_instance: dict[str, ProgramElement] = {}

    total_saved = 0

    # نجمّع في groups حسب depth_level
    depth_groups: dict[int, list[dict]] = defaultdict(list)
    for item in items_sorted:
        depth_groups[item.get("depth_level", 0)].append(item)

    with transaction.atomic():
        for depth in sorted(depth_groups.keys()):
            batch = depth_groups[depth]
            to_create: list[ProgramElement] = []

            for item in batch:
                slug = _unique_slug(
                    item.get("name", "element"), existing_slugs)

                # ── حل الـ parent FK ──────────────────────────────────
                parent_instance = None
                parent_key = item.get("_parent_key")
                if parent_key and parent_key in key_to_instance:
                    parent_instance = key_to_instance[parent_key]

                pe = ProgramElement(
                    program=program,
                    created_by=user,
                    slug=slug,
                    # هوية
                    name=item["name"][:255],
                    display_text=item.get("display_text", "")[:500],
                    element_type=item.get("element_type", "OTHER"),
                    description="",
                    # Automation
                    automation_id=item.get("automation_id", ""),
                    class_name=item.get("class_name", ""),
                    selector_type=item.get("selector_type", "ui"),
                    selector_value=item.get("selector_value", ""),
                    keyboard_shortcut=item.get("keyboard_shortcut", ""),
                    # إحداثيات
                    x_coordinate=item.get("x_coordinate", 0),
                    y_coordinate=item.get("y_coordinate", 0),
                    width=item.get("width", 0),
                    height=item.get("height", 0),
                    # شجرة
                    tree_path=item.get("tree_path", ""),
                    depth_level=item.get("depth_level", 0),
                    parent_element=parent_instance,
                    # حالة
                    is_visible=item.get("is_visible", True),
                    is_enabled=item.get("is_enabled", True),
                    is_clickable=item.get("is_clickable", True),
                    is_active=True,
                    # extra
                    raw_properties=item.get("raw_properties", {}),
                    stability_score=item.get("stability_score", 1.0),
                )
                to_create.append(pe)

            # ── Bulk insert هذا الـ depth ─────────────────────────────
            created = ProgramElement.objects.bulk_create(
                to_create,
                ignore_conflicts=True,
                batch_size=200,
            )

            # ── حدّث الـ map (unique_key → DB instance) ───────────────
            # bulk_create بيرجع instances مع id بعد الحفظ (Django 4.1+)
            for item, instance in zip(batch, created):
                ukey = item.get("_unique_key", item["name"])
                if instance.pk:
                    key_to_instance[ukey] = instance

            total_saved += len(created)
            logger.info(f"  depth={depth}: saved {len(created)} elements")

    logger.info(f"✅ Total saved: {total_saved}")
    return total_saved


# ══════════════════════════════════════════════════════════════════════════════
# SLUG HELPER
# ══════════════════════════════════════════════════════════════════════════════

def _unique_slug(name: str, existing: set[str]) -> str:
    base = slugify(name) or "element"
    slug = base
    i = 1
    while slug in existing:
        slug = f"{base}-{i}"
        i += 1
    existing.add(slug)
    return slug
