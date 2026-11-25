import api from '../Shared/api'
import { endpoints } from '../Shared/endpoints'

const unwrap = (data) => (Array.isArray(data) ? data : data?.results || [])

export const listGoalsPage = async (params = {}) =>
  (await api.get(endpoints.goals.list, { params })).data
export const listGoals = async (params = {}) => unwrap(await listGoalsPage(params))
export const getGoal = async (id) => (await api.get(endpoints.goals.detail(id))).data
export const getGoalAnalytics = async () => (await api.get(endpoints.goals.analytics)).data
export const createGoal = async (payload) => (await api.post(endpoints.goals.list, payload)).data
export const updateGoal = async (id, payload) =>
  (await api.patch(endpoints.goals.detail(id), payload)).data
export const deleteGoal = async (id) => {
  await api.delete(endpoints.goals.detail(id))
  return true
}
export const completeGoal = async (id, notes = '') =>
  (await api.post(endpoints.goals.complete(id), { notes })).data
export const pauseGoal = async (id) => (await api.post(endpoints.goals.pause(id))).data
export const resumeGoal = async (id) => (await api.post(endpoints.goals.resume(id))).data
export const archiveGoal = async (id) => (await api.post(endpoints.goals.archive(id))).data
export const duplicateGoal = async (id) => (await api.post(endpoints.goals.duplicate(id))).data
export const updateGoalProgress = async (id, progress_percent) =>
  (await api.post(endpoints.goals.progress(id), { progress_percent })).data
export const getGoalHistory = async (id) =>
  unwrap((await api.get(endpoints.goals.history(id))).data)
export const getGoalRisk = async (id) => (await api.get(endpoints.goals.risk(id))).data
export const generateGoalPlan = async (id, instructions = '') =>
  (await api.post(endpoints.goals.plan(id), { instructions })).data
export const askGoalCoach = async (id, message) =>
  (await api.post(endpoints.goals.coach(id), { message })).data
export const getGoalPlans = async (id) => unwrap((await api.get(endpoints.goals.plans(id))).data)
export const approveGoalPlan = async (id, proposal_id) =>
  (await api.post(endpoints.goals.approvePlan(id), { proposal_id })).data
export const rejectGoalPlan = async (id, proposal_id) =>
  (await api.post(endpoints.goals.rejectPlan(id), { proposal_id })).data
export const listGoalMilestones = async (goal) =>
  unwrap((await api.get(endpoints.goals.milestones, { params: goal ? { goal } : {} })).data)
export const createGoalMilestone = async (payload) =>
  (await api.post(endpoints.goals.milestones, payload)).data
export const updateGoalMilestone = async (id, payload) =>
  (await api.patch(endpoints.goals.milestone(id), payload)).data
export const deleteGoalMilestone = async (id) => {
  await api.delete(endpoints.goals.milestone(id))
  return true
}
export const listGoalProjects = async (id) =>
  unwrap((await api.get(endpoints.goals.projects(id))).data)
export const linkGoalProject = async (id, project_id) =>
  (await api.post(endpoints.goals.projects(id), { project_id })).data
export const addGoalNote = async (id, note) =>
  (await api.post(endpoints.goals.notes(id), { note })).data
export const reorderGoalMilestones = async (id, milestone_ids) =>
  (await api.post(endpoints.goals.reorderMilestones(id), { milestone_ids })).data

export default {
  listGoals,
  listGoalsPage,
  getGoal,
  getGoalAnalytics,
  createGoal,
  updateGoal,
  deleteGoal,
  completeGoal,
  pauseGoal,
  resumeGoal,
  archiveGoal,
  duplicateGoal,
  updateGoalProgress,
  getGoalHistory,
  getGoalRisk,
  generateGoalPlan,
  askGoalCoach,
  getGoalPlans,
  approveGoalPlan,
  rejectGoalPlan,
  listGoalMilestones,
  createGoalMilestone,
  updateGoalMilestone,
  deleteGoalMilestone,
  listGoalProjects,
  linkGoalProject,
  addGoalNote,
  reorderGoalMilestones,
}
