import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAiToolsLaboratoryStore } from '../aiToolsLaboratoryStore'
import * as labApi from '@/services/AI_Tools_Laboratory/AI_Tools_Laboratory'

vi.mock('@/services/AI_Tools_Laboratory/AI_Tools_Laboratory', () => {
  const resource = () => ({ list: vi.fn(), create: vi.fn(), update: vi.fn(), remove: vi.fn() })
  return {
    categoriesApi: resource(),
    toolsApi: { ...resource(), summary: vi.fn() },
    configurationsApi: resource(),
    executionsApi: resource(),
  }
})

describe('aiToolsLaboratoryStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    labApi.categoriesApi.list.mockResolvedValue([])
    labApi.toolsApi.list.mockResolvedValue([{ id: 1, name: 'Tool A' }])
    labApi.configurationsApi.list.mockResolvedValue([])
    labApi.executionsApi.list.mockResolvedValue([])
    labApi.toolsApi.summary.mockResolvedValue({ tools_total: 1 })
  })

  it('loads every resource and the summary from the API', async () => {
    const store = useAiToolsLaboratoryStore()
    await store.refresh()
    expect(store.tools).toEqual([{ id: 1, name: 'Tool A' }])
    expect(store.summary.tools_total).toBe(1)
  })

  it('creates through the API and then reloads the list', async () => {
    labApi.toolsApi.create.mockResolvedValue({ id: 2 })
    const store = useAiToolsLaboratoryStore()
    await store.save('tools', { name: 'B' })
    expect(labApi.toolsApi.create).toHaveBeenCalledWith({ name: 'B' })
    expect(labApi.toolsApi.list).toHaveBeenCalled()
    expect(labApi.toolsApi.summary).toHaveBeenCalled()
  })

  it('updates when an id is given', async () => {
    labApi.toolsApi.update.mockResolvedValue({ id: 1 })
    const store = useAiToolsLaboratoryStore()
    await store.save('tools', { name: 'C' }, 1)
    expect(labApi.toolsApi.update).toHaveBeenCalledWith(1, { name: 'C' })
  })

  it('keeps the error and rethrows when the API rejects', async () => {
    const failure = new Error('400')
    labApi.toolsApi.create.mockRejectedValue(failure)
    const store = useAiToolsLaboratoryStore()
    await expect(store.save('tools', {})).rejects.toBe(failure)
    expect(store.error).toBe(failure)
  })

  it('refreshes dependent lists after deleting a tool', async () => {
    labApi.toolsApi.remove.mockResolvedValue(true)
    const store = useAiToolsLaboratoryStore()
    await store.remove('tools', 1)
    expect(labApi.configurationsApi.list).toHaveBeenCalled()
    expect(labApi.executionsApi.list).toHaveBeenCalled()
  })
})
