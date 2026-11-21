# Frontend Utilities, Styles, and Assets

## Utilities and composables
Reusable source lives in frontend_vue/src/composables/, src/utils/, src/plugins/, src/presets/, and src/assets/. The full file/path catalog is in source-file-catalog.md.

## Styling
**VERIFIED:** Source inventory contains SCSS/CSS assets, including global style entry points imported by main.js. Domain styles are organized below assets/scss/ and are cataloged by path.

## Binary assets
Image assets are inventoried by filename but not interpreted as source code. Binary files do not expose functions or callers. Generated/vendor assets and node_modules are excluded from project source catalogs.


## Non-code resource inventory

The source tree also includes frontend_vue/src/composables/api-flow-demo.html, frontend_vue/src/views/finance/test.html, and Markdown resources under frontend_vue/src/views/automation/Project_Context_Analysis.md and Project_Context_Profile.md. These were identified by filename only and are not used as architectural evidence. Binary images under frontend_vue/src/assets/Images/ are assets, not executable source; inventory them by path if their UI usage becomes relevant.
