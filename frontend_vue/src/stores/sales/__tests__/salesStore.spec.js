import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useSalesStore } from '../salesStore'
import * as salesApi from '@/services/Sales/Sales'

vi.mock('@/services/Sales/Sales', () => {
  const resource = () => ({ list: vi.fn(), create: vi.fn(), update: vi.fn(), remove: vi.fn() })
  return {
    deals: resource(),
    offers: resource(),
    sales: resource(),
    activities: resource(),
    setDealStage: vi.fn(),
    getPipeline: vi.fn(),
    refundSale: vi.fn(),
  }
})

const primeLists = () => {
  salesApi.deals.list.mockResolvedValue([{ id: 1, title: 'Course', stage: 'prospecting' }])
  salesApi.offers.list.mockResolvedValue([])
  salesApi.sales.list.mockResolvedValue([])
  salesApi.activities.list.mockResolvedValue([])
  salesApi.getPipeline.mockResolvedValue({ open_count: 1, win_rate: null, stages: {} })
}

describe('salesStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('loads deals and pipeline from the API service', async () => {
    primeLists()
    const store = useSalesStore()
    await store.fetchAll()
    expect(store.deals[0].title).toBe('Course')
    expect(store.pipeline.open_count).toBe(1)
    expect(store.loading).toBe(false)
  })

  it('keeps the error and rethrows when the API fails', async () => {
    const failure = new Error('API unavailable')
    salesApi.deals.list.mockRejectedValue(failure)
    salesApi.offers.list.mockResolvedValue([])
    salesApi.sales.list.mockResolvedValue([])
    salesApi.activities.list.mockResolvedValue([])
    salesApi.getPipeline.mockResolvedValue({})
    const store = useSalesStore()
    await expect(store.fetchAll()).rejects.toBe(failure)
    expect(store.error).toBe(failure)
    expect(store.loading).toBe(false)
  })

  it('creates or updates through the service, then reloads server state', async () => {
    primeLists()
    salesApi.deals.create.mockResolvedValue({ id: 2 })
    salesApi.deals.update.mockResolvedValue({ id: 1 })
    const store = useSalesStore()
    await store.save('deals', { title: 'New' })
    expect(salesApi.deals.create).toHaveBeenCalledWith({ title: 'New' })
    await store.save('deals', { title: 'Edit' }, 1)
    expect(salesApi.deals.update).toHaveBeenCalledWith(1, { title: 'Edit' })
    expect(salesApi.deals.list).toHaveBeenCalledTimes(2)
  })

  it('moves a deal stage and refunds a sale via the dedicated actions', async () => {
    primeLists()
    salesApi.setDealStage.mockResolvedValue({ id: 1, stage: 'lost' })
    salesApi.refundSale.mockResolvedValue({ id: 5, status: 'refunded' })
    const store = useSalesStore()
    await store.setStage(1, 'lost', 'Price')
    expect(salesApi.setDealStage).toHaveBeenCalledWith(1, 'lost', 'Price')
    await store.refund(5)
    expect(salesApi.refundSale).toHaveBeenCalledWith(5)
  })

  it('removes a row via the service', async () => {
    primeLists()
    salesApi.deals.remove.mockResolvedValue()
    const store = useSalesStore()
    await store.fetchAll()
    await store.remove('deals', 1)
    expect(salesApi.deals.remove).toHaveBeenCalledWith(1)
  })
})
