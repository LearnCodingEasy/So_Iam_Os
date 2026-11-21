# automation source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## automation/admin.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from django.contrib import admin; from .models import Program, ProgramElement, Workflow, WorkflowNode, WorkflowEdge, Action, Task, TaskRun, ScreenState, Delay
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/apps.py
- Type/area: Python module
- Definitions: class AutomationConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/celery.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): import os; from celery import Celery
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/consumers.py
- Type/area: Python module
- Definitions: class WorkflowLogConsumer(AsyncWebsocketConsumer):; async def connect(self):; async def disconnect(self, close_code):; async def send_log(self, event):
- Imports (first four): from channels.generic.websocket import AsyncWebsocketConsumer; import json
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/engine_runtime.py
- Type/area: Python module
- Definitions: def _open_program(program_obj, timeout=20):; def _close_program(path):; def _get_program_status(path):; def _click_element(element_id, program_obj=None):; def _focus_program_window(program_obj=None, title=None):; def _press(key):; def _hotkey(keys_str):; def _typewrite(text, program_obj=None, typing_delay=0.01):; def _run_cmd(cmd):; def _wait(seconds):; def _print(message):; def run_action_instance(action, program_obj=None, task_run=None):
- Imports (first four): from automation.engine.logger import EngineLogger; import subprocess; import time; import pyautogui
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/generate_edit_json.py
- Type/area: Python module
- Definitions: def convert_run_to_edit_json(run_json_path, video_source):
- Imports (first four): import json; import os
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/permission_policy.py
- Type/area: Python module
- Definitions: def effective_policy(workflow):; def required_permissions(workflow):; def validate_permissions(workflow, approved=False):
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/routing.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from django.urls import re_path; from .consumers import WorkflowLogConsumer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/runner.py
- Type/area: Python module
- Definitions: def start_task(task_id):
- Imports (first four): import time; from .models import Task, TaskRun, Action; from .engine_runtime import run_action_instance; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/tasks.py
- Type/area: Python module
- Definitions: def execute_workflow_task(self, workflow_id: str, user_id: str, task_run_id: str):
- Imports (first four): from celery import shared_task; from django.utils import timezone; from automation.models import Workflow, TaskRun; from automation.workflow_runner import execute_workflow
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/window_manager.py
- Type/area: Python module
- Definitions: def focus_window(program):; def maximize_window(program):
- Imports (first four): import pygetwindow as gw
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/workflow_runner.py
- Type/area: Python module
- Definitions: def execute_workflow(workflow_id, user, task_run=None):; def generate_timings_json(task_run, log_data):
- Imports (first four): import json; import os; import time; import uuid
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/ai/agent.py
- Type/area: Python module
- Definitions: class Action(BaseModel):; class AgentResponse(BaseModel):; def parse_prompt(prompt: str, user=None):
- Imports (first four): import json; from typing import List; from pydantic import BaseModel; from ai.services import AIService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from django.urls import path, include; from rest_framework.routers import DefaultRouter; from automation.api.views import ProgramViewSet, ProgramElementViewSet, WorkflowViewSet, WorkflowNodeViewSet, WorkflowEdgeViewSet, ActionViewSet, TaskViewSet, TaskRunViewSet, ScreenStateViewSet, DelayViewSet, get_open_windows
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/serializers/action_serializers.py
- Type/area: Python API source
- Definitions: class ActionSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from automation.models import Action
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/serializers/delay_serializers.py
- Type/area: Python API source
- Definitions: class DelaySerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from automation.models import Delay
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/serializers/program_element_serializers.py
- Type/area: Python API source
- Definitions: class ProgramElementSerializer(serializers.ModelSerializer):; def get_get_image(self, obj):; class Meta:; def validate_program(self, value):
- Imports (first four): from rest_framework import serializers; from automation.models import ProgramElement
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/serializers/program_serializers.py
- Type/area: Python API source
- Definitions: class ProgramSerializer(serializers.ModelSerializer):; def get_get_image(self, obj):; class Meta:; def get_image_url(self, obj):
- Imports (first four): from rest_framework import serializers; from automation.models import Program
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/serializers/screen_state_serializers.py
- Type/area: Python API source
- Definitions: class ScreenStateSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from automation.models import ScreenState
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/serializers/task_run_serializers.py
- Type/area: Python API source
- Definitions: class TaskRunSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from automation.models import TaskRun
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/serializers/task_serializers.py
- Type/area: Python API source
- Definitions: class TaskSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from automation.models import Task
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/serializers/workflow_edge_serializers.py
- Type/area: Python API source
- Definitions: class WorkflowEdgeSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from automation.models import WorkflowEdge
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/serializers/workflow_node_serializers.py
- Type/area: Python API source
- Definitions: class WorkflowNodeSerializer(serializers.ModelSerializer):; class Meta:; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from automation.models import WorkflowNode; from automation.api.serializers.action_serializers import ActionSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/serializers/workflow_serializers.py
- Type/area: Python API source
- Definitions: class WorkflowSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from automation.models import Workflow
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .program_serializers import ProgramSerializer; from .program_element_serializers import ProgramElementSerializer; from .workflow_serializers import WorkflowSerializer; from .action_serializers import ActionSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/views/action_views.py
- Type/area: Python API source
- Definitions: class ActionViewSet(viewsets.ModelViewSet):; def get_queryset(self): return Action.objects.filter(created_by=self.request.user); def perform_create(self, serializer):; def update_type(self, request, pk=None):; def execute(self, request, pk=None):; def templates_by_program(self, request):
- Imports (first four): from rest_framework import viewsets, permissions; from rest_framework.decorators import action; from rest_framework.response import Response; from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/views/common.py
- Type/area: Python API source
- Definitions: def get_open_windows(request):
- Imports (first four): from automation.services.window_service import list_open_windows; from rest_framework.decorators import api_view; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/views/delay_views.py
- Type/area: Python API source
- Definitions: class DelayViewSet(viewsets.ReadOnlyModelViewSet):; def get_queryset(self): return Delay.objects.filter(created_by=self.request.user); def perform_create(self, serializer):
- Imports (first four): from rest_framework import viewsets, permissions; from rest_framework.parsers import MultiPartParser, FormParser, JSONParser; from automation.models import Delay; from automation.api.serializers import DelaySerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/views/program_element_views.py
- Type/area: Python API source
- Definitions: class ProgramElementViewSet(viewsets.ModelViewSet):; def get_queryset(self): return ProgramElement.objects.filter(created_by=self.request.user); def perform_create(self, serializer):
- Imports (first four): from rest_framework import viewsets, permissions; from rest_framework.parsers import MultiPartParser, FormParser, JSONParser; from automation.models import ProgramElement; from automation.api.serializers import ProgramElementSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/views/program_views.py
- Type/area: Python API source
- Definitions: class ProgramViewSet(viewsets.ModelViewSet):; def get_queryset(self): return Program.objects.filter(created_by=self.request.user); def perform_create(self, serializer):; def open(self, request, pk=None):; def close(self, request, pk=None):; def status(self, request, pk=None):; def focus(self, request, pk=None):; def maximize(self, request, pk=None):; def scan_elements(self, request, pk=None):
- Imports (first four): from rest_framework import viewsets, permissions; from rest_framework.decorators import action; from rest_framework.response import Response; from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/views/screen_state_views.py
- Type/area: Python API source
- Definitions: class ScreenStateViewSet(viewsets.ModelViewSet):; def get_queryset(self): return ScreenState.objects.filter(created_by=self.request.user); def perform_create(self, serializer):; def bulk_create(self, request):; def by_task_run(self, request):
- Imports (first four): from rest_framework import viewsets, status, permissions; from rest_framework.decorators import action; from rest_framework.response import Response; from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/views/task_run_views.py
- Type/area: Python API source
- Definitions: class TaskRunViewSet(viewsets.ModelViewSet):; def get_queryset(self): return TaskRun.objects.filter(created_by=self.request.user); def perform_create(self, serializer):
- Imports (first four): from rest_framework import viewsets, permissions; from rest_framework.parsers import MultiPartParser, FormParser, JSONParser; from automation.models import TaskRun; from automation.api.serializers import TaskRunSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/views/task_views.py
- Type/area: Python API source
- Definitions: class TaskViewSet(viewsets.ModelViewSet):; def get_queryset(self): return Task.objects.filter(created_by=self.request.user); def perform_create(self, serializer):
- Imports (first four): from rest_framework import viewsets, permissions; from rest_framework.parsers import MultiPartParser, FormParser, JSONParser; from automation.models import Task; from automation.api.serializers import TaskSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/views/workflow_edge_views.py
- Type/area: Python API source
- Definitions: class WorkflowEdgeViewSet(viewsets.ModelViewSet):; def get_queryset(self): return WorkflowEdge.objects.filter(created_by=self.request.user); def perform_create(self, serializer):
- Imports (first four): from rest_framework import viewsets, permissions; from rest_framework.parsers import MultiPartParser, FormParser, JSONParser; from automation.models import WorkflowEdge; from automation.api.serializers import WorkflowEdgeSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/views/workflow_node_views.py
- Type/area: Python API source
- Definitions: class WorkflowNodeViewSet(viewsets.ModelViewSet):; def get_queryset(self): return WorkflowNode.objects.filter(created_by=self.request.user); def perform_create(self, serializer):; def run(self, request, pk=None):; def full_events(self, request, pk=None):
- Imports (first four): from rest_framework import viewsets, permissions; from rest_framework.decorators import action; from rest_framework.response import Response; from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/views/workflow_views.py
- Type/area: Python API source
- Definitions: class WorkflowViewSet(viewsets.ModelViewSet):; def get_queryset(self): return Workflow.objects.filter(created_by=self.request.user); def perform_create(self, serializer):; def run(self, request, pk=None):; def full_events(self, request, pk=None):; def save_all(self, request, pk=None):
- Imports (first four): from rest_framework import viewsets, permissions; from rest_framework.decorators import action; from rest_framework.response import Response; from automation.models import Workflow, WorkflowNode, WorkflowEdge, TaskRun
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .workflow_views import console, WorkflowViewSet; from .common import get_open_windows; from .program_views import ProgramViewSet; from .program_element_views import ProgramElementViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/engine/executor.py
- Type/area: Python module
- Definitions: class ActionExecutor:; def execute(self, action):
- Imports (first four): from .registry import get_action
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/engine/logger.py
- Type/area: Python module
- Definitions: class EngineLogger:; def _write(self, payload: dict):; def log(; def warning(self, message, **kwargs):; def error(self, message, **kwargs):; def success(self):; def fail(self, error):; def build_ai_summary(self):; def __init__(self, task_run: TaskRun | None = None):; def _broadcast(self, level, message, data=None):; def info(self, message, data=None, **kwargs):; def error(self, message, data=None, **kwargs):
- Imports (first four): import json; import time; import uuid; from automation.models import TaskRun
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/engine/registry.py
- Type/area: Python module
- Definitions: def register_action(name):; def decorator(cls):; def get_action(name):
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/engine/router.py
- Type/area: Python module
- Definitions: def get_next_node(current_node, result):
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/engine/runner.py
- Type/area: Python module
- Definitions: class WorkflowRunner:; def __init__(self, task_run: TaskRun):; def get_start_node(self):; def run(self):
- Imports (first four): import time; from automation.models import TaskRun; from .executor import ActionExecutor; from .router import get_next_node
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/engine/scanner_engine.py
- Type/area: Python module
- Definitions: class RawElement:; def scan_window_elements(pattern: str) -> list[dict]:; def _detect_app_type(pattern: str) -> str:; def _match_shortcut_library(pattern: str) -> Optional[str]:; def _scan_uia_tree(pattern: str) -> list[RawElement]:; def _dfs(elem, parent_key: Optional[str], depth: int, path: str):; def _build_uia_element(; def _scan_win32_flat(pattern: str) -> list[RawElement]:; def _build_shortcuts(lib_key: str) -> list[RawElement]:; def _find_window(pattern: str, Desktop, backend: str):; def _map_control_type(ctrl_type: str) -> str:; def _is_random_id(auto_id: str) -> bool:; def _is_junk_text(text: str) -> bool:; def _clean_name(raw: str) -> str:; def _raw_to_dict(e: RawElement) -> dict:
- Imports (first four): from __future__ import annotations; import re; import time; import logging
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/engine/handlers/click.py
- Type/area: Python module
- Definitions: class ClickAction:; def execute(self, payload):
- Imports (first four): from ..registry import register_action
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/engine/handlers/wait.py
- Type/area: Python module
- Definitions: class WaitAction:; def execute(self, payload):
- Imports (first four): import time; from ..registry import register_action
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/engine/handlers/write.py
- Type/area: Python module
- Definitions: class WriteAction:; def execute(self, payload):
- Imports (first four): from ..registry import register_action
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; import uuid; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/models/action.py
- Type/area: Python model source
- Definitions: class Action(models.Model):; def save(self, *args, **kwargs):; def __str__(self):
- Imports (first four): from django.db import models; import uuid; from django.utils.text import slugify; from users_accounts.models import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/models/delay.py
- Type/area: Python model source
- Definitions: class Delay(models.Model):; def save(self, *args, **kwargs):; def __str__(self):
- Imports (first four): from django.db import models; import uuid; from django.utils.text import slugify; from users_accounts.models import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/models/program.py
- Type/area: Python model source
- Definitions: class Program(models.Model):; def window_title(self):; def get_image(self):; def save(self, *args, **kwargs):; def __str__(self):
- Imports (first four): from django.db import models; from django.conf import settings; import uuid; from django.utils.text import slugify
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/models/program_element.py
- Type/area: Python model source
- Definitions: class ProgramElement(models.Model):; class Meta:; def get_image(self):; def save(self, *args, **kwargs):; def __str__(self):
- Imports (first four): from django.db import models; from django.conf import settings; import uuid; from django.utils.text import slugify
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/models/screen_state.py
- Type/area: Python model source
- Definitions: class ScreenState(models.Model):; def save(self, *args, **kwargs):; def __str__(self):
- Imports (first four): from django.db import models; import uuid; from django.utils.text import slugify; from users_accounts.models import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/models/task.py
- Type/area: Python model source
- Definitions: class Task(models.Model):; def save(self, *args, **kwargs):; def __str__(self):
- Imports (first four): from django.db import models; import uuid; from django.utils.text import slugify; from users_accounts.models import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/models/task_run.py
- Type/area: Python model source
- Definitions: class TaskRun(models.Model):; def save(self, *args, **kwargs):; def __str__(self):
- Imports (first four): from django.db import models; import uuid; from django.utils.text import slugify; from users_accounts.models import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/models/workflow.py
- Type/area: Python model source
- Definitions: class Workflow(models.Model):; def save(self, *args, **kwargs):; def __str__(self):
- Imports (first four): from django.db import models; import uuid; from django.utils.text import slugify; from users_accounts.models import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/models/workflow_edge.py
- Type/area: Python model source
- Definitions: class WorkflowEdge(models.Model):; def save(self, *args, **kwargs):; def __str__(self):
- Imports (first four): from django.db import models; import uuid; from django.utils.text import slugify; from users_accounts.models import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/models/workflow_node.py
- Type/area: Python model source
- Definitions: class WorkflowNode(models.Model):; def save(self, *args, **kwargs):; def __str__(self):
- Imports (first four): from django.db import models; import uuid; from django.utils.text import slugify; from users_accounts.models import User
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .program import Program; from .program_element import ProgramElement; from .workflow import Workflow; from .workflow_node import WorkflowNode
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/services/automation.py
- Type/area: Python service source
- Definitions: class ElementFinder:; def find_by_name(program_id: int, name: str):; def find_by_control_type(program_id: int, control_type: str):; def find_by_xpath(program_id: int, xpath: str):; def find_by_position(program_id: int, x: int, y: int, tolerance: int = 5):; class AutomationEngine:; def click_element(element_id: int) -> bool:; def type_text(element_id: int, text: str) -> bool:; def use_keyboard_shortcut(element_id: int) -> bool:
- Imports (first four): from models import ProgramElement; from django.db.models import Q; import pyautogui; import time
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/services/macos_scanner.py
- Type/area: Python service source
- Definitions: class macOSAccessibilityScanner:; def __init__(self, bundle_id: str):; def scan_complete_ui_tree(self) -> List[Dict]:; def _traverse_tree(self, element, parent_path: str, depth: int,; def _extract_properties(self, element, parent_path: str, depth: int,; def _map_macos_role(role: str) -> str:; def _is_interactive(element_data: Dict) -> bool:; def _get_attr(element, attr: str, default):
- Imports (first four): from PyObjC import objc; from Cocoa import NSWorkspace; from typing import List, Dict, Optional
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/services/program_service.py
- Type/area: Python service source
- Definitions: def scan_and_store_elements(program, user, custom_pattern: str = None) -> int:; def _filter_duplicates(; def _hierarchical_bulk_insert(; def _unique_slug(name: str, existing: set[str]) -> str:
- Imports (first four): from __future__ import annotations; import logging; from collections import defaultdict; from django.db import transaction
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/services/scanner_service.py
- Type/area: Python service source
- Definitions: def scan_ui_elements(window_title_pattern):
- Imports (first four): from pywinauto import Application, Desktop; import logging
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/services/screenshot.py
- Type/area: Python service source
- Definitions: def capture_screen(task_run, user, program_obj=None, action_id=None, status="ok"):
- Imports (first four): import pyautogui; import tempfile; from django.core.files import File; from automation.models import ScreenState
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/services/window_service.py
- Type/area: Python service source
- Definitions: def list_open_windows():; def _extract_app_name(title: str) -> str:; class WindowsUIAutomationScanner:; def __init__(self, process_id: int, window_handle: int):; def scan_complete_ui_tree(self) -> List[Dict]:; def _traverse_tree(self, element, parent_path: str, depth: int,; def _extract_properties(self, element, parent_path: str, depth: int,; def _map_control_type(windows_type: str) -> str:; def _is_interactive(element_data: Dict) -> bool:; def _extract_shortcut(name: str) -> Optional[str]:; def _safe_get(d: dict, key: str, default):
- Imports (first four): from typing import List, Dict, Optional; from pywinauto import Application; import win32com.client; import re
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/tests/test_automation.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): from django.test import TestCase
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## automation/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

