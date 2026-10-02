import api from './api'
import { endpoints } from './endpoints'

const listOf = (response) => response?.data?.results ?? response?.data ?? []
const dataOf = (response) => response?.data

export const listNotifications = async (params = {}) => listOf(await api.get(endpoints.notifications.list, { params }))
export const unreadCount = async () => dataOf(await api.get(endpoints.notifications.unreadCount))
export const markRead = async (id) => dataOf(await api.post(endpoints.notifications.read(id)))
export const markAllRead = async () => dataOf(await api.post(endpoints.notifications.readAll))
export const archiveNotification = async (id) => {
  await api.post(endpoints.notifications.archive(id))
  return true
}
export const updateNotification = async (id, payload) => dataOf(await api.patch(endpoints.notifications.detail(id), payload))
export const deleteNotification = async (id) => {
  await api.delete(endpoints.notifications.detail(id))
  return true
}
