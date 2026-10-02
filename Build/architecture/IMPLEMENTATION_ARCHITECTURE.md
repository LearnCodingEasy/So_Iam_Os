# So_Iam_OS — Integrated Implementation Architecture

This document records the implementation direction for the complete application.

## Domain flow

`User → Goals → Learning → Skills/Progress → Tasks → Jobs/Skill Gap → Learning recommendations`

`Knowledge → Extraction → AI analysis → Learning structure → Assessment/Practice → Progress`

## Backend boundaries

- `core`: dashboard, shared infrastructure, cache and learning settings.
- `tasks`: execution/planning work connected to goals and learning.
- `goals`: user goals and progress ownership.
- `learning`: skills, goals, paths, topics, lessons, resources, assessments and progress.
- `knowledge`: user-owned knowledge items/files and topic connections.
- `ai`: provider configuration, conversations, topic chat and learning generation workflows.
- `jobs_opportunity`: sources, opportunities, requirements, matches and applications.

## Frontend boundaries

- `services/`: API contract only; endpoint paths live in `services/endpoints.js`.
- `stores/`: durable client state such as authentication.
- `composables/`: cross-cutting UI behavior (theme, toast).
- `components/`: reusable presentation and domain components.
- `views/`: route-level orchestration; large learning screens should progressively delegate to components.
- `assets/scss/`: design tokens, base rules, components and page-level styling.

## Progress source of truth

Learning progress is persisted by Django. The canonical summary endpoint is:

`GET /api/learning/progress/summary/`

The frontend must display server-calculated progress rather than hard-coded percentages.

## Long-running work

Knowledge extraction/analysis, AI generation and job aggregation should use Celery when the operation can exceed a normal HTTP request window. The frontend should poll task status and display a user-visible state.

## Security

- Never commit production secrets.
- Every user-owned endpoint must filter by authenticated user ownership.
- File access must remain user-scoped.
- User code must not execute directly inside the Django process; a sandboxed execution service is required before enabling arbitrary code execution.
