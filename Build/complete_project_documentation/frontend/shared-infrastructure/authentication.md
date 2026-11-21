# Shared Frontend Authentication

## Store and token keys
**VERIFIED:** frontend_vue/src/stores/accounts/user.js is the Pinia account store. It persists access/refresh/profile values in localStorage under user.access, user.refresh, user.info, initializes session state, and requests the current user through the shared API service.

## Token refresh and route behavior
The primary client in frontend_vue/src/services/Shared/api.js reads user.access/user.refresh, performs a single-flight refresh request, persists rotated tokens, retries one 401 request, clears auth storage on failure, and dispatches so-iam-auth-expired. frontend_vue/src/router/index.js initializes the store and applies route metadata. These are source behaviors; no token was used against a server.

## Other auth paths
**PARTIAL:** frontend_vue/src/services/Shared/axiosInstance.js uses a distinct auth_token key. Global Axios defaults are assigned in main.js; AI streaming uses getValidAccessToken(). Account callback code reads tokens from callback context. These paths require separate validation.

**UNKNOWN:** Deployed OAuth callback configuration, token storage security in deployment, and server-side revocation/logout lifecycle.

