"""Validation helpers for files accepted by the knowledge ingestion pipeline.

The client-provided filename and Content-Type are untrusted. We use the file
signature/container and a bounded size check before storing a file for parsing.
"""
from pathlib import Path
import zipfile

MAX_KNOWLEDGE_FILE_SIZE = 25 * 1024 * 1024
ALLOWED_KNOWLEDGE_EXTENSIONS = {".md", ".markdown", ".txt", ".pdf", ".docx", ".json"}


def _read_prefix(uploaded_file, length=8192):
    try:
        uploaded_file.seek(0)
        prefix = uploaded_file.read(length)
    finally:
        try:
            uploaded_file.seek(0)
        except (AttributeError, OSError):
            pass
    return prefix


def validate_knowledge_upload(uploaded_file):
    """Raise ValueError unless upload is a supported, plausibly valid file."""
    if uploaded_file is None:
        raise ValueError("A file is required.")

    size = getattr(uploaded_file, "size", None)
    if not isinstance(size, int) or size <= 0:
        raise ValueError("The uploaded file is empty or its size is unknown.")
    if size > MAX_KNOWLEDGE_FILE_SIZE:
        raise ValueError("Maximum knowledge file size is 25 MB.")

    original_name = str(getattr(uploaded_file, "name", ""))
    suffix = Path(original_name.replace("\\", "/")).suffix.lower()
    if suffix not in ALLOWED_KNOWLEDGE_EXTENSIONS:
        raise ValueError("Supported knowledge files are MD, TXT, JSON, PDF and DOCX.")

    prefix = _read_prefix(uploaded_file)
    if suffix == ".pdf":
        if not prefix.startswith(b"%PDF-"):
            raise ValueError("The uploaded file does not have a valid PDF signature.")
    elif suffix == ".docx":
        try:
            uploaded_file.seek(0)
            with zipfile.ZipFile(uploaded_file) as archive:
                names = set(archive.namelist())
                if "[Content_Types].xml" not in names or "word/document.xml" not in names:
                    raise ValueError("The uploaded DOCX file is not a valid Word document.")
        except (zipfile.BadZipFile, OSError) as exc:
            raise ValueError("The uploaded DOCX file is damaged or invalid.") from exc
        finally:
            try:
                uploaded_file.seek(0)
            except (AttributeError, OSError):
                pass
    else:
        try:
            # Text formats must be valid UTF-8; avoid silently indexing arbitrary binary data.
            uploaded_file.seek(0)
            uploaded_file.read().decode("utf-8-sig")
        except (UnicodeDecodeError, AttributeError) as exc:
            raise ValueError("The uploaded text file must use UTF-8 encoding.") from exc
        finally:
            try:
                uploaded_file.seek(0)
            except (AttributeError, OSError):
                pass

    return {"extension": suffix, "size": size}
