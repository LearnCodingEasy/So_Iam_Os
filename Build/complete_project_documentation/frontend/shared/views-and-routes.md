# shared views and routes

Route paths and names are copied from frontend_vue/src/router/index.js at the cited lines. Guard status reflects route metadata only; it does not establish backend authorization.

- **/** — route name home, router/index.js:L60; requiresAuth.
- **/About** — route name About, router/index.js:L69; requiresAuth.
- **/:catchAll(.*)** — route name NotFound, router/index.js:L307; catchall.


Routed view source files: views/shared/AboutView.vue; views/shared/HomeView.vue; views/shared/Page_Not_Found.vue.
