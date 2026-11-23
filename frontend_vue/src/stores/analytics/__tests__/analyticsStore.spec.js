import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAnalyticsStore } from '../analyticsStore'
import * as api from '@/services/Analytics/Analytics'

vi.mock('@/services/Analytics/Analytics', () => ({
  listMetrics: vi.fn(),
  listEvents: vi.fn(),
  listReports: vi.fn(),
  getEventCounts: vi.fn(),
  listSnapshots: vi.fn(),
  getMetricSummary: vi.fn(),
  createMetric: vi.fn(),
  updateMetric: vi.fn(),
  deleteMetric: vi.fn(),
  createSnapshot: vi.fn(),
  createEvent: vi.fn(),
  createReport: vi.fn(),
  updateReport: vi.fn(),
  deleteReport: vi.fn(),
  generateReport: vi.fn(),
}))

describe('analyticsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('refresh loads metrics, events, reports and event counts from the API', async () => {
    api.listMetrics.mockResolvedValue([{ id: 1, key: 'mrr' }])
    api.listEvents.mockResolvedValue([])
    api.listReports.mockResolvedValue([{ id: 2, title: 'Weekly' }])
    api.getEventCounts.mockResolvedValue({ total: 2, events: [{ name: 'a', count: 2 }] })
    const store = useAnalyticsStore()
    await store.refresh()
    expect(store.metrics[0].key).toBe('mrr')
    expect(store.reports).toHaveLength(1)
    expect(store.eventCounts.total).toBe(2)
    expect(store.loading).toBe(false)
  })

  it('keeps the error and rethrows it', async () => {
    const failure = new Error('down')
    api.listMetrics.mockRejectedValue(failure)
    const store = useAnalyticsStore()
    await expect(store.fetchMetrics()).rejects.toBe(failure)
    expect(store.error).toBe(failure)
  })

  it('saveMetric creates without id and updates with id, then reloads', async () => {
    api.createMetric.mockResolvedValue({ id: 1 })
    api.updateMetric.mockResolvedValue({ id: 1 })
    api.listMetrics.mockResolvedValue([])
    const store = useAnalyticsStore()
    await store.saveMetric({ key: 'k', name: 'K' })
    await store.saveMetric({ name: 'K2' }, 1)
    expect(api.createMetric).toHaveBeenCalledWith({ key: 'k', name: 'K' })
    expect(api.updateMetric).toHaveBeenCalledWith(1, { name: 'K2' })
    expect(api.listMetrics).toHaveBeenCalledTimes(2)
  })

  it('removeMetric drops the row and generateReport replaces the report', async () => {
    api.deleteMetric.mockResolvedValue()
    api.generateReport.mockResolvedValue({ id: 2, generated_at: 'now' })
    const store = useAnalyticsStore()
    store.metrics = [{ id: 1 }, { id: 3 }]
    store.reports = [{ id: 2, generated_at: null }]
    await store.removeMetric(1)
    await store.generateReport(2)
    expect(store.metrics).toEqual([{ id: 3 }])
    expect(store.reports[0].generated_at).toBe('now')
  })
})
