# Shared Frontend Router

## Router implementation
**VERIFIED:** frontend_vue/src/router/index.js creates Vue Router with HTML5 history, declares routes, starts/ends NProgress, initializes the Pinia user store, and enforces requiresAuth/requiresGuest metadata through beforeEach.

## Route inventory
| Path | Name | Route metadata / source |
|---|---|---|
| / | home | requiresAuth, L60 |
| /About | About | requiresAuth, L69 |
| /login | login | requiresGuest, L82 |
| /auth-callback | AuthCallback | no guard metadata in route object, L92 |
| /profile/:id | profile | requiresAuth, L102 |
| /knowledge | knowledge | requiresAuth, L115 |
| /learning | learning | requiresAuth, L127 |
| /learning/topics/:topicId | learning-topic | requiresAuth, L135 |
| /goals | goals | requiresAuth, L146 |
| /tasks/today | today-tasks | requiresAuth, L152 |
| /progress | progress | requiresAuth, L158 |
| /jobs | jobs | requiresAuth, L164 |
| /scraper | scraper | requiresAuth, L170 |
| /tasks | tasks | requiresAuth, L176 |
| /codex | codex | requiresAuth, L182 |
| /projects | projects | requiresAuth, L183 |
| /challenges | challenges | requiresAuth, L185 |
| /finance | finance | requiresAuth, L190 |
| /memory | memory | requiresAuth, L191 |
| /ai/agents | ai-agents | requiresAuth, L193 |
| /social | social | requiresAuth, L198 |
| /notifications | notifications | requiresAuth, L200 |
| /system/frontend | frontend-enhancements | requiresAuth, L210 |
| /settings | settings | requiresAuth, L220 |
| /ai | ai-chat | requiresAuth, L230 |
| /ai/control | ai-control | requiresAuth, L236 |
| /ai/operations | ai-operations | requiresAuth, L242 |
| /dashboard | dashboard | requiresAuth, L252 |
| /automation | automation | requiresAuth, L261 |
| /automation_Dashboard | automation_Dashboard | requiresAuth, L267 |
| /automation_ProgramList | automation_ProgramList | requiresAuth, L273 |
| /automation_programs_create | automation_programs_create | requiresAuth, L279 |
| /automation/:id | automation_programs_edit | requiresAuth, L285 |
| /automation_TaskCreate | automation_TaskCreate | requiresAuth, L291 |
| /automation_TaskEditor | automation_TaskEditor | requiresAuth, L297 |
| /:catchAll(.*) | NotFound | catchall, L307 |

All lines refer to frontend_vue/src/router/index.js. **VERIFIED** means declared only; no route navigation was executed.

## Guard behavior
The beforeEach handler initializes the user store if needed, reads isLoggedIn, redirects protected routes to login with redirect query, and redirects authenticated guests to home. An auth-expired window event also redirects to login. Callback route behavior and production OAuth return paths remain **UNKNOWN**.

