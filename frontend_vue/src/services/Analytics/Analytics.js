import api from '@/services/Shared/api'

const data = (r) => r?.data ?? r
const list = (r) => (Array.isArray(data(r)) ? data(r) : data(r)?.results || [])

const BASE = '/analytics'

// Metrics
export const listMetrics = (params = {}) => api.get(`${BASE}/metrics/`, { params }).then(list)
export const createMetric = (payload) => api.post(`${BASE}/metrics/`, payload).then(data)
export const updateMetric = (id, payload) => api.patch(`${BASE}/metrics/${id}/`, payload).then(data)
export const deleteMetric = (id) => api.delete(`${BASE}/metrics/${id}/`)
export const getMetricSummary = (id, params = {}) =>
  api.get(`${BASE}/metrics/${id}/summary/`, { params }).then(data)

// Snapshots
export const listSnapshots = (params = {}) => api.get(`${BASE}/snapshots/`, { params }).then(list)
export const createSnapshot = (payload) => api.post(`${BASE}/snapshots/`, payload).then(data)
export const deleteSnapshot = (id) => api.delete(`${BASE}/snapshots/${id}/`)

// Events
export const listEvents = (params = {}) => api.get(`${BASE}/events/`, { params }).then(list)
export const createEvent = (payload) => api.post(`${BASE}/events/`, payload).then(data)
export const deleteEvent = (id) => api.delete(`${BASE}/events/${id}/`)
export const getEventCounts = (params = {}) => api.get(`${BASE}/events/counts/`, { params }).then(data)

// Reports
export const listReports = (params = {}) => api.get(`${BASE}/reports/`, { params }).then(list)
export const createReport = (payload) => api.post(`${BASE}/reports/`, payload).then(data)
export const updateReport = (id, payload) => api.patch(`${BASE}/reports/${id}/`, payload).then(data)
export const deleteReport = (id) => api.delete(`${BASE}/reports/${id}/`)
export const generateReport = (id) => api.post(`${BASE}/reports/${id}/generate/`).then(data)
