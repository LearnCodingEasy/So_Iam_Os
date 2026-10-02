# backend_django\automation\services\window_service.py


from typing import List, Dict, Optional
from pywinauto import Application
import win32com.client
import re


def list_open_windows():
    from pywinauto import Desktop
    windows = Desktop(backend="uia").windows()
    result = []

    for w in windows:
        title = w.window_text()
        if not title or not title.strip():
            continue

        # ✅ استخرج اسم التطبيق الحقيقي
        app_name = _extract_app_name(title)

        result.append({
            "title": title,
            "suggested_pattern": f".*{re.escape(app_name)}.*",
            "app_name": app_name,  # ← للعرض في الـ UI
        })

    return result


def _extract_app_name(title: str) -> str:

    # لو فيه " - " → اسم التطبيق بعد آخر " - "
    if " - " in title:
        last_part = title.split(" - ")[-1].strip()
        # تجاهل لو الجزء الأخير رقم أو قصير جداً
        if len(last_part) > 2 and not last_part[0].isdigit():
            return last_part

    # لو مفيش " - " → استخدم أول كلمة (زي OBS، Calculator)
    first_word = title.split()[0] if title.split() else title
    return first_word


class WindowsUIAutomationScanner:
    """استخراج العناصر من تطبيقات Windows باستخدام UI Automation"""

    def __init__(self, process_id: int, window_handle: int):
        self.process_id = process_id
        self.window_handle = window_handle
        self.max_depth = 15

    def scan_complete_ui_tree(self) -> List[Dict]:
        """فحص كامل شجرة واجهة المستخدم"""
        try:
            app = Application(backend='uia').connect(
                process=self.process_id,
                timeout=10
            )
            root_window = app.window(handle=self.window_handle)

            elements = []
            self._traverse_tree(
                element=root_window,
                parent_path="",
                depth=0,
                elements=elements
            )
            return elements

        except Exception as e:
            print(f"خطأ في الفحص: {e}")
            return []

    def _traverse_tree(self, element, parent_path: str, depth: int,
                       elements: List[Dict], parent_id: Optional[str] = None):
        """فحص تكراري (DFS) لشجرة العناصر"""
        if depth > self.max_depth:
            return

        try:
            element_data = self._extract_properties(
                element, parent_path, depth, parent_id)

            if self._is_interactive(element_data):
                elements.append(element_data)

            # الانتقال للعناصر الفرعية
            try:
                for idx, child in enumerate(element.children()):
                    child_path = f"{parent_path}/{element_data.get('tag_name', 'Element')}[{idx}]"
                    self._traverse_tree(
                        child, child_path, depth + 1, elements,
                        element_data.get('automation_id')
                    )
            except:
                pass

        except Exception as e:
            print(f"خطأ: {e}")

    def _extract_properties(self, element, parent_path: str, depth: int,
                            parent_id: Optional[str]) -> Dict:
        """استخراج جميع خصائص العنصر"""
        try:
            props = element.element_info

            # الموقع والحجم
            rect = element.rectangle()
            x, y = rect.left, rect.top
            width, height = rect.right - rect.left, rect.bottom - rect.top

            automation_id = self._safe_get(props, 'automation_id', '')
            class_name = self._safe_get(props, 'class_name', '')
            control_type = self._map_control_type(
                props.get('control_type', 'Other'))
            name = self._safe_get(props, 'name', f"Element_{class_name}")

            # استخراج اختصار لوحة المفاتيح إن وجد
            keyboard_shortcut = self._extract_shortcut(name)

            return {
                'automation_id': automation_id,
                'name': name[:255],
                'display_text': self._safe_get(props, 'value', '')[:500],
                'element_type': control_type,
                'class_name': class_name[:500],
                'tag_name': props.get('control_type', 'Element'),
                'x_coordinate': x,
                'y_coordinate': y,
                'width': width,
                'height': height,
                'tree_path': parent_path,
                'depth_level': depth,
                'parent_id': parent_id,
                'is_visible': self._safe_get(props, 'visible', True),
                'is_enabled': self._safe_get(props, 'enabled', True),
                'is_focusable': self._safe_get(props, 'focusable', False),
                'keyboard_shortcut': keyboard_shortcut,
                'help_text': self._safe_get(props, 'help_text', ''),
                'raw_properties': dict(props),
            }
        except Exception as e:
            print(f"خطأ في الاستخراج: {e}")
            return {}

    @staticmethod
    def _map_control_type(windows_type: str) -> str:
        """تحويل أنواع Windows إلى النموذج الموحد"""
        mapping = {
            'Button': 'BUTTON', 'Edit': 'INPUT', 'CheckBox': 'CHECKBOX',
            'RadioButton': 'RADIO', 'Menu': 'MENU', 'MenuItem': 'MENU',
            'ListBox': 'LISTBOX', 'ComboBox': 'COMBOBOX', 'TabControl': 'TAB',
            'Window': 'WINDOW', 'Pane': 'PANE', 'Text': 'TEXT',
            'Hyperlink': 'LINK', 'Tree': 'TREEVIEW', 'DataGrid': 'DATAGRID',
        }
        return mapping.get(windows_type, 'OTHER')

    @staticmethod
    def _is_interactive(element_data: Dict) -> bool:
        """تحديد العناصر التفاعلية فقط"""
        if not element_data or not element_data.get('is_visible'):
            return False
        if element_data.get('width', 0) == 0 or element_data.get('height', 0) == 0:
            return False
        interactive_types = {'BUTTON', 'INPUT', 'CHECKBOX', 'RADIO', 'MENU',
                             'LISTBOX', 'COMBOBOX', 'TAB', 'LINK', 'TREEVIEW'}
        return element_data.get('element_type') in interactive_types

    @staticmethod
    def _extract_shortcut(name: str) -> Optional[str]:
        """استخراج اختصار من النص: 'Save (Ctrl+S)' → 'Ctrl+S'"""
        match = re.search(r'\(([Ctrl|Shift|Alt|F\d]+\+[A-Za-z0-9]+)\)', name)
        return match.group(1) if match else None

    @staticmethod
    def _safe_get(d: dict, key: str, default):
        try:
            return d.get(key, default)
        except:
            return default
