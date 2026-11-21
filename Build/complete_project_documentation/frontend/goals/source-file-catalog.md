# goals source-file catalog

Files associated with this domain's view/service/store/component directories are listed. Imports and declaration names are static excerpts; global callers are not exhaustive.


## views/goals/Goals.vue
- Type: .vue
- Declarations: L128: const store = useGoalsStore(); L129: const toast = useAppToast(); L130: const search = ref(''); L131: const statusFilter = ref(null); L132: const categoryFilter = ref(null); L133: const sortBy = ref('-created_at'); L134: const page = ref(1); L135: const pageSize = 20; L136: const editorVisible = ref(false); L137: const detailsVisible = ref(false); L138: const milestoneVisible = ref(false); L139: const proposalVisible = ref(false); L140: const saving = ref(false); L141: const savingMilestone = ref(false); L142: const planning = ref(false); L143: const coachLoading = ref(false); L144: const coachQuestion = ref(''); L145: const coachAnswer = ref(null); L146: const approving = ref(false); L147: const editingId = ref(null); L148: const selectedGoal = ref(null); L149: const milestones = ref([]); L150: const linkedTasks = ref([]); L151: const history = ref([]); L152: const linkedProjects = ref([]); L153: const learningGoalOptions = ref([]); L154: const noteText = ref(''); L155: const proposal = ref(null); L156: const planInstructions = ref(''); L157: const form = reactive({ title: '', description: '', category: 'personal', priority: 'medium', status: 'active', start_date: new Date().toISOString().slice(0, 10), target_date: '', estimated_minutes: 0, measurement_unit: '', initial_value: null, current_value: null, target_value: null, progress_percent: 0, learning_goals: [] })
- Imports (first five): import { computed, onMounted, reactive, ref, watch } from 'vue'; import { useGoalsStore } from '@/stores/goals/goalsStore'; import { useAppToast } from '@/composables/useAppToast'; import * as goalApi from '@/services/Goals/goals'; import { createTask, listTasks } from '@/services/Tasks/tasks'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Goals/goals.js
- Type: .js
- Declarations: L4: const unwrap = (data) => (Array.isArray(data) ? data : data?.results || []); L6: export const listGoalsPage = async (params = {}) => (await api.get(endpoints.goals.list, { params })).data; L7: export const listGoals = async (params = {}) => unwrap(await listGoalsPage(params)); L8: export const getGoal = async (id) => (await api.get(endpoints.goals.detail(id))).data; L9: export const getGoalAnalytics = async () => (await api.get(endpoints.goals.analytics)).data; L10: export const createGoal = async (payload) => (await api.post(endpoints.goals.list, payload)).data; L11: export const updateGoal = async (id, payload) => (await api.patch(endpoints.goals.detail(id), payload)).data; L12: export const deleteGoal = async (id) => { await api.delete(endpoints.goals.detail(id)); return true }; L13: export const completeGoal = async (id, notes = '') => (await api.post(endpoints.goals.complete(id), { notes })).data; L14: export const pauseGoal = async (id) => (await api.post(endpoints.goals.pause(id))).data; L15: export const resumeGoal = async (id) => (await api.post(endpoints.goals.resume(id))).data; L16: export const archiveGoal = async (id) => (await api.post(endpoints.goals.archive(id))).data; L17: export const duplicateGoal = async (id) => (await api.post(endpoints.goals.duplicate(id))).data; L18: export const updateGoalProgress = async (id, progress_percent) => (await api.post(endpoints.goals.progress(id), { progress_percent })).data; L19: export const getGoalHistory = async (id) => unwrap((await api.get(endpoints.goals.history(id))).data); L20: export const getGoalRisk = async (id) => (await api.get(endpoints.goals.risk(id))).data; L21: export const generateGoalPlan = async (id, instructions = '') => (await api.post(endpoints.goals.plan(id), { instructions })).data; L22: export const askGoalCoach = async (id, message) => (await api.post(endpoints.goals.coach(id), { message })).data; L23: export const getGoalPlans = async (id) => unwrap((await api.get(endpoints.goals.plans(id))).data); L24: export const approveGoalPlan = async (id, proposal_id) => (await api.post(endpoints.goals.approvePlan(id), { proposal_id })).data; L25: export const rejectGoalPlan = async (id, proposal_id) => (await api.post(endpoints.goals.rejectPlan(id), { proposal_id })).data; L26: export const listGoalMilestones = async (goal) => unwrap((await api.get(endpoints.goals.milestones, { params: goal ? { goal } : {} })).data); L27: export const createGoalMilestone = async (payload) => (await api.post(endpoints.goals.milestones, payload)).data; L28: export const updateGoalMilestone = async (id, payload) => (await api.patch(endpoints.goals.milestone(id), payload)).data; L29: export const deleteGoalMilestone = async (id) => { await api.delete(endpoints.goals.milestone(id)); return true }; L30: export const listGoalProjects = async (id) => unwrap((await api.get(endpoints.goals.projects(id))).data); L31: export const linkGoalProject = async (id, project_id) => (await api.post(endpoints.goals.projects(id), { project_id })).data; L32: export const addGoalNote = async (id, note) => (await api.post(endpoints.goals.notes(id), { note })).data; L33: export const reorderGoalMilestones = async (id, milestone_ids) => (await api.post(endpoints.goals.reorderMilestones(id), { milestone_ids })).data
- Imports (first five): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/goals/goalsStore.js
- Type: .js
- Declarations: L5: export const useGoalsStore = defineStore('goals', () => {; L6: const items = ref([]); L7: const analytics = ref(null); L8: const count = ref(0); L9: const next = ref(null); L10: const previous = ref(null); L11: const loading = ref(false); L12: const analyticsLoading = ref(false); L13: const error = ref(null); L15: async function fetchGoals(params = {}) {; L19: const pageData = await goalApi.listGoalsPage(params); L33: async function fetchAnalytics() {; L43: async function refresh() {
- Imports (first five): import { defineStore } from 'pinia'; import { ref } from 'vue'; import * as goalApi from '@/services/Goals/goals'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/goals/GoalCard.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/goals/GoalStats.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/goals/GoalsToolbar.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.

