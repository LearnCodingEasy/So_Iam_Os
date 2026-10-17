"""Deterministic metadata extraction for user-owned knowledge items.

This module intentionally works offline: it does not send private content to an
external AI provider. Results are heuristics and should be treated as suggestions.
"""
import re
from collections import Counter

TECH_TERMS = (
    "django", "python", "vue", "javascript", "typescript", "react",
    "sql", "sqlite", "postgresql", "docker", "celery", "redis",
    "api", "rest", "html", "css", "scss", "machine learning", "llm",
)


def extract_metadata(title="", description="", content=""):
    text = "\n".join(part for part in (title, description, content) if part).strip()
    headings = re.findall(r"(?m)^#{1,6}\s+(.+?)\s*#*\s*$", content or "")
    paragraphs = [
        re.sub(r"\s+", " ", p).strip()
        for p in re.split(r"\n\s*\n", content or "")
        if re.sub(r"\s+", " ", p).strip()
        and not re.match(r"^\s*#", p)
        and not re.match(r"^\s*```", p)
    ]
    clean = re.sub(r"```[\s\S]*?```", " ", text)
    clean = re.sub(r"`([^`]*)`", r"\1", clean)
    words = re.findall(r"(?u)\b[\w+#.-]{3,}\b", clean.lower())
    stopwords = {
        "the", "and", "for", "with", "that", "this", "from", "are", "was",
        "you", "your", "have", "has", "into", "will", "can", "not", "but",
        "then", "than", "when", "what", "how", "using", "use", "all",
    }
    counts = Counter(w for w in words if w not in stopwords and not w.isdigit())
    keywords = [word for word, _ in counts.most_common(12)]
    lower = text.lower()
    tech_tags = [term for term in TECH_TERMS if term in lower]
    summary = (paragraphs[0] if paragraphs else re.sub(r"\s+", " ", description or title)).strip()
    return {
        "headings": headings[:50],
        "keywords": keywords,
        "summary": summary[:600],
        "technology_tags": tech_tags,
        "language_hint": "ar" if re.search(r"[\u0600-\u06ff]", text) else "en",
        "word_count": len(words),
    }
