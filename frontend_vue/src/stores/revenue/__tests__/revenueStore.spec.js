import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useRevenueStore } from '../revenueStore'
import * as api from '@/services/Revenue/Revenue'

vi.mock('@/services/Revenue/Revenue', () => {
  const crud = () => ({ list: vi.fn(), create: vi.fn(), update: vi.fn(), remove: vi.fn() })
  return {
    sourcesApi: crud(),
    streamsApi: crud(),
    recordsApi: crud(),
    recurringApi: crud(),
    getSummary: vi.fn(),
    getMrr: vi.fn(),
    recordFromSale: vi.fn(),
  }
})

const seed = () => {
  api.sourcesApi.list.mockResolvedValue([{ id: 1, name: 'Mentoring' }])
  api.streamsApi.list.mockResolvedValue([{ id: 2, name: '1:1' }])
  api.recordsApi.list.mockResolvedValue([{ id: 3, amount: '100.00' }])
  api.recurringApi.list.mockResolvedValue([{ id: 4, amount: '1200.00' }])
  api.getSummary.mockResolvedValue({ totals: { USD: '100.00' } })
  api.getMrr.mockResolvedValue({ mrr: { USD: '100.00' } })
}

describe('revenueStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    seed()
  })

  it('loads all collections, summary and MRR from the API', async () => {
    const store = useRevenueStore()
    await store.fetchAll()
    expect(store.sources[0].name).toBe('Mentoring')
    expect(store.records[0].amount).toBe('100.00')
    expect(store.summary.totals.USD).toBe('100.00')
    expect(store.mrr.mrr.USD).toBe('100.00')
    expect(store.loading).toBe(false)
  })

  it('keeps and rethrows API errors', async () => {
    api.sourcesApi.list.mockRejectedValue(new Error('down'))
    const store = useRevenueStore()
    await expect(store.fetchAll()).rejects.toThrow('down')
    expect(store.error.message).toBe('down')
    expect(store.loading).toBe(false)
  })

  it('creates and updates through the service then reloads', async () => {
    api.recordsApi.create.mockResolvedValue({ id: 9 })
    const store = useRevenueStore()
    await store.save('records', { amount: '5.00', received_on: '2026-01-01' })
    expect(api.recordsApi.create).toHaveBeenCalledOnce()
    await store.save('records', { amount: '6.00' }, 9)
    expect(api.recordsApi.update).toHaveBeenCalledWith(9, { amount: '6.00' })
    expect(api.recordsApi.list).toHaveBeenCalledTimes(2)
  })

  it('reloads dependants after deleting a source', async () => {
    const store = useRevenueStore()
    await store.remove('sources', 1)
    expect(api.sourcesApi.remove).toHaveBeenCalledWith(1)
    expect(api.streamsApi.list).toHaveBeenCalled()
    expect(api.recurringApi.list).toHaveBeenCalled()
  })

  it('attributes a sale and refreshes records', async () => {
    api.recordFromSale.mockResolvedValue({ id: 3 })
    const store = useRevenueStore()
    await store.recordFromSale(12)
    expect(api.recordFromSale).toHaveBeenCalledWith(12)
    expect(store.records).toHaveLength(1)
  })
})
