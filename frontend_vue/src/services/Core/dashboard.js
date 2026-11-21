import api from '../Shared/api'
import { endpoints } from '../Shared/endpoints'

export const dashboardService = {
  async get() {
    const response = await api.get(endpoints.core.dashboard)
    return response.data
  },
}

export default dashboardService
