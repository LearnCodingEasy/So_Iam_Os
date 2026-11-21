# projects services and API

Service files found under services/Projects. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Projects/projects.js
L4: const unwrap = (payload) => (Array.isArray(payload) ? payload : payload?.results || [])
L6: export const listProjectsPage = async (params = {}) =>
L8: export const listProjects = async (params = {}) => unwrap(await listProjectsPage(params))
L9: export const getProject = async (id) => (await api.get(`${domainEndpoints.projects}${id}/`)).data
L10: export const createProject = async (payload) =>
L12: export const updateProject = async (id, payload) =>
L14: export const deleteProject = async (id) => {


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
