import api from '@/services/Shared/api'

const BASE = '/marketing'
const data = (r) => r?.data ?? r
const list = (r) => {
  const d = data(r)
  return Array.isArray(d) ? d : d?.results || []
}
const withId = (path, id) => `${BASE}/${path}/${id}/`

const resource = (path) => ({
  list: (params = {}) => api.get(`${BASE}/${path}/`, { params }).then(list),
  create: (payload) => api.post(`${BASE}/${path}/`, payload).then(data),
  update: (id, payload) => api.patch(withId(path, id), payload).then(data),
  remove: (id) => api.delete(withId(path, id)),
})

export const channels = resource('channels')
export const campaigns = resource('campaigns')
export const content = resource('content')
export const leadSources = resource('lead-sources')

export const getCampaignOverview = () => api.get(`${BASE}/campaigns/overview/`).then(data)
export const getCampaignPerformance = (id) =>
  api.get(`${BASE}/campaigns/${id}/performance/`).then(data)
export const publishContent = (id) => api.post(`${BASE}/content/${id}/publish/`).then(data)

export const marketingApi = {
  channels,
  campaigns,
  content,
  leadSources,
  getCampaignOverview,
  getCampaignPerformance,
  publishContent,
}
export default marketingApi
