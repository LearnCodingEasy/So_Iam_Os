import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from '@/services/Architecture/Architecture'

export const useArchitectureStore = defineStore('architecture', () => {
  const architectures = ref([])
  const selectedId = ref(null)
  const components = ref([])
  const dependencies = ref([])
  const decisions = ref([])
  const graph = ref(null)
  const loading = ref(false)
  const detailLoading = ref(false)
  const error = ref(null)

  async function track(flag, fn) {
    flag.value = true
    error.value = null
    try {
      return await fn()
    } catch (cause) {
      error.value = cause
      throw cause
    } finally {
      flag.value = false
    }
  }

  const fetchArchitectures = (params = {}) =>
    track(loading, async () => {
      architectures.value = await api.listArchitectures(params)
      return architectures.value
    })

  // Loads components, dependencies, decisions and graph of one architecture.
  const selectArchitecture = (id) =>
    track(detailLoading, async () => {
      selectedId.value = id
      if (id == null) {
        components.value = []
        dependencies.value = []
        decisions.value = []
        graph.value = null
        return
      }
      const [c, d, dec, g] = await Promise.all([
        api.listComponents({ architecture: id }),
        api.listDependencies(),
        api.listDecisions({ architecture: id }),
        api.getArchitectureGraph(id),
      ])
      components.value = c
      const ids = new Set(c.map((x) => x.id))
      dependencies.value = d.filter((x) => ids.has(x.source))
      decisions.value = dec
      graph.value = g
    })

  const reloadSelected = () => (selectedId.value == null ? null : selectArchitecture(selectedId.value))

  async function saveArchitecture(payload, id = null) {
    const saved = id ? await api.updateArchitecture(id, payload) : await api.createArchitecture(payload)
    await fetchArchitectures()
    return saved
  }

  async function removeArchitecture(id) {
    await api.deleteArchitecture(id)
    if (selectedId.value === id) await selectArchitecture(null)
    await fetchArchitectures()
  }

  // Generic child-resource mutations; the detail data is reloaded so the graph stays accurate.
  const childApi = {
    component: [api.createComponent, api.updateComponent, api.deleteComponent],
    dependency: [api.createDependency, api.updateDependency, api.deleteDependency],
    decision: [api.createDecision, api.updateDecision, api.deleteDecision],
  }

  async function saveChild(kind, payload, id = null) {
    const [create, update] = childApi[kind]
    const saved = id ? await update(id, payload) : await create(payload)
    await reloadSelected()
    return saved
  }

  async function removeChild(kind, id) {
    await childApi[kind][2](id)
    await reloadSelected()
  }

  return {
    architectures, selectedId, components, dependencies, decisions, graph,
    loading, detailLoading, error,
    fetchArchitectures, selectArchitecture, saveArchitecture, removeArchitecture, saveChild, removeChild,
  }
})
