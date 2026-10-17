from celery import shared_task


@shared_task(bind=True, name="codex.run_local_ai_job")
def run_local_ai_job(self, job_id):
    from django.utils import timezone
    from .models import LocalAIJob, FileRegistry
    from .services.extensions import project_root, markdown_index, architecture_analyze

    job = LocalAIJob.objects.select_related("project").get(id=job_id)
    job.status = "running"
    job.started_at = timezone.now()
    job.save(update_fields=["status", "started_at"])
    try:
        payload = job.input_data or {}
        if job.task_type in {"summarize", "metadata"}:
            path = str(payload.get("path", ""))
            root = project_root(job.project)
            target = (root / path).resolve()
            if root not in target.parents or not target.is_file():
                raise ValueError("Invalid project file path.")
            text = target.read_text(encoding="utf-8", errors="ignore")
            job.result = {
                "path": path,
                "kind": target.suffix.lower().lstrip("."),
                "size": target.stat().st_size,
                "lines": text.count("\n") + (1 if text else 0),
                "summary": text[:1200] if job.task_type == "summarize" else "",
            }
        elif job.task_type == "classify":
            path = str(payload.get("path", ""))
            record = FileRegistry.objects.filter(project=job.project, path=path).first()
            job.result = {"path": path, "kind": record.kind if record else "unknown", "app_label": record.app_label if record else ""}
        elif job.task_type == "markdown_index":
            job.result = markdown_index(job.project, payload.get("path", ""))
        elif job.task_type == "architecture":
            job.result = architecture_analyze(job.project, payload.get("path", ""))
        else:
            job.result = {"message": "Local AI task completed.", "input": payload}
        job.status = "completed"
        job.completed_at = timezone.now()
        job.save(update_fields=["status", "result", "completed_at"])
        return job.result
    except Exception as exc:
        job.status = "failed"
        job.error = str(exc)
        job.completed_at = timezone.now()
        job.save(update_fields=["status", "error", "completed_at"])
        raise
