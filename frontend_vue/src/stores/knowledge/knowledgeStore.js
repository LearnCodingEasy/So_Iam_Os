import { defineStore } from 'pinia'
import { ref } from 'vue'
import { knowledgeService } from '@/services/Knowledge/Knowledge'

function unwrapList(payload) {
  if (Array.isArray(payload)) return payload
  return Array.isArray(payload?.results) ? payload.results : []
}

// Browser File objects cannot travel inside a JSON body (JSON.stringify turns
// them into `{}`), so they are separated from the item payload and uploaded
// through the multipart `upload-file` endpoint after the item is persisted.
function splitFiles(data = {}) {
  const { files, ...payload } = data || {}
  const pending = Array.isArray(files)
    ? files.filter((f) => typeof File !== 'undefined' && f instanceof File)
    : []
  return { payload, pending }
}

export const useKnowledgeStore = defineStore('knowledge', () => {
  const items = ref([])
  const count = ref(0)
  const next = ref(null)
  const previous = ref(null)
  const filesByKnowledgeId = ref({})
  const loading = ref(false)
  const saving = ref(false)
  const error = ref(null)
  // Result of the most recent save: which files the backend confirmed and which failed.
  const lastUploadReport = ref({ uploaded: [], failed: [] })

  async function uploadPending(knowledgeId, pending) {
    const report = { uploaded: [], failed: [] }
    for (const file of pending) {
      try {
        // Success is only recorded after the backend returns the persisted record.
        const saved = await uploadFile(knowledgeId, file)
        report.uploaded.push(saved)
      } catch (cause) {
        const data = cause?.response?.data
        const message =
          data?.file?.[0] || data?.file || data?.detail || cause?.message || 'Upload failed'
        report.failed.push({ name: file.name, message: String(message) })
      }
    }
    lastUploadReport.value = report
    return report
  }

  async function fetchItems(params = {}) {
    loading.value = true
    error.value = null
    try {
      const payload = await knowledgeService.getAll(params)
      items.value = unwrapList(payload)
      count.value = payload?.count ?? items.value.length
      next.value = payload?.next ?? null
      previous.value = payload?.previous ?? null
      return items.value
    } catch (cause) {
      error.value = cause
      throw cause
    } finally {
      loading.value = false
    }
  }

  async function fetchItem(id) {
    return knowledgeService.getById(id)
  }

  async function createItem(data) {
    saving.value = true
    error.value = null
    try {
      const { payload, pending } = splitFiles(data)
      const created = await knowledgeService.create(payload)
      items.value = [created, ...items.value.filter((item) => item.id !== created.id)]
      count.value += 1
      await uploadPending(created.id, pending)
      return created
    } catch (cause) {
      error.value = cause
      throw cause
    } finally {
      saving.value = false
    }
  }

  async function updateItem(id, data) {
    saving.value = true
    error.value = null
    try {
      const { payload, pending } = splitFiles(data)
      const updated = await knowledgeService.update(id, payload)
      items.value = items.value.map((item) => (item.id === id ? updated : item))
      await uploadPending(id, pending)
      return updated
    } catch (cause) {
      error.value = cause
      throw cause
    } finally {
      saving.value = false
    }
  }

  async function archiveItem(id) {
    const archived = await knowledgeService.archive(id)
    items.value = items.value.filter((item) => item.id !== id)
    count.value = Math.max(0, count.value - 1)
    return archived
  }

  async function restoreItem(id) {
    const restored = await knowledgeService.restore(id)
    items.value = [restored, ...items.value.filter((item) => item.id !== id)]
    count.value += 1
    return restored
  }

  async function deleteItem(id) {
    await knowledgeService.remove(id)
    items.value = items.value.filter((item) => item.id !== id)
    count.value = Math.max(0, count.value - 1)
  }

  async function extractItemMetadata(id) {
    const result = await knowledgeService.extractMetadata(id)
    const updated = result?.item
    if (updated) items.value = items.value.map((item) => (item.id === id ? updated : item))
    return result
  }

  async function fetchFiles(knowledgeId, force = false) {
    if (!force && filesByKnowledgeId.value[knowledgeId]) {
      return filesByKnowledgeId.value[knowledgeId]
    }
    const files = await knowledgeService.getFiles(knowledgeId)
    filesByKnowledgeId.value = { ...filesByKnowledgeId.value, [knowledgeId]: unwrapList(files) }
    return filesByKnowledgeId.value[knowledgeId]
  }

  async function uploadFile(knowledgeId, file, description = '') {
    const uploaded = await knowledgeService.uploadFile(knowledgeId, file, description)
    const current = filesByKnowledgeId.value[knowledgeId] || []
    filesByKnowledgeId.value = {
      ...filesByKnowledgeId.value,
      [knowledgeId]: [uploaded, ...current],
    }
    return uploaded
  }

  async function deleteFile(fileId, knowledgeId) {
    await knowledgeService.deleteFile(fileId)
    if (knowledgeId != null && filesByKnowledgeId.value[knowledgeId]) {
      filesByKnowledgeId.value = {
        ...filesByKnowledgeId.value,
        [knowledgeId]: filesByKnowledgeId.value[knowledgeId].filter((file) => file.id !== fileId),
      }
    }
  }

  async function connectTopic(knowledgeId, topicId) {
    const result = await knowledgeService.connectTopic(knowledgeId, topicId)
    await fetchItem(knowledgeId).then((updated) => {
      items.value = items.value.map((item) => (item.id === knowledgeId ? updated : item))
    })
    return result
  }

  async function disconnectTopic(knowledgeId, topicId) {
    const result = await knowledgeService.disconnectTopic(knowledgeId, topicId)
    await fetchItem(knowledgeId).then((updated) => {
      items.value = items.value.map((item) => (item.id === knowledgeId ? updated : item))
    })
    return result
  }

  async function archiveAll(params = {}) {
    const result = await knowledgeService.archiveAll(params)
    items.value = []
    count.value = 0
    return result
  }

  function clearError() {
    error.value = null
  }

  return {
    items,
    count,
    next,
    previous,
    filesByKnowledgeId,
    loading,
    saving,
    error,
    fetchItems,
    fetchItem,
    createItem,
    updateItem,
    archiveItem,
    restoreItem,
    deleteItem,
    extractItemMetadata,
    fetchFiles,
    uploadFile,
    deleteFile,
    lastUploadReport,
    connectTopic,
    disconnectTopic,
    archiveAll,
    clearError,
  }
})
