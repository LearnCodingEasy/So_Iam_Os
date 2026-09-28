import api from './api'
import { endpoints } from './endpoints'

const unwrap = (data) => (Array.isArray(data) ? data : data?.results || [])

export const listTasks = async (params = {}) => unwrap((await api.get(endpoints.tasks.list, { params })).data)
export const listTodayTasks = async () => unwrap((await api.get(endpoints.tasks.today)).data)
export const getTask = async (id) => (await api.get(endpoints.tasks.detail(id))).data
export const createTask = async (payload) => (await api.post(endpoints.tasks.list, payload)).data
export const updateTask = async (id, payload) => (await api.patch(endpoints.tasks.detail(id), payload)).data
export const deleteTask = async (id) => { await api.delete(endpoints.tasks.detail(id)); return true }
export const completeTask = async (id, actual_minutes) => (await api.post(endpoints.tasks.complete(id), { actual_minutes })).data
export const postponeTask = async (id, until) => (await api.post(endpoints.tasks.postpone(id), { until })).data
export const generateTodayTasks = async (payload={}) => (await api.post(endpoints.tasks.generate, payload)).data

export default { listTasks, listTodayTasks, getTask, createTask, updateTask, deleteTask, completeTask, postponeTask }
