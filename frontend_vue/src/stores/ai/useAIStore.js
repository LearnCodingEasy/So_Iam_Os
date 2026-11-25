import { defineStore } from 'pinia'
import { ref } from 'vue'
import aiControl from '@/services/AI/aiControl'

const asArray = (value) => (Array.isArray(value) ? value : value?.results || [])

export const useAIStore = defineStore('ai-management', () => {
  const providers = ref([])
  const credentials = ref([])
  const settings = ref(null)
  const conversations = ref([])
  const executions = ref([])
  const usage = ref({})
  const budgets = ref([])
  const audit = ref([])
  const workflows = ref([])
  const health = ref(null)
  const capabilities = ref([])
  const loading = ref(false)
  const error = ref(null)
  let activeLoads = 0
  const beginLoad = () => {
    activeLoads += 1
    loading.value = true
  }
  const endLoad = () => {
    activeLoads = Math.max(0, activeLoads - 1)
    loading.value = activeLoads > 0
  }

  async function refreshControl() {
    beginLoad()
    error.value = null
    try {
      const [providerResult, credentialResult, settingResult, healthResult, capabilityResult] =
        await Promise.all([
          aiControl.listAIProviders(),
          aiControl.getCredentials(),
          aiControl.getAISettings(),
          aiControl.getAIHealth(),
          aiControl.getAICapabilities(),
        ])
      providers.value = asArray(providerResult?.providers || providerResult)
      credentials.value = asArray(credentialResult)
      settings.value = settingResult
      health.value = healthResult
      capabilities.value = asArray(capabilityResult?.features || capabilityResult)
      return true
    } catch (cause) {
      error.value = cause
      throw cause
    } finally {
      endLoad()
    }
  }

  async function refreshOperations() {
    beginLoad()
    error.value = null
    try {
      const [executionResult, usageResult, budgetResult, auditResult, workflowResult] =
        await Promise.all([
          aiControl.listAIExecutions(),
          aiControl.getAIUsage(),
          aiControl.listAIBudgets(),
          aiControl.listAIAudit(),
          aiControl.listAIWorkflows(),
        ])
      executions.value = asArray(executionResult)
      usage.value = usageResult || {}
      budgets.value = asArray(budgetResult)
      audit.value = asArray(auditResult)
      workflows.value = asArray(workflowResult)
      return true
    } catch (cause) {
      error.value = cause
      throw cause
    } finally {
      endLoad()
    }
  }

  async function refreshAll() {
    await Promise.all([refreshControl(), refreshOperations()])
  }

  return {
    providers,
    credentials,
    settings,
    conversations,
    executions,
    usage,
    budgets,
    audit,
    workflows,
    health,
    capabilities,
    loading,
    error,
    refreshControl,
    refreshOperations,
    refreshAll,
  }
})

export default useAIStore
