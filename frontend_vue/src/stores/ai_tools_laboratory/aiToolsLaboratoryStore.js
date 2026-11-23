import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as labApi from '@/services/AI_Tools_Laboratory/AI_Tools_Laboratory'

const apis = {
  categories: labApi.categoriesApi,
  tools: labApi.toolsApi,
  configurations: labApi.configurationsApi,
  executions: labApi.executionsApi,
}

export const useAiToolsLaboratoryStore = defineStore('ai_tools_laboratory', () => {
  const state = {
    categories: ref([]),
    tools: ref([]),
    configurations: ref([]),
    executions: ref([]),
  }
  const summary = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function guarded(fn) {
    error.value = null
    try {
      return await fn()
    } catch (cause) {
      error.value = cause
      throw cause
    }
  }

  async function fetchAll(resource, params = {}) {
    loading.value = true
    try {
      const result = await guarded(() => apis[resource].list(params))
      state[resource].value = result
      return result
    } finally {
      loading.value = false
    }
  }

  async function fetchSummary() {
    summary.value = await guarded(() => labApi.toolsApi.summary())
    return summary.value
  }

  // Create/update/delete always go to Django first; local lists are refreshed
  // from the server afterwards so the UI never shows unsaved state.
  async function save(resource, payload, id = null) {
    const saved = await guarded(() =>
      id ? apis[resource].update(id, payload) : apis[resource].create(payload),
    )
    await fetchAll(resource)
    if (resource !== 'categories') await fetchSummary().catch(() => {})
    return saved
  }

  async function remove(resource, id) {
    await guarded(() => apis[resource].remove(id))
    // Deleting a tool cascades to its configurations and executions.
    const refresh = resource === 'tools' ? ['tools', 'configurations', 'executions'] : [resource]
    await Promise.all(refresh.map((name) => fetchAll(name)))
    if (resource !== 'categories') await fetchSummary().catch(() => {})
  }

  async function refresh() {
    await Promise.all([
      fetchAll('categories'),
      fetchAll('tools'),
      fetchAll('configurations'),
      fetchAll('executions'),
      fetchSummary(),
    ])
  }

  return {
    categories: state.categories,
    tools: state.tools,
    configurations: state.configurations,
    executions: state.executions,
    summary,
    loading,
    error,
    fetchAll,
    fetchSummary,
    save,
    remove,
    refresh,
  }
})
