# ADR 0001 — Preserve Existing Domain Architecture

## Status

Accepted

## Context

So_Iam_OS already contains functional domains for:

* Users
* Knowledge
* Learning
* AI

The Learning application already contains a substantial data model and business logic.

Creating duplicate models for these domains would introduce:

* duplicated data
* inconsistent APIs
* migration complexity
* synchronization problems
* broken frontend contracts

## Decision

The existing domain models must be reused and extended.

The project will not create duplicate versions of:

```text
Skill
LearningGoal
LearningPath
LearningTopic
KnowledgeItem
AIConversation
AIMessage
User
```

## Goals

A new global Goal domain may be introduced because the existing:

```text
LearningGoal
```

is specifically educational.

The relationship between:

```text
Goal
LearningGoal
```

will be finalized during Architecture Lock.

## Tasks

The existing `tasks` application will be developed after the Goal architecture is finalized.

## AI

The existing:

```text
BaseAIProvider
AIService
AIConversation
AIMessage
```

will be extended rather than replaced.

## Frontend

Existing Vue services and views will be preserved.

New features must use the same API layer.

## Security

AI credentials must remain server-side.

Frontend applications must never receive raw provider API keys.

## Consequences

This approach minimizes:

* migrations
* duplicated models
* breaking changes
* frontend rewrites

while allowing the project to evolve toward:

```text
Knowledge
    ↓
Learning
    ↓
Goals
    ↓
Tasks
    ↓
AI
```
