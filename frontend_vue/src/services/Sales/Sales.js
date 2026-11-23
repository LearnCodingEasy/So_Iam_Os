import api from '@/services/Shared/api'

// All paths are relative to the API base (".../api"). Contract: backend_django/sales/api/urls.py
const unwrap = (r) => r?.data ?? r
const asList = (payload) => (Array.isArray(payload) ? payload : payload?.results || [])

const resource = (base) => ({
  list: async (params = {}) => asList(unwrap(await api.get(`${base}/`, { params }))),
  create: async (payload) => unwrap(await api.post(`${base}/`, payload)),
  update: async (id, payload) => unwrap(await api.patch(`${base}/${id}/`, payload)),
  remove: async (id) => {
    await api.delete(`${base}/${id}/`)
  },
})

export const offers = resource('/sales/offers')
export const deals = resource('/sales/deals')
export const sales = resource('/sales/sales')
export const activities = resource('/sales/activities')

export const setDealStage = async (id, stage, lostReason = '') =>
  unwrap(await api.post(`/sales/deals/${id}/set-stage/`, { stage, lost_reason: lostReason }))
export const getPipeline = async () => unwrap(await api.get('/sales/deals/pipeline/'))
export const refundSale = async (id) => unwrap(await api.post(`/sales/sales/${id}/refund/`))

export default { offers, deals, sales, activities, setDealStage, getPipeline, refundSale }
