# ai services and API

Service files found under services/AI. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/AI/Ai.js
L5: export const sendMessage = async ({ message, conversation_id = null, provider = null, model = '', ...options }) => {
L13: export const streamMessage = async ({ message, conversation_id = null, provider = null, model = '', onChunk, signal, ...options }) => {
L22: export const getConversations = async () => (await api.get(endpoints.ai.conversations)).data
L23: export const getConversation = async (id) => (await api.get(endpoints.ai.conversation(id))).data
L24: export const createConversation = async (payload = {}) => (await api.post(endpoints.ai.conversations, payload)).data
L25: export const deleteConversation = async (id) => { await api.delete(endpoints.ai.conversation(id)); return true }
L26: export const getAIHealth = async () => (await api.get(endpoints.ai.health)).data
L27: export const getAICapabilities = async () => (await api.get(endpoints.ai.capabilities)).data

## services/AI/aiControl.js
L4: const unwrap = (data) => (Array.isArray(data) ? data : data?.results || [])
L6: export const getAISettings = async () => (await api.get(endpoints.ai.settings)).data
L7: export const updateAISettings = async (payload) =>
L10: export const getCredentials = async () => unwrap((await api.get(endpoints.ai.credentials)).data)
L11: export const saveCredential = async (payload) =>
L13: export const deleteCredential = async (provider) => {
L18: export const getProviderModels = async (provider, force = false) =>
L20: export const testProviderConnection = async (provider, model = '') =>
L22: export const listAIProviders = async () => (await api.get(endpoints.ai.providers)).data
L23: export const getAIUsage = async () => (await api.get(endpoints.ai.usage)).data
L24: export const listAIExecutions = async () => (await api.get(endpoints.ai.executions)).data
L25: export const listAIBudgets = async () => unwrap((await api.get(endpoints.ai.budgets)).data)
L26: export const createAIBudget = async (payload) => (await api.post(endpoints.ai.budgets, payload)).data
L27: export const updateAIBudget = async (id, payload) => (await api.patch(endpoints.ai.budget(id), payload)).data
L28: export const deleteAIBudget = async (id) => { await api.delete(endpoints.ai.budget(id)); return true }
L29: export const listAIAudit = async () => unwrap((await api.get(endpoints.ai.audit)).data)
L30: export const submitAIFeedback = async (payload) => (await api.post(endpoints.ai.feedback, payload)).data
L31: export const listAIWorkflows = async () => unwrap((await api.get(endpoints.ai.workflows)).data)
L32: export const createAIWorkflow = async (payload) => (await api.post(endpoints.ai.workflows, payload)).data
L33: export const getAIWorkflow = async (id) => (await api.get(endpoints.ai.workflow(id))).data
L34: export const updateAIWorkflow = async (id, payload) => (await api.patch(endpoints.ai.workflow(id), payload)).data
L35: export const deleteAIWorkflow = async (id) => { await api.delete(endpoints.ai.workflow(id)); return true }
L36: export const getAIWorkflowRuns = async (id) => unwrap((await api.get(endpoints.ai.workflowRuns(id))).data)
L37: export const listAIConversations = async () => unwrap((await api.get(endpoints.ai.conversations)).data)
L38: export const createAIConversation = async (payload = {}) => (await api.post(endpoints.ai.conversations, payload)).data
L39: export const getAIConversation = async (id) => (await api.get(endpoints.ai.conversation(id))).data
L40: export const setAIConversationAction = async (id, action) => (await api.post(endpoints.ai.conversation(id), { action })).data
L41: export const getAIConversationContext = async (id) => (await api.get(endpoints.ai.conversationContext(id))).data
L42: export const getAIHealth = async () => (await api.get(endpoints.ai.health)).data
L43: export const getAICapabilities = async () => (await api.get(endpoints.ai.capabilities)).data
L44: export const inspectAIContext = async (conversationId) =>
L46: export const validateAIWorkflow = async (graph) =>
L48: export const proposeAITask = async (payload) =>
L50: export const selectAIAgent = async (payload) =>
L53: export const listPromptProfiles = async () => unwrap((await api.get(endpoints.ai.prompts)).data)
L54: export const createPromptProfile = async (payload) =>
L56: export const getPromptProfile = async (id) => (await api.get(endpoints.ai.prompt(id))).data
L57: export const updatePromptProfile = async (id, payload) =>
L59: export const deletePromptProfile = async (id) => {
L64: export const previewLearningPlan = async ({ message, provider, model }) =>
L67: export const approveLearningPlan = async (plan) =>
L69: export const startLearningPlanAsync = async (payload) =>
L71: export const getTaskStatus = async (taskId) => (await api.get(endpoints.ai.taskStatus(taskId))).data
L72: export const sendTopicMessage = async (payload) => (await api.post(endpoints.ai.topicChat, payload)).data
L73: export const createAgentPlan = async (payload) => (await api.post(endpoints.ai.agentPlan, payload)).data

## services/AI/aiPlatformService.js
L4: export const getSettings = aiControl.getAISettings
L5: export const saveSettings = aiControl.updateAISettings
L6: export const listCredentials = aiControl.getCredentials
L7: export const saveCredential = aiControl.saveCredential
L8: export const deleteCredential = aiControl.deleteCredential
L9: export const testProvider = aiControl.testProviderConnection
L10: export const listProviders = aiControl.listAIProviders
L11: export const listProviderModels = aiControl.getProviderModels
L12: export const getHealth = aiControl.getAIHealth
L13: export const getCapabilities = aiControl.getAICapabilities
L14: export const getUsage = aiControl.getAIUsage
L15: export const listExecutions = aiControl.listAIExecutions
L16: export const listBudgets = aiControl.listAIBudgets
L17: export const saveBudget = aiControl.createAIBudget
L18: export const updateBudget = aiControl.updateAIBudget
L19: export const deleteBudget = aiControl.deleteAIBudget
L20: export const listAuditLogs = aiControl.listAIAudit
L21: export const sendFeedback = aiControl.submitAIFeedback
L22: export const listWorkflows = aiControl.listAIWorkflows
L23: export const saveWorkflow = aiControl.createAIWorkflow
L24: export const getWorkflow = aiControl.getAIWorkflow
L25: export const updateWorkflow = aiControl.updateAIWorkflow
L26: export const deleteWorkflow = aiControl.deleteAIWorkflow
L27: export const listWorkflowRuns = aiControl.getAIWorkflowRuns
L29: export const runWorkflow = async () => { throw new Error('Workflow execution is not supported by the current backend API.') }

## services/AI/AIService.js
L6: function buildPayload(messages, model = '', options = {}) {
L7: const history = Array.isArray(messages) ? messages : []
L8: const latestUser = [...history].reverse().find((item) => item?.role === 'user' && item?.content?.trim())
L10: const payload = { message: latestUser.content.trim() }
L14: const systemMessage = history.find((item) => item?.role === 'system' && item?.content?.trim())
L27: const error = new Error(data.error || 'AI request failed.')
L34: const body = error?.response?.data
L42: const payload = buildPayload(messages, model, options)
L43: const accessToken = await getValidAccessToken()
L46: const baseURL = String(api.defaults.baseURL || '').replace(/\/+$/, '')
L47: const streamPath = endpoints.ai.chatStream.startsWith('/')
L50: const response = await fetch(`${baseURL}${streamPath}`, {
L66: const error = new Error(body.error || body.detail || `AI streaming request failed (${response.status}).`)
L73: const contentType = response.headers.get('content-type') || ''
L75: const body = await response.json()
L77: const content = body?.message?.content || ''
L82: const result = {
L95: const delta = event.data.delta || ''
L102: const error = new Error(event.data.error || 'AI streaming failed.')

## services/AI/sse.js
L2: export function parseSSEEvent(block) {
L4: const data = []
L7: const separator = rawLine.indexOf(':')
L8: const field = separator < 0 ? rawLine : rawLine.slice(0, separator)
L15: const raw = data.join('\n')
L23: export async function consumeSSEStream(stream, onEvent) {
L24: const reader = stream.getReader()
L25: const decoder = new TextDecoder()
L27: const dispatch = (block) => {
L28: const event = parseSSEEvent(block)


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
