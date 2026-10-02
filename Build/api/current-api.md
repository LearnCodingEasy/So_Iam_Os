# So_Iam_OS — Current API Contract

## Authentication

Base API:

```text
/api/
```

Authentication uses JWT.

Frontend sends:

```http
Authorization: Bearer <access_token>
```

---

# Users

```http
/api/users/me/
```

Returns the authenticated user.

Authentication:

```text
JWT required
```

---

# Knowledge

Base:

```text
/api/knowledge/
```

Knowledge endpoints are owned by the Knowledge application.

Knowledge data is user-scoped.

---

# Learning

Base:

```text
/api/learning/
```

Current learning resources include:

```text
skills
goals
paths
topics
progress
assessments
applications
revisions
```

Important distinction:

```text
/api/learning/goals/
```

currently refers to:

```text
LearningGoal
```

It must not yet be interpreted as the future global:

```text
Goal
```

domain.

---

# AI

Base:

```text
/api/ai/
```

Current endpoints:

```http
POST /api/ai/chat/

GET /api/ai/conversations/

POST /api/ai/conversations/

GET /api/ai/conversations/<id>/

DELETE /api/ai/conversations/<id>/
```

---

# Current AI Request Flow

```text
Vue
 ↓
POST /api/ai/chat/
 ↓
AIChatView
 ↓
AIService
 ↓
AI Provider
```

---

# Future API Domains

The following APIs are planned but should not be considered implemented yet:

```text
/api/goals/
/api/tasks/
/api/settings/
/api/ai/providers/
/api/ai/models/
```

They will be defined after Architecture Lock.

---

# Contract Rule

Frontend code must not invent field names that are not returned by the backend.

Every new feature must define:

```text
Endpoint
Method
Authentication
Request
Response
Validation
Errors
Permissions
```

before frontend implementation.
