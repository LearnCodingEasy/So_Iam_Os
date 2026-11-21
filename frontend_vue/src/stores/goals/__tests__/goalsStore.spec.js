import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useGoalsStore } from '../goalsStore'
import * as goalApi from '@/services/Goals/goals'

vi.mock('@/services/Goals/goals', () => ({
  listGoalsPage: vi.fn(),
  getGoalAnalytics: vi.fn(),
}))

describe('goalsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('loads real goals and analytics through the API service', async () => {
    goalApi.listGoalsPage.mockResolvedValue({ count: 1, results: [{ id: 7, title: 'Ship project' }] })
    goalApi.getGoalAnalytics.mockResolvedValue({ total: 1, active: 1, average_progress: 25 })
    const store = useGoalsStore()
    await store.refresh()
    expect(store.items).toHaveLength(1)
    expect(store.items[0].id).toBe(7)
    expect(store.analytics.average_progress).toBe(25)
    expect(goalApi.listGoalsPage).toHaveBeenCalledOnce()
    expect(goalApi.getGoalAnalytics).toHaveBeenCalledOnce()
  })

  it('retains an API error and rethrows it for the UI toast layer', async () => {
    const failure = new Error('API unavailable')
    goalApi.listGoalsPage.mockRejectedValue(failure)
    const store = useGoalsStore()
    await expect(store.fetchGoals()).rejects.toBe(failure)
    expect(store.error).toBe(failure)
    expect(store.loading).toBe(false)
  })
})
