# automation services and workflows

## Service/task/signal source


### automation/tasks.py
L7: def execute_workflow_task(self, workflow_id: str, user_id: str, task_run_id: str):

### automation/services/automation.py
L7: class ElementFinder:
L11: def find_by_name(program_id: int, name: str):
L20: def find_by_control_type(program_id: int, control_type: str):
L28: def find_by_xpath(program_id: int, xpath: str):
L32: def find_by_position(program_id: int, x: int, y: int, tolerance: int = 5):
L41: class AutomationEngine:
L45: def click_element(element_id: int) -> bool:
L59: def type_text(element_id: int, text: str) -> bool:
L71: def use_keyboard_shortcut(element_id: int) -> bool:

### automation/services/macos_scanner.py
L6: class macOSAccessibilityScanner:
L9: def __init__(self, bundle_id: str):
L13: def scan_complete_ui_tree(self) -> List[Dict]:
L36: def _traverse_tree(self, element, parent_path: str, depth: int,
L62: def _extract_properties(self, element, parent_path: str, depth: int,
L102: def _map_macos_role(role: str) -> str:
L114: def _is_interactive(element_data: Dict) -> bool:
L120: def _get_attr(element, attr: str, default):

### automation/services/program_service.py
L19: def scan_and_store_elements(program, user, custom_pattern: str = None) -> int:
L65: def _filter_duplicates(
L96: def _hierarchical_bulk_insert(
L196: def _unique_slug(name: str, existing: set[str]) -> str:

### automation/services/scanner_service.py
L8: def scan_ui_elements(window_title_pattern):

### automation/services/screenshot.py
L8: def capture_screen(task_run, user, program_obj=None, action_id=None, status="ok"):

### automation/services/window_service.py
L10: def list_open_windows():
L32: def _extract_app_name(title: str) -> str:
L46: class WindowsUIAutomationScanner:
L49: def __init__(self, process_id: int, window_handle: int):
L54: def scan_complete_ui_tree(self) -> List[Dict]:
L76: def _traverse_tree(self, element, parent_path: str, depth: int,
L103: def _extract_properties(self, element, parent_path: str, depth: int,
L149: def _map_control_type(windows_type: str) -> str:
L161: def _is_interactive(element_data: Dict) -> bool:
L172: def _extract_shortcut(name: str) -> Optional[str]:
L178: def _safe_get(d: dict, key: str, default):


The index does not prove callers, scheduling, successful external calls, or runtime completion. See [background jobs and integrations](../../08-background-jobs-and-integrations.md).
