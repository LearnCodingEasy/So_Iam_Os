import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as agentsApi from '@/services/Agents/Agents'

export const useAgentsStore = defineStore('agents', () => {
  const agents = ref([])
  const configurations = ref([])
  const runs = ref([])
  const executions = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function track(fn) {
    loading.value = true
    error.value = null
    try {
      return await fn()
    } catch (cause) {
      error.value = cause
      throw cause
    } finally {
      loading.value = false
    }
  }

  const fetchAgents = (params) =>
    track(async () => (agents.value = await agentsApi.listAgents(params)))
  const fetchConfigurations = (params) =>
    track(async () => (configurations.value = await agentsApi.listConfigurations(params)))
  const fetchRuns = (params) => track(async () => (runs.value = await agentsApi.listRuns(params)))
  const fetchExecutions = (runId) =>
    track(async () => (executions.value = await agentsApi.listExecutions({ run: runId })))

  async function refresh() {
    await Promise.all([fetchAgents(), fetchRuns()])
  }

  async function saveAgent(payload, id = null) {
    const saved = await track(() =>
      id ? agentsApi.updateAgent(id, payload) : agentsApi.createAgent(payload),
    )
    await fetchAgents()
    return saved
  }

  async function removeAgent(id) {
    await track(() => agentsApi.deleteAgent(id))
    await Promise.all([fetchAgents(), fetchRuns()])
  }

  async function addConfiguration(payload) {
    const saved = await track(() => agentsApi.createConfiguration(payload))
    await fetchConfigurations({ agent: payload.agent })
    return saved
  }

  async function activateConfiguration(configuration) {
    const saved = await track(() => agentsApi.activateConfiguration(configuration.id))
    await fetchConfigurations({ agent: configuration.agent })
    return saved
  }

  async function startRun(payload) {
    const run = await track(() => agentsApi.createRun(payload))
    await fetchRuns()
    return run
  }

  // approve / cancel / execute all return the updated run
  async function runAction(action, id) {
    const fn = { approve: agentsApi.approveRun, cancel: agentsApi.cancelRun, execute: agentsApi.executeRun }[action]
    const run = await track(() => fn(id))
    await fetchRuns()
    return run
  }

  return {
    agents, configurations, runs, executions, loading, error,
    fetchAgents, fetchConfigurations, fetchRuns, fetchExecutions, refresh,
    saveAgent, removeAgent, addConfiguration, activateConfiguration, startRun, runAction,
  }
})
