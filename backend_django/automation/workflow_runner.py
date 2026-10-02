# backend_django\automation\workflow_runner.py

import json
import os
import time
import uuid
import pyautogui
from automation.engine.logger import EngineLogger
from django.conf import settings

from .engine_runtime import _get_program_status
from .models import Workflow, WorkflowNode, TaskRun
from .engine_runtime import run_action_instance

# ---------------------------------------
# تنفيذ الوورك فلو كامل
# ---------------------------------------


def execute_workflow(workflow_id, user):

    workflow = Workflow.objects.get(id=workflow_id)

    task_run = TaskRun.objects.create(
        workflow=workflow,
        created_by=user,
        status="running",
        logs=""
    )

    log_data = {
        "task_run_id": str(task_run.id),
        "workflow": {
            "id": str(workflow.id),
            "name": workflow.name
        },
        "started_at": time.time(),
        "status": "running",
        "nodes": []
    }

    nodes = WorkflowNode.objects.filter(
        workflow_id=workflow_id
    ).order_by("created_at")

    for node in nodes:

        node_log = {
            "node_id": str(node.id),
            "label": node.label,
            "node_type": node.node_type,
            "program": None,
            "started_at": time.time(),
            "status": "running",
            "actions": []
        }

        # لو فيه برنامج مرتبط
        if node.program:
            node_log["program"] = {
                "id": str(node.program.id),
                "name": node.program.name,
                "executable_path": node.program.executable_path
            }

        actions = node.actions.all().order_by("created_at")

        for action in actions:
            action_start = time.time()
            selected_element = None
            if hasattr(action, 'program_element') and action.program_element:
                selected_element = {
                    "id": str(action.program_element.id),
                    "name": action.program_element.name,
                    "class_name": action.program_element.class_name,
                    "role": action.program_element.role,
                    "location": action.payload.get("location") if action.payload else None
                }
            result = run_action_instance(action, node.program, task_run)

            action_log = {
                "action_id": str(action.id),
                "type": action.action_type,
                "payload": action.payload,
                "program_element": selected_element,  # 🔥 تسجيل بيانات العنصر هنا
                "started_at": action_start,
                "finished_at": time.time(),
                "status": result.get("status"),
                "error": result.get("error")
            }

            node_log["actions"].append(action_log)

            if result.get("status") != "ok":
                node_log["status"] = "failed"
                break

        node_log["finished_at"] = time.time()
        if node_log["status"] == "running":
            node_log["status"] = "success"

        if node_log["status"] == "failed":
            log_data["status"] = "failed"
            break

        log_data["nodes"].append(node_log)

    log_data["finished_at"] = time.time()
    if log_data["status"] != "failed":
        log_data["status"] = "success"

    # حفظ الملف
    log_path = os.path.join(
        settings.MEDIA_ROOT,
        "runs",
        f"{task_run.id}.json"
    )
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=4)

    # task_run.status = "success"
    # task_run.save()

    # return {"status": "ok", "task_run_id": task_run.id}
    task_run.status = log_data["status"]
    task_run.save()

    # 🎬 Generate Timings File
    timings_path = generate_timings_json(task_run, log_data)

    return {
        "status": "ok",
        "task_run_id": task_run.id,
        "timings_file": timings_path
    }


def generate_timings_json(task_run, log_data):
    """
    🎬 Generate Timings JSON for Editing
    Compatible with:
    - MoviePy
    - Adobe Premiere (Markers / Timeline)
    """

    workflow_name = log_data["workflow"]["name"]
    base_time = log_data["started_at"]

    timings = {
        "meta": {
            "workflow_name": workflow_name,
            "task_run_id": str(task_run.id),
            "generated_at": time.time(),
            "fps": 30,
            "resolution": "1920x1080"
        },
        "timeline": []
    }

    for node in log_data["nodes"]:

        node_start = node["started_at"] - base_time
        node_end = node["finished_at"] - base_time

        timings["timeline"].append({
            "type": "node",
            "id": node["node_id"],
            "label": node["label"],
            "start": round(node_start, 3),
            "end": round(node_end, 3),
            "duration": round(node_end - node_start, 3),
            "status": node["status"]
        })

        for action in node["actions"]:
            action_start = action["started_at"] - base_time
            action_end = action["finished_at"] - base_time

            timings["timeline"].append({
                "type": "action",
                "node_id": node["node_id"],
                "action_id": action["action_id"],
                "action_type": action["type"],
                "program_element": action.get("program_element"),
                "start": round(action_start, 3),
                "end": round(action_end, 3),
                "duration": round(action_end - action_start, 3),
                "status": action["status"],
                "error": action.get("error")
            })

    # حفظ الملف
    file_name = f"Timings_{workflow_name}.json"
    file_path = os.path.join(
        settings.MEDIA_ROOT,
        "runs",
        file_name
    )

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(timings, f, indent=4)

    return file_path
