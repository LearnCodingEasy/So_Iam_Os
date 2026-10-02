# services/automation.py
from models import ProgramElement
from django.db.models import Q
import pyautogui
import time

class ElementFinder:
    """البحث المتقدم عن العناصر"""
    
    @staticmethod
    def find_by_name(program_id: int, name: str):
        return ProgramElement.objects.filter(
            program_id=program_id,
            name__icontains=name,
            is_visible=True,
            is_enabled=True
        )
    
    @staticmethod
    def find_by_control_type(program_id: int, control_type: str):
        return ProgramElement.objects.filter(
            program_id=program_id,
            element_type=control_type,
            is_enabled=True
        )
    
    @staticmethod
    def find_by_xpath(program_id: int, xpath: str):
        return ProgramElement.objects.get(program_id=program_id, xpath=xpath)
    
    @staticmethod
    def find_by_position(program_id: int, x: int, y: int, tolerance: int = 5):
        """البحث عن عنصر بناءً على موقعه"""
        return ProgramElement.objects.filter(
            program_id=program_id,
            x_coordinate__range=(x - tolerance, x + tolerance),
            y_coordinate__range=(y - tolerance, y + tolerance),
        ).order_by('-width', '-height').first()


class AutomationEngine:
    """تنفيذ إجراءات الأتمتة"""
    
    @staticmethod
    def click_element(element_id: int) -> bool:
        """النقر على عنصر"""
        try:
            elem = ProgramElement.objects.get(id=element_id)
            center_x = elem.x_coordinate + (elem.width // 2)
            center_y = elem.y_coordinate + (elem.height // 2)
            pyautogui.moveTo(center_x, center_y, duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            return True
        except:
            return False
    
    @staticmethod
    def type_text(element_id: int, text: str) -> bool:
        """كتابة نص"""
        try:
            AutomationEngine.click_element(element_id)
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(text)
            return True
        except:
            return False
    
    @staticmethod
    def use_keyboard_shortcut(element_id: int) -> bool:
        """استخدام اختصار لوحة المفاتيح"""
        try:
            elem = ProgramElement.objects.get(id=element_id)
            if not elem.keyboard_shortcut:
                return False
            keys = elem.keyboard_shortcut.lower().split('+')
            pyautogui.hotkey(*keys)
            return True
        except:
            return False
