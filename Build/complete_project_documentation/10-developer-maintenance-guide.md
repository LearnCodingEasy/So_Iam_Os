# Developer Maintenance Guide

## Trace a feature
1. Find its route in frontend_vue/src/router/index.js.
2. Follow its view and component imports under frontend_vue/src/views/ and components/.
3. Follow store/service imports under stores/ and services/.
4. Check services/Shared/endpoints.js or find direct HTTP/fetch code.
5. Follow backend_django/backend_django/urls.py to the domain api/urls.py.
6. Trace handler to serializer, service, model, task, and side effects.

This is a source-navigation method, not proof each discovered path is active.

## Extend a domain
**INFERRED recommendation:** Follow the domain's local API, serializer, ownership, service, frontend client, and error-handling patterns after inspecting adjacent implementations. Do not assume patterns are uniform across apps.

## Cross-domain work
Inspect both sides of foreign-key writes, user ownership, progress/cache/task side effects, and relevant consumers. Examples are indexed in 03-cross-application-dependencies.md.

## Verification
This guide does not authorize tests/builds/migrations/scripts. Such verification requires separate authorization. The package scripts are listed in frontend_vue/package.json; backend entry/config is in backend_django/.

