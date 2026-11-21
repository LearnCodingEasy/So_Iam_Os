# Shared Frontend State

## Pinia
**VERIFIED:** frontend_vue/src/main.js installs Pinia. Stores exist under frontend_vue/src/stores/ for accounts, AI, Automation, Codex, Goals, Knowledge, Projects, and shared UI state. Store exports and state are cataloged in frontend_vue domain state-management.md files.

## Browser persistence
Source uses localStorage for account tokens/profile, theme, locale/debug preferences, topic chat identifiers, and automation node graph data. Evidence: stores/accounts/user.js; stores/shared/; services/Automation/nodeStorageService.js; learning view/service modules.

## Boundaries and risks
**PARTIAL:** Not all feature state is centralized in Pinia; views also manage local refs/reactive state. Multiple persistence keys and API clients mean shared-state ownership is feature-specific. No browser storage or state behavior was runtime-tested.

