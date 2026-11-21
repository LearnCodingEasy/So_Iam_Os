# goals services and API

Service files found under services/Goals. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Goals/goals.js
L4: const unwrap = (data) => (Array.isArray(data) ? data : data?.results || [])
L6: export const listGoalsPage = async (params = {}) => (await api.get(endpoints.goals.list, { params })).data
L7: export const listGoals = async (params = {}) => unwrap(await listGoalsPage(params))
L8: export const getGoal = async (id) => (await api.get(endpoints.goals.detail(id))).data
L9: export const getGoalAnalytics = async () => (await api.get(endpoints.goals.analytics)).data
L10: export const createGoal = async (payload) => (await api.post(endpoints.goals.list, payload)).data
L11: export const updateGoal = async (id, payload) => (await api.patch(endpoints.goals.detail(id), payload)).data
L12: export const deleteGoal = async (id) => { await api.delete(endpoints.goals.detail(id)); return true }
L13: export const completeGoal = async (id, notes = '') => (await api.post(endpoints.goals.complete(id), { notes })).data
L14: export const pauseGoal = async (id) => (await api.post(endpoints.goals.pause(id))).data
L15: export const resumeGoal = async (id) => (await api.post(endpoints.goals.resume(id))).data
L16: export const archiveGoal = async (id) => (await api.post(endpoints.goals.archive(id))).data
L17: export const duplicateGoal = async (id) => (await api.post(endpoints.goals.duplicate(id))).data
L18: export const updateGoalProgress = async (id, progress_percent) => (await api.post(endpoints.goals.progress(id), { progress_percent })).data
L19: export const getGoalHistory = async (id) => unwrap((await api.get(endpoints.goals.history(id))).data)
L20: export const getGoalRisk = async (id) => (await api.get(endpoints.goals.risk(id))).data
L21: export const generateGoalPlan = async (id, instructions = '') => (await api.post(endpoints.goals.plan(id), { instructions })).data
L22: export const askGoalCoach = async (id, message) => (await api.post(endpoints.goals.coach(id), { message })).data
L23: export const getGoalPlans = async (id) => unwrap((await api.get(endpoints.goals.plans(id))).data)
L24: export const approveGoalPlan = async (id, proposal_id) => (await api.post(endpoints.goals.approvePlan(id), { proposal_id })).data
L25: export const rejectGoalPlan = async (id, proposal_id) => (await api.post(endpoints.goals.rejectPlan(id), { proposal_id })).data
L26: export const listGoalMilestones = async (goal) => unwrap((await api.get(endpoints.goals.milestones, { params: goal ? { goal } : {} })).data)
L27: export const createGoalMilestone = async (payload) => (await api.post(endpoints.goals.milestones, payload)).data
L28: export const updateGoalMilestone = async (id, payload) => (await api.patch(endpoints.goals.milestone(id), payload)).data
L29: export const deleteGoalMilestone = async (id) => { await api.delete(endpoints.goals.milestone(id)); return true }
L30: export const listGoalProjects = async (id) => unwrap((await api.get(endpoints.goals.projects(id))).data)
L31: export const linkGoalProject = async (id, project_id) => (await api.post(endpoints.goals.projects(id), { project_id })).data
L32: export const addGoalNote = async (id, note) => (await api.post(endpoints.goals.notes(id), { note })).data
L33: export const reorderGoalMilestones = async (id, milestone_ids) => (await api.post(endpoints.goals.reorderMilestones(id), { milestone_ids })).data


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
