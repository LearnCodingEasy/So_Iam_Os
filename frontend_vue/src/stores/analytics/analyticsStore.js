import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as analyticsApi from '@/services/Analytics/Analytics'

export const useAnalyticsStore = defineStore('analytics', () => {
  const metrics = ref([])
  const snapshots = ref([])
  const events = ref([])
  const reports = ref([])
  const eventCounts = ref({ total: 0, events: [] })
  const summary = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function run(task) {
    loading.value = true
    error.value = null
    try {
      return await task()
    } catch (cause) {
      error.value = cause
      throw cause
    } finally {
      loading.value = false
    }
  }

  const fetchMetrics = (params) =>
    run(async () => (metrics.value = await analyticsApi.listMetrics(params)))
  const fetchEvents = (params) =>
    run(async () => (events.value = await analyticsApi.listEvents(params)))
  const fetchReports = (params) =>
    run(async () => (reports.value = await analyticsApi.listReports(params)))
  const fetchEventCounts = (params) =>
    run(async () => (eventCounts.value = await analyticsApi.getEventCounts(params)))
  const fetchSnapshots = (metricId) =>
    run(
      async () =>
        (snapshots.value = await analyticsApi.listSnapshots(metricId ? { metric: metricId } : {})),
    )
  const fetchSummary = (metricId, params) =>
    run(async () => (summary.value = await analyticsApi.getMetricSummary(metricId, params)))

  async function refresh() {
    await Promise.all([fetchMetrics(), fetchEvents(), fetchReports(), fetchEventCounts()])
  }

  async function saveMetric(payload, id = null) {
    const saved = await run(() =>
      id ? analyticsApi.updateMetric(id, payload) : analyticsApi.createMetric(payload),
    )
    await fetchMetrics()
    return saved
  }
  async function removeMetric(id) {
    await run(() => analyticsApi.deleteMetric(id))
    metrics.value = metrics.value.filter((m) => m.id !== id)
  }
  async function addSnapshot(payload) {
    const saved = await run(() => analyticsApi.createSnapshot(payload))
    await fetchSnapshots(payload.metric)
    return saved
  }
  async function addEvent(payload) {
    const saved = await run(() => analyticsApi.createEvent(payload))
    await Promise.all([fetchEvents(), fetchEventCounts()])
    return saved
  }
  async function saveReport(payload, id = null) {
    const saved = await run(() =>
      id ? analyticsApi.updateReport(id, payload) : analyticsApi.createReport(payload),
    )
    await fetchReports()
    return saved
  }
  async function removeReport(id) {
    await run(() => analyticsApi.deleteReport(id))
    reports.value = reports.value.filter((r) => r.id !== id)
  }
  async function generateReport(id) {
    const report = await run(() => analyticsApi.generateReport(id))
    reports.value = reports.value.map((r) => (r.id === id ? report : r))
    return report
  }

  return {
    metrics,
    snapshots,
    events,
    reports,
    eventCounts,
    summary,
    loading,
    error,
    fetchMetrics,
    fetchEvents,
    fetchReports,
    fetchEventCounts,
    fetchSnapshots,
    fetchSummary,
    refresh,
    saveMetric,
    removeMetric,
    addSnapshot,
    addEvent,
    saveReport,
    removeReport,
    generateReport,
  }
})
