# automation/engine/logger.py

import json
import time
import uuid

from automation.models import TaskRun
from django.utils import timezone

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class EngineLogger:

    # -----------------------------------------
    # Core Writer
    # -----------------------------------------
    def _write(self, payload: dict):
        """
        يحول الحدث إلى JSON ويضيفه في logs
        """
        self.task_run.logs += json.dumps(payload, ensure_ascii=False) + "\n"
        self.task_run.save(update_fields=["logs"])

    # -----------------------------------------
    # Public Log Method
    # -----------------------------------------
    def log(
        self,
        message: str,
        level: str = "INFO",
        data: dict | None = None,
        screenshot: str | None = None,
        started_at: float | None = None,
    ):
        self.step_counter += 1

        duration = None
        if started_at:
            duration = round(time.time() - started_at, 3)

        payload = {
            "id": str(uuid.uuid4()),
            "time": str(timezone.now()),
            "level": level,
            "step": self.step_counter,
            "message": message,
            "duration": duration,
            "data": data or {},
            "screenshot": screenshot,
        }

        self._write(payload)

    # -----------------------------------------
    # Helpers
    # -----------------------------------------

    def warning(self, message, **kwargs):
        self.log(message, level="WARNING", **kwargs)

    def error(self, message, **kwargs):
        self.log(message, level="ERROR", **kwargs)

    # -----------------------------------------
    # Finish States
    # -----------------------------------------
    def success(self):
        total_time = round(time.time() - self.run_started_at, 3)

        self.task_run.status = "success"
        self.task_run.finished_at = timezone.now()
        self.task_run.execution_time = total_time
        self.task_run.save()

    def fail(self, error):
        self.error(str(error))

        total_time = round(time.time() - self.run_started_at, 3)

        self.task_run.status = "failed"
        self.task_run.finished_at = timezone.now()
        self.task_run.execution_time = total_time
        self.task_run.save()

    # -----------------------------------------
    # AI Summary
    # -----------------------------------------
    def build_ai_summary(self):
        """
        يجمع اللوج ويعمل ملخص بسيط.
        لاحقًا تقدر تبعته لـ LLM.
        """
        lines = self.task_run.logs.splitlines()

        total_steps = len(lines)
        errors = [l for l in lines if '"level": "ERROR"' in l]
        warnings = [l for l in lines if '"level": "WARNING"' in l]

        summary = {
            "total_steps": total_steps,
            "errors_count": len(errors),
            "warnings_count": len(warnings),
            "status": self.task_run.status,
        }

        self.task_run.ai_summary = json.dumps(summary, ensure_ascii=False)
        self.task_run.save(update_fields=["ai_summary"])

        return summary

    # -----------------------------------------
    # WebSocket
    # -----------------------------------------

    def __init__(self, task_run: TaskRun | None = None):
        self.task_run = task_run
        self.step_counter = 0
        self.run_started_at = time.time()
        self.channel_layer = get_channel_layer()

    def _broadcast(self, level, message, data=None):

        if not self.task_run:
            return

        group_name = f"workflow_{self.task_run.id}"

        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                "type": "send_log",
                "data": {
                    "level": level,
                    "message": message,
                    "data": data,
                    "timestamp": time.time()
                }
            }
        )

    def info(self, message, data=None, **kwargs):
        self.log(message, level="INFO", data=data)
        self._broadcast("info", message, data)

    def error(self, message, data=None, **kwargs):
        self._broadcast("error", message, data)
