# services/macos_scanner.py
from PyObjC import objc
from Cocoa import NSWorkspace
from typing import List, Dict, Optional

class macOSAccessibilityScanner:
    """استخراج العناصر من تطبيقات macOS باستخدام Accessibility API"""
    
    def __init__(self, bundle_id: str):
        self.bundle_id = bundle_id
        self.max_depth = 15
        
    def scan_complete_ui_tree(self) -> List[Dict]:
        """فحص شجرة العناصر على macOS"""
        try:
            app = NSWorkspace.sharedWorkspace().runningApplications()
            target_app = None
            
            for app_instance in app:
                if app_instance.bundleIdentifier() == self.bundle_id:
                    target_app = app_instance
                    break
            
            if not target_app:
                raise Exception(f"التطبيق {self.bundle_id} غير مفتوح")
            
            app_element = target_app.accessibilityObject()
            elements = []
            self._traverse_tree(app_element, "", 0, elements)
            return elements
            
        except Exception as e:
            print(f"خطأ: {e}")
            return []
    
    def _traverse_tree(self, element, parent_path: str, depth: int, 
                       elements: List[Dict], parent_id: Optional[str] = None):
        """فحص تكراري لشجرة Accessibility"""
        if depth > self.max_depth:
            return
        
        try:
            element_data = self._extract_properties(element, parent_path, depth, parent_id)
            if self._is_interactive(element_data):
                elements.append(element_data)
            
            # العناصر الفرعية
            try:
                children_count = element.accessibilityNumberOfChildren()
                for idx in range(children_count):
                    child = element.accessibilityChildAtIndex_(idx)
                    if child:
                        child_path = f"{parent_path}/{element_data.get('tag_name')}[{idx}]"
                        self._traverse_tree(child, child_path, depth + 1, elements,
                                         element_data.get('accessibility_id'))
            except:
                pass
                
        except Exception as e:
            print(f"خطأ: {e}")
    
    def _extract_properties(self, element, parent_path: str, depth: int, 
                            parent_id: Optional[str]) -> Dict:
        """استخراج خصائص العنصر"""
        try:
            role = self._get_attr(element, 'accessibilityRole', '')
            name = self._get_attr(element, 'accessibilityLabel', '')
            value = self._get_attr(element, 'accessibilityValue', '')
            
            frame = self._get_attr(element, 'accessibilityFrame', None)
            x, y, width, height = 0, 0, 0, 0
            if frame:
                x, y, width, height = frame[0], frame[1], frame[2], frame[3]
            
            accessibility_id = f"{role}_{id(element)}"
            control_type = self._map_macos_role(role)
            
            return {
                'accessibility_id': accessibility_id,
                'name': name or f"Element_{role}",
                'display_text': value or '',
                'element_type': control_type,
                'tag_name': role,
                'class_name': role,
                'x_coordinate': int(x),
                'y_coordinate': int(y),
                'width': int(width),
                'height': int(height),
                'tree_path': parent_path,
                'depth_level': depth,
                'parent_id': parent_id,
                'is_visible': True,
                'is_enabled': self._get_attr(element, 'accessibilityEnabled', True),
                'is_focusable': role in ['AXButton', 'AXTextField', 'AXCheckBox'],
                'raw_properties': {'role': role},
            }
        except Exception as e:
            print(f"خطأ: {e}")
            return {}
    
    @staticmethod
    def _map_macos_role(role: str) -> str:
        """تحويل أدوار macOS إلى النموذج الموحد"""
        mapping = {
            'AXButton': 'BUTTON', 'AXTextField': 'INPUT', 'AXCheckBox': 'CHECKBOX',
            'AXRadioButton': 'RADIO', 'AXMenu': 'MENU', 'AXMenuItem': 'MENU',
            'AXList': 'LISTBOX', 'AXComboBox': 'COMBOBOX', 'AXTabGroup': 'TAB',
            'AXWindow': 'WINDOW', 'AXScrollArea': 'PANE', 'AXStaticText': 'TEXT',
            'AXLink': 'LINK', 'AXOutline': 'TREEVIEW', 'AXTable': 'DATAGRID',
        }
        return mapping.get(role, 'OTHER')
    
    @staticmethod
    def _is_interactive(element_data: Dict) -> bool:
        interactive_types = {'BUTTON', 'INPUT', 'CHECKBOX', 'RADIO', 'MENU',
                            'LISTBOX', 'COMBOBOX', 'TAB', 'LINK', 'TREEVIEW'}
        return element_data.get('element_type') in interactive_types
    
    @staticmethod
    def _get_attr(element, attr: str, default):
        try:
            return getattr(element, attr)() if hasattr(element, attr) else default
        except:
            return default
