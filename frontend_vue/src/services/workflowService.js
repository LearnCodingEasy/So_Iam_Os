// src/services/workflowService.js

import api from './api'

export default {
  list() {
    return api.get('automation/workflows/')
  },
  get(id) {
    return api.get(`automation/workflows/${id}/`)
  },
  create(data) {
    return api.post('automation/workflows/', data)
  },
  start(id) {
    return api.post(`automation/workflows/${id}/start/`)
  },
}
