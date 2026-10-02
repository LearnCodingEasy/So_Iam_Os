# automation/engine/scanner_engine.py
"""
UI Automation Tree Discovery Engine
=====================================
استراتيجية الـ ID (بالأولوية):
  1. automation_id  — ثابت حتى لو اتغير الـ label
  2. name           — الاسم الظاهر
  3. control_type + index في الأب — fallback آمن

دعم المنصات:
  - UIA  (WPF / Win32 حديث / Electron Accessibility Tree)
  - win32 (MSAA — تطبيقات قديمة)
  - ShortcutLibrary (Electron apps اللي بتعطّل UIA عمداً)
"""

from __future__ import annotations
import re
import time
import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

# ─── نوع الـ control → ELEMENT_TYPE ───────────────────────────────────────────
_CONTROL_MAP: dict[str, str] = {
    "button": "BUTTON", "togglebutton": "BUTTON", "splitbutton": "BUTTON",
    "edit": "INPUT", "combobox": "INPUT", "spinner": "INPUT",
    "datepicker": "INPUT", "dateti": "INPUT",
    "checkbox": "CHECKBOX",
    "radiobutton": "RADIO",
    "menuitem": "MENU", "menu": "MENU", "menubar": "MENU",
    "listitem": "LISTBOX", "listbox": "LISTBOX",
    "tabitem": "TAB",
    "hyperlink": "LINK",
    "text": "TEXT", "static": "TEXT",
    "treeitem": "OTHER", "dataitem": "OTHER",
}

# عناصر بتتفلتر (containers لا تفيد الأتوميشن)
_SKIP_CONTROLS = {
    "pane", "group", "window", "scrollbar", "thumb",
    "titlebar", "statusbar", "separator", "image",
    "document", "header", "scrollviewer", "custom",
    "progressbar", "tooltip",
}

_IGNORED_CLASSES = {
    "Chrome_WidgetWin_1", "Chrome_WidgetWin_0",
    "Shell_TrayWnd", "WorkerW", "Progman", "tooltips_class32",
}

# حد أقصى للأبعاد (فوق ده = container مش عنصر)
_MAX_ELEMENT_W = 1400
_MAX_ELEMENT_H = 900


# ─── Data class للعنصر أثناء البناء ──────────────────────────────────────────
@dataclass
class RawElement:
    """تمثيل مؤقت للعنصر قبل الحفظ في الـ DB."""
    # هوية
    name: str
    display_text: str
    element_type: str
    automation_id: str
    class_name: str
    selector_value: str
    keyboard_shortcut: str
    # إحداثيات
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    # حالة
    is_visible: bool = True
    is_enabled: bool = True
    is_clickable: bool = True
    raw_properties: dict = field(default_factory=dict)
    # شجرة (يتملى بعدين)
    tree_path: str = ""
    depth_level: int = 0
    parent_key: Optional[str] = None          # unique_key بتاع الأب
    unique_key: str = ""                       # المفتاح الفريد للعنصر ده
    stability_score: float = 1.0


