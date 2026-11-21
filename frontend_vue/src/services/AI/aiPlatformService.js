import aiControl from './aiControl'

// Backward-compatible facade: AI API ownership remains in aiControl.js.
export const getSettings = aiControl.getAISettings
export const saveSettings = aiControl.updateAISettings
export const listCredentials = aiControl.getCredentials
export const saveCredential = aiControl.saveCredential
export const deleteCredential = aiControl.deleteCredential
export const testProvider = aiControl.testProviderConnection
export const listProviders = aiControl.listAIProviders
export const listProviderModels = aiControl.getProviderModels
export const getHealth = aiControl.getAIHealth
export const getCapabilities = aiControl.getAICapabilities
export const getUsage = aiControl.getAIUsage
export const listExecutions = aiControl.listAIExecutions
export const listBudgets = aiControl.listAIBudgets
export const saveBudget = aiControl.createAIBudget
export const updateBudget = aiControl.updateAIBudget
export const deleteBudget = aiControl.deleteAIBudget
export const listAuditLogs = aiControl.listAIAudit
export const sendFeedback = aiControl.submitAIFeedback
export const listWorkflows = aiControl.listAIWorkflows
export const saveWorkflow = aiControl.createAIWorkflow
export const getWorkflow = aiControl.getAIWorkflow
export const updateWorkflow = aiControl.updateAIWorkflow
export const deleteWorkflow = aiControl.deleteAIWorkflow
export const listWorkflowRuns = aiControl.getAIWorkflowRuns
// There is no workflow execution endpoint in the current Django URL configuration.
export const runWorkflow = async () => { throw new Error('Workflow execution is not supported by the current backend API.') }

export default {
  getSettings, saveSettings, listCredentials, saveCredential, deleteCredential,
  testProvider, listProviders, listProviderModels, getHealth, getCapabilities,
  listExecutions, getUsage, listBudgets, saveBudget, updateBudget, deleteBudget,
  listAuditLogs, sendFeedback, listWorkflows, saveWorkflow, getWorkflow,
  updateWorkflow, deleteWorkflow, runWorkflow, listWorkflowRuns,
}
