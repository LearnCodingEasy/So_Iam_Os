import api from './api'
import { endpoints } from './endpoints'

const unwrap = (data) => (Array.isArray(data) ? data : data?.results || [])

export const getAISettings = async () => (await api.get(endpoints.ai.settings)).data
export const updateAISettings = async (payload) => (await api.patch(endpoints.ai.settings, payload)).data

export const getCredentials = async () => unwrap((await api.get(endpoints.ai.credentials)).data)
export const saveCredential = async (payload) => (await api.post(endpoints.ai.credentials, payload)).data
export const deleteCredential = async (provider) => { await api.delete(endpoints.ai.credential(provider)); return true }

export const getProviderModels = async (provider) => (await api.get(endpoints.ai.providerModels(provider))).data

export const listPromptProfiles = async () => unwrap((await api.get(endpoints.ai.prompts)).data)
export const createPromptProfile = async (payload) => (await api.post(endpoints.ai.prompts, payload)).data
export const updatePromptProfile = async (id, payload) => (await api.patch(endpoints.ai.prompt(id), payload)).data
export const deletePromptProfile = async (id) => { await api.delete(endpoints.ai.prompt(id)); return true }

export const previewLearningPlan = async ({ message, provider, model }) =>
  (await api.post(endpoints.ai.learningPreview, { message, provider, model })).data

export const approveLearningPlan = async (plan) =>
  (await api.post(endpoints.ai.learningApprove, plan)).data

export default {
  getAISettings,
  updateAISettings,
  getCredentials,
  saveCredential,
  deleteCredential,
  getProviderModels,
  listPromptProfiles,
  createPromptProfile,
  updatePromptProfile,
  deletePromptProfile,
  previewLearningPlan,
  approveLearningPlan,
}

export const startLearningPlanAsync = async (payload) => (await api.post(endpoints.ai.learningAsync, payload)).data
export const getTaskStatus = async (taskId) => (await api.get(endpoints.ai.taskStatus(taskId))).data
