import api from './api'

export default {
  list() {
    return api.get('automation/tasks/')
  },
  get(id) {
    return api.get(`automation/tasks/${id}/`)
  },
  create(data) {
    return api.post('automation/tasks/', data)
  },
}
