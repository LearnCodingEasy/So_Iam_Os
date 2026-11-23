import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAgentsStore } from '../agentsStore'
import * as agentsApi from '@/services/Agents/Agents'

vi.mock('@/services/Agents/Agents', () => ({
  listAgents: vi.fn(),
  listRuns: vi.fn(),
  listConfigurations: vi.fn(),
  listExecutions: vi.fn(),
  createAgent: vi.fn(),
  updateAgent: vi.fn(),
  deleteAgent: vi.fn(),
  createConfiguration: vi.fn(),
  activateConfiguration: vi.fn(),
  createRun: vi.fn(),
  approveRun: vi.fn(),
  cancelRun: vi.fn(),
  executeRun: vi.fn(),
}))

describe('agentsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    agentsApi.listAgents.mockResolvedValue([])
    agentsApi.listRuns.mockResolvedValue([])
  })

  it('loads agents and runs from the API service', async () => {
    agentsApi.listAgents.mockResolvedValue([{ id: 1, name: 'Researcher' }])
    agentsApi.listRuns.mockResolvedValue([{ id: 5, status: 'pending' }])
    const store = useAgentsStore()
    await store.refresh()
    expect(store.agents[0].name).toBe('Researcher')
    expect(store.runs[0].id).toBe(5)
  })

  it('creates when no id is given, updates otherwise, then reloads', async () => {
    const store = useAgentsStore()
    agentsApi.createAgent.mockResolvedValue({ id: 2 })
    await store.saveAgent({ name: 'New' })
    expect(agentsApi.createAgent).toHaveBeenCalledWith({ name: 'New' })
    agentsApi.updateAgent.mockResolvedValue({ id: 2 })
    await store.saveAgent({ name: 'Renamed' }, 2)
    expect(agentsApi.updateAgent).toHaveBeenCalledWith(2, { name: 'Renamed' })
    expect(agentsApi.listAgents).toHaveBeenCalledTimes(2)
  })

  it('routes run actions to the matching endpoint', async () => {
    agentsApi.executeRun.mockResolvedValue({ id: 5, status: 'succeeded' })
    const store = useAgentsStore()
    const run = await store.runAction('execute', 5)
    expect(agentsApi.executeRun).toHaveBeenCalledWith(5)
    expect(run.status).toBe('succeeded')
  })

  it('keeps the API error and rethrows it', async () => {
    const failure = new Error('409')
    agentsApi.approveRun.mockRejectedValue(failure)
    const store = useAgentsStore()
    await expect(store.runAction('approve', 5)).rejects.toBe(failure)
    expect(store.error).toBe(failure)
    expect(store.loading).toBe(false)
  })
})
