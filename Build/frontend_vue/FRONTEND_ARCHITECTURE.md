# Frontend Architecture

## API

All HTTP requests use `src/services/api.js`. Do not create new Axios clients inside views.

Environment variable: `VITE_API_BASE_URL`.

## Feedback

Use `useAppToast()` for success, information, warning and error feedback. API errors are normalized by `src/utils/apiError.js`.

## Theme

`useTheme()` persists the selected theme in `localStorage` under `so_iam_os.theme` and toggles PrimeVue's `.p-dark` selector.

## Responsive design

New shared styling belongs under `src/assets/scss/`. Prefer design tokens and reusable classes over page-local hard-coded colors.

## Route protection

Protected routes use `meta.requiresAuth` and are enforced by the router guard. The user store restores and refreshes JWT tokens before allowing protected navigation.
