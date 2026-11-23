import api from '@/services/Shared/api'
import { domainEndpoints as e } from '@/services/Shared/endpoints'

// Contract: backend_django/challenges/api/urls.py (mounted at /api/challenges/).
// NOTE: kept as `challenges.js` (not `Challenges.js`) because the project is developed on
// Windows, where a differently-cased twin file would collide on the case-insensitive filesystem.
const BASE = '/challenges'
const data = (r) => r?.data ?? r
const list = (r) => (Array.isArray(data(r)) ? data(r) : data(r)?.results || [])

const resource = (url) => ({
  list: (params = {}) => api.get(url, { params }).then(list),
  create: (payload) => api.post(url, payload).then(data),
  update: (id, payload) => api.patch(`${url}${id}/`, payload).then(data),
  remove: (id) => api.delete(`${url}${id}/`).then(() => undefined),
})

export const challenges = resource(e.challenges)
export const steps = resource(`${BASE}/steps/`)
export const attempts = resource(`${BASE}/attempts/`)
export const progress = resource(`${BASE}/progress/`)

export const completeStep = (id) => api.post(`${e.challenges}${id}/complete-step/`).then(data)

// Backward-compatible export used before the store existed.
export const challengesApi = {
  list: () => challenges.list(),
  create: (p) => challenges.create(p),
  update: (id, p) => challenges.update(id, p),
  remove: (id) => challenges.remove(id),
}

export default { challenges, steps, attempts, progress, completeStep, challengesApi }
