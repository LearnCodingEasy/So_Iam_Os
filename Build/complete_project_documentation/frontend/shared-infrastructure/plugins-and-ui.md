# Frontend Plugins and UI Frameworks

## Bootstrap registration
**VERIFIED:** frontend_vue/src/main.js registers Vue Router, Pinia, Vue Query, i18n, FloatingVue, PrimeVue and services/components, markdown support, icon packages, and toast systems. Imports in main.js are the direct evidence; registration does not prove every imported control is used.

## Configuration
Vite, PWA, alias, CSS, test-runner, and lint configuration files are under frontend_vue/ (vite.config.js, postcss.config.js, tailwind.config.js, vitest.config.js, eslint.config.js). frontend_vue/package.json declares dependency and script names; none were run.

## UI caveat
Several notification channels and UI libraries coexist. Feature docs identify local use; this is not an assertion that all are active in production.

