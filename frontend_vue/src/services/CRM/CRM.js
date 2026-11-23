import api from '@/services/Shared/api'

const data = (r) => r?.data ?? r
const rows = (r) => {
  const d = data(r)
  return Array.isArray(d) ? d : d?.results || []
}
const clean = (params = {}) =>
  Object.fromEntries(Object.entries(params).filter(([, v]) => v !== '' && v != null))

const BASE = '/crm'

function resource(name) {
  const url = `${BASE}/${name}/`
  return {
    list: (params) => api.get(url, { params: clean(params) }).then(rows),
    create: (payload) => api.post(url, payload).then(data),
    update: (id, payload) => api.patch(`${url}${id}/`, payload).then(data),
    remove: (id) => api.delete(`${url}${id}/`),
  }
}

export const companies = resource('companies')
export const contacts = resource('contacts')
export const interactions = resource('interactions')
export const relationships = resource('relationships')

export const listFollowUps = (days = 7) =>
  api.get(`${BASE}/interactions/follow-ups/`, { params: { days } }).then(rows)
export const getPipeline = () => api.get(`${BASE}/relationships/pipeline/`).then(data)
