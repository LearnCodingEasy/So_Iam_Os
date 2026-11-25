import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useMarketingStore } from '../marketingStore'
import * as api from '@/services/Marketing/Marketing'

vi.mock('@/services/Marketing/Marketing', () => {
  const res = () => ({ list: vi.fn(), create: vi.fn(), update: vi.fn(), remove: vi.fn() })
  return {
    campaigns: res(),
    content: res(),
    leadSources: res(),
    channels: res(),
    getCampaignOverview: vi.fn(),
    getCampaignPerformance: vi.fn(),
    publishContent: vi.fn(),
  }
})

describe('marketingStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    api.getCampaignOverview.mockResolvedValue({ campaigns: 1 })
  })

  it('loads every collection and the overview from the API', async () => {
    api.campaigns.list.mockResolvedValue([{ id: 1, name: 'Launch' }])
    api.content.list.mockResolvedValue([])
    api.leadSources.list.mockResolvedValue([])
    api.channels.list.mockResolvedValue([])
    const store = useMarketingStore()
    await store.fetchAll()
    expect(store.campaigns[0].name).toBe('Launch')
    expect(store.overview.campaigns).toBe(1)
    expect(store.loading).toBe(false)
  })

  it('keeps the error and rethrows when loading fails', async () => {
    api.campaigns.list.mockRejectedValue(new Error('down'))
    api.content.list.mockResolvedValue([])
    api.leadSources.list.mockResolvedValue([])
    api.channels.list.mockResolvedValue([])
    const store = useMarketingStore()
    await expect(store.fetchAll()).rejects.toThrow('down')
    expect(store.error.message).toBe('down')
    expect(store.loading).toBe(false)
  })

  it('does not change local state when the server rejects a save', async () => {
    api.campaigns.create.mockRejectedValue(new Error('400'))
    const store = useMarketingStore()
    await expect(store.save('campaigns', { name: '' })).rejects.toThrow('400')
    expect(store.campaigns).toEqual([])
  })

  it('creates, updates and deletes using server responses', async () => {
    const store = useMarketingStore()
    api.campaigns.create.mockResolvedValue({ id: 5, name: 'A' })
    await store.save('campaigns', { name: 'A' })
    api.campaigns.update.mockResolvedValue({ id: 5, name: 'B' })
    await store.save('campaigns', { name: 'B' }, 5)
    expect(store.campaigns).toEqual([{ id: 5, name: 'B' }])
    api.campaigns.remove.mockResolvedValue()
    await store.remove('campaigns', 5)
    expect(store.campaigns).toEqual([])
  })

  it('replaces content with the server copy after publish', async () => {
    const store = useMarketingStore()
    store.content = [{ id: 2, status: 'draft' }]
    api.publishContent.mockResolvedValue({ id: 2, status: 'published', published_at: 'now' })
    await store.publish(2)
    expect(store.content[0].status).toBe('published')
  })
})
