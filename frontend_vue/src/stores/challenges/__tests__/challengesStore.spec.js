import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useChallengesStore } from '../challengesStore'
import * as api from '@/services/Challenges/challenges'

vi.mock('@/services/Challenges/challenges', () => {
  const resource = () => ({ list: vi.fn(), create: vi.fn(), update: vi.fn(), remove: vi.fn() })
  return { challenges: resource(), steps: resource(), attempts: resource(), progress: resource(), completeStep: vi.fn() }
})

const prime = () => {
  api.challenges.list.mockResolvedValue([{ id: 1, title: 'Build API', steps: [] }])
  api.attempts.list.mockResolvedValue([])
  api.progress.list.mockResolvedValue([{ id: 1, challenge: 1, progress_percent: 50 }])
}

describe('challengesStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('loads challenges, attempts and progress from the API service', async () => {
    prime()
    const store = useChallengesStore()
    await store.fetchAll()
    expect(store.challenges[0].title).toBe('Build API')
    expect(store.progress[0].progress_percent).toBe(50)
    expect(store.loading).toBe(false)
  })

  it('keeps the error and rethrows when the API fails', async () => {
    api.challenges.list.mockRejectedValue(new Error('API unavailable'))
    api.attempts.list.mockResolvedValue([])
    api.progress.list.mockResolvedValue([])
    const store = useChallengesStore()
    await expect(store.fetchAll()).rejects.toThrow('API unavailable')
    expect(store.error.message).toBe('API unavailable')
    expect(store.loading).toBe(false)
  })

  it('creates through the service then re-reads server state', async () => {
    prime()
    api.challenges.create.mockResolvedValue({ id: 2 })
    const store = useChallengesStore()
    await store.save('challenges', { title: 'New' })
    expect(api.challenges.create).toHaveBeenCalledWith({ title: 'New' })
    expect(api.challenges.list).toHaveBeenCalledTimes(1)
  })

  it('updates when an id is given', async () => {
    prime()
    api.steps.update.mockResolvedValue({ id: 5 })
    const store = useChallengesStore()
    await store.save('steps', { title: 'Renamed' }, 5)
    expect(api.steps.update).toHaveBeenCalledWith(5, { title: 'Renamed' })
  })

  it('completeStep calls the backend action and refreshes progress', async () => {
    prime()
    api.completeStep.mockResolvedValue({ completed_steps: 1, progress_percent: 50 })
    const store = useChallengesStore()
    const row = await store.completeStep(1)
    expect(api.completeStep).toHaveBeenCalledWith(1)
    expect(row.progress_percent).toBe(50)
    expect(api.progress.list).toHaveBeenCalledTimes(1)
  })

  it('removes through the service then re-reads server state', async () => {
    prime()
    api.challenges.remove.mockResolvedValue(undefined)
    const store = useChallengesStore()
    await store.remove('challenges', 1)
    expect(api.challenges.remove).toHaveBeenCalledWith(1)
    expect(api.challenges.list).toHaveBeenCalledTimes(1)
  })
})
