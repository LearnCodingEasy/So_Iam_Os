# backend_django\automation\runner.py

import time
from .models import Task, TaskRun, Action
from .engine_runtime import run_action_instance
from django.utils import timezone


RUNNING_TASKS = set()


def start_task(task_id):
    if task_id in RUNNING_TASKS:
        return {"status": "already_running"}

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return {"status": "error", "error": "task_not_found"}

    run = TaskRun.objects.create(task=task)
    RUNNING_TASKS.add(task_id)

    try:
        logs = []
        timings = []

        program = task.program

        start_time = time.time()

        for action in task.actions.filter(enabled=True).order_by("order"):
            t0 = time.time()

            logs.append(f"▶ {action.action_type} : {action.value}")

            result = run_action_instance(action, program)

            if result.get("status") != "ok":
                raise Exception(result.get("error"))

            time.sleep(action.delay)

            timings.append({
                "action": action.action_type,
                "duration": round(time.time() - t0, 3)
            })

        run.status = "success"
        logs.append("✅ Task Finished Successfully")

    except Exception as e:
        run.status = "error"
        logs.append(f"❌ Error: {str(e)}")

    finally:
        run.logs = logs
        run.timings = timings
        run.finished_at = timezone.now()
        run.save()
        RUNNING_TASKS.remove(task_id)

    return {"status": "started", "run_id": run.id}
