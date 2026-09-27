import api from './api'
import { endpoints } from './endpoints'

export const dashboardService = {
  async get() {
    const response = await api.get(endpoints.core.dashboard)
    return response.data
  },
}

export default dashboardService