# ─── Shortcut Library (Electron apps) ────────────────────────────────────────
_SHORTCUT_LIBRARIES: dict[str, list[dict]] = {
    "visual studio code": [
        {"name": "Save File",       "automation_id": "Ctrl+S",
            "keyboard_shortcut": "Ctrl+S",       "element_type": "BUTTON"},
        {"name": "Save All",        "automation_id": "Ctrl+K S",
            "keyboard_shortcut": "Ctrl+K S",     "element_type": "BUTTON"},
        {"name": "Open File",       "automation_id": "Ctrl+O",
            "keyboard_shortcut": "Ctrl+O",       "element_type": "BUTTON"},
        {"name": "New File",        "automation_id": "Ctrl+N",
            "keyboard_shortcut": "Ctrl+N",       "element_type": "BUTTON"},
        {"name": "Command Palette", "automation_id": "Ctrl+Shift+P",
            "keyboard_shortcut": "Ctrl+Shift+P", "element_type": "BUTTON"},
        {"name": "Find in File",    "automation_id": "Ctrl+F",
            "keyboard_shortcut": "Ctrl+F",       "element_type": "INPUT"},
        {"name": "Toggle Terminal", "automation_id": "Ctrl+`",
            "keyboard_shortcut": "Ctrl+`",       "element_type": "BUTTON"},
        {"name": "Format Document", "automation_id": "Shift+Alt+F",
            "keyboard_shortcut": "Shift+Alt+F",  "element_type": "BUTTON"},
        {"name": "Run/Debug",       "automation_id": "F5",
            "keyboard_shortcut": "F5",           "element_type": "BUTTON"},
    ],
    "obs": [
        {"name": "Start Recording", "automation_id": "OBS_RECORD",
            "keyboard_shortcut": "Ctrl+R",       "element_type": "BUTTON"},
        {"name": "Start Streaming", "automation_id": "OBS_STREAM",
            "keyboard_shortcut": "Ctrl+Shift+S", "element_type": "BUTTON"},
        {"name": "Screenshot",      "automation_id": "OBS_SHOT",
            "keyboard_shortcut": "Ctrl+F10",     "element_type": "BUTTON"},
        {"name": "Mute Audio",      "automation_id": "OBS_MUTE",
            "keyboard_shortcut": "Ctrl+M",       "element_type": "BUTTON"},
    ],
    "whatsapp": [
        {"name": "New Chat",     "automation_id": "WA_NEW",
            "keyboard_shortcut": "Ctrl+N",  "element_type": "BUTTON"},
        {"name": "Search",       "automation_id": "WA_SEARCH",
            "keyboard_shortcut": "Ctrl+F",  "element_type": "INPUT"},
        {"name": "Send Message", "automation_id": "WA_SEND",
            "keyboard_shortcut": "Enter",   "element_type": "BUTTON"},
        {"name": "Attach File",  "automation_id": "WA_ATTACH",
            "keyboard_shortcut": "Ctrl+O",  "element_type": "BUTTON"},
    ],
    "excel": [
        {"name": "Save",          "automation_id": "FileSave",
            "keyboard_shortcut": "Ctrl+S",   "element_type": "BUTTON"},
        {"name": "New Workbook",  "automation_id": "FileNew",
            "keyboard_shortcut": "Ctrl+N",   "element_type": "BUTTON"},
        {"name": "Bold",          "automation_id": "Bold",
            "keyboard_shortcut": "Ctrl+B",   "element_type": "BUTTON"},
        {"name": "Find/Replace",  "automation_id": "Find",
            "keyboard_shortcut": "Ctrl+F",   "element_type": "INPUT"},
        {"name": "Sum Formula",   "automation_id": "AutoSum",
            "keyboard_shortcut": "Alt+=",    "element_type": "BUTTON"},
        {"name": "New Sheet",     "automation_id": "NewSheet",
            "keyboard_shortcut": "Shift+F11", "element_type": "BUTTON"},
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def scan_window_elements(pattern: str) -> list[dict]:
    """
    Entry point يُستدعى من program_service.
    يرجع list من dicts جاهزة للـ DB
    مع حقل extra: parent_key و unique_key للـ hierarchy.
    """
    # ── 1. كشف نوع التطبيق ────────────────────────────────────────────
    lib_key = _match_shortcut_library(pattern)
    app_type = _detect_app_type(pattern)

    logger.info(f"🔍 Scanning '{pattern}' | type={app_type} | lib={lib_key}")

    raw_elements: list[RawElement] = []

    # ── 2. محاولة UIA أولاً (الأفضل دائماً) ──────────────────────────
    if app_type != "win32_legacy":
        raw_elements = _scan_uia_tree(pattern)

    # ── 3. fallback لـ win32 لو UIA فشل ──────────────────────────────
    if not raw_elements and app_type in ("win32_legacy", "unknown"):
        raw_elements = _scan_win32_flat(pattern)

    # ── 4. دمج Shortcut Library (مهم لـ Electron) ────────────────────
    if lib_key:
        shortcuts = _build_shortcuts(lib_key)
        existing_ids = {
            e.automation_id for e in raw_elements if e.automation_id}
        for s in shortcuts:
            if s.automation_id not in existing_ids:
                raw_elements.append(s)

    if not raw_elements:
        logger.warning(f"⚠️  No elements found for '{pattern}'")
        return []

    logger.info(f"✅ Found {len(raw_elements)} elements total")
    return [_raw_to_dict(e) for e in raw_elements]


# ══════════════════════════════════════════════════════════════════════════════
# APP TYPE DETECTION
# ══════════════════════════════════════════════════════════════════════════════

def _detect_app_type(pattern: str) -> str:
    name = re.sub(r'[.*?()\[\]\\]', '', pattern).lower().strip()
    electron_hints = ["visual studio code", "whatsapp", "slack",
                      "discord", "figma", "notion", "postman", "obsidian"]
    if any(h in name for h in electron_hints):
        return "electron"
    return "unknown"


def _match_shortcut_library(pattern: str) -> Optional[str]:
    # أضف \\ للـ regex عشان تشيل الـ backslashes
    clean = re.sub(r'[.*?()\[\]\\]', '', pattern).lower().strip()
    for key in _SHORTCUT_LIBRARIES:
        if key in clean:
            return key
    return None


# ══════════════════════════════════════════════════════════════════════════════
# UIA TREE SCANNER — DFS RECURSIVE
# ══════════════════════════════════════════════════════════════════════════════

def _scan_uia_tree(pattern: str) -> list[RawElement]:
    """
    DFS scan عبر UIA.
    بيبني شجرة كاملة مع parent_key و tree_path.
    """
    try:
        from pywinauto import Desktop
    except ImportError:
        logger.error("pywinauto مش مثبّت")
        return []

    window = _find_window(pattern, Desktop, "uia")
    if not window:
        logger.warning(f"❌ Window not found (UIA): '{pattern}'")
        return []

    try:
        if window.is_minimized():
            window.restore()
        window.set_focus()
        time.sleep(0.4)
    except Exception:
        pass

    logger.info(f"✅ UIA connected: '{window.window_text()}'")

    elements: list[RawElement] = []
    type_counters: dict[str, int] = {}   # لحساب index كل نوع عند الأب

    def _dfs(elem, parent_key: Optional[str], depth: int, path: str):
        """
        DFS recursive.
        كل element بيتحول لـ RawElement مع parent_key.
        """
        if depth > 20:   # حماية من loops
            return

        try:
            ctrl_type = str(elem.control_type()).lower()
        except Exception:
            return

        # نتخطى الـ containers بس نكمل DFS في أولادهم
        should_skip = ctrl_type in _SKIP_CONTROLS

        elem_key = None

        if not should_skip:
            raw = _build_uia_element(
                elem, ctrl_type, parent_key, depth, path, type_counters)
            if raw:
                elements.append(raw)
                elem_key = raw.unique_key

        # DFS في الأولاد
        try:
            children = elem.children()
        except Exception:
            return

        for child in children:
            new_path = f"{path}/{ctrl_type}" if path else ctrl_type
            # لو الأب skip → الأولاد بيرثوا parent_key بتاع الجد
            _dfs(child, elem_key or parent_key, depth + 1, new_path)

    # ابدأ من أولاد النافذة مباشرة
    try:
        for child in window.children():
            _dfs(child, parent_key=None, depth=0, path="")
    except Exception as e:
        logger.error(f"DFS error: {e}")

    return elements


def _build_uia_element(
    elem,
    ctrl_type: str,
    parent_key: Optional[str],
    depth: int,
    path: str,
    type_counters: dict,
) -> Optional[RawElement]:
    """بيبني RawElement من UIA element."""
    # ── Class filter ──────────────────────────────────────────────────
    try:
        class_name = elem.class_name()
        if class_name in _IGNORED_CLASSES:
            return None
    except Exception:
        class_name = ""

    # ── AutomationId + Name ───────────────────────────────────────────
    try:
        auto_id = elem.automation_id() or ""
    except Exception:
        auto_id = ""

    try:
        text = elem.window_text() or ""
    except Exception:
        text = ""

    # ── Priority ID strategy ──────────────────────────────────────────
    # 1. AutomationId  2. Name  3. Type+Index
    if auto_id and not _is_random_id(auto_id):
        unique_key = auto_id
        stability = 1.0
    elif text and not _is_junk_text(text):
        unique_key = f"{path}/{text}"
        stability = 0.8
    else:
        # Type+Index fallback
        type_idx_key = f"{path}/{ctrl_type}"
        type_counters[type_idx_key] = type_counters.get(type_idx_key, 0) + 1
        unique_key = f"{type_idx_key}[{type_counters[type_idx_key]}]"
        stability = 0.4

    # ── Bounds ────────────────────────────────────────────────────────
    try:
        rect = elem.rectangle()
    except Exception:
        return None

    w, h = rect.width(), rect.height()
    if w <= 0 or h <= 0:
        return None
    if w > _MAX_ELEMENT_W and h > _MAX_ELEMENT_H:
        return None   # تجاهل containers الكبيرة

    # ── Is enabled ───────────────────────────────────────────────────
    try:
        is_enabled = elem.is_enabled()
    except Exception:
        is_enabled = True

    # ── Build RawElement ──────────────────────────────────────────────
    clean_name = _clean_name(text or auto_id or ctrl_type)
    element_type = _map_control_type(ctrl_type)
    is_clickable = ctrl_type.replace(" ", "").lower() in {
        k for k in _CONTROL_MAP if "button" in k or "edit" in k
        or "menu" in k or "tab" in k or "link" in k or "checkbox" in k or "radio" in k
    }

    return RawElement(
        name=clean_name[:255],
        display_text=text[:500],
        element_type=element_type,
        automation_id=auto_id,
        class_name=class_name,
        selector_value=auto_id or text,
        keyboard_shortcut="",
        x=rect.left,
        y=rect.top,
        width=w,
        height=h,
        is_visible=True,
        is_enabled=is_enabled,
        is_clickable=is_clickable,
        raw_properties={"control_type": ctrl_type, "uia": True},
        tree_path=path,
        depth_level=depth,
        parent_key=parent_key,
        unique_key=unique_key,
        stability_score=stability,
    )


# ══════════════════════════════════════════════════════════════════════════════
# WIN32 FLAT SCANNER (Legacy fallback)
# ══════════════════════════════════════════════════════════════════════════════

def _scan_win32_flat(pattern: str) -> list[RawElement]:
    try:
        from pywinauto import Desktop
    except ImportError:
        return []

    window = _find_window(pattern, Desktop, "win32")
    if not window:
        return []

    logger.info(f"✅ win32 connected: '{window.window_text()}'")
    elements: list[RawElement] = []
    seen: set[str] = set()

    try:
        for elem in window.descendants(depth=12):
            try:
                text = elem.window_text()
                class_name = elem.class_name()
                ctrl_type = str(elem.friendly_class_name())
            except Exception:
                continue

            if not text and not class_name:
                continue
            if class_name in _IGNORED_CLASSES:
                continue

            key = text or class_name
            if key in seen:
                continue
            seen.add(key)

            try:
                rect = elem.rectangle()
                w, h = rect.width(), rect.height()
                if w <= 0 or h <= 0 or (w > _MAX_ELEMENT_W and h > _MAX_ELEMENT_H):
                    continue
            except Exception:
                continue

            elements.append(RawElement(
                name=_clean_name(text or class_name)[:255],
                display_text=text[:500],
                element_type=_map_control_type(ctrl_type),
                automation_id="",
                class_name=class_name,
                selector_value=text or class_name,
                keyboard_shortcut="",
                x=rect.left, y=rect.top, width=w, height=h,
                is_visible=True, is_enabled=True, is_clickable=True,
                raw_properties={"control_type": ctrl_type, "win32": True},
                unique_key=f"win32/{key}",
                stability_score=0.6,
            ))
    except Exception as e:
        logger.error(f"win32 scan error: {e}")

    return elements


# ══════════════════════════════════════════════════════════════════════════════
# SHORTCUT LIBRARY BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def _build_shortcuts(lib_key: str) -> list[RawElement]:
    """يحوّل shortcut library لـ RawElement list."""
    result = []
    for i, s in enumerate(_SHORTCUT_LIBRARIES[lib_key]):
        result.append(RawElement(
            name=s["name"],
            display_text=s["name"],
            element_type=s.get("element_type", "BUTTON"),
            automation_id=s["automation_id"],
            class_name="",
            selector_value=s["automation_id"],
            keyboard_shortcut=s.get("keyboard_shortcut", ""),
            x=0, y=0, width=0, height=0,
            is_visible=True, is_enabled=True, is_clickable=True,
            raw_properties={"source": "shortcut_library"},
            tree_path=f"shortcuts/{lib_key}",
            depth_level=1,
            unique_key=s["automation_id"],
            stability_score=1.0,
        ))
    return result


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _find_window(pattern: str, Desktop, backend: str):
    """بيدوّر على النافذة بـ regex أو partial match."""
    # محاولة 1: regex كامل
    try:
        wins = Desktop(backend=backend).windows(
            title_re=re.compile(pattern, re.IGNORECASE)
        )
        if wins:
            return wins[0]
    except Exception:
        pass

    # محاولة 2: partial string match (بعد إزالة special chars)
    try:
        clean = re.sub(r'[.*?()\[\]]', '', pattern).strip()
        matches = [
            w for w in Desktop(backend=backend).windows()
            if w.window_text() and clean.lower() in w.window_text().lower()
        ]
        if matches:
            return matches[0]
    except Exception:
        pass

    return None


def _map_control_type(ctrl_type: str) -> str:
    t = ctrl_type.lower().replace(" ", "")
    for key, val in _CONTROL_MAP.items():
        if key in t:
            return val
    return "OTHER"


def _is_random_id(auto_id: str) -> bool:
    """
    بيكتشف لو الـ automation_id random-generated مش ثابت.
    مثلاً: "ContentView-12" أو UUIDs أو أرقام بس.
    """
    if not auto_id:
        return True
    if re.fullmatch(r'[\da-fA-F\-]{8,}', auto_id):   # UUID-like
        return True
    if re.fullmatch(r'\d+', auto_id):                  # رقم بس
        return True
    if re.search(r'\d{4,}', auto_id):                  # فيه 4+ أرقام متتالية
        return True
    return False


def _is_junk_text(text: str) -> bool:
    """بيكتشف نصوص مش مفيدة للـ identification."""
    if not text or len(text.strip()) == 0:
        return True
    if re.fullmatch(r'[\W\d]+', text):                 # symbols أو أرقام بس
        return True
    if len(text) > 200:                                 # طويل جداً (tooltip?)
        return True
    return False


def _clean_name(raw: str) -> str:
    """بينظف الاسم: يشيل special chars الزيادة ويحتفظ بالمعنى."""
    if not raw:
        return "Element"
    # اشيل whitespace زيادة
    name = " ".join(raw.split())
    # اشيل invisible characters
    name = re.sub(r'[\x00-\x1f\x7f]', '', name)
    return name.strip() or "Element"


def _raw_to_dict(e: RawElement) -> dict:
    """يحوّل RawElement لـ dict جاهز للـ DB layer."""
    return {
        "name": e.name,
        "display_text": e.display_text,
        "element_type": e.element_type,
        "automation_id": e.automation_id,
        "class_name": e.class_name,
        "selector_type": "ui",
        "selector_value": e.selector_value,
        "keyboard_shortcut": e.keyboard_shortcut,
        "x_coordinate": e.x,
        "y_coordinate": e.y,
        "width": e.width,
        "height": e.height,
        "is_visible": e.is_visible,
        "is_enabled": e.is_enabled,
        "is_clickable": e.is_clickable,
        "raw_properties": e.raw_properties,
        "tree_path": e.tree_path,
        "depth_level": e.depth_level,
        "stability_score": e.stability_score,
        # هذين الحقلين يستخدمهم الـ DB layer
        "_parent_key": e.parent_key,
        "_unique_key": e.unique_key,
    }
