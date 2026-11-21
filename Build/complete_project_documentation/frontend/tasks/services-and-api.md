# tasks services and API

Service files found under services/Tasks. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Tasks/tasks.js
L4: const unwrap = (data) => (Array.isArray(data) ? data : data?.results || [])
L6: export const listTasks = async (params = {}) => unwrap((await api.get(endpoints.tasks.list, { params })).data)
L7: export const listTodayTasks = async () => unwrap((await api.get(endpoints.tasks.today)).data)
L8: export const getTask = async (id) => (await api.get(endpoints.tasks.detail(id))).data
L9: export const createTask = async (payload) => (await api.post(endpoints.tasks.list, payload)).data
L10: export const updateTask = async (id, payload) => (await api.patch(endpoints.tasks.detail(id), payload)).data
L11: export const deleteTask = async (id) => { await api.delete(endpoints.tasks.detail(id)); return true }
L12: export const completeTask = async (id, actual_minutes) => (await api.post(endpoints.tasks.complete(id), { actual_minutes })).data
L13: export const postponeTask = async (id, until) => (await api.post(endpoints.tasks.postpone(id), { until })).data
L14: export const generateTodayTasks = async (payload={}) => (await api.post(endpoints.tasks.generate, payload)).data
L15: export const startTask = async (id) => (await api.post(endpoints.tasks.start(id))).data
L16: export const cancelTask = async (id) => (await api.post(endpoints.tasks.cancel(id))).data
L17: export const reopenTask = async (id) => (await api.post(endpoints.tasks.reopen(id))).data
L18: export const getTaskStats = async () => (await api.get(endpoints.tasks.stats)).data
L19: export const getTaskProgress = async () => (await api.get(endpoints.tasks.progress)).data
L20: export const getTaskCalendar = async (params = {}) => (await api.get(endpoints.tasks.calendar, { params })).data
L21: export const getOverdueTasks = async (params = {}) => unwrap((await api.get(endpoints.tasks.overdue, { params })).data)
L22: export const getTaskGenerationStatus = async (taskId) => (await api.get(endpoints.tasks.generationStatus(taskId))).data


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
