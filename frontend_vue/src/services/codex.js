import api from '@/services/api'
import { endpoints } from '@/services/endpoints'
const list = (data) =>
  Array.isArray(data) ? data : Array.isArray(data?.results) ? data.results : []
export default {
  overview: async () => (await api.get(endpoints.codex.overview)).data,
  scan: async () => (await api.post(endpoints.codex.scan)).data,
  context: async () => (await api.get(endpoints.codex.context)).data,
  features: async () => list((await api.get(endpoints.codex.features)).data),
  files: async () => list((await api.get(endpoints.codex.files)).data),
  apis: async () => list((await api.get(endpoints.codex.apis)).data),
  protected: async () => list((await api.get(endpoints.codex.protected)).data),
  changes: async () => list((await api.get(endpoints.codex.changes)).data),
  snapshots: async () => list((await api.get(endpoints.codex.snapshots)).data),
  planChange: async (payload) => (await api.post(endpoints.codex.planChange, payload)).data,
  createSnapshot: async (payload) => (await api.post(endpoints.codex.createSnapshot, payload)).data,
  async askOpenAI(message) {
    const response = await api.post('/codex/ai/', {
      message,
    })

    return response.data
  },
}
