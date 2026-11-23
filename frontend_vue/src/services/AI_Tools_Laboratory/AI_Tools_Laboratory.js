import api from '@/services/Shared/api'

// Django: backend_django/ai_tools_laboratory/api/urls.py, mounted at /api/ai-tools/
const BASE = '/ai-tools'

const data = (response) => response?.data ?? response
const rows = (response) => {
  const body = data(response)
  return Array.isArray(body) ? body : body?.results || []
}

function resource(path) {
  const root = `${BASE}/${path}/`
  return {
    list: (params = {}) => api.get(root, { params }).then(rows),
    get: (id) => api.get(`${root}${id}/`).then(data),
    create: (payload) => api.post(root, payload).then(data),
    update: (id, payload) => api.patch(`${root}${id}/`, payload).then(data),
    remove: (id) => api.delete(`${root}${id}/`).then(() => true),
  }
}

export const categoriesApi = resource('categories')
export const toolsApi = {
  ...resource('tools'),
  summary: () => api.get(`${BASE}/tools/summary/`).then(data),
}
export const configurationsApi = resource('configurations')
export const executionsApi = resource('executions')
