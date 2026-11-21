# notifications services and API

Service files found under services/Notifications. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Notifications/notifications.js
L4: const listOf = (response) => response?.data?.results ?? response?.data ?? []
L5: const dataOf = (response) => response?.data
L7: export const listNotifications = async (params = {}) => listOf(await api.get(endpoints.notifications.list, { params }))
L8: export const unreadCount = async () => dataOf(await api.get(endpoints.notifications.unreadCount))
L9: export const markRead = async (id) => dataOf(await api.post(endpoints.notifications.read(id)))
L10: export const markAllRead = async () => dataOf(await api.post(endpoints.notifications.readAll))
L11: export const archiveNotification = async (id) => {
L15: export const updateNotification = async (id, payload) => dataOf(await api.patch(endpoints.notifications.detail(id), payload))
L16: export const deleteNotification = async (id) => {


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
