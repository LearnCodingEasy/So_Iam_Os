import api from './api'
import { endpoints } from './endpoints'

// ===================================================
// 🧠 Knowledge API
// ===================================================

export const knowledgeService = {
  // -----------------------------------------------
  // 📚 Get all knowledge
  // -----------------------------------------------
  async getAll(params = {}) {
    const response = await api.get(endpoints.knowledge.items, {
      params,
    })

    return response.data
  },

  // -----------------------------------------------
  // 🔎 Get knowledge by ID
  // -----------------------------------------------
  async getById(id) {
    const response = await api.get(endpoints.knowledge.item(id))
    return response.data
  },

  // -----------------------------------------------
  // ➕ Create knowledge
  // -----------------------------------------------
  async create(data) {
    const response = await api.post(endpoints.knowledge.items, data)
    return response.data
  },

  // -----------------------------------------------
  // ✏️ Update knowledge
  // -----------------------------------------------
  async update(id, data) {
    const response = await api.patch(endpoints.knowledge.item(id), data)

    return response.data
  },

  // -----------------------------------------------
  // 🗃️ Archive knowledge
  // -----------------------------------------------
  async archive(id) {
    const response = await api.post(endpoints.knowledge.archive(id))
    return response.data
  },

  async restore(id) {
    const response = await api.post(endpoints.knowledge.restore(id))
    return response.data
  },

  async remove(id) {
    await api.delete(endpoints.knowledge.item(id))
    return true
  },

  // -----------------------------------------------
  // 📎 Get files
  // -----------------------------------------------
  async getFiles(knowledgeId) {
    const response = await api.get(endpoints.knowledge.itemFiles(knowledgeId))

    return response.data
  },

  // -----------------------------------------------
  // 📤 Upload file
  // -----------------------------------------------
  async uploadFile(knowledgeId, file, description = '') {
    const formData = new FormData()

    formData.append('file', file)

    if (description) {
      formData.append('description', description)
    }

    const response = await api.post(endpoints.knowledge.uploadFile(knowledgeId), formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    return response.data
  },

  // -----------------------------------------------
  // 📤 Upload multiple files
  // -----------------------------------------------
  async uploadFiles(knowledgeId, files = []) {
    const uploaded = []

    for (const file of files) {
      const result = await this.uploadFile(knowledgeId, file)

      uploaded.push(result)
    }

    return uploaded
  },

  // -----------------------------------------------
  // 🗑️ Delete file
  // -----------------------------------------------
  async deleteFile(fileId) {
    await api.delete(endpoints.knowledge.file(fileId))
    return true
  },

  // -----------------------------------------------
  // 🔗 Get knowledge for a learning topic
  // -----------------------------------------------
  async getByLearningTopic(topicId) {
    const response = await api.get(endpoints.knowledge.items, {
      params: {
        learning_topic: topicId,
      },
    })

    return response.data
  },
}
