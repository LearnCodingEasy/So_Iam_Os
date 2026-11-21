# Updated Frontend Setup

1. Enter `frontend_vue`.
2. Use Node 22+ (the project declares Node 22.18+ or Node 24.12+).
3. Run `npm install` in a network-enabled environment to regenerate and validate the lockfile.
4. Run `npm run build`.
5. Run `npm run test:unit`.
6. Run `npm run lint`.

The upgrade adds exactly 10 direct frontend libraries. Their current versions were checked against npm package metadata on 2026-11-11. The package registry was not reachable from the execution sandbox, so dependency installation and production compilation remain external-test pending.

## New libraries

- `@vueuse/core` — Vue composables/browser utilities
- `@tanstack/vue-query` — Server-state caching/refetching
- `vue-i18n` — Arabic/English localization
- `floating-vue` — Tooltips/popovers
- `vue-virtual-scroller` — Large-list virtualization
- `vue-draggable-plus` — Vue 3 drag/drop sorting
- `@tiptap/vue-3` — Vue 3 rich text editor
- `@tiptap/starter-kit` — Editor baseline extensions
- `filepond` — Accessible file intake UI
- `vue-sonner` — Modern toast notifications
