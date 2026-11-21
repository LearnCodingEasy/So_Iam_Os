# automation views and routes

Route paths and names are copied from frontend_vue/src/router/index.js at the cited lines. Guard status reflects route metadata only; it does not establish backend authorization.

- **/automation** — route name automation, router/index.js:L261; requiresAuth.
- **/automation_Dashboard** — route name automation_Dashboard, router/index.js:L267; requiresAuth.
- **/automation_ProgramList** — route name automation_ProgramList, router/index.js:L273; requiresAuth.
- **/automation_programs_create** — route name automation_programs_create, router/index.js:L279; requiresAuth.
- **/automation/:id** — route name automation_programs_edit, router/index.js:L285; requiresAuth.
- **/automation_TaskCreate** — route name automation_TaskCreate, router/index.js:L291; requiresAuth.
- **/automation_TaskEditor** — route name automation_TaskEditor, router/index.js:L297; requiresAuth.


Routed view source files: views/automation/AutomationView.vue; views/automation/DashboardAutomationView.vue; views/automation/icon.vue; views/automation/ProgramCreate.vue; views/automation/ProgramEdit.vue; views/automation/ProgramList.vue; views/automation/TaskCreate.vue; views/automation/TaskEditor.vue.
