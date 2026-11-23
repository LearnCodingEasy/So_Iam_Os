import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as salesApi from '@/services/Sales/Sales'

// Resource name -> service collection. Every mutation re-reads server state.
const RESOURCES = { deals: salesApi.deals, offers: salesApi.offers, sales: salesApi.sales, activities: salesApi.activities }

export const useSalesStore = defineStore('sales', () => {
  const deals = ref([])
  const offers = ref([])
  const sales = ref([])
  const activities = ref([])
  const pipeline = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const state = { deals, offers, sales, activities }

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

  async function fetchAll() {
    return run(async () => {
      const [d, o, s, a, p] = await Promise.all([
        salesApi.deals.list(),
        salesApi.offers.list(),
        salesApi.sales.list(),
        salesApi.activities.list(),
        salesApi.getPipeline(),
      ])
      deals.value = d
      offers.value = o
      sales.value = s
      activities.value = a
      pipeline.value = p
    })
  }

  async function fetchPipeline() {
    pipeline.value = await salesApi.getPipeline()
    return pipeline.value
  }

  async function save(resource, payload, id = null) {
    const api = RESOURCES[resource]
    const saved = await run(() => (id ? api.update(id, payload) : api.create(payload)))
    await fetchAll()
    return saved
  }

  async function remove(resource, id) {
    await run(() => RESOURCES[resource].remove(id))
    state[resource].value = state[resource].value.filter((row) => row.id !== id)
    await fetchAll()
  }

  async function setStage(id, stage, lostReason = '') {
    const deal = await run(() => salesApi.setDealStage(id, stage, lostReason))
    await fetchAll() // winning also creates a sale and changes the pipeline
    return deal
  }

  async function refund(id) {
    const sale = await run(() => salesApi.refundSale(id))
    await fetchAll()
    return sale
  }

  return { deals, offers, sales, activities, pipeline, loading, error, fetchAll, fetchPipeline, save, remove, setStage, refund }
})
