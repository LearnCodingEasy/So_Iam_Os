import api from './api'
import { endpoints } from './endpoints'

const unwrap = (response) => response.data
const list = (response) => {
  const data = response.data
  return Array.isArray(data) ? data : (Array.isArray(data?.results) ? data.results : [])
}

export const scraperApi = {
  sources: async (params = {}) => list(await api.get(endpoints.scraper.sources, { params })),
  stats: async () => unwrap(await api.get(endpoints.scraper.stats)),
  createSource: async (payload) => unwrap(await api.post(endpoints.scraper.sources, payload)),
  updateSource: async (id, payload) => unwrap(await api.patch(endpoints.scraper.source(id), payload)),
  deleteSource: (id) => api.delete(endpoints.scraper.source(id)),
  testSource: async (id) => unwrap(await api.post(endpoints.scraper.testSource(id))),
  runSource: async (id) => unwrap(await api.post(endpoints.scraper.runSource(id))),
  runs: async (params = {}) => list(await api.get(endpoints.scraper.runs, { params })),
  run: async (id) => unwrap(await api.get(endpoints.scraper.run(id))),
  runResults: async (id) => list(await api.get(endpoints.scraper.runResults(id))),
  selectors: async (params = {}) => list(await api.get(endpoints.scraper.selectors, { params })),
  createSelector: async (payload) => unwrap(await api.post(endpoints.scraper.selectors, payload)),
  updateSelector: async (id, payload) => unwrap(await api.patch(endpoints.scraper.selector(id), payload)),
  deleteSelector: (id) => api.delete(endpoints.scraper.selector(id)),
  configs: async (params = {}) => list(await api.get(endpoints.scraper.configs, { params })),
  createConfig: async (payload) => unwrap(await api.post(endpoints.scraper.configs, payload)),
  updateConfig: async (id, payload) => unwrap(await api.patch(endpoints.scraper.config(id), payload)),
  deleteConfig: (id) => api.delete(endpoints.scraper.config(id)),
}
