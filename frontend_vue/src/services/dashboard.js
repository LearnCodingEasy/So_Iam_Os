import api from './api'

export const dashboardService = {
  async get() {
    const response = await api.get('/core/dashboard/')
    return response.data
  },
}
