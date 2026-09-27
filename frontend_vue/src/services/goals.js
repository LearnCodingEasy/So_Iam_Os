import api from './api'
import { endpoints } from './endpoints'

const unwrap = (data) => (Array.isArray(data) ? data : data?.results || [])

export const listGoals = async (params = {}) => unwrap((await api.get(endpoints.goals.list, { params })).data)
export const getGoal = async (id) => (await api.get(endpoints.goals.detail(id))).data
export const createGoal = async (payload) => (await api.post(endpoints.goals.list, payload)).data
export const updateGoal = async (id, payload) => (await api.patch(endpoints.goals.detail(id), payload)).data
export const deleteGoal = async (id) => { await api.delete(endpoints.goals.detail(id)); return true }
export const completeGoal = async (id, notes = '') => (await api.post(endpoints.goals.complete(id), { notes })).data
export const pauseGoal = async (id) => (await api.post(endpoints.goals.pause(id))).data
export const resumeGoal = async (id) => (await api.post(endpoints.goals.resume(id))).data
export const updateGoalProgress = async (id, progress_percent) => (await api.post(endpoints.goals.progress(id), { progress_percent })).data

export default { listGoals, getGoal, createGoal, updateGoal, deleteGoal, completeGoal, pauseGoal, resumeGoal, updateGoalProgress }
