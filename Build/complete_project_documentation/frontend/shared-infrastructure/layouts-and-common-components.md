# Layouts and Common Components

## Application shell
**VERIFIED:** frontend_vue/src/App.vue renders RouterView and includes shared toast/confirmation and debug console elements. Authenticated shell components are under frontend_vue/src/components/ai/layout/ and are reused by app-level routing.

## Shared component locations
Common UI source resides under frontend_vue/src/components/shared/, components/core/, and components/ai/layout/. Feature-specific groups include automation and Codex subtrees. Exact files are listed in the frontend domain catalogs.

## Component contracts
Props, emitted events, slots, and exposed methods are documented only where explicit Vue declarations were found. **UNKNOWN:** runtime parent-child behavior for components not exhaustively traced. See each frontend domain's components.md.

