import api from '@/services/Shared/api'

const data = (r) => r?.data ?? r
const list = (r) => {
  const d = data(r)
  return Array.isArray(d) ? d : d?.results || []
}

const BASE = '/revenue'
export const revenueEndpoints = {
  sources: `${BASE}/sources/`,
  streams: `${BASE}/streams/`,
  records: `${BASE}/records/`,
  recurring: `${BASE}/recurring/`,
  summary: `${BASE}/records/summary/`,
  fromSale: `${BASE}/records/from-sale/`,
  mrr: `${BASE}/recurring/mrr/`,
}

const crud = (url) => ({
  list: (params = {}) => api.get(url, { params }).then(list),
  create: (payload) => api.post(url, payload).then(data),
  update: (id, payload) => api.patch(`${url}${id}/`, payload).then(data),
  remove: (id) => api.delete(`${url}${id}/`),
})

export const sourcesApi = crud(revenueEndpoints.sources)
export const streamsApi = crud(revenueEndpoints.streams)
export const recordsApi = crud(revenueEndpoints.records)
export const recurringApi = crud(revenueEndpoints.recurring)

export const getSummary = (params = {}) => api.get(revenueEndpoints.summary, { params }).then(data)
export const getMrr = () => api.get(revenueEndpoints.mrr).then(data)
export const recordFromSale = (saleId) => api.post(revenueEndpoints.fromSale, { sale: saleId }).then(data)
