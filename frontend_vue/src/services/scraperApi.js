import api from './api'

const unwrap = (response) => response.data
export const scraperApi = {
  sources: (params = {}) => api.get('/scraper/sources/', { params }).then(unwrap),
  stats: () => api.get('/scraper/sources/stats/').then(unwrap),
  createSource: (payload) => api.post('/scraper/sources/', payload).then(unwrap),
  updateSource: (id, payload) => api.patch(`/scraper/sources/${id}/`, payload).then(unwrap),
  deleteSource: (id) => api.delete(`/scraper/sources/${id}/`),
  testSource: (id) => api.post(`/scraper/sources/${id}/test_connection/`).then(unwrap),
  runSource: (id) => api.post(`/scraper/sources/${id}/run/`).then(unwrap),
  runs: (params = {}) => api.get('/scraper/runs/', { params }).then(unwrap),
}
