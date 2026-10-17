from celery import shared_task
from django.utils import timezone
from automation.models import Workflow, TaskRun
from automation.workflow_runner import execute_workflow

@shared_task(bind=True)
def execute_workflow_task(self, workflow_id: str, user_id: str, task_run_id: str):
    try:
        workflow = Workflow.objects.get(id=workflow_id, created_by_id=user_id)
        task_run = TaskRun.objects.get(id=task_run_id, workflow=workflow, created_by_id=user_id)
        result = execute_workflow(workflow.id, workflow.created_by, task_run=task_run)
        task_run.refresh_from_db()
        task_run.finished_at = timezone.now()
        task_run.logs = str(result)[:10000]
        task_run.save(update_fields=["finished_at", "logs", "updated_at"])
        return {"workflow_id": workflow_id, "task_run_id": task_run_id, "status": "success", "result": result}
    except Exception as exc:
        try:
            task_run = TaskRun.objects.get(id=task_run_id, created_by_id=user_id)
            task_run.status = "failed"; task_run.finished_at = timezone.now(); task_run.logs = str(exc)[:10000]
            task_run.save(update_fields=["status", "finished_at", "logs", "updated_at"])
        except Exception:
            pass
        raise
