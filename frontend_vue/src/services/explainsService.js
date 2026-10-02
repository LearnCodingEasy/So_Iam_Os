// src/services/explainsService.js
import api from './api'

const explainService = {
  /**
    // Params
    list(params = {}) {
      return api.get('/explain/explains/', params)
    },
    list() {
      return api.get('/explain/explains/')
    },
  */
  // All List
  async list() {
    const res = await api.get('/explain/explains/')
    console.log('API DATA 👉', res.data)
    return res.data
  },
  get(id) {
    return api.get(`/explain/explains/${id}/`)
  },
  create(data) {
    return api.post('/explain/explains/', data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  update(id, data) {
    return api.put(`/explain/explains/${id}/`, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  delete(id) {
    return api.delete(`/explain/explains/${id}/`)
  },
  // ExplainCategory
  async listExplainCategory() {
    const res = await api.get('/explain/explains_category/')
    console.log('API DATA 👉', res.data)
    return res.data
  },
}

export default explainService
