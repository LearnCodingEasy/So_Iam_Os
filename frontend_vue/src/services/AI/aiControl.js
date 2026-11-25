import api from '../Shared/api'
import { endpoints } from '../Shared/endpoints'

const unwrap = (data) => (Array.isArray(data) ? data : data?.results || [])

export const getAISettings = async () => (await api.get(endpoints.ai.settings)).data
export const updateAISettings = async (payload) =>
  (await api.patch(endpoints.ai.settings, payload)).data

export const getCredentials = async () => unwrap((await api.get(endpoints.ai.credentials)).data)
export const saveCredential = async (payload) =>
  (await api.post(endpoints.ai.credentials, payload)).data
export const deleteCredential = async (provider) => {
  await api.delete(endpoints.ai.credential(provider))
  return true
}

export const getProviderModels = async (provider, force = false) =>
  (await api.get(`${endpoints.ai.providerModels(provider)}${force ? '?refresh=1' : ''}`)).data
export const testProviderConnection = async (provider, model = '') =>
  (await api.post(endpoints.ai.providerTest(provider), { model })).data
export const listAIProviders = async () => (await api.get(endpoints.ai.providers)).data
export const getAIUsage = async () => (await api.get(endpoints.ai.usage)).data
export const listAIExecutions = async () => (await api.get(endpoints.ai.executions)).data
export const listAIBudgets = async () => unwrap((await api.get(endpoints.ai.budgets)).data)
export const createAIBudget = async (payload) =>
  (await api.post(endpoints.ai.budgets, payload)).data
export const updateAIBudget = async (id, payload) =>
  (await api.patch(endpoints.ai.budget(id), payload)).data
export const deleteAIBudget = async (id) => {
  await api.delete(endpoints.ai.budget(id))
  return true
}
export const listAIAudit = async () => unwrap((await api.get(endpoints.ai.audit)).data)
export const submitAIFeedback = async (payload) =>
  (await api.post(endpoints.ai.feedback, payload)).data
export const listAIWorkflows = async () => unwrap((await api.get(endpoints.ai.workflows)).data)
export const createAIWorkflow = async (payload) =>
  (await api.post(endpoints.ai.workflows, payload)).data
export const getAIWorkflow = async (id) => (await api.get(endpoints.ai.workflow(id))).data
export const updateAIWorkflow = async (id, payload) =>
  (await api.patch(endpoints.ai.workflow(id), payload)).data
export const deleteAIWorkflow = async (id) => {
  await api.delete(endpoints.ai.workflow(id))
  return true
}
export const getAIWorkflowRuns = async (id) =>
  unwrap((await api.get(endpoints.ai.workflowRuns(id))).data)
export const listAIConversations = async () =>
  unwrap((await api.get(endpoints.ai.conversations)).data)
export const createAIConversation = async (payload = {}) =>
  (await api.post(endpoints.ai.conversations, payload)).data
export const getAIConversation = async (id) => (await api.get(endpoints.ai.conversation(id))).data
export const setAIConversationAction = async (id, action) =>
  (await api.post(endpoints.ai.conversation(id), { action })).data
export const getAIConversationContext = async (id) =>
  (await api.get(endpoints.ai.conversationContext(id))).data
export const getAIHealth = async () => (await api.get(endpoints.ai.health)).data
export const getAICapabilities = async () => (await api.get(endpoints.ai.capabilities)).data
export const inspectAIContext = async (conversationId) =>
  (await api.get(endpoints.ai.conversationContext(conversationId))).data
export const validateAIWorkflow = async (graph) =>
  (await api.post(endpoints.ai.workflowValidate, graph)).data
export const proposeAITask = async (payload) =>
  (await api.post(endpoints.ai.taskProposal, payload)).data
export const selectAIAgent = async (payload) =>
  (await api.post(endpoints.ai.agentSelect, payload)).data

export const listPromptProfiles = async () => unwrap((await api.get(endpoints.ai.prompts)).data)
export const createPromptProfile = async (payload) =>
  (await api.post(endpoints.ai.prompts, payload)).data
export const getPromptProfile = async (id) => (await api.get(endpoints.ai.prompt(id))).data
export const updatePromptProfile = async (id, payload) =>
  (await api.patch(endpoints.ai.prompt(id), payload)).data
export const deletePromptProfile = async (id) => {
  await api.delete(endpoints.ai.prompt(id))
  return true
}

export const previewLearningPlan = async ({ message, provider, model }) =>
  (await api.post(endpoints.ai.learningPreview, { message, provider, model })).data

export const approveLearningPlan = async (plan) =>
  (await api.post(endpoints.ai.learningApprove, plan)).data
export const startLearningPlanAsync = async (payload) =>
  (await api.post(endpoints.ai.learningAsync, payload)).data
export const getTaskStatus = async (taskId) => (await api.get(endpoints.ai.taskStatus(taskId))).data
export const sendTopicMessage = async (payload) =>
  (await api.post(endpoints.ai.topicChat, payload)).data
export const createAgentPlan = async (payload) =>
  (await api.post(endpoints.ai.agentPlan, payload)).data

export default {
  getAISettings,
  updateAISettings,
  getCredentials,
  saveCredential,
  deleteCredential,
  getProviderModels,
  testProviderConnection,
  listAIProviders,
  getAIUsage,
  listAIExecutions,
  listAIBudgets,
  createAIBudget,
  updateAIBudget,
  deleteAIBudget,
  listAIAudit,
  submitAIFeedback,
  listAIWorkflows,
  createAIWorkflow,
  getAIWorkflow,
  updateAIWorkflow,
  deleteAIWorkflow,
  getAIWorkflowRuns,
  getAIConversation,
  setAIConversationAction,
  getAIConversationContext,
  listAIConversations,
  createAIConversation,
  getAIHealth,
  getAICapabilities,
  inspectAIContext,
  validateAIWorkflow,
  proposeAITask,
  selectAIAgent,
  listPromptProfiles,
  createPromptProfile,
  getPromptProfile,
  updatePromptProfile,
  deletePromptProfile,
  previewLearningPlan,
  approveLearningPlan,
  startLearningPlanAsync,
  getTaskStatus,
  sendTopicMessage,
  createAgentPlan,
}
