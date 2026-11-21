# Authentication and Permissions

## Backend
**VERIFIED:** backend_django/backend_django/settings.py configures JWT authentication and authenticated-by-default DRF permissions; AUTH_USER_MODEL is users_accounts.User. Signup is explicitly public in users_accounts/api/views/users_accounts_views.py. Other account methods declare authentication.

## Frontend
**VERIFIED:** frontend_vue/src/router/index.js initializes stores/accounts/user.js and checks requiresAuth/requiresGuest. The primary client in frontend_vue/src/services/Shared/api.js uses localStorage keys user.access and user.refresh, handles token refresh and dispatches auth events. The user store persists token/profile data.

## Ownership
**PARTIAL:** Ownership checks use per-app patterns including filtered querysets, serializer validation, and create hooks. Examples: goals/api/views/goals_views.py; learning/api/views/user_owned_queryset_mixin_views.py; knowledge/api/views/knowledge_file_views.py; personal_finance/api/views/owned_views.py. Complete endpoint-by-endpoint authorization analysis remains pending.

## Client variation and unknowns
**VERIFIED:** frontend_vue/src/services/Shared/axiosInstance.js uses a different credential convention from api.js; other Axios/fetch paths exist. **UNKNOWN:** full OAuth callback lifecycle and production behavior. See backend app security-and-testing.md and frontend/shared-infrastructure/authentication.md.

