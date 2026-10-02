# So_Iam_OS — Current Domain Model

## 1. User

The central entity of the system is:

`users_accounts.User`

The project uses a custom Django user model.

```text
User
```

is the owner of user-specific data across the system.

Main relationships currently include:

```text
User
 ├── LearningGoal
 ├── LearningPath
 ├── AIConversation
 └── KnowledgeItem
```

---

# 2. Knowledge

The Knowledge application manages user-owned knowledge.

Main entities:

```text
KnowledgeItem
KnowledgeFile
```

A KnowledgeItem can be connected to the Learning system.

Current relationship:

```text
KnowledgeItem
       │
       └── LearningTopic
```

Knowledge is therefore not isolated from Learning.

It can become a source of:

- learning material
- notes
- references
- applications
- AI context

---

# 3. Learning

The Learning application is currently the most complete domain.

Main entities:

```text
Skill
LearningGoal
LearningPath
LearningTopic
Lesson
LearningResource
LearningNote
LearningProgress
LearningSession
Assessment
AssessmentQuestion
AssessmentChoice
AssessmentAttempt
AssessmentResponse
KnowledgeApplication
ApplicationSubmission
ApplicationReview
LearningRevision
```

---

# 4. Skill

`Skill` currently represents a reusable/global skill definition.

Examples:

```text
Django
Python
Vue.js
JavaScript
Docker
```

It is not currently modeled as a direct User-owned entity.

User-specific learning state is currently represented through LearningGoal, LearningPath, LearningProgress, and related learning entities.

This distinction must be preserved during Architecture Lock.

---

# 5. LearningGoal

A LearningGoal represents an educational objective belonging to a user.

Relationship:

```text
User
  │
  └── LearningGoal
          │
          └── Skill
```

A LearningGoal may contain:

- title
- description
- reason
- current level
- target level
- status
- target date

---

# 6. LearningPath

A LearningPath belongs to a user and is connected to a LearningGoal.

```text
User
  │
  └── LearningGoal
          │
          └── LearningPath
```

The LearningPath contains ordered LearningTopics.

---

# 7. LearningTopic

A LearningTopic belongs to a LearningPath.

```text
LearningPath
      │
      └── LearningTopic
```

A topic can have:

- Skill
- Lessons
- Resources
- Notes
- Progress
- Assessment
- Knowledge relation
- Prerequisites
- Knowledge Application

---

# 8. AI

The AI application currently contains:

```text
AIConversation
AIMessage
```

AI providers are implemented through a provider abstraction.

Current providers include:

```text
Ollama
OpenRouter
```

Current conceptual flow:

```text
Vue
 ↓
Django API
 ↓
AIService
 ↓
AI Provider
 ↓
Ollama / OpenRouter
```

The system should continue using this architecture.

---

# 9. Current AI Limitations

The current AI architecture does not yet provide:

- user-specific AI settings
- user-owned provider API keys
- OpenAI provider
- provider model discovery
- structured prompt management
- rich context building
- approval workflow for AI-generated Learning Paths

These are future architecture responsibilities.

---

# 10. Goals

The `goals` Django application currently exists but does not yet contain a production domain model.

Therefore the current system must not assume that:

```text
Goal
```

already exists.

The distinction between:

```text
Goal
LearningGoal
```

must be resolved during Architecture Lock.

---

# 11. Tasks

The `tasks` Django application currently exists but does not yet contain the required task domain.

The final relationship between:

```text
Goal
Task
LearningPath
Skill
```

must be defined during Architecture Lock.

---

# 12. Current High-Level Architecture

```text
                         User
                           │
          ┌────────────────┼────────────────┐
          │                │                │
      Knowledge         Learning            AI
          │                │                │
          │          LearningGoal      Conversations
          │                │
          │          LearningPath
          │                │
          │          LearningTopic
          │                │
          └──────────────┬─┘
                         │
                   Knowledge Context
```

---

# 13. Future Architecture Direction

The target architecture is:

```text
User
 │
 ├── Knowledge
 │
 ├── Goals
 │     └── Tasks
 │
 ├── Skills
 │
 ├── Learning
 │     ├── LearningGoals
 │     ├── LearningPaths
 │     ├── Topics
 │     └── Progress
 │
 └── AI
       ├── Settings
       ├── Conversations
       ├── Providers
       ├── Models
       └── Context
```

The exact relationships will be finalized during:

```text
Phase 2 — Architecture Lock
```

---

# 14. Architecture Rules

The project must follow these rules:

1. Do not duplicate existing domain models.
2. Do not replace LearningGoal without a migration strategy.
3. Do not expose AI provider API keys to Vue.
4. Vue communicates with Django only.
5. AI providers are accessed through backend abstractions.
6. Knowledge remains reusable across Learning and AI.
7. Goals and Tasks must be user-scoped.
8. API contracts must be explicit.
9. Business logic should remain in backend services.
10. Existing Learning functionality must remain backward compatible.
