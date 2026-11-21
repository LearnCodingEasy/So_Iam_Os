# Configuration and Deployment Boundaries

## Backend configuration
**VERIFIED:** backend_django/backend_django/settings.py configures environment file selection, Django/DRF/auth, database, media, cache, Celery, Channels, CORS/CSRF, and production security checks. Production checks require configured secret material and PostgreSQL. No secret values are reproduced.

## Frontend configuration
**VERIFIED:** frontend_vue/vite.config.js configures Vue, aliases, PWA behavior and asset caching; frontend_vue/package.json declares dependencies/scripts; frontend_vue/src/services/Shared/api.js reads VITE_API_BASE_URL with a local default.

## Runtime dependencies and unknowns
Configuration references PostgreSQL, Redis, media filesystem, AI providers, and job sources. **UNKNOWN:** actual deployment manifests/environment values, secret manager, TLS, object storage, worker topology, provider credentials, and service health. No deployment command was run.

