# Learning and Knowledge Domains

This note is limited to domain-specific entities, flows, integration, and gaps. Shared architecture is in [System Architecture](../01-system-architecture.md), API traceability in [API and Integration Map](../04-api-and-integration-map.md), data conventions in [Data Architecture](../05-data-architecture.md), and operational risks in [Security and Operations](../06-security-and-operations.md).

## Learning

**VERIFIED:** `backend_django/learning/models/` contains skills, goals, paths, topics, lessons, resources, notes, progress, sessions, assessments/attempts/responses, revisions, and application/submission/review records. `learning/api/urls.py` registers a broad set of resources, with behavior in `learning/api/views/`, validation in serializers, and service logic under `learning/services/`.

The frontend has routed Learning and topic views plus services under `frontend_vue/src/views/learning/` and `frontend_vue/src/services/Learning/`. **PARTIAL:** The frontend dashboard fans out across multiple resource calls; this is source behavior, not proof all requests succeed together.

## Knowledge

**VERIFIED:** `backend_django/knowledge/models/knowledge_item.py` and `knowledge_file.py` define user-owned items and attached files. `knowledge/api/views/knowledge_item_views.py` and `knowledge_file_views.py` implement item/file operations including file upload, archive, extraction metadata, and topic connections. File processing is present in `backend_django/knowledge/tasks/knowledge_file_tasks.py` and `knowledge/services/`.

The frontend integrates Knowledge views, a Pinia store, and service modules under `frontend_vue/src/views/knowledge/`, `stores/knowledge/`, and `services/Knowledge/`.

## Domain relationship

**VERIFIED:** Learning topics can reference knowledge items (`backend_django/learning/models/learning_topic.py`); knowledge-item endpoints also expose topic connection operations (`backend_django/knowledge/api/views/knowledge_item_views.py`). This supports a relationship between stored knowledge and a learning topic, but does not by itself establish a complete learning loop.

## Domain-specific gaps

- **UNKNOWN:** Parser coverage and extraction quality across all uploaded file types; inspect extractor implementations for exact support.
- **PARTIAL:** Knowledge upload code can leave processing pending if async enqueueing fails; runtime retry behavior is not established.
- **UNKNOWN:** Whether all learning resources and application/review flows are reachable in the current routed UI.
- **INFERRED recommendation:** Document user ownership rules for nested learning records and file access consistently; shared authorization concerns are covered in [Security and Operations](../06-security-and-operations.md).
