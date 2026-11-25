import api from '@/services/Shared/api'

// Paths are relative to the /api base URL (Django: backend_django/urls.py -> api/agents/).
const BASE = '/agents'
const data = (r) => r?.data ?? r
const list = (r) => {
  const d = data(r)
  return Array.isArray(d) ? d : d?.results || []
}

// Agents
export const listAgents = (params = {}) => api.get(`${BASE}/agents/`, { params }).then(list)
export const createAgent = (payload) => api.post(`${BASE}/agents/`, payload).then(data)
export const updateAgent = (id, payload) => api.patch(`${BASE}/agents/${id}/`, payload).then(data)
export const deleteAgent = (id) => api.delete(`${BASE}/agents/${id}/`)

// Configurations (versioned; the backend allocates the version number)
export const listConfigurations = (params = {}) =>
  api.get(`${BASE}/configurations/`, { params }).then(list)
export const createConfiguration = (payload) =>
  api.post(`${BASE}/configurations/`, payload).then(data)
export const updateConfiguration = (id, payload) =>
  api.patch(`${BASE}/configurations/${id}/`, payload).then(data)
export const deleteConfiguration = (id) => api.delete(`${BASE}/configurations/${id}/`)
export const activateConfiguration = (id) =>
  api.post(`${BASE}/configurations/${id}/activate/`).then(data)

// Runs
export const listRuns = (params = {}) => api.get(`${BASE}/runs/`, { params }).then(list)
export const createRun = (payload) => api.post(`${BASE}/runs/`, payload).then(data)
export const deleteRun = (id) => api.delete(`${BASE}/runs/${id}/`)
export const approveRun = (id) => api.post(`${BASE}/runs/${id}/approve/`).then(data)
export const cancelRun = (id) => api.post(`${BASE}/runs/${id}/cancel/`).then(data)
export const executeRun = (id) => api.post(`${BASE}/runs/${id}/execute/`).then(data)

// Executions (read-only step records)
export const listExecutions = (params = {}) => api.get(`${BASE}/executions/`, { params }).then(list)
