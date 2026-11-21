# accounts views and routes

Route paths and names are copied from frontend_vue/src/router/index.js at the cited lines. Guard status reflects route metadata only; it does not establish backend authorization.

- **/login** — route name login, router/index.js:L82; requiresGuest.
- **/auth-callback** — route name AuthCallback, router/index.js:L92; callback route has no guard metadata.
- **/profile/:id** — route name profile, router/index.js:L102; requiresAuth.


Routed view source files: views/accounts/auth-callback.vue; views/accounts/AuthCallback.vue; views/accounts/LoginView.vue; views/accounts/ProfileView.vue.
