import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from '@/services/Marketing/Marketing'

export const useMarketingStore = defineStore('marketing', () => {
  const campaigns = ref([])
  const content = ref([])
  const leadSources = ref([])
  const channels = ref([])
  const overview = ref(null)
  const performance = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function run(fn) {
    error.value = null
    try {
      return await fn()
    } catch (cause) {
      error.value = cause
      throw cause
    }
  }

  async function fetchAll() {
    loading.value = true
    try {
      await run(async () => {
        const [c, ct, l, ch, o] = await Promise.all([
          api.campaigns.list(),
          api.content.list(),
          api.leadSources.list(),
          api.channels.list(),
          api.getCampaignOverview(),
        ])
        campaigns.value = c
        content.value = ct
        leadSources.value = l
        channels.value = ch
        overview.value = o
      })
    } finally {
      loading.value = false
    }
  }

  async function refreshOverview() {
    overview.value = await run(() => api.getCampaignOverview())
  }

  const targets = { campaigns, content, leadSources, channels }

  // Persist through the API first; local state only changes after the server accepts it.
  async function save(kind, payload, id = null) {
    const svc = api[kind]
    const saved = await run(() => (id ? svc.update(id, payload) : svc.create(payload)))
    const rows = targets[kind]
    rows.value = id ? rows.value.map((r) => (r.id === id ? saved : r)) : [saved, ...rows.value]
    if (kind === 'campaigns') await refreshOverview().catch(() => {})
    return saved
  }

  async function remove(kind, id) {
    await run(() => api[kind].remove(id))
    targets[kind].value = targets[kind].value.filter((r) => r.id !== id)
    if (kind === 'campaigns') await refreshOverview().catch(() => {})
  }

  async function publish(id) {
    const saved = await run(() => api.publishContent(id))
    content.value = content.value.map((r) => (r.id === id ? saved : r))
    await refreshOverview().catch(() => {})
    return saved
  }

  async function loadPerformance(id) {
    performance.value = await run(() => api.getCampaignPerformance(id))
    return performance.value
  }

  return {
    campaigns,
    content,
    leadSources,
    channels,
    overview,
    performance,
    loading,
    error,
    fetchAll,
    refreshOverview,
    save,
    remove,
    publish,
    loadPerformance,
  }
})
