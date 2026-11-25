import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useKnowledgeStore } from '../knowledgeStore'
import { knowledgeService } from '@/services/Knowledge/Knowledge'

vi.mock('@/services/Knowledge/Knowledge', () => ({
  knowledgeService: {
    getAll: vi.fn(),
    getById: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    archive: vi.fn(),
    restore: vi.fn(),
    remove: vi.fn(),
    extractMetadata: vi.fn(),
    getFiles: vi.fn(),
    uploadFile: vi.fn(),
    deleteFile: vi.fn(),
    connectTopic: vi.fn(),
    disconnectTopic: vi.fn(),
    archiveAll: vi.fn(),
  },
}))

describe('knowledge store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('normalizes paginated responses and retains pagination metadata', async () => {
    knowledgeService.getAll.mockResolvedValue({
      count: 1,
      next: '/next',
      previous: null,
      results: [{ id: 4 }],
    })
    const store = useKnowledgeStore()
    await store.fetchItems({ search: 'vue' })
    expect(store.items).toEqual([{ id: 4 }])
    expect(store.count).toBe(1)
    expect(store.next).toBe('/next')
    expect(knowledgeService.getAll).toHaveBeenCalledWith({ search: 'vue' })
  })

  it('adds created records and updates existing records', async () => {
    const store = useKnowledgeStore()
    store.items = [{ id: 1, title: 'Old' }]
    knowledgeService.create.mockResolvedValue({ id: 2, title: 'New' })
    knowledgeService.update.mockResolvedValue({ id: 1, title: 'Updated' })
    await store.createItem({ title: 'New' })
    await store.updateItem(1, { title: 'Updated' })
    expect(store.items).toEqual([
      { id: 2, title: 'New' },
      { id: 1, title: 'Updated' },
    ])
    expect(store.count).toBe(1)
  })

  it('removes archived records from the active collection', async () => {
    const store = useKnowledgeStore()
    store.items = [{ id: 1 }, { id: 2 }]
    store.count = 2
    knowledgeService.archive.mockResolvedValue({ id: 1, is_archived: true })
    await store.archiveItem(1)
    expect(store.items).toEqual([{ id: 2 }])
    expect(store.count).toBe(1)
  })

  it('stores uploaded files in the per-knowledge cache', async () => {
    const store = useKnowledgeStore()
    knowledgeService.uploadFile.mockResolvedValue({ id: 7, original_name: 'guide.pdf' })
    await store.uploadFile(3, new File(['content'], 'guide.pdf'))
    expect(store.filesByKnowledgeId[3]).toEqual([{ id: 7, original_name: 'guide.pdf' }])
  })
  it('never sends File objects in the JSON create payload and uploads them via multipart', async () => {
    const store = useKnowledgeStore()
    const file = new File(['content'], 'guide.pdf')
    knowledgeService.create.mockResolvedValue({ id: 9, title: 'Doc' })
    knowledgeService.uploadFile.mockResolvedValue({ id: 70, original_name: 'guide.pdf' })
    await store.createItem({ title: 'Doc', files: [file] })
    expect(knowledgeService.create).toHaveBeenCalledWith({ title: 'Doc' })
    expect(knowledgeService.uploadFile).toHaveBeenCalledWith(9, file, '')
    expect(store.lastUploadReport.uploaded).toHaveLength(1)
    expect(store.lastUploadReport.failed).toHaveLength(0)
  })

  it('reports a failed upload instead of claiming success', async () => {
    const store = useKnowledgeStore()
    knowledgeService.create.mockResolvedValue({ id: 9, title: 'Doc' })
    knowledgeService.uploadFile.mockRejectedValue({
      response: { data: { file: ['Unsupported type'] } },
    })
    await store.createItem({ title: 'Doc', files: [new File(['x'], 'bad.exe')] })
    expect(store.lastUploadReport.uploaded).toHaveLength(0)
    expect(store.lastUploadReport.failed[0]).toEqual({
      name: 'bad.exe',
      message: 'Unsupported type',
    })
  })
})
