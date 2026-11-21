# ai source-file catalog

Files associated with this domain's view/service/store/component directories are listed. Imports and declaration names are static excerpts; global callers are not exhaustive.


## views/ai/AgentPlanner.vue
- Type: .vue
- Declarations: L52: const direction = computed(() => locale.value === 'ar' ? 'rtl' : 'ltr'); L53: const request = ref(''); L54: const planning = ref(false), selecting = ref(false), proposing = ref(false); L55: const error = ref(''), proposalError = ref(''); L56: const result = ref(null), selection = ref(null), proposal = ref(null); L57: const task = reactive({ title: '', description: '', priority: 'medium' }); L58: const stepsText = ref(''); L59: const priorityOptions = [{ label: 'Ù…Ù†Ø®ÙØ¶Ø©', value: 'low' }, { label: 'Ù…ØªÙˆØ³Ø·Ø©', value: 'medium' }, { label: 'Ø¹Ø§Ù„ÙŠØ©', value: 'high' }, { label: 'Ø¹Ø§Ø¬Ù„Ø©', value: 'urgent' }]; L61: async function plan() {; L68: async function selectAgent() {; L75: async function createProposal() {
- Imports (first five): import { computed, reactive, ref } from 'vue'; import { useI18n } from 'vue-i18n'; import Button from 'primevue/button'; import Card from 'primevue/card'; import Textarea from 'primevue/textarea'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/ai/AI.vue
- Type: .vue
- Declarations: L125: const providerOptions = [; L132: const settings = ref({ preferred_provider: 'ollama', preferred_model: '' }); L133: const selectedProvider = ref('ollama'); L134: const selectedModel = ref(''); L135: const apiKey = ref(''); L136: const credentials = ref([]); L137: const providerRows = ref([]); L138: const modelOptions = ref([]); L139: const providerMessage = ref(null); L140: const chatError = ref(''); L141: const planError = ref(''); L142: const messages = ref([]); L143: const prompt = ref(''); L144: const planPrompt = ref(''); L145: const plan = ref(null); L146: const taskStatus = ref(null); L147: const sending = ref(false); L148: const generating = ref(false); L149: const approving = ref(false); L150: const savingCredential = ref(false); L151: const savingSettings = ref(false); L152: const testingProvider = ref(false); L153: const loadingModels = ref(false); L155: const credentialStatus = computed(() =>; L159: function providerLabel(provider) {; L163: async function refreshProviderData() {; L172: async function load() {; L184: async function saveProviderCredential() {; L200: async function removeCredential(provider) {; L210: async function saveProviderSettings() {
- Imports (first five): import { computed, onMounted, ref } from 'vue'; import Button from 'primevue/button'; import Card from 'primevue/card'; import Message from 'primevue/message'; import Password from 'primevue/password'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/ai/AIChat.vue
- Type: .vue
- Declarations: L547: const direction = computed(() => locale.value === 'ar' ? 'rtl' : 'ltr'); L549: const HelpButton = defineComponent({; L572: const helpCopy = {; L631: const sidebarCollapsed = ref(false); L632: const settingsOpen = ref(false); L633: const contextDialog = ref(false); L634: const contextLoading = ref(false); L635: const conversationContext = ref(null); L636: const contextError = ref(''); L637: const settingsTab = ref('general'); L638: const settingsTabs = [; L644: const conversations = ref([]); L645: const activeConversationId = ref(null); L646: const lastArchivedConversation = ref(null); L647: const messages = ref([]); L648: const draft = ref(''); L649: const sending = ref(false); L650: const streamController = ref(null); L651: const retryDraft = ref(''); L652: const retryIdempotencyKey = ref(''); L653: const loadingConversations = ref(false); L654: const savingSettings = ref(false); L655: const modelsLoading = ref(false); L656: const credentialsBusy = ref(false); L657: const promptsBusy = ref(false); L658: const backendAvailable = ref(false); L659: const errorMessage = ref(''); L660: const settingsNotice = ref(''); L661: const settingsNoticeType = ref('success'); L662: const toast = ref('')
- Imports (first five): import { computed, defineComponent, h, onMounted, reactive, ref, nextTick } from 'vue'; import aiControl from '@/services/AI/aiControl'; import { sendMessage as sendNonStreamingMessage, streamMessage } from '@/services/AI/Ai'; import MarkdownRenderer from '@/components/ai/MarkdownRenderer.vue'; import { useI18n } from 'vue-i18n'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/ai/AIControl.vue
- Type: .vue
- Declarations: L144: const direction = computed(() => locale.value === 'ar' ? 'rtl' : 'ltr'); L146: const providerOptions = [; L153: const settings = ref({ preferred_provider: 'ollama', preferred_model: '' }); L154: const selectedProvider = ref('ollama'); L155: const selectedModel = ref(''); L157: const credentials = ref([]); L158: const providerRows = ref([]); L159: const modelOptions = ref([]); L160: const providerMessage = ref(null); L161: const chatError = ref(''); L162: const planError = ref(''); L163: const messages = ref([]); L164: const prompt = ref(''); L165: const planPrompt = ref(''); L166: const plan = ref(null); L167: const taskStatus = ref(null); L168: const sending = ref(false); L169: const generating = ref(false); L170: const asyncGenerating = ref(false); L171: const approving = ref(false); L172: const savingCredential = ref(false); L173: const savingSettings = ref(false); L174: const testingProvider = ref(false); L175: const loadingModels = ref(false); L177: const credentialSchema = toTypedSchema(z.object({; L192: const planMarkdown = computed(() => plan.value ? `\`\`\`json\n${JSON.stringify(plan.value, null, 2)}\n\`\`\`` : ''); L194: const credentialStatus = computed(() =>; L198: function providerLabel(provider) {; L202: async function refreshProviderData() {; L211: async function load() {
- Imports (first five): import { computed, onMounted, ref } from 'vue'; import { useI18n } from 'vue-i18n'; import { gsap } from 'gsap'; import { useForm } from 'vee-validate'; import { toTypedSchema } from '@vee-validate/zod'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/ai/AIOperationsView.vue
- Type: .vue
- Declarations: L196: const direction = computed(() => locale.value === 'ar' ? 'rtl' : 'ltr'); L197: const store = useAIStore(); L199: const activeTab = ref('executions'); L200: const errorMessage = ref(''); L201: const budgetDialog = ref(false), workflowDialog = ref(false), runsDialog = ref(false), auditDialog = ref(false); L202: const savingBudget = ref(false), savingWorkflow = ref(false), validatingWorkflow = ref(false), diagnosticsLoading = ref(false), sendingFeedback = ref(false); L203: const workflowRuns = ref([]), selectedRun = ref(null), selectedAudit = ref(null), workflowValidation = ref(null); L204: const feedbackMessage = ref(null); L205: const workflowJson = ref('{\n  "nodes": [],\n  "edges": []\n}'); L206: const workflowForm = reactive({ id: null, name: '', description: '' }); L207: const budgetForm = reactive({ id: null, scope: 'user', scope_key: '', daily_cost_limit: null, monthly_cost_limit: null, daily_token_limit: null, monthly_token_limit: null, enabled: true }); L208: const feedback = reactive({ message_id: null, sentiment: 'like', reason: '', comment: '', feedback_category: '', rating: null }); L209: const scopeOptions = [{ label: 'Ù…Ø³ØªØ®Ø¯Ù…', value: 'user' }, { label: 'Agent', value: 'agent' }, { label: 'Ù…Ø²ÙˆØ¯', value: 'provider' }]; L210: const sentimentOptions = [{ label: 'Ø¥ÙŠØ¬Ø§Ø¨ÙŠ', value: 'like' }, { label: 'Ø³Ù„Ø¨ÙŠ', value: 'dislike' }]; L212: function statusSeverity(status) { return ({ succeeded: 'success', completed: 'success', failed: 'danger', running: 'info', queued: 'warn', pending: 'warn' })[status] || 'secondary' }; L213: function displayValue(value) { return value && typeof value === 'object' ? JSON.stringify(value) : (value ?? 'â€”') }; L214: function messageOf(error, fallback) { return error?.response?.data?.detail || error?.response?.data?.error || error?.message || fallback }; L215: async function refresh() {; L220: async function loadDiagnostics() {; L229: function openBudgetCreate() {; L233: function editBudget(item) { Object.assign(budgetForm, { ...item }); budgetDialog.value = true }; L234: async function saveBudget() {; L237: const payload = { scope: budgetForm.scope, scope_key: budgetForm.scope_key, daily_cost_limit: budgetForm.daily_cost_limit, monthly_cost_limit: budgetForm.monthly_cost_limit, daily_token_limit: budgetForm.daily_token_limit, monthly_token_limit: budgetForm.monthly_token_limit, enabled: budgetForm.enabled }; L245: async function removeBudget(item) {; L250: function openWorkflowCreate() {; L256: async function editWorkflow(item) {; L258: const full = await aiControl.getAIWorkflow(item.id); L265: async function validateWorkflow() {; L269: const graph = JSON.parse(workflowJson.value); L275: async function saveWorkflow() {
- Imports (first five): import { onMounted, reactive, ref } from 'vue'; import { computed } from 'vue'; import { useI18n } from 'vue-i18n'; import { storeToRefs } from 'pinia'; import Button from 'primevue/button'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/AI/Ai.js
- Type: .js
- Declarations: L5: export const sendMessage = async ({ message, conversation_id = null, provider = null, model = '', ...options }) => {; L13: export const streamMessage = async ({ message, conversation_id = null, provider = null, model = '', onChunk, signal, ...options }) => {; L22: export const getConversations = async () => (await api.get(endpoints.ai.conversations)).data; L23: export const getConversation = async (id) => (await api.get(endpoints.ai.conversation(id))).data; L24: export const createConversation = async (payload = {}) => (await api.post(endpoints.ai.conversations, payload)).data; L25: export const deleteConversation = async (id) => { await api.delete(endpoints.ai.conversation(id)); return true }; L26: export const getAIHealth = async () => (await api.get(endpoints.ai.health)).data; L27: export const getAICapabilities = async () => (await api.get(endpoints.ai.capabilities)).data
- Imports (first five): import AIService from './AIService'; import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/AI/aiControl.js
- Type: .js
- Declarations: L4: const unwrap = (data) => (Array.isArray(data) ? data : data?.results || []); L6: export const getAISettings = async () => (await api.get(endpoints.ai.settings)).data; L7: export const updateAISettings = async (payload) =>; L10: export const getCredentials = async () => unwrap((await api.get(endpoints.ai.credentials)).data); L11: export const saveCredential = async (payload) =>; L13: export const deleteCredential = async (provider) => {; L18: export const getProviderModels = async (provider, force = false) =>; L20: export const testProviderConnection = async (provider, model = '') =>; L22: export const listAIProviders = async () => (await api.get(endpoints.ai.providers)).data; L23: export const getAIUsage = async () => (await api.get(endpoints.ai.usage)).data; L24: export const listAIExecutions = async () => (await api.get(endpoints.ai.executions)).data; L25: export const listAIBudgets = async () => unwrap((await api.get(endpoints.ai.budgets)).data); L26: export const createAIBudget = async (payload) => (await api.post(endpoints.ai.budgets, payload)).data; L27: export const updateAIBudget = async (id, payload) => (await api.patch(endpoints.ai.budget(id), payload)).data; L28: export const deleteAIBudget = async (id) => { await api.delete(endpoints.ai.budget(id)); return true }; L29: export const listAIAudit = async () => unwrap((await api.get(endpoints.ai.audit)).data); L30: export const submitAIFeedback = async (payload) => (await api.post(endpoints.ai.feedback, payload)).data; L31: export const listAIWorkflows = async () => unwrap((await api.get(endpoints.ai.workflows)).data); L32: export const createAIWorkflow = async (payload) => (await api.post(endpoints.ai.workflows, payload)).data; L33: export const getAIWorkflow = async (id) => (await api.get(endpoints.ai.workflow(id))).data; L34: export const updateAIWorkflow = async (id, payload) => (await api.patch(endpoints.ai.workflow(id), payload)).data; L35: export const deleteAIWorkflow = async (id) => { await api.delete(endpoints.ai.workflow(id)); return true }; L36: export const getAIWorkflowRuns = async (id) => unwrap((await api.get(endpoints.ai.workflowRuns(id))).data); L37: export const listAIConversations = async () => unwrap((await api.get(endpoints.ai.conversations)).data); L38: export const createAIConversation = async (payload = {}) => (await api.post(endpoints.ai.conversations, payload)).data; L39: export const getAIConversation = async (id) => (await api.get(endpoints.ai.conversation(id))).data; L40: export const setAIConversationAction = async (id, action) => (await api.post(endpoints.ai.conversation(id), { action })).data; L41: export const getAIConversationContext = async (id) => (await api.get(endpoints.ai.conversationContext(id))).data; L42: export const getAIHealth = async () => (await api.get(endpoints.ai.health)).data; L43: export const getAICapabilities = async () => (await api.get(endpoints.ai.capabilities)).data
- Imports (first five): import api from '../Shared/api'; import { endpoints } from '../Shared/endpoints'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/AI/aiPlatformService.js
- Type: .js
- Declarations: L4: export const getSettings = aiControl.getAISettings; L5: export const saveSettings = aiControl.updateAISettings; L6: export const listCredentials = aiControl.getCredentials; L7: export const saveCredential = aiControl.saveCredential; L8: export const deleteCredential = aiControl.deleteCredential; L9: export const testProvider = aiControl.testProviderConnection; L10: export const listProviders = aiControl.listAIProviders; L11: export const listProviderModels = aiControl.getProviderModels; L12: export const getHealth = aiControl.getAIHealth; L13: export const getCapabilities = aiControl.getAICapabilities; L14: export const getUsage = aiControl.getAIUsage; L15: export const listExecutions = aiControl.listAIExecutions; L16: export const listBudgets = aiControl.listAIBudgets; L17: export const saveBudget = aiControl.createAIBudget; L18: export const updateBudget = aiControl.updateAIBudget; L19: export const deleteBudget = aiControl.deleteAIBudget; L20: export const listAuditLogs = aiControl.listAIAudit; L21: export const sendFeedback = aiControl.submitAIFeedback; L22: export const listWorkflows = aiControl.listAIWorkflows; L23: export const saveWorkflow = aiControl.createAIWorkflow; L24: export const getWorkflow = aiControl.getAIWorkflow; L25: export const updateWorkflow = aiControl.updateAIWorkflow; L26: export const deleteWorkflow = aiControl.deleteAIWorkflow; L27: export const listWorkflowRuns = aiControl.getAIWorkflowRuns; L29: export const runWorkflow = async () => { throw new Error('Workflow execution is not supported by the current backend API.') }
- Imports (first five): import aiControl from './aiControl'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/AI/AIService.js
- Type: .js
- Declarations: L6: function buildPayload(messages, model = '', options = {}) {; L7: const history = Array.isArray(messages) ? messages : []; L8: const latestUser = [...history].reverse().find((item) => item?.role === 'user' && item?.content?.trim()); L10: const payload = { message: latestUser.content.trim() }; L14: const systemMessage = history.find((item) => item?.role === 'system' && item?.content?.trim()); L27: const error = new Error(data.error || 'AI request failed.'); L34: const body = error?.response?.data; L42: const payload = buildPayload(messages, model, options); L43: const accessToken = await getValidAccessToken(); L46: const baseURL = String(api.defaults.baseURL || '').replace(/\/+$/, ''); L47: const streamPath = endpoints.ai.chatStream.startsWith('/'); L50: const response = await fetch(`${baseURL}${streamPath}`, {; L66: const error = new Error(body.error || body.detail || `AI streaming request failed (${response.status}).`); L73: const contentType = response.headers.get('content-type') || ''; L75: const body = await response.json(); L77: const content = body?.message?.content || ''; L82: const result = {; L95: const delta = event.data.delta || ''; L102: const error = new Error(event.data.error || 'AI streaming failed.')
- Imports (first five): import api, { getValidAccessToken } from '../Shared/api'; import { endpoints } from '../Shared/endpoints'; import { consumeSSEStream } from './sse'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/AI/sse.js
- Type: .js
- Declarations: L2: export function parseSSEEvent(block) {; L4: const data = []; L7: const separator = rawLine.indexOf(':'); L8: const field = separator < 0 ? rawLine : rawLine.slice(0, separator); L15: const raw = data.join('\n'); L23: export async function consumeSSEStream(stream, onEvent) {; L24: const reader = stream.getReader(); L25: const decoder = new TextDecoder(); L27: const dispatch = (block) => {; L28: const event = parseSSEEvent(block)
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/ai/useAIStore.js
- Type: .js
- Declarations: L5: const asArray = (value) => Array.isArray(value) ? value : value?.results || []; L7: export const useAIStore = defineStore('ai-management', () => {; L8: const providers = ref([]); L9: const credentials = ref([]); L10: const settings = ref(null); L11: const conversations = ref([]); L12: const executions = ref([]); L13: const usage = ref({}); L14: const budgets = ref([]); L15: const audit = ref([]); L16: const workflows = ref([]); L17: const health = ref(null); L18: const capabilities = ref([]); L19: const loading = ref(false); L20: const error = ref(null); L22: const beginLoad = () => { activeLoads += 1; loading.value = true }; L23: const endLoad = () => { activeLoads = Math.max(0, activeLoads - 1); loading.value = activeLoads > 0 }; L25: async function refreshControl() {; L45: async function refreshOperations() {; L65: async function refreshAll() {
- Imports (first five): import { defineStore } from 'pinia'; import { ref } from 'vue'; import aiControl from '@/services/AI/aiControl'
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

