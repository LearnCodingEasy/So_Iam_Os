"""Focused regression tests for untrusted knowledge uploads (no Django setup needed)."""
import io
import unittest

from .file_validation import validate_knowledge_upload


class Upload(io.BytesIO):
    def __init__(self, name, content):
        super().__init__(content)
        self.name = name
        self.size = len(content)


class KnowledgeFileValidationTests(unittest.TestCase):
    def test_accepts_utf8_markdown_and_resets_stream(self):
        upload = Upload("notes.md", "# Django\nمحتوى".encode("utf-8"))
        result = validate_knowledge_upload(upload)
        self.assertEqual(result["extension"], ".md")
        self.assertEqual(upload.tell(), 0)

    def test_rejects_unsupported_extension(self):
        with self.assertRaisesRegex(ValueError, "Supported knowledge files"):
            validate_knowledge_upload(Upload("script.exe", b"MZ"))

    def test_rejects_pdf_extension_with_wrong_signature(self):
        with self.assertRaisesRegex(ValueError, "PDF signature"):
            validate_knowledge_upload(Upload("document.pdf", b"not a pdf"))

    def test_rejects_invalid_utf8_text(self):
        with self.assertRaisesRegex(ValueError, "UTF-8"):
            validate_knowledge_upload(Upload("notes.txt", b"\xff\xfe\x00"))

    def test_rejects_empty_file(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            validate_knowledge_upload(Upload("empty.txt", b""))

    def test_rejects_corrupt_docx_container(self):
        with self.assertRaisesRegex(ValueError, "DOCX"):
            validate_knowledge_upload(Upload("document.docx", b"not a zip"))


if __name__ == "__main__":
    unittest.main()
