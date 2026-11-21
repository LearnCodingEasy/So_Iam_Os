# core source-file catalog

Files associated with this domain's view/service/store/component directories are listed. Imports and declaration names are static excerpts; global callers are not exhaustive.


## views/core/DashboardView.vue
- Type: .vue
- Declarations: L388: const isOnline = useOnline(); L390: const isDark = useDark(); L393: const dashboard = ref(null); L394: const loading = ref(true); L395: const error = ref(null); L397: const loadDashboard = async () => {; L401: const data = await dashboardService.get(); L420: const selectedRange = ref('Ø´Ù‡Ø±ÙŠ'); L421: const isModalOpen = ref(false); L423: const newItemForm = ref({; L428: const serviceOptions = [; L436: const userName = computed(() => dashboard.value?.user?.name || 'Ù…. Ø­Ø³Ø§Ù… Ø±Ø´Ø§Ø¯ Ø¹Ø¨ÙˆØ¯'); L437: const learningStats = computed(() => dashboard.value?.stats?.learning || {}); L438: const recentKnowledge = computed(() => dashboard.value?.recent?.knowledge || []); L439: const tasks = computed(() => dashboard.value?.recent?.tasks || dashboard.value?.tasks || []); L441: const statsList = computed(() => {; L442: const data = dashboard.value?.stats || {}; L480: const lineChartData = computed(() => {; L481: const isDarkTheme = isDark.value; L482: const taskStats = dashboard.value?.stats?.tasks || {}; L483: const total = taskStats.total || 10; L484: const completed = taskStats.completed || 5; L485: const pending = taskStats.pending || 5; L521: const lineChartOptions = computed(() => ({; L559: const refreshDashboard = async () => {; L565: const exportReport = () => {; L571: const openNewItemModal = () => {; L575: const submitNewItem = () => {
- Imports (first five): import { ref, computed, onMounted } from 'vue'; import { RouterLink } from 'vue-router'; import { useOnline, useDark } from '@vueuse/core'; import { toast } from 'vue-sonner'; import { dashboardService } from '@/services/Core/dashboard'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/core/MyProgress.vue
- Type: .vue
- Declarations: L8: const toast = useAppToast(); L9: const summary=ref({overall_progress:0,topics_total:0,topics_completed:0,goals:[]}),loading=ref(true),error=ref(''); L10: async function load(){loading.value=true;error.value='';try{summary.value=(await api.get('/learning/progress/summary/')).data}catch(e){error.value = getApiErrorMessage(e, 'ØªØ¹Ø°Ø± ØªØ­Ù…ÙŠÙ„ Ø§Ù„ØªÙ‚Ø¯Ù….')}finally { loading.value = false }}
- Imports (first five): import { onMounted, ref } from 'vue'; import { useAppToast } from '@/composables/useAppToast'; import { getApiErrorMessage } from '@/utils/apiError'; import api from '@/services/Shared/api'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/core/Settings.vue
- Type: .vue
- Declarations: L145: const providers = ['ollama', 'openai', 'openrouter'],; L169: async function load() {; L173: const g = await api.get('/learning/goals/'); L182: async function loadModels() {; L185: const r = await getProviderModels(settings.preferred_provider); L194: async function save() {; L204: async function saveLearning() {; L214: async function addCredential() {; L224: async function removeCredential(p) {; L232: async function createPrompt() {; L243: async function deletePromptProfile(id) {
- Imports (first five): import { onMounted, reactive, ref, watch } from 'vue'; import api from '@/services/Shared/api'; import Button from 'primevue/button'; import Card from 'primevue/card'; import Select from 'primevue/select'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Core/dashboard.js
- Type: .js
- Declarations: L4: export const dashboardService = {; L6: const response = await api.get(endpoints.core.dashboard)
- Imports (first five): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Core/settings.js
- Type: .js
- Declarations: L2: export const getLearningSettings = async () => (await api.get('/core/learning-settings/')).data; L3: export const updateLearningSettings = async (payload) => (await api.patch('/core/learning-settings/', payload)).data
- Imports (first five): import api from '../Shared/api'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/accounts/user.js
- Type: .js
- Declarations: L9: const ACCESS_TOKEN_KEY = 'user.access'; L10: const REFRESH_TOKEN_KEY = 'user.refresh'; L11: const USER_KEY = 'user.info'; L16: const defaultUser = () => ({; L48: export const useUserStore = defineStore('user', {; L127: const accessToken = event.detail?.access; L128: const refreshToken = event.detail?.refresh; L140: const access = localStorage.getItem(ACCESS_TOKEN_KEY); L142: const refresh = localStorage.getItem(REFRESH_TOKEN_KEY); L144: const storedUser = localStorage.getItem(USER_KEY); L172: const parsedUser = JSON.parse(storedUser); L199: const response = await api.get('/users/me/'); L210: const hasStoredSession = Boolean(; L309: const refresh = this.user.refresh || localStorage.getItem(REFRESH_TOKEN_KEY); L316: const response = await api.post('/users/refresh/', {; L320: const newAccess = response.data?.access; L321: const newRefresh = response.data?.refresh || refresh
- Imports (first five): import { defineStore } from 'pinia'; import api from '@/services/Shared/api'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/ai/useAIStore.js
- Type: .js
- Declarations: L5: const asArray = (value) => Array.isArray(value) ? value : value?.results || []; L7: export const useAIStore = defineStore('ai-management', () => {; L8: const providers = ref([]); L9: const credentials = ref([]); L10: const settings = ref(null); L11: const conversations = ref([]); L12: const executions = ref([]); L13: const usage = ref({}); L14: const budgets = ref([]); L15: const audit = ref([]); L16: const workflows = ref([]); L17: const health = ref(null); L18: const capabilities = ref([]); L19: const loading = ref(false); L20: const error = ref(null); L22: const beginLoad = () => { activeLoads += 1; loading.value = true }; L23: const endLoad = () => { activeLoads = Math.max(0, activeLoads - 1); loading.value = activeLoads > 0 }; L25: async function refreshControl() {; L45: async function refreshOperations() {; L65: async function refreshAll() {
- Imports (first five): import { defineStore } from 'pinia'; import { ref } from 'vue'; import aiControl from '@/services/AI/aiControl'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/automation/useProgramElementStore.js
- Type: .js
- Declarations: L15: export const useProgramElementStore = defineStore('programElement', () => {; L19: const elements = ref([]); L20: const currentElement = ref(null); L21: const isLoading = ref(false); L23: const form = ref({; L42: const SELECTOR_TYPES = [; L52: const currentElementId = computed(() => currentElement.value?.id ?? null); L54: const elementById = (id) => elements.value.find((e) => e.id === id) ?? null; L57: const elementsByProgram = (programId) => elements.value.filter((e) => e.program === programId); L62: function validateForm(f = form.value) {; L69: function validateImageSize(file, maxMB = 5) {; L79: function buildFormData(f = form.value) {; L80: const fd = new FormData(); L97: function resetForm(defaultProgramId = null) {; L115: function fillFormFromData(data) {; L133: function onImageChange(event) {; L134: const file = event.target?.files?.[0]; L136: const sizeErr = validateImageSize(file); L150: async function loadElements() {; L161: async function loadElement(id) {; L169: async function selectElement(id) {; L175: async function createElement() {; L176: const response = await automationService.createProgramElement(buildFormData()); L177: const data = response.data; L184: async function updateElement(id) {; L185: const response = await automationService.updateProgramElement(id, buildFormData()); L186: const data = response.data; L187: const idx = elements.value.findIndex((e) => e.id === id); L194: async function deleteElement(id) {; L195: const response = await automationService.deleteProgramElement(id)
- Imports (first five): import { defineStore } from 'pinia'; import { ref, computed } from 'vue'; import automationService from '@/services/Automation/AutomationService'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/automation/useProgramStore.js
- Type: .js
- Declarations: L15: export const useProgramStore = defineStore('program', () => {; L19: const programs = ref([]); L20: const currentProgram = ref(null); L21: const isLoading = ref(false); L22: const isScanning = ref(false); L24: const form = ref({; L37: const currentProgramId = computed(() => currentProgram.value?.id ?? null); L39: const programById = (id) => programs.value.find((p) => p.id === id) ?? null; L44: function validateForm(f = form.value) {; L50: function validateImageSize(file, maxMB = 5) {; L60: function buildFormData(f = form.value) {; L61: const fd = new FormData(); L72: function resetForm() {; L84: function fillFormFromData(data) {; L96: function onImageChange(event) {; L97: const file = event.target?.files?.[0]; L99: const sizeErr = validateImageSize(file); L113: async function loadPrograms() {; L124: async function loadProgram(id) {; L132: async function selectProgram(id) {; L137: async function createProgram() {; L138: const response = await automationService.createProgram(buildFormData()); L139: const data = response.data; L147: async function updateProgram(id) {; L148: const response = await automationService.updateProgram(id, buildFormData()); L149: const data = response.data; L150: const idx = programs.value.findIndex((p) => p.id === id); L157: async function deleteProgram(id) {; L158: const response = await automationService.deleteProgram(id); L170: async function openProgram(id) {
- Imports (first five): import { defineStore } from 'pinia'; import { ref, computed } from 'vue'; import automationService from '@/services/Automation/AutomationService'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/automation/useTaskStore.js
- Type: .js
- Declarations: L16: export const useTaskStore = defineStore('task', () => {; L20: const tasks = ref([]); L21: const currentTask = ref(null); L23: const currentTaskRunId = ref(null); L24: const isLoading = ref(false); L26: const form = ref({; L35: const currentTaskId = computed(() => currentTask.value?.id ?? null); L37: const taskById = (id) => tasks.value.find((t) => t.id === id) ?? null; L40: const tasksByProgram = (programId) => tasks.value.filter((t) => t.program === programId); L45: function validateForm(f = form.value) {; L54: function buildFormData(f = form.value) {; L55: const fd = new FormData(); L62: function resetForm() {; L66: function fillFormFromData(data) {; L79: async function loadTasks() {; L90: async function loadTask(id) {; L98: async function selectTask(id) {; L104: async function createTask() {; L105: const response = await automationService.createTask(buildFormData()); L106: const data = response.data; L115: async function updateTask(id) {; L116: const response = await automationService.updateTask(id, buildFormData()); L117: const data = response.data; L118: const idx = tasks.value.findIndex((t) => t.id === id); L126: async function deleteTask(id) {; L127: const response = await automationService.deleteTask(id); L141: function setTaskRunId(runId) {; L145: function clearTaskRunId() {
- Imports (first five): import { defineStore } from 'pinia'; import { ref, computed } from 'vue'; import automationService from '@/services/Automation/AutomationService'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/automation/useWorkflowStore.js
- Type: .js
- Declarations: L18: export const useWorkflowStore = defineStore('workflow', () => {; L22: const workflows = ref([]); L23: const currentWorkflow = ref(null); L24: const nodes = ref([]); L25: const edges = ref([]); L27: const isLoading = ref(false); L28: const isSaving = ref(false); L29: const isInitialized = ref(false); L31: const formWorkflow = ref({ name: '', description: '', status: 'draft' }); L36: const currentWorkflowId = computed(() => currentWorkflow.value?.id ?? null); L38: const workflowById = (id) => workflows.value.find((w) => w.id === id) ?? null; L43: function mapNode(n) {; L70: function mapEdge(e) {; L83: async function loadWorkflows() {; L96: async function loadWorkflowEvents(workflowId) {; L124: async function selectWorkflow(id) {; L138: async function createWorkflow(payload) {; L151: async function updateWorkflow(id, payload) {; L153: const idx = workflows.value.findIndex((w) => w.id === id); L163: async function deleteWorkflow(id) {; L181: async function saveWorkflow({ selectedNode = null, showActionPanel = false } = {}) {; L185: const exists = workflows.value.find((w) => w.id === currentWorkflowId.value); L193: const openNodeLabel = showActionPanel ? (selectedNode?.data?.node?.label ?? null) : null; L196: const payload = {; L216: const refreshed = nodes.value.find((n) => n.data?.node?.label === openNodeLabel); L228: const debouncedAutoSave = debounce(function (opts) {; L235: function triggerAutoSave(opts = {}) {; L239: function cancelAutoSave() {; L246: function clearCanvas() {; L254: function autoLayout(direction = 'TB') {
- Imports (first five): import { defineStore } from 'pinia'; import { ref, computed } from 'vue'; import { debounce } from 'lodash'; import dagre from 'dagre'; import automationService from '@/services/Automation/AutomationService'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/codex/codex.js
- Type: .js
- Declarations: L4: export const useCodexStore = defineStore('codex', {; L83: const result = await codex.bootstrap(); L106: const result = await codex.registry.bootstrap(); L111: const result = await codex.scan()
- Imports (first five): import { defineStore } from 'pinia'; import codex from '@/services/Codex/codex'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/goals/goalsStore.js
- Type: .js
- Declarations: L5: export const useGoalsStore = defineStore('goals', () => {; L6: const items = ref([]); L7: const analytics = ref(null); L8: const count = ref(0); L9: const next = ref(null); L10: const previous = ref(null); L11: const loading = ref(false); L12: const analyticsLoading = ref(false); L13: const error = ref(null); L15: async function fetchGoals(params = {}) {; L19: const pageData = await goalApi.listGoalsPage(params); L33: async function fetchAnalytics() {; L43: async function refresh() {
- Imports (first five): import { defineStore } from 'pinia'; import { ref } from 'vue'; import * as goalApi from '@/services/Goals/goals'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/knowledge/knowledgeStore.js
- Type: .js
- Declarations: L5: function unwrapList(payload) {; L13: function splitFiles(data = {}) {; L15: const pending = Array.isArray(files) ? files.filter((f) => typeof File !== 'undefined' && f instanceof File) : []; L19: export const useKnowledgeStore = defineStore('knowledge', () => {; L20: const items = ref([]); L21: const count = ref(0); L22: const next = ref(null); L23: const previous = ref(null); L24: const filesByKnowledgeId = ref({}); L25: const loading = ref(false); L26: const saving = ref(false); L27: const error = ref(null); L29: const lastUploadReport = ref({ uploaded: [], failed: [] }); L31: async function uploadPending(knowledgeId, pending) {; L32: const report = { uploaded: [], failed: [] }; L36: const saved = await uploadFile(knowledgeId, file); L39: const data = cause?.response?.data; L40: const message = data?.file?.[0] || data?.file || data?.detail || cause?.message || 'Upload failed'; L48: async function fetchItems(params = {}) {; L52: const payload = await knowledgeService.getAll(params); L66: async function fetchItem(id) {; L70: async function createItem(data) {; L75: const created = await knowledgeService.create(payload); L88: async function updateItem(id, data) {; L93: const updated = await knowledgeService.update(id, payload); L105: async function archiveItem(id) {; L106: const archived = await knowledgeService.archive(id); L112: async function restoreItem(id) {; L113: const restored = await knowledgeService.restore(id); L119: async function deleteItem(id) {
- Imports (first five): import { defineStore } from 'pinia'; import { ref } from 'vue'; import { knowledgeService } from '@/services/Knowledge/Knowledge'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/projects/projects.js
- Type: .js
- Declarations: L5: export const useProjectsStore = defineStore('projects', () => {; L6: const items = ref([]); L7: const count = ref(0); L8: const next = ref(null); L9: const previous = ref(null); L10: const loading = ref(false); L11: const saving = ref(false); L12: const error = ref(null); L14: async function fetchProjects(params = {}) {; L18: const page = await projectsApi.listProjectsPage(params); L32: async function getProject(id) {; L36: async function createProject(payload) {; L39: const item = await projectsApi.createProject(payload); L46: async function updateProject(id, payload) {; L49: const item = await projectsApi.updateProject(id, payload); L55: async function deleteProject(id) {
- Imports (first five): import { defineStore } from 'pinia'; import { ref } from 'vue'; import * as projectsApi from '@/services/Projects/projects'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/shared/counter.js
- Type: .js
- Declarations: L4: export const useCounterStore = defineStore('counter', () => {; L5: const count = ref(0); L6: const doubleCount = computed(() => count.value * 2); L7: function increment() {
- Imports (first five): import { ref, computed } from 'vue'; import { defineStore } from 'pinia'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/shared/primeTheme.js
- Type: .js
- Declarations: L4: const _appState = reactive({ theme: 'Aura', darkTheme: false })
- Imports (first five): import { reactive } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/core/FrontendEnhancementCenter.vue
- Type: .vue
- Declarations: L116: const isDark = useDark({ selector: 'html', attribute: 'class', valueDark: 'p-dark', valueLight: '' }); L117: const prefersReducedMotion = computed(() => usePreferredReducedMotion().value === 'reduce'); L119: const query = useQuery({; L122: const response = await api.get('/ai/health/'); L129: const editor = useEditor({; L134: const cards = ref([; L141: const activity = Array.from({ length: 250 }, (_, index) => ({; L146: const fileInput = ref(null); L164: function toggleLocale() {; L169: function notify() {
- Imports (first five): import { computed, onBeforeUnmount, onMounted, ref } from 'vue'; import { useI18n } from 'vue-i18n'; import { useDark, usePreferredReducedMotion } from '@vueuse/core'; import { useQuery } from '@tanstack/vue-query'; import { EditorContent, useEditor } from '@tiptap/vue-3'
- Consumers: direct route/import references are listed where identified; no full call graph.

