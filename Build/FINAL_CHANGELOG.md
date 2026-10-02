# FINAL CHANGELOG

## Core
- Unified Vue AppLayout.
- Added responsive sidebar/header shell.
- Added Tasks Calendar workspace.
- Added Social workspace.
- Added Notification Center.

## Backend
- Added notification domain, API and service.
- Added social matching domain and API.
- Added task calendar fields/API.
- Added AI router and provider health API.
- Added RemoteOK/Wuzzuf source adapters.
- Added notification hooks for task completion and job applications.

## Contracts
- Fixed missing Jobs apply endpoint builder.
- Added canonical notification/social/calendar endpoint builders.

## Security
- Removed environment-specific secret files from final deliverable.
- Added `.env.example`.
- Preserved backend-only AI credentials.

## Dependencies
- Added backend `requirements.txt`.
- Aligned PrimeVue theme package with PrimeVue 5.
