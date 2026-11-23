import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as revenueApi from '@/services/Revenue/Revenue'

const collections = {
  sources: revenueApi.sourcesApi,
  streams: revenueApi.streamsApi,
  records: revenueApi.recordsApi,
  recurring: revenueApi.recurringApi,
}

export const useRevenueStore = defineStore('revenue', () => {
  const sources = ref([])
  const streams = ref([])
  const records = ref([])
  const recurring = ref([])
  const summary = ref(null)
  const mrr = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const state = { sources, streams, records, recurring }

  async function run(fn) {
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

  async function fetchAll(params = {}) {
    return run(async () => {
      const [s, st, r, rec, sum, m] = await Promise.all([
        revenueApi.sourcesApi.list(),
        revenueApi.streamsApi.list(),
        revenueApi.recordsApi.list(),
        revenueApi.recurringApi.list(),
        revenueApi.getSummary(params),
        revenueApi.getMrr(),
      ])
      sources.value = s
      streams.value = st
      records.value = r
      recurring.value = rec
      summary.value = sum
      mrr.value = m
    })
  }

  async function refreshTotals(params = {}) {
    const [sum, m] = await Promise.all([revenueApi.getSummary(params), revenueApi.getMrr()])
    summary.value = sum
    mrr.value = m
  }

  // kind is one of: sources | streams | records | recurring
  async function save(kind, payload, id = null) {
    return run(async () => {
      const api = collections[kind]
      const saved = id ? await api.update(id, payload) : await api.create(payload)
      state[kind].value = await api.list()
      await refreshTotals()
      return saved
    })
  }

  async function remove(kind, id) {
    return run(async () => {
      await collections[kind].remove(id)
      state[kind].value = await collections[kind].list()
      // deleting a source/stream cascades server-side, so reload dependants
      if (kind === 'sources') streams.value = await revenueApi.streamsApi.list()
      if (kind === 'sources' || kind === 'streams') recurring.value = await revenueApi.recurringApi.list()
      if (kind === 'sources' || kind === 'streams') records.value = await revenueApi.recordsApi.list()
      await refreshTotals()
    })
  }

  async function recordFromSale(saleId) {
    return run(async () => {
      const record = await revenueApi.recordFromSale(saleId)
      records.value = await revenueApi.recordsApi.list()
      await refreshTotals()
      return record
    })
  }

  return {
    sources, streams, records, recurring, summary, mrr, loading, error,
    fetchAll, refreshTotals, save, remove, recordFromSale,
  }
})
