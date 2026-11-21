# automation source-file catalog

Files associated with this domain's view/service/store/component directories are listed. Imports and declaration names are static excerpts; global callers are not exhaustive.


## views/automation/AutomationView.vue
- Type: .vue
- Declarations: L56: const toast = useToast(); L57: const confirm = useConfirm(); L59: const tracker = useApiTracker(); L60: const programStore = useProgramStore(); L61: const elementStore = useProgramElementStore(); L62: const workflowStore = useWorkflowStore(); L63: const taskStore = useTaskStore(); L69: function useAsyncAction() {; L70: const loading = ref(false); L71: const run = async (apiFn, options = {}) => {; L83: const validErr = validate(); L97: const result = await tracker.execute({ serviceFn: apiFn }); L108: const status = err?.response?.status; L109: const body = err?.response?.data; L134: const programAction = useAsyncAction(); L135: const elementAction = useAsyncAction(); L136: const workflowAction = useAsyncAction(); L137: const taskAction = useAsyncAction(); L138: const nodeAction = useAsyncAction(); L145: const createProgramVisible = ref(false); L146: const editProgramVisible = ref(false); L147: const createProgramElementVisible = ref(false); L148: const editProgramElementVisible = ref(false); L149: const createTaskVisible = ref(false); L150: const editTaskVisible = ref(false); L151: const showVersions = ref(false); L152: const showRealtimeGraph = ref(false); L155: const showActionPanel = ref(false); L156: const newActionTypeForPanel = ref('open_program'); L157: const selectedNode = ref(null)
- Imports (first five): import { ref, reactive, watch, onMounted, onUnmounted } from 'vue'; import { useVueFlow } from '@vue-flow/core'; import { debounce } from 'lodash'; import { useToast } from 'primevue/usetoast'; import { useConfirm } from 'primevue/useconfirm'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/automation/DashboardAutomationView.vue
- Type: .vue
- Declarations: L24: const tasks = ref([]); L25: const load = async () => {; L26: const res = await taskService.list(); L30: const run = async (id) => {; L31: const res = await taskService.run(id)
- Imports (first five): import { ref, onMounted } from 'vue'; import taskService from '../../services/Automation/taskService'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/automation/icon.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/automation/ProgramCreate.vue
- Type: .vue
- Declarations: L136: const form = ref({; L161: const onImageChange = (e) => {; L183: const createProgram = async () => {; L185: const formData = new FormData(); L223: const res = await programService.createProgram(formData)
- Imports (first five): import { ref } from 'vue'; import programService from '@/services/Automation/AutomationService'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/automation/ProgramEdit.vue
- Type: .vue
- Declarations: L139: const route = useRoute(); L145: const currentId = ref(null); L150: const form = ref({; L175: const onImageChange = (e) => {; L197: const createProgram = async () => {; L199: const formData = new FormData(); L237: const res = await programService.createProgram(formData); L249: const getExplain = async () => {; L252: const res = await programService.get(currentId.value)
- Imports (first five): import { ref, onMounted } from 'vue'; import { useRoute } from 'vue-router'; import programService from '@/services/Automation/AutomationService'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/automation/ProgramList.vue
- Type: .vue
- Declarations: L21: const programs = ref([]); L22: const load = async () => {; L23: const res = await programService.list(); L26: const open = async (id) => {
- Imports (first five): import { ref, onMounted } from 'vue'; import programService from '../../services/Automation/AutomationService'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/automation/TaskCreate.vue
- Type: .vue
- Declarations: L27: const programs = ref([]); L28: const name = ref(''); L29: const programId = ref(''); L30: const actionsJson = ref('[]'); L33: const r = await api.get('automation/programs/'); L37: const create = async () => {; L44: const payload = {; L50: const res = await api.post('automation/tasks/', payload); L51: const taskId = res.data.id; L54: const actions = JSON.parse(actionsJson.value || '[]')
- Imports (first five): import { ref, onMounted } from 'vue'; import api from '../../services/Shared/api'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/automation/TaskEditor.vue
- Type: .vue
- Declarations: L22: const route = useRoute(); L23: const taskId = route.params.id; L24: const task = ref(null); L25: const actions = ref([]); L26: const runs = ref([]); L28: const load = async ()=>{; L29: const t = await api.get(`/tasks/${taskId}/`); L31: const a = await api.get(`/tasks/${taskId}/actions/`); L33: const tr = await api.get(`/taskruns/?task=${taskId}`); L36: const runTask = async ()=>{; L37: const res = await api.post(`/tasks/${taskId}/run/`); L45: const pollLogs = async (run_id) => {; L46: const interval = setInterval(async ()=>{; L47: const r = await api.get(`/taskruns/${run_id}/logs/`)
- Imports (first five): import { ref, onMounted } from 'vue'; import api from '../../services/Shared/api'; import { useRoute } from 'vue-router'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Automation/AutomationService.js
- Type: .js
- Declarations: L60: const q = programId ? `?program=${programId}` : ''; L121: const q = workflowId ? `?workflow=${workflowId}` : ''; L152: const q = workflowId ? `?workflow=${workflowId}` : ''; L172: const q = nodeId ? `?node=${nodeId}` : ''; L233: const q = taskRunId ? `?task_run=${taskRunId}` : ''
- Imports (first five): import api from '../Shared/api'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Automation/nodeStorageService.js
- Type: .js
- Declarations: L3: const STORAGE_KEY = 'vueflow_graph'; L10: function read() {; L11: const raw = localStorage.getItem(STORAGE_KEY); L16: const parsed = JSON.parse(raw); L27: function write(graph) {; L36: export function getGraph() {; L41: export function getOne(id) {; L42: const graph = read(); L46: export function getEdge(id) {; L47: const graph = read(); L51: export function createNode(node) {; L52: const graph = read(); L58: export function updateNode(id, newData) {; L59: const graph = read(); L60: const index = graph.nodes.findIndex((n) => n.id === id); L71: export function removeNode(id) {; L72: const graph = read(); L78: export function removeEdge(id) {; L79: const graph = read(); L85: export function saveGraph(nodes, edges) {
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Automation/taskService.js
- Type: .js
- Declarations: none matched
- Imports (first five): import api from '../Shared/api'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Automation/workflowService.js
- Type: .js
- Declarations: none matched
- Imports (first five): import api from '../Shared/api'
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


## components/automation/AIPrompt.vue
- Type: .vue
- Declarations: L6: const prompt = ref(''); L7: const result = ref(null); L8: const loading = ref(false); L9: const error = ref(''); L11: async function runPrompt() {; L17: const response = await api.post(endpoints.ai.agentPlan, { request: prompt.value.trim() })
- Imports (first five): import { ref } from 'vue'; import api from '@/services/Shared/api'; import { endpoints } from '@/services/Shared/endpoints'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/ApiFlowPanel.vue
- Type: .vue
- Declarations: L102: const props = defineProps({; L110: const openIdx = ref(null); L112: function toggleDetail(i) {; L116: function getConnectorClass(i) {; L117: const cur = props.stages[i]?.status; L119: const next = props.stages[i + 1]?.status; L126: const overallClass = computed(() => {; L127: const hasFail = props.stages.some((s) => s.status === 'fail'); L128: const hasActive = props.stages.some((s) => s.status === 'active'); L129: const allDone = props.stages.find((s) => s.id === 'done')?.status === 'pass'; L136: const overallLabel = computed(() => {; L137: const hasFail = props.stages.some((s) => s.status === 'fail'); L138: const hasActive = props.stages.some((s) => s.status === 'active'); L139: const allDone = props.stages.find((s) => s.id === 'done')?.status === 'pass'; L146: const statusChipClass = computed(() => {; L147: const s = props.meta?.status
- Imports (first five): import { ref, computed } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/ProgramsView.vue
- Type: .vue
- Declarations: L216: const toast = useToast(); L218: const confirm = useConfirm(); L221: const emit = defineEmits(['program-selected']); L223: const selectProgram = async (id) => {; L234: const programs = ref([]); L235: const loadingPrograms = ref(false); L236: const currentProgramId = ref(null); L237: const ceateProgramVisible = ref(false); L238: const editProgramVisible = ref(false); L239: const formProgram = ref({; L260: const loadPrograms = async () => {; L274: const loadProgram = async (id) => {; L290: const onImageChangeProgram = (e) => {; L293: const createProgram = async () => {; L296: const formData = new FormData(); L330: const openEditProgram = async (id) => {; L348: const editProgram = async () => {; L351: const formData = new FormData(); L385: const confirmDeleteProgram = (program) => {; L409: const deleteProgram = async (id) => {; L440: const openProgram = async (programId) => {; L444: const closeProgram = async (programId) => {; L448: const statusProgram = async (programId) => {; L453: const focusProgram = async (programId) => {; L474: const maximizeProgram = async (programId) => {
- Imports (first five): import { ref,  } from 'vue'; import automationService from '@/services/Automation/AutomationService'; import { useToast } from 'primevue/usetoast'; import { useConfirm } from 'primevue/useconfirm'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Action/ActionPanel.vue
- Type: .vue
- Declarations: L6: const props = defineProps({; L12: const emit = defineEmits([; L23: const actionOptions = [; L36: const getNodeId = () => props.selectedNode?.data?.node?.backend_id ?? props.selectedNode?.id; L256: const props = defineProps({; L262: const emit = defineEmits([; L273: const nodeType = computed(() => props.selectedNode?.data?.node?.node_type?.toLowerCase() ?? ''); L274: const isProgramNode = computed(() => nodeType.value === 'program'); L275: const isProgramElementNode = computed(() => nodeType.value === 'program-element'); L276: const isDelayNode = computed(() => ['delay', 'timing', 'wait'].includes(nodeType.value)); L281: const ACTION_OPTIONS = {; L311: const currentOptions = computed(() => {; L312: const key = nodeType.value; L319: const nodeData = computed(() => props.selectedNode?.data ?? {}); L320: const node = computed(() => nodeData.value.node ?? {}); L321: const actions = computed(() => nodeData.value.actions ?? []); L322: const elementMeta = computed(() => {; L323: const n = node.value; L337: const getNodeId = () => node.value.backend_id ?? props.selectedNode?.id; L340: const stabilityPercent = computed(() => Math.round((elementMeta.value.stability_score ?? 1) * 100)); L341: const stabilityColor = computed(() => {; L342: const s = elementMeta.value.stability_score ?? 1; L351: const PAYLOAD_NEEDS_TEXT = ['typing', 'keyboard_shortcut', 'hotkey']; L352: const PAYLOAD_NEEDS_SECONDS = ['wait']; L354: const actionNeedsText = (type) => PAYLOAD_NEEDS_TEXT.includes(type); L355: const actionNeedsSeconds = (type) => PAYLOAD_NEEDS_SECONDS.includes(type)
- Imports (first five): import { computed } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Edge/CustomEdge.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import { Handle, Position } from '@vue-flow/core'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Execution/LiveConsole.vue
- Type: .vue
- Declarations: L25: const props = defineProps({; L33: const emit = defineEmits(['close', 'done', 'error']); L36: const logs = ref([]); L37: const status = ref('connecting') // connecting | running | success | failed | closed; L38: const ws = ref(null); L39: const consoleEl = ref(null); L40: const isMinimized = ref(false); L44: const connect = () => {; L47: const url = `${props.wsBaseUrl}/ws/workflow/${props.taskRunId}/`; L63: const msg = JSON.parse(data); L83: const handleMessage = (msg) => {; L108: const addLog = (level, message, nodeId = null) => {; L133: const closeConsole = () => {; L139: const clearLogs = () => {; L144: const levelClass = (level) =>; L153: const statusLabel = {
- Imports (first five): import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Execution/RealtimeGraph.vue
- Type: .vue
- Declarations: L22: const props = defineProps({; L29: const emit = defineEmits(['close', 'update:visible']); L33: const nodeStats = ref(new Map()) // node_id â†’ { label, status, duration_ms }; L34: const startTime = ref(null); L35: const elapsed = ref(0); L40: const totalNodes = computed(() => props.nodes.length); L41: const executedCount = computed(; L44: const successCount = computed(; L47: const failedCount = computed(; L50: const successRate = computed(() => {; L51: const done = successCount.value + failedCount.value; L55: const progressPercent = computed(() =>; L59: const elapsedFormatted = computed(() => {; L60: const s = Math.floor(elapsed.value / 1000); L61: const ms = elapsed.value % 1000; L66: const barData = computed(() => {; L68: const stat = nodeStats.value.get(n.id) ?? { status: 'idle', duration_ms: 0 }; L78: const maxDuration = computed(() => {; L79: const max = Math.max(...barData.value.map((b) => b.duration_ms), 1); L83: const barColor = (status) =>; L92: const connect = () => {; L106: const msg = JSON.parse(data); L108: const existing = nodeStats.value.get(msg.node_id) ?? {}; L116: const started = existing.startedAt ?? Date.now(); L117: const duration_ms = Date.now() - started
- Imports (first five): import { ref, computed, watch, onBeforeUnmount } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Node/CustomNode.vue
- Type: .vue
- Declarations: L44: const localAction = ref(props.data?.action?.action_type ?? 'open_program') // âš™ Ù†ÙˆØ¹ Ø§Ù„Ø£ÙƒØ´Ù†; L46: const localDelay = ref(props.data?.config?.delay ?? 0) // â± Ù‚ÙŠÙ…Ø© Ø§Ù„ØªØ£Ø®ÙŠØ±; L48: const localTypingText = ref(props.data?.config?.text ?? '') // âŒ¨ Ø§Ù„Ù†Øµ Ø§Ù„Ù…ÙƒØªÙˆØ¨; L59: const nodeTypeClass = computed(() => {; L60: const type = node.value.node_type?.toLowerCase(); L74: const dynamicIcon = computed(() => {; L75: const type = node.value.node_type; L89: const isProgramNode = computed(() => node.value.node_type?.toLowerCase() === 'program'); L96: const isProgramElementNode = computed(; L105: const isDelayNode = computed(() => {; L106: const type = node.value.node_type?.toLowerCase(); L116: const actionColor = computed(() => {; L149: const isRunningAction = computed(() =>; L158: const statusClass = computed(() => ({; L183: const updateAction = () => {; L184: const payload = {; L201: const updateTypingAction = () => {; L213: const updateDelay = () => {; L460: const props = defineProps({; L464: const emit = defineEmits([; L479: const data = computed(() => props.data ?? {}); L480: const node = computed(() => data.value.node ?? {}); L481: const config = computed(() => node.value.config ?? {}); L482: const actions = computed(() => data.value.actions ?? []); L485: const primaryAction = computed(() => actions.value?.[0] ?? null); L491: const nodeType = computed(() => node.value.node_type?.toLowerCase() ?? ''); L493: const isProgramNode = computed(() => nodeType.value === 'program'); L494: const isProgramElementNode = computed(() => nodeType.value === 'program-element'); L495: const isDelayNode = computed(() => ['delay', 'timing', 'wait'].includes(nodeType.value)); L496: const isTypingNode = computed(() => nodeType.value === 'typing')
- Imports (first five): import { ref, watch, computed } from 'vue'; import { Handle, Position } from '@vue-flow/core'; import { ref, watch, computed } from 'vue'; import { Handle, Position } from '@vue-flow/core'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Node/NodeMarketplace.vue
- Type: .vue
- Declarations: L30: const props = defineProps({; L41: const emit = defineEmits([; L57: const activeTab = ref(0) // 0=Programs, 1=Elements, 2=Plugins, 3=Tasks, 4=Workflows; L58: const searchText = ref(''); L59: const activeCategory = ref('all') // all | programs | input | timing | ai; L62: const allPlugins = computed(() => registry.getMarketplaceItems()); L64: const filteredPlugins = computed(() => {; L70: const q = searchText.value.toLowerCase(); L82: const filteredPrograms = computed(() => {; L84: const q = searchText.value.toLowerCase(); L88: const filteredElements = computed(() => {; L90: const q = searchText.value.toLowerCase(); L95: const draggingId = ref(null); L97: const onDragStart = (type, id) => {; L102: const onDragEnd = () => {; L106: const onPluginDragStart = (plugin) => {; L112: const categories = computed(() => [; L122: const tabs = [
- Imports (first five): import { ref, computed } from 'vue'; import registry, { PLUGIN_CATEGORIES } from '@/plugins/PluginRegistry'; import NodePluginCard from './NodePluginCard.vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Node/NodePluginCard.vue
- Type: .vue
- Declarations: L20: const props = defineProps({; L32: const emit = defineEmits([; L37: const onDragStart = (e) => {
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Node/NodeVisualBuilder.vue
- Type: .vue
- Declarations: L24: const props = defineProps({; L29: const emit = defineEmits(['confirm', 'cancel', 'update:visible']); L32: const label = ref(''); L33: const customColor = ref(''); L34: const formData = ref({}); L35: const error = ref(null); L51: const nodeColor = computed(() => customColor.value || props.plugin?.color || '#334155'); L54: const handleConfirm = () => {; L57: const validErr = registry.validate(props.plugin.id, formData.value); L64: const payload = props.plugin ? registry.buildPayload(props.plugin.id, formData.value) : {}
- Imports (first five): import { ref, watch, computed } from 'vue'; import registry from '@/plugins/PluginRegistry'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/nodes/DelayNode.vue
- Type: .vue
- Declarations: L18: const props = defineProps(['id', 'data']); L21: const updateDelay = () => {; L22: const node = findNode(props.id)
- Imports (first five): import { useVueFlow } from '@vue-flow/core'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Program/CreateProgram.vue
- Type: .vue
- Declarations: L5: const props = defineProps({; L10: const emit = defineEmits(['update:visible', 'image-change', 'submit'])
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Program/EditProgram.vue
- Type: .vue
- Declarations: L4: const props = defineProps({; L9: const emit = defineEmits(['update:visible', 'save']); L11: const editProgramVisible = ref(false); L13: const formProgram = ref({; L40: const onImageChangeProgram = (e) => {; L44: const saveProgram = () => {
- Imports (first five): import { ref, watch } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Workflow/WorkflowCanvas.vue
- Type: .vue
- Declarations: L33: const props = defineProps({; L43: const emit = defineEmits([; L57: const nodeTypes = computed(() => ({ custom: CustomNode })); L58: const edgeTypes = computed(() => ({ custom: CustomEdge })); L61: const onNodeDragStop = ({ node }) => emit('node-drag-stop', node); L62: const onNodeClick = (event) => emit('node-click', event); L63: const onConnect = (params) => emit('connect', params); L64: const onDrop = (e) => emit('drop', e); L65: const onDragOver = (e) => {
- Imports (first five): import { computed } from 'vue'; import { VueFlow, Panel } from '@vue-flow/core'; import { Background } from '@vue-flow/background'; import { Controls } from '@vue-flow/controls'; import { MiniMap } from '@vue-flow/minimap'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Workflow/WorkflowToolbar.vue
- Type: .vue
- Declarations: L34: const emit = defineEmits([; L44: const layoutOptions = [; L52: const statusOptions = [
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/automation/Workflow/WorkflowVersions.vue
- Type: .vue
- Declarations: L26: const props = defineProps({; L31: const emit = defineEmits(['restore', 'close', 'update:visible']); L33: const toast = useToast(); L34: const versions = ref([]); L35: const loading = ref(false); L36: const restoring = ref(null) // id of version being restored; L46: const loadVersions = async () => {; L90: const restoreVersion = async (version) => {; L110: const formatDate = (iso) => {; L111: const d = new Date(iso)
- Imports (first five): import { ref, watch } from 'vue'; import automationService from '@/services/Automation/AutomationService'; import { useToast } from 'primevue/usetoast'
- Consumers: direct route/import references are listed where identified; no full call graph.

