from celery import shared_task
from django.utils import timezone
from .models import KnowledgeFile


def _extract_text(file_obj):
    name = file_obj.original_name.lower()
    if name.endswith((".md", ".markdown", ".txt")):
        with file_obj.file.open("rb") as handle:
            return handle.read().decode("utf-8", errors="replace")
    # PDF/DOCX extraction is optional so the base installation stays safe.
    if name.endswith(".pdf"):
        try:
            import pypdf
            reader = pypdf.PdfReader(file_obj.file)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except ImportError:
            return ""
    if name.endswith(".docx"):
        try:
            from docx import Document
            doc = Document(file_obj.file)
            return "\n".join(p.text for p in doc.paragraphs)
        except ImportError:
            return ""
    return ""


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=2)
def process_knowledge_file(self, file_id):
    obj = KnowledgeFile.objects.select_related("knowledge").get(pk=file_id)
    obj.processing_status = KnowledgeFile.ProcessingStatus.PROCESSING
    obj.processing_error = ""
    obj.save(update_fields=["processing_status", "processing_error", "updated_at"])
    try:
        text = _extract_text(obj)
        if text:
            obj.knowledge.content = text[:2_000_000]
            obj.knowledge.save(update_fields=["content", "updated_at"])
        obj.processing_status = KnowledgeFile.ProcessingStatus.COMPLETED
        obj.processed_at = timezone.now()
        obj.save(update_fields=["processing_status", "processed_at", "updated_at"])
        return {"file_id": obj.id, "status": obj.processing_status}
    except Exception as exc:
        obj.processing_status = KnowledgeFile.ProcessingStatus.FAILED
        obj.processing_error = str(exc)[:2000]
        obj.save(update_fields=["processing_status", "processing_error", "updated_at"])
        raise
