# automation\tasks.py
from celery import shared_task
from django.utils import timezone
from automation.models import Workflow


@shared_task(bind=True)
def execute_workflow_task(self, workflow_id: str):
    """
    Execute workflow nodes sequentially.
    """
    try:
        workflow = Workflow.objects.get(id=workflow_id)

        results = []

        for node in workflow.nodes.all().order_by("created_at"):

            # مثال بسيط لتنفيذ node
            result = {
                "node_id": str(node.id),
                "name": node.label,
                "status": "executed"
            }

            results.append(result)

        return {
            "workflow_id": workflow_id,
            "status": "completed",
            "nodes_executed": len(results),
            "results": results
        }

    except Workflow.DoesNotExist:
        return {
            "status": "error",
            "message": f"Workflow {workflow_id} not found"
        }
