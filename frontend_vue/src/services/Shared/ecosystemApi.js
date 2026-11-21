/**
 * Cross-app API facade for Django apps that did not previously have a single
 * consolidated service entry point. Existing app-specific services remain the
 * preferred choice for specialized actions and backward compatibility.
 *
 * Paths are relative to the API base URL configured in services/api.js.
 */
import api from './api'

const normalizeBase = (base) => `/${String(base).replace(/^\/+|\/+$/g, '')}/`
const withId = (base, id) => `${normalizeBase(base)}${encodeURIComponent(id)}/`

function resource(base) {
  const root = normalizeBase(base)
  return {
    list: (params = {}) => api.get(root, { params }),
    retrieve: (id) => api.get(withId(base, id)),
    create: (payload) => api.post(root, payload),
    update: (id, payload) => api.put(withId(base, id), payload),
    patch: (id, payload) => api.patch(withId(base, id), payload),
    remove: (id) => api.delete(withId(base, id)),
    action: (id, action, payload = {}) =>
      api.post(`${withId(base, id)}${String(action).replace(/^\/+|\/+$/g, '')}/`, payload),
    post: (path, payload = {}) => api.post(`${root}${String(path).replace(/^\/+/, '')}`, payload),
    get: (path, params = {}) => api.get(`${root}${String(path).replace(/^\/+/, '')}`, { params }),
  }
}

export const coreApi = {
  health: () => api.get('/core/health/'),
  dashboard: () => api.get('/core/dashboard/'),
  learningSettings: () => api.get('/core/learning-settings/'),
}

export const socialApi = {
  profile: () => api.get('/social/profile/'),
  recommendations: (params = {}) => api.get('/social/recommendations/', { params }),
  get: (path, params = {}) => api.get(`/social/${String(path).replace(/^\/+/, '')}`, { params }),
  post: (path, payload = {}) => api.post(`/social/${String(path).replace(/^\/+/, '')}`, payload),
  patch: (path, payload = {}) => api.patch(`/social/${String(path).replace(/^\/+/, '')}`, payload),
  delete: (path) => api.delete(`/social/${String(path).replace(/^\/+/, '')}`),
}

export const memoryApi = { items: resource('memory/items') }
export const projectsApi = {
  projects: resource('projects/projects'),
  members: resource('projects/members'),
  contexts: resource('projects/contexts'),
}
export const challengesApi = {
  challenges: resource('challenges/challenges'),
  steps: resource('challenges/steps'),
  attempts: resource('challenges/attempts'),
  progress: resource('challenges/progress'),
}
export const financeApi = {
  categories: resource('finance/categories'),
  transactions: resource('finance/transactions'),
  budgets: resource('finance/budgets'),
  debts: resource('finance/debts'),
  savingsGoals: resource('finance/savings-goals'),
  subscriptions: resource('finance/subscriptions'),
  debtPayments: resource('finance/debt-payments'),
  loans: resource('finance/loans'),
  loanPayments: resource('finance/loan-payments'),
  recurringCashflows: resource('finance/recurring-cashflows'),
  profile: resource('finance/profile'),
  habits: resource('finance/habits'),
  alerts: resource('finance/alerts'),
  scenarios: resource('finance/scenarios'),
  health: () => api.get('/finance/health/'),
  forecast: (params = {}) => api.get('/finance/forecast/', { params }),
  forecastScenario: (payload) => api.post('/finance/forecast/scenario/', payload),
  dailySummary: (params = {}) => api.get('/finance/daily-summary/', { params }),
  report: (period) => api.get(`/finance/reports/${encodeURIComponent(period)}/`),
  coach: (payload) => api.post('/finance/ai/coach/', payload),
  refreshAlerts: (payload = {}) => api.post('/finance/alerts/refresh/', payload),
  ecosystem: () => api.get('/finance/ecosystem/'),
  contract: () => api.get('/finance/contract/'),
}

export const appApi = {
  users: resource('users'),
  notifications: resource('notifications'),
  tasks: resource('tasks'),
  goals: resource('goals'),
  learning: resource('learning'),
  knowledge: resource('knowledge'),
  jobs: resource('jobs'),
  ai: resource('ai'),
  codex: resource('codex'),
  automation: resource('automation'),
  codexEndpoint: (path, payload = {}) => api.post(`/codex/${String(path).replace(/^\/+/, '')}`, payload),
  aiEndpoint: (path, payload = {}) => api.post(`/ai/${String(path).replace(/^\/+/, '')}`, payload),
}

export default { coreApi, socialApi, memoryApi, projectsApi, challengesApi, financeApi, appApi }
