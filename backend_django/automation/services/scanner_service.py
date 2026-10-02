from pywinauto import Application, Desktop
import logging

# إعداد الـ logging لمتابعة الأخطاء في التيرمينال
logger = logging.getLogger(__name__)


def scan_ui_elements(window_title_pattern):
    try:
        # 1. البحث عن كل النوافذ المطابقة للنمط باستخدام Desktop
        # نستخدم backend="uia" لأنه الأفضل للبرامج الحديثة و Chrome
        des = Desktop(backend="uia")
        all_windows = des.windows(
            title_re=window_title_pattern, visible_only=True)

        if not all_windows:
            return {"error": f"Window not found: {window_title_pattern}", "stage": "connect"}

        # 2. حل مشكلة التكرار: اختر أول نافذة مطابقة فقط (الأكثر أهمية)
        target_window = all_windows[0]

        print(f"✅ Connected to: {target_window.window_text()}")

        # 3. إحضار النافذة للمقدمة (ضروري لبعض العناصر لكي تظهر)
        try:
            target_window.set_focus()
        except Exception as e:
            print(f"⚠️ Could not set focus: {e}")

        elements = []

        # 4. جلب العناصر (Descendants)
        # ملاحظة: في المتصفحات مثل Chrome، قد تحتاج لثانية انتظار ليحمل الـ Accessibility tree
        all_descendants = target_window.descendants()

        for elem in all_descendants:
            try:
                # استخراج المعرفات
                auto_id = elem.automation_id()
                # نستخدم الـ ControlType كبديل لو الـ Name فارغ
                control_type = elem.element_info.control_type

                # ✅ تحسين الـ Selector: نستخدم الـ AutomationId أو الـ Name
                selector_value = auto_id if auto_id else elem.window_text()

                if not selector_value:
                    continue

                name = elem.window_text() or f"{control_type} Element"

                # جلب الإحداثيات بأمان
                rect = elem.rectangle()

                elements.append({
                    "name": name[:100],  # تقليم الاسم لقاعدة البيانات
                    "element_type": elem.friendly_class_name(),
                    "selector_value": str(selector_value),
                    "x": rect.left,
                    "y": rect.top,
                    "width": rect.width(),
                    "height": rect.height(),
                })
            except Exception:
                continue

        # إذا لم يجد عناصر، ربما بسبب صلاحيات الويندوز
        if not elements:
            return {"error": "No accessible elements found. Try running as Admin.", "stage": "scan"}

        return elements

    except Exception as e:
        logger.error(f"Scan failed: {str(e)}")
        return {
            "error": "Scan process failed",
            "details": str(e),
            "stage": "connect"
        }
