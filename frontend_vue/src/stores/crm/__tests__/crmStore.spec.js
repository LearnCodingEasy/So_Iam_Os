import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useCrmStore } from '../crmStore'
import * as crmApi from '@/services/CRM/CRM'

vi.mock('@/services/CRM/CRM', () => {
  const resource = () => ({ list: vi.fn(), create: vi.fn(), update: vi.fn(), remove: vi.fn() })
  return {
    contacts: resource(),
    companies: resource(),
    interactions: resource(),
    relationships: resource(),
    listFollowUps: vi.fn(),
    getPipeline: vi.fn(),
  }
})

describe('crmStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    crmApi.contacts.list.mockResolvedValue([])
    crmApi.interactions.list.mockResolvedValue([])
    crmApi.relationships.list.mockResolvedValue([])
    crmApi.listFollowUps.mockResolvedValue([])
    crmApi.getPipeline.mockResolvedValue({ total: 0, stages: {} })
  })

  it('loads contacts from the API service', async () => {
    crmApi.contacts.list.mockResolvedValue([{ id: 1, first_name: 'Ada' }])
    const store = useCrmStore()
    await store.fetchContacts({ search: 'ada' })
    expect(store.contacts[0].first_name).toBe('Ada')
    expect(crmApi.contacts.list).toHaveBeenCalledWith({ search: 'ada' })
    expect(store.loading).toBe(false)
  })

  it('keeps the error and rethrows it', async () => {
    const failure = new Error('down')
    crmApi.contacts.list.mockRejectedValue(failure)
    const store = useCrmStore()
    await expect(store.fetchContacts()).rejects.toBe(failure)
    expect(store.error).toBe(failure)
    expect(store.loading).toBe(false)
  })

  it('creates then reloads, and updates by id', async () => {
    crmApi.contacts.create.mockResolvedValue({ id: 2 })
    crmApi.contacts.update.mockResolvedValue({ id: 2 })
    const store = useCrmStore()
    await store.save('contacts', { first_name: 'Bob' })
    expect(crmApi.contacts.create).toHaveBeenCalledWith({ first_name: 'Bob' })
    await store.save('contacts', { job_title: 'CTO' }, 2)
    expect(crmApi.contacts.update).toHaveBeenCalledWith(2, { job_title: 'CTO' })
    expect(crmApi.contacts.list).toHaveBeenCalledTimes(2)
  })

  it('refreshes pipeline after a relationship change', async () => {
    crmApi.relationships.update.mockResolvedValue({ id: 1 })
    const store = useCrmStore()
    await store.save('relationships', { stage: 'customer' }, 1)
    expect(crmApi.getPipeline).toHaveBeenCalled()
  })

  it('removes and reloads', async () => {
    crmApi.interactions.remove.mockResolvedValue({})
    const store = useCrmStore()
    await store.remove('interactions', 5)
    expect(crmApi.interactions.remove).toHaveBeenCalledWith(5)
    expect(crmApi.listFollowUps).toHaveBeenCalled()
  })
})
