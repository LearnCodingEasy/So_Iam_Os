from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .file_validation import validate_knowledge_upload
from .models import KnowledgeFile


def _extract_text(file_obj):
    """Extract text from supported formats without trusting MIME metadata."""
    name = file_obj.original_name.lower()
    with file_obj.file.open("rb") as handle:
        if name.endswith((".md", ".markdown", ".txt", ".json")):
            return handle.read().decode("utf-8-sig")
        if name.endswith(".pdf"):
            try:
                import pypdf
            except ImportError as exc:
                raise RuntimeError("PDF extraction requires the optional pypdf package.") from exc
            reader = pypdf.PdfReader(handle)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        if name.endswith(".docx"):
            try:
                from docx import Document
            except ImportError as exc:
                raise RuntimeError("DOCX extraction requires the optional python-docx package.") from exc
            document = Document(handle)
            return "\n".join(paragraph.text for paragraph in document.paragraphs)
    raise ValueError("This file type is not supported for text extraction.")


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=2)
def process_knowledge_file(self, file_id):
    obj = KnowledgeFile.objects.select_related("knowledge").get(pk=file_id)
    obj.processing_status = KnowledgeFile.ProcessingStatus.PROCESSING
    obj.processing_error = ""
    obj.save(update_fields=["processing_status", "processing_error", "updated_at"])
    try:
        validate_knowledge_upload(obj.file)
        text = _extract_text(obj)
        if not text.strip():
            raise ValueError("No extractable text was found in this file.")

        # Never overwrite authored knowledge or content extracted from another file.
        # Preserve per-file extraction in metadata so multiple attachments do not race.
        metadata = dict(obj.metadata or {})
        metadata["extraction"] = {
            "text": text[:2_000_000],
            "character_count": len(text),
            "extracted_at": timezone.now().isoformat(),
        }
        obj.metadata = metadata
        obj.processing_status = KnowledgeFile.ProcessingStatus.COMPLETED
        obj.processed_at = timezone.now()
        obj.processing_error = ""
        obj.save(update_fields=["metadata", "processing_status", "processed_at", "processing_error", "updated_at"])

        with transaction.atomic():
            knowledge = obj.knowledge
            if not knowledge.content.strip():
                knowledge.content = text[:2_000_000]
                knowledge.save(update_fields=["content", "updated_at"])
        return {"file_id": obj.id, "status": obj.processing_status, "characters": len(text)}
    except Exception as exc:
        obj.processing_status = KnowledgeFile.ProcessingStatus.FAILED
        obj.processing_error = str(exc)[:500]
        obj.save(update_fields=["processing_status", "processing_error", "updated_at"])
        raise
