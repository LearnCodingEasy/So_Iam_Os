# projects source-file catalog

Files associated with this domain's view/service/store/component directories are listed. Imports and declaration names are static excerpts; global callers are not exhaustive.


## views/projects/ProjectsView.vue
- Type: .vue
- Declarations: L135: const store = useProjectsStore(); L136: const toast = useToast(); L137: const search = ref(''); L138: const statusFilter = ref(null); L139: const sortBy = ref('-updated_at'); L140: const dialogVisible = ref(false); L141: const detailsVisible = ref(false); L142: const detailsLoading = ref(false); L143: const selectedProject = ref(null); L144: const editing = ref(null); L145: const deletingId = ref(null); L146: const formError = ref(''); L147: const form = reactive({ title: '', description: '', status: 'planning', repository_url: '', website_url: '', metadataJson: '{}' }); L148: const statusOptions = [; L153: const sortOptions = [; L157: const errorText = computed(() => store.error?.response?.data?.detail || store.error?.message || 'Unable to load projects.'); L158: const filteredProjects = computed(() => {; L159: const query = search.value.trim().toLowerCase(); L163: const key = sortBy.value.replace(/^-/, ''); L164: const direction = sortBy.value.startsWith('-') ? -1 : 1; L168: const load = () => store.fetchProjects({ ordering: sortBy.value, search: search.value || undefined, status: statusFilter.value || undefined }); L170: const resetForm = () => Object.assign(form, { title: '', description: '', status: 'planning', repository_url: '', website_url: '', metadataJson: '{}' }); L171: const openDetails = async (project) => {; L182: const openCreate = () => { editing.value = null; formError.value = ''; resetForm(); dialogVisible.value = true }; L183: const openEdit = (project) => {; L188: const save = async () => {; L195: const payload = { ...fields, metadata }; L205: const remove = async (project) => {; L215: const statusLabel = (value) => statusOptions.find(x => x.value === value)?.label || value || 'Unknown'; L216: const formatDate = (value) => value ? new Date(value).toLocaleDateString() : 'â€”'
- Imports (first five): import { computed, onMounted, reactive, ref, watch } from 'vue'; import { useProjectsStore } from '@/stores/projects/projects'; import Card from 'primevue/card'; import Button from 'primevue/button'; import Column from 'primevue/column'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Projects/projects.js
- Type: .js
- Declarations: L4: const unwrap = (payload) => (Array.isArray(payload) ? payload : payload?.results || []); L6: export const listProjectsPage = async (params = {}) =>; L8: export const listProjects = async (params = {}) => unwrap(await listProjectsPage(params)); L9: export const getProject = async (id) => (await api.get(`${domainEndpoints.projects}${id}/`)).data; L10: export const createProject = async (payload) =>; L12: export const updateProject = async (id, payload) =>; L14: export const deleteProject = async (id) => {
- Imports (first five): import api from '../Shared/api'; import { domainEndpoints } from '../Shared/endpoints'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/projects/projects.js
- Type: .js
- Declarations: L5: export const useProjectsStore = defineStore('projects', () => {; L6: const items = ref([]); L7: const count = ref(0); L8: const next = ref(null); L9: const previous = ref(null); L10: const loading = ref(false); L11: const saving = ref(false); L12: const error = ref(null); L14: async function fetchProjects(params = {}) {; L18: const page = await projectsApi.listProjectsPage(params); L32: async function getProject(id) {; L36: async function createProject(payload) {; L39: const item = await projectsApi.createProject(payload); L46: async function updateProject(id, payload) {; L49: const item = await projectsApi.updateProject(id, payload); L55: async function deleteProject(id) {
- Imports (first five): import { defineStore } from 'pinia'; import { ref } from 'vue'; import * as projectsApi from '@/services/Projects/projects'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/accounts/ImageCropperDialog.vue
- Type: .vue
- Declarations: L15: const props = defineProps({ file: { type: [File, Object], default: null }, aspectRatio: { type: Number, default: 1 } }); L16: const emit = defineEmits(['cropped', 'cancel']); L17: const visible = ref(false), previewUrl = ref(''), imageRef = ref(null), cropper = ref(null); L20: function crop() { const canvas = cropper.value?.getCroppedCanvas({ maxWidth: 1200, maxHeight: 1200 }); if (!canvas) return; canvas.toBlob((blob) => { if (!blob) return; emit('cropped', new File([blob], props.file?.name || 'cropped-image.jpg', { type: blob.type || 'image/jpeg' })); visible.value = false }, 'image/jpeg', 0.9) }; L21: function cleanup(emitCancel = true) { cropper.value?.destroy(); cropper.value = null; if (objectUrl) URL.revokeObjectURL(objectUrl); objectUrl = ''; previewUrl.value = ''; if (emitCancel && visible.value) emit('cancel') }
- Imports (first five): import { nextTick, onBeforeUnmount, ref, watch } from 'vue'; import Dialog from 'primevue/dialog'; import Button from 'primevue/button'; import Cropper from 'cropperjs'; import 'cropperjs/dist/cropper.css'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/accounts/LoginForm.vue
- Type: .vue
- Declarations: L63: const router = useRouter(); L64: const userStore = useUserStore(); L70: const loading = ref(false); L71: const error = ref(null); L73: const formLogin = ref({; L82: const submitFormLogin = async () => {; L88: const response = await usersAccountsAPI.login({; L97: const userResponse = await usersAccountsAPI.me(); L118: const loginWithGoogle = () => {; L126: const loginWithFacebook = () => {
- Imports (first five): import { ref } from 'vue'; import { useRouter } from 'vue-router'; import { usersAccountsAPI } from '@/services/Accounts/usersAccounts'; import { useUserStore } from '@/stores/accounts/user'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/accounts/SignupForm.vue
- Type: .vue
- Declarations: L102: const formSignup = ref({; L116: const day = ref(''); L117: const month = ref(''); L118: const year = ref(''); L124: const errorsSignup = ref([]); L125: const loading = ref(false); L131: const submitFormSignup = async () => {; L177: const response = await usersAccountsAPI.signup({; L219: const data = err.response.data
- Imports (first five): import { ref } from 'vue'; import { usersAccountsAPI } from '@/services/Accounts/usersAccounts'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/ai/AIActivityLog.vue
- Type: .vue
- Declarations: L21: const events = ref([]); L25: function addEvent(detail = {}) {; L26: const phase = detail.phase; L39: function formatTime(value) {
- Imports (first five): import { onBeforeUnmount, onMounted, ref } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/ai/AIChat.vue
- Type: .vue
- Declarations: L249: const HelpButton = defineComponent({; L263: const helpCopy = {; L280: const sidebarCollapsed = ref(false); L281: const settingsOpen = ref(false); L282: const settingsTab = ref('general'); L283: const settingsTabs = [; L289: const conversations = ref([]); L290: const activeConversationId = ref(null); L291: const messages = ref([]); L292: const draft = ref(''); L293: const sending = ref(false); L294: const loadingConversations = ref(false); L295: const savingSettings = ref(false); L296: const modelsLoading = ref(false); L297: const credentialsBusy = ref(false); L298: const promptsBusy = ref(false); L299: const backendAvailable = ref(false); L300: const errorMessage = ref(''); L301: const settingsNotice = ref(''); L302: const settingsNoticeType = ref('success'); L303: const toast = ref(''); L304: const messagesContainer = ref(null); L305: const availableModels = ref([]); L306: const credentials = ref([]); L307: const promptProfiles = ref([]); L308: const settings = reactive({; L315: const credentialForm = reactive({ provider: 'openai', api_key: '' }); L316: const promptForm = reactive({; L320: const helpDialog = reactive({ open: false, title: '', body: '' }); L322: const activeConversationTitle = computed(() => {
- Imports (first five): import { computed, defineComponent, h, onMounted, reactive, ref, nextTick } from 'vue'; import api from '@/services/Shared/api'; import aiControl from '@/services/AI/aiControl'; import { endpoints } from '@/services/Shared/endpoints'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/ai/AIProviderUsageChart.vue
- Type: .vue
- Declarations: L7: const props = defineProps({ rows: { type: Array, default: () => [] } }); L8: const data = computed(() => ({ labels: props.rows.map((row) => row.provider), datasets: [{ label: 'Messages', data: props.rows.map((row) => row.count || 0), borderWidth: 1 }] })); L9: const options = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
- Imports (first five): import { computed } from 'vue'; import { Bar } from 'vue-chartjs'; import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/ai/AIStatusIndicator.vue
- Type: .vue
- Declarations: L18: const status = ref('checking'); L21: const label = computed(() => ({; L29: async function check() {
- Imports (first five): import { computed, onBeforeUnmount, onMounted, ref } from 'vue'; import api from '@/services/Shared/api'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/ai/MarkdownRenderer.vue
- Type: .vue
- Declarations: L17: const props = defineProps({ content: { type: String, default: '' } }); L20: const safeHtml = computed(() => {; L21: const html = marked.parse(props.content || ''); L22: const sanitized = DOMPurify.sanitize(html, {; L26: const wrapper = document.createElement('div'); L29: const language = [...block.classList].find((name) => name.startsWith('language-'))?.slice(9)
- Imports (first five): import { computed } from 'vue'; import { marked } from 'marked'; import DOMPurify from 'dompurify'; import Prism from 'prismjs'; import 'prismjs/components/prism-markup'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/ai/dashboard/OpportunityRow.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/ai/dashboard/Recommendation.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/ai/dashboard/SkillBar.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/ai/dashboard/StatCard.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/ai/layout/AppLayout.vue
- Type: .vue
- Declarations: L25: const sidebarCollapsed = ref(false); L26: const mobileMenuOpen = ref(false)
- Imports (first five): import { ref } from 'vue'; import Sidebar from './Sidebar.vue'; import Topbar from './Topbar.vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/ai/layout/Sidebar.vue
- Type: .vue
- Declarations: L61: const mainItems = [; L79: const secondaryItems = [
- Imports (first five): import { RouterLink } from 'vue-router'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/ai/layout/Topbar.vue
- Type: .vue
- Declarations: L25: const route = useRoute(); L26: const isDark = ref(false); L27: const pageTitle = computed(() => route.meta?.title || ({; L33: const pageDescription = computed(() => route.meta?.description || 'Ù…Ø³Ø§Ø­Ø© Ø§Ù„Ø¹Ù…Ù„ Ø§Ù„Ø´Ø®ØµÙŠØ©'); L35: function applyTheme(value) {; L41: function toggleTheme() { applyTheme(!isDark.value) }
- Imports (first five): import { computed, onMounted, ref, watch } from 'vue'; import { RouterLink, useRoute } from 'vue-router'
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


## components/codex/Build/WorkspaceView.vue
- Type: .vue
- Declarations: L7: const buildSteps = ref([
- Imports (first five): import { ref } from 'vue'; import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/Capabilities/CapabilitiesView.vue
- Type: .vue
- Declarations: L11: const activeTab = ref('features'); L13: const mockFeatures = ref([; L19: const mockTools = ref([
- Imports (first five): import { ref } from 'vue'; import Card from 'primevue/card'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tabs from 'primevue/tabs'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/dialogs/CodexInfoDialog.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Dialog from 'primevue/dialog'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/dialogs/CodexPromptDialog.vue
- Type: .vue
- Declarations: L8: const props = defineProps({; L13: const emit = defineEmits(['update:visible', 'update:promptType']); L16: const promptCopyState = ref(''); L18: async function copyPrompt() {
- Imports (first five): import { ref } from 'vue'; import Dialog from 'primevue/dialog'; import SelectButton from 'primevue/selectbutton'; import Textarea from 'primevue/textarea'; import Button from 'primevue/button'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/dialogs/CodexResultDialog.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Dialog from 'primevue/dialog'; import Button from 'primevue/button'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/Layout/CodexRightSidebar.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Button from 'primevue/button'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/Layout/CodexSidebar.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/Layout/CodexTopbar.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Tabs from 'primevue/tabs'; import TabList from 'primevue/tablist'; import Tab from 'primevue/tab'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/panels/CodexAnalysisPanel.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/panels/CodexChatPanel.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Button from 'primevue/button'; import InputText from 'primevue/inputtext'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/panels/CodexGovernancePanel.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/panels/CodexPipelinePanel.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/panels/CodexRegistryPanel.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/workspace/CodexCodeEditor.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Button from 'primevue/button'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/workspace/CodexFileActions.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/workspace/CodexInspectorWorkspace.vue
- Type: .vue
- Declarations: L4: const props = defineProps({; L11: const emit = defineEmits(['openFile', 'askAI', 'scan']); L13: const activeApp = ref(null); L14: const activeRoute = ref(''); L15: const inspectEnabled = ref(false); L16: const viewport = ref('desktop'); L17: const selectedElement = ref(null); L18: const resourcePaths = ref([]); L19: const previewError = ref(''); L20: const frame = ref(null); L23: const appFeatures = computed(() => [...props.features].sort((a, b) => (a.name || '').localeCompare(b.name || ''))); L24: const activeRoutes = computed(() => {; L26: const slug = String(activeApp.value.app_label || activeApp.value.name || '').toLowerCase().replace(/[^a-z0-9]+/g, ''); L28: const routeText = `${route.name || ''} ${route.path || ''}`.toLowerCase().replace(/[^a-z0-9]+/g, ''); L32: const currentRoute = computed(() => props.routes.find((route) => route.path === activeRoute.value) || null); L33: const matchedFile = computed(() => {; L34: const path = selectedElement.value?.sourcePath; L36: const normalized = path.replaceAll('\\', '/').replace(/^.*?frontend_vue\//, 'frontend_vue/'); L39: const relatedApis = computed(() => {; L40: const observed = resourcePaths.value; L42: const path = url.split('?')[0].replace(/\/$/, ''); L43: const endpoint = String(api.path || '').replace(/\/$/, ''); L48: function chooseApp(app) {; L53: const candidates = props.routes.filter((route) => {; L54: const slug = String(app.app_label || app.name || '').toLowerCase().replace(/[^a-z0-9]+/g, ''); L55: const routeText = `${route.name || ''} ${route.path || ''}`.toLowerCase().replace(/[^a-z0-9]+/g, ''); L61: function readElement(element, doc) {; L62: const chain = []; L67: const tag = node.tagName?.toLowerCase(); L76: const instance = node.__vueParentComponent
- Imports (first five): import { computed, onBeforeUnmount, ref, watch } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/workspace/CodexProjectExplorer.vue
- Type: .vue
- Declarations: L4: const props = defineProps({; L13: const filteredFiles = computed(() => {; L14: const q = (props.fileQuery || '').trim().toLowerCase()
- Imports (first five): import { computed } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/workspace/CodexTerminal.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/core/FrontendEnhancementCenter.vue
- Type: .vue
- Declarations: L116: const isDark = useDark({ selector: 'html', attribute: 'class', valueDark: 'p-dark', valueLight: '' }); L117: const prefersReducedMotion = computed(() => usePreferredReducedMotion().value === 'reduce'); L119: const query = useQuery({; L122: const response = await api.get('/ai/health/'); L129: const editor = useEditor({; L134: const cards = ref([; L141: const activity = Array.from({ length: 250 }, (_, index) => ({; L146: const fileInput = ref(null); L164: function toggleLocale() {; L169: function notify() {
- Imports (first five): import { computed, onBeforeUnmount, onMounted, ref } from 'vue'; import { useI18n } from 'vue-i18n'; import { useDark, usePreferredReducedMotion } from '@vueuse/core'; import { useQuery } from '@tanstack/vue-query'; import { EditorContent, useEditor } from '@tiptap/vue-3'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceApiTest.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceBudgets.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceCoach.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import Textarea from 'primevue/textarea'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceCrudDialog.vue
- Type: .vue
- Declarations: L407: const props = defineProps({; L439: const emit = defineEmits(['update:visible', 'update:form', 'cancel', 'save']); L441: const localForm = ref({}); L468: const formTitle = computed(() => {; L469: const labels = {
- Imports (first five): import { computed, ref, watch } from 'vue'; import Dialog from 'primevue/dialog'; import Button from 'primevue/button'; import InputText from 'primevue/inputtext'; import InputNumber from 'primevue/inputnumber'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceDebts.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceForecast.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import InputNumber from 'primevue/inputnumber'; import Select from 'primevue/select'; import DataTable from 'primevue/datatable'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceHabits.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceHealthAlerts.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Tag from 'primevue/tag'; import Badge from 'primevue/badge'; import ProgressBar from 'primevue/progressbar'; import Button from 'primevue/button'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceHero.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Button from 'primevue/button'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceIntegrations.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceKpiGrid.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceLoans.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceOverview.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Tag from 'primevue/tag'; import Button from 'primevue/button'; import ProgressBar from 'primevue/progressbar'; import DataTable from 'primevue/datatable'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinancePaymentDialog.vue
- Type: .vue
- Declarations: L46: const props = defineProps({; L67: const emit = defineEmits(['update:visible', 'update:paymentForm', 'cancel', 'save']); L69: const localForm = ref({
- Imports (first five): import { ref, watch } from 'vue'; import Dialog from 'primevue/dialog'; import Button from 'primevue/button'; import InputNumber from 'primevue/inputnumber'; import InputText from 'primevue/inputtext'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceRecurring.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceReports.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceSavings.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'; import ProgressBar from 'primevue/progressbar'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceSectionNav.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import SelectButton from 'primevue/selectbutton'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/finance/FinanceTransactions.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
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


## components/knowledge/KnowledgeCard.vue
- Type: .vue
- Declarations: L21: const emit = defineEmits(['edit', 'archive']); L23: const typeIcons = {; L35: const getIcon = (type) => {; L39: const getTypeLabel = (type) => {; L40: const labels = {; L55: const formatDate = (date) => {
- Imports (first five): import {; import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/knowledge/KnowledgeEmptyState.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/knowledge/KnowledgeForm.vue
- Type: .vue
- Declarations: L4: const props = defineProps({; L16: const emit = defineEmits(['submit', 'cancel']); L22: const form = reactive({; L37: const tagsInput = ref(''); L43: const selectedFiles = ref([]); L45: const fileInput = ref(null); L47: const isDragging = ref(false); L50: const acceptedFileTypes = [; L88: const acceptedFileTypesString = acceptedFileTypes.join(','); L94: const knowledgeTypes = [; L110: const existingFiles = computed(() => {; L122: const resetForm = () => {; L144: const fillForm = (knowledge) => {; L180: const openFilePicker = () => {; L188: const isValidFile = (file) => {; L189: const extension = `.${file.name.split('.').pop()?.toLowerCase()}`; L197: const addFiles = (files) => {; L202: const incomingFiles = Array.from(files); L209: const alreadyExists = selectedFiles.value.some(; L228: const handleFileChange = (event) => {; L237: const handleDragOver = (event) => {; L242: const handleDragLeave = (event) => {; L247: const handleDrop = (event) => {; L257: const removeSelectedFile = (index) => {; L265: const formatFileSize = (size) => {; L270: const units = ['B', 'KB', 'MB', 'GB']; L271: const unitIndex = Math.floor(Math.log(size) / Math.log(1024)); L272: const safeIndex = Math.min(unitIndex, units.length - 1); L273: const value = size / Math.pow(1024, safeIndex); L282: const getFileIcon = (file) => {
- Imports (first five): import { reactive, ref, watch, computed } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/learning/AIReviewPanel.vue
- Type: .vue
- Declarations: L4: const props = defineProps({; L11: const score = computed(() => {; L15: const scoreClass = computed(() => {; L31: const list = (value) => {
- Imports (first five): import { computed } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/learning/ApplicationComposer.vue
- Type: .vue
- Declarations: L11: const props = defineProps({; L23: const emit = defineEmits(['updated']); L25: const title = ref(props.application?.title || ''); L27: const content = ref(props.application?.content || ''); L29: const saving = ref(false); L31: const submitting = ref(false); L33: const reviewing = ref(false); L35: const error = ref(''); L37: const currentApplication = ref(props.application); L39: const isReviewed = computed(() => {; L44: const saveApplication = async () => {; L90: const submitApplication = async () => {; L105: const result = await submitKnowledgeApplication(application.id); L119: const runReview = async () => {; L128: const review = await reviewKnowledgeApplication(currentApplication.value.id)
- Imports (first five): import { computed, ref } from 'vue'; import {
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/learning/LearningPathEditor.vue
- Type: .vue
- Declarations: L17: const props = defineProps({; L34: const emit = defineEmits(['refresh']); L36: const selectedPathId = ref(props.paths[0]?.id || null); L38: const savingOrder = ref(false); L40: const savingTopic = ref(false); L42: const deletingTopic = ref(false); L44: const error = ref(''); L46: const showTopicModal = ref(false); L48: const editingTopic = ref(null); L50: const topicForm = ref({; L58: const selectedPath = computed(() => {; L62: const pathTopics = computed(() => {; L68: const getProgress = (topicId) => {; L69: const item = props.progress.find((entry) => entry.topic === topicId); L74: const selectPath = (pathId) => {; L78: const openCreateTopic = () => {; L94: const openEditTopic = (topic) => {; L110: const closeTopicModal = () => {; L119: const saveTopic = async () => {; L171: const removeTopic = async (topic) => {; L172: const confirmed = window.confirm(`Delete "${topic.title}"?`); L194: const saveOrder = async () => {; L203: const topicIds = pathTopics.value.map((topic) => topic.id)
- Imports (first five): import { computed, ref } from 'vue'; import { RouterLink } from 'vue-router'; import draggable from 'vuedraggable'; import LearningTopicCard from './LearningTopicCard.vue'; import {
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/learning/LearningTopicCard.vue
- Type: .vue
- Declarations: L14: const statusLabel = (status) => {; L15: const labels = {
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/GlobalToastNotification.vue
- Type: .vue
- Declarations: L9: const toast = useToast();; L12: const showNotification = (severity, summary, detail) => {
- Imports (first five): import { useToast } from 'primevue/usetoast';; import { provide } from 'vue';
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/HeaderView.vue
- Type: .vue
- Declarations: L14: const router = useRouter(); L15: const route = useRoute(); L16: const userStore = useUserStore(); L18: const sidebarOpen = ref(true); L19: const mobileMenuOpen = ref(false); L20: const profileMenu = ref(null); L21: const searchQuery = ref(''); L23: const menuItems = [; L66: const secondaryItems = [; L72: const userName = computed(() => {; L76: const userEmail = computed(() => userStore.user?.email || ''); L78: const userInitials = computed(() => {; L79: const name = userName.value.trim(); L89: const avatarUrl = computed(() => userStore.user?.avatar_url || null); L91: const currentRouteLabel = computed(() => {; L92: const item = [...menuItems, ...secondaryItems].find((entry) => {; L100: const profileRoute = computed(() => {; L101: const id = userStore.user?.id; L105: const profileMenuItems = computed(() => [; L124: function userProfileRoute() {; L128: function toggleSidebar() {; L132: function closeSidebarOnMobile() {; L139: function toggleProfileMenu(event) {; L143: function submitSearch() {; L144: const query = searchQuery.value.trim(); L153: function logout() {; L159: function handleKeydown(event) {
- Imports (first five): import { computed, onBeforeUnmount, onMounted, ref } from 'vue'; import { RouterLink, useRoute, useRouter } from 'vue-router'; import { useUserStore } from '@/stores/accounts/user'; import Avatar from 'primevue/avatar'; import Badge from 'primevue/badge'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/HelloWorld.spec.js
- Type: .js
- Declarations: L8: const wrapper = mount(HelloWorld, { props: { msg: 'Hello Vitest' } })
- Imports (first five): import { describe, it, expect } from 'vitest'; import { mount } from '@vue/test-utils'; import HelloWorld from './HelloWorld.vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/HelloWorld.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/IconCommunity.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/IconDocumentation.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/IconEcosystem.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/IconSupport.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/IconTooling.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/LiveDebugConsole.vue
- Type: .vue
- Declarations: L10: const enabled = import.meta.env.DEV || import.meta.env.VITE_DEBUG_CONSOLE === 'true'; L11: const wsEnabled = import.meta.env.VITE_DEBUG_CONSOLE === 'true'; L12: const WS_URL = import.meta.env.VITE_DEBUG_WS_URL || 'ws://127.0.0.1:8000/ws/debug/'; L13: const MAX_LOGS = 500; L16: const open = ref(false); L17: const minimized = ref(false); L18: const paused = ref(false); L19: const autoScroll = ref(true); L20: const searchQuery = ref(''); L21: const activeFilter = ref('all') // 'all' | 'error' | 'warn' | 'network' | 'pinia'; L24: const logs = ref([]); L25: const status = ref('closed') // 'connecting' | 'connected' | 'closed' | 'error'; L30: const frontendConsoleEl = ref(null); L31: const backendConsoleEl = ref(null); L32: const toastMessage = ref(''); L33: const showToastFlag = ref(false); L36: const filterTabs = [; L45: function showToast(msg) {; L55: async function copyToClipboard(text, successMsg = 'ØªÙ… Ø§Ù„Ù†Ø³Ø® Ø¥Ù„Ù‰ Ø§Ù„Ø­Ø§ÙØ¸Ø© Ø¨Ù†Ø¬Ø§Ø­') {; L65: const addLog = (entry) => {; L68: const normalizedSource = (entry.source || 'APP').toUpperCase(); L69: const normalizedLevel = (entry.level || 'info').toLowerCase(); L70: const formattedPayload = entry.payload ? JSON.stringify(entry.payload, null, 2) : null; L72: const newEntry = {; L96: const targetEl = newEntry.isBackend ? backendConsoleEl.value : frontendConsoleEl.value; L105: function connect() {; L125: const d = JSON.parse(e.data); L154: function disconnect() {; L164: function toggle() {; L172: function onApi(e) {
- Imports (first five): import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'; import Button from 'primevue/button'; import InputText from 'primevue/inputtext'; import IconField from 'primevue/iconfield'; import InputIcon from 'primevue/inputicon'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/ThemeSwitcher.vue
- Type: .vue
- Declarations: L19: const THEME_KEY = 'so_iam_os.theme'; L30: const saved = localStorage.getItem(THEME_KEY); L31: const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches; L32: const isDark = saved ? saved === 'dark' : prefersDark; L33: const root = document.documentElement; L40: const root = document.getElementsByTagName('html')[0]; L41: const isDark = !root.classList.contains('p-dark')
- Imports (first five): import { updatePreset, updateSurfacePalette } from '@primevue/themes'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/TheWelcome.vue
- Type: .vue
- Declarations: L9: const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')
- Imports (first five): import WelcomeItem from './WelcomeItem.vue'; import DocumentationIcon from './IconDocumentation.vue'; import ToolingIcon from './IconTooling.vue'; import EcosystemIcon from './IconEcosystem.vue'; import CommunityIcon from './IconCommunity.vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/shared/WelcomeItem.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.

