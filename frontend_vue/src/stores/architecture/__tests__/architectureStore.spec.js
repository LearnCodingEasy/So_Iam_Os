import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useArchitectureStore } from '../architectureStore'
import * as api from '@/services/Architecture/Architecture'

vi.mock('@/services/Architecture/Architecture', () => ({
  listArchitectures: vi.fn(),
  createArchitecture: vi.fn(),
  updateArchitecture: vi.fn(),
  deleteArchitecture: vi.fn(),
  getArchitectureGraph: vi.fn(),
  listComponents: vi.fn(),
  createComponent: vi.fn(),
  updateComponent: vi.fn(),
  deleteComponent: vi.fn(),
  listDependencies: vi.fn(),
  createDependency: vi.fn(),
  updateDependency: vi.fn(),
  deleteDependency: vi.fn(),
  listDecisions: vi.fn(),
  createDecision: vi.fn(),
  updateDecision: vi.fn(),
  deleteDecision: vi.fn(),
}))

describe('architectureStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('loads architectures from the API service', async () => {
    api.listArchitectures.mockResolvedValue([{ id: 1, name: 'Core' }])
    const store = useArchitectureStore()
    await store.fetchArchitectures()
    expect(store.architectures).toEqual([{ id: 1, name: 'Core' }])
    expect(store.loading).toBe(false)
  })

  it('keeps and rethrows API errors', async () => {
    const failure = new Error('down')
    api.listArchitectures.mockRejectedValue(failure)
    const store = useArchitectureStore()
    await expect(store.fetchArchitectures()).rejects.toBe(failure)
    expect(store.error).toBe(failure)
    expect(store.loading).toBe(false)
  })

  it('loads detail data and only keeps dependencies of the selected architecture', async () => {
    api.listComponents.mockResolvedValue([{ id: 10 }, { id: 11 }])
    api.listDependencies.mockResolvedValue([
      { id: 1, source: 10, target: 11 },
      { id: 2, source: 99, target: 98 },
    ])
    api.listDecisions.mockResolvedValue([{ id: 5 }])
    api.getArchitectureGraph.mockResolvedValue({ nodes: [], edges: [], metrics: {} })
    const store = useArchitectureStore()
    await store.selectArchitecture(3)
    expect(api.listComponents).toHaveBeenCalledWith({ architecture: 3 })
    expect(store.dependencies.map((d) => d.id)).toEqual([1])
    expect(store.decisions).toHaveLength(1)
    expect(store.graph).toEqual({ nodes: [], edges: [], metrics: {} })
  })

  it('reloads the selected architecture after a child mutation', async () => {
    api.listComponents.mockResolvedValue([])
    api.listDependencies.mockResolvedValue([])
    api.listDecisions.mockResolvedValue([])
    api.getArchitectureGraph.mockResolvedValue({})
    api.createComponent.mockResolvedValue({ id: 1 })
    const store = useArchitectureStore()
    await store.selectArchitecture(3)
    await store.saveChild('component', { architecture: 3, name: 'api' })
    expect(api.createComponent).toHaveBeenCalledWith({ architecture: 3, name: 'api' })
    expect(api.listComponents).toHaveBeenCalledTimes(2)
  })
})
