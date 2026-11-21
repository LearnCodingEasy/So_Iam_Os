def extract_text(file_obj):
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
