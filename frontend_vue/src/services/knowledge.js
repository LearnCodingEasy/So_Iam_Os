import api from './api'

// ===================================================
// 🧠 Knowledge API
// ===================================================

export const knowledgeService = {
  // -----------------------------------------------
  // 📚 Get all knowledge
  // -----------------------------------------------

  async getAll(params = {}) {
    const response = await api.get('/knowledge/items/', {
      params,
    })

    return response.data
  },

  // -----------------------------------------------
  // 🔎 Get knowledge by ID
  // -----------------------------------------------

  async getById(id) {
    const response = await api.get(`/knowledge/items/${id}/`)

    return response.data
  },

  // -----------------------------------------------
  // ➕ Create knowledge
  // -----------------------------------------------

  async create(data) {
    const response = await api.post('/knowledge/items/', data)

    return response.data
  },

  // -----------------------------------------------
  // ✏️ Update knowledge
  // -----------------------------------------------

  async update(id, data) {
    const response = await api.patch(`/knowledge/items/${id}/`, data)

    return response.data
  },

  // -----------------------------------------------
  // 🗃️ Archive knowledge
  // -----------------------------------------------

  async archive(id) {
    await api.delete(`/knowledge/items/${id}/`)

    return true
  },
}
