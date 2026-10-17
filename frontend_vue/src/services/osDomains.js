import api from './api'
import { domainEndpoints as e } from './endpoints'
const data = r => r?.data ?? r
const list = r => Array.isArray(data(r)) ? data(r) : (data(r)?.results || [])
export const memoryApi = { list:()=>api.get(e.memory).then(list), create:p=>api.post(e.memory,p).then(data), update:(id,p)=>api.patch(`${e.memory}${id}/`,p).then(data), remove:id=>api.delete(`${e.memory}${id}/`) }
export const projectsApi = { list:()=>api.get(e.projects).then(list), create:p=>api.post(e.projects,p).then(data), update:(id,p)=>api.patch(`${e.projects}${id}/`,p).then(data), remove:id=>api.delete(`${e.projects}${id}/`) }
export const challengesApi = { list:()=>api.get(e.challenges).then(list), create:p=>api.post(e.challenges,p).then(data), update:(id,p)=>api.patch(`${e.challenges}${id}/`,p).then(data), remove:id=>api.delete(`${e.challenges}${id}/`) }
export const financeApi = {
  categories: () => api.get(e.financeCategories).then(list),
  category: (id) => api.get(`${e.financeCategories}${id}/`).then(data),
  createCategory: (payload) => api.post(e.financeCategories, payload).then(data),
  updateCategory: (id, payload) => api.patch(`${e.financeCategories}${id}/`, payload).then(data),
  removeCategory: (id) => api.delete(`${e.financeCategories}${id}/`),

  transactions: () => api.get(e.financeTransactions).then(list),
  transaction: (id) => api.get(`${e.financeTransactions}${id}/`).then(data),
  summary: () => api.get(e.financeSummary).then(data),
  dashboard: () => api.get(e.financeDashboard).then(data),
  insights: () => api.get(e.financeInsights).then(data),
  history: (params = {}) => api.get(e.financeHistory, { params }).then(data),
  spending: () => api.get(e.financeSpending).then(data),
  addTransaction: (payload) => api.post(e.financeTransactions, payload).then(data),
  updateTransaction: (id, payload) => api.patch(`${e.financeTransactions}${id}/`, payload).then(data),
  removeTransaction: (id) => api.delete(`${e.financeTransactions}${id}/`),

  budgets: () => api.get(e.financeBudgets).then(list),
  budget: (id) => api.get(`${e.financeBudgets}${id}/`).then(data),
  createBudget: (payload) => api.post(e.financeBudgets, payload).then(data),
  updateBudget: (id, payload) => api.patch(`${e.financeBudgets}${id}/`, payload).then(data),
  removeBudget: (id) => api.delete(`${e.financeBudgets}${id}/`),

  debts: () => api.get(e.financeDebts).then(list),
  debt: (id) => api.get(`${e.financeDebts}${id}/`).then(data),
  debtPayments: (id) => api.get(`${e.financeDebts}${id}/payments/`).then(list),
  payDebt: (id, payload) => api.post(`${e.financeDebts}${id}/pay/`, payload).then(data),
  createDebt: (payload) => api.post(e.financeDebts, payload).then(data),
  updateDebt: (id, payload) => api.patch(`${e.financeDebts}${id}/`, payload).then(data),
  removeDebt: (id) => api.delete(`${e.financeDebts}${id}/`),

  savings: () => api.get(e.financeSavings).then(list),
  savingsGoal: (id) => api.get(`${e.financeSavings}${id}/`).then(data),
  savingPlan: (id) => api.get(`${e.financeSavings}${id}/plan/`).then(data),
  createSavingPlan: (id) => api.post(`${e.financeSavings}${id}/plan/`, {}).then(data),
  createSavings: (payload) => api.post(e.financeSavings, payload).then(data),
  updateSavings: (id, payload) => api.patch(`${e.financeSavings}${id}/`, payload).then(data),
  removeSavings: (id) => api.delete(`${e.financeSavings}${id}/`),

  subscriptions: () => api.get(e.financeSubscriptions).then(list),
  subscription: (id) => api.get(`${e.financeSubscriptions}${id}/`).then(data),
  createSubscription: (payload) => api.post(e.financeSubscriptions, payload).then(data),
  updateSubscription: (id, payload) => api.patch(`${e.financeSubscriptions}${id}/`, payload).then(data),
  removeSubscription: (id) => api.delete(`${e.financeSubscriptions}${id}/`),

  loans: () => api.get(e.financeLoans).then(list),
  createLoan: (payload) => api.post(e.financeLoans, payload).then(data),
  updateLoan: (id, payload) => api.patch(`${e.financeLoans}${id}/`, payload).then(data),
  removeLoan: (id) => api.delete(`${e.financeLoans}${id}/`),
  payLoan: (id, payload) => api.post(`${e.financeLoans}${id}/pay/`, payload).then(data),

  recurringCashflows: () => api.get(e.financeRecurringCashflows).then(list),
  createRecurringCashflow: (payload) => api.post(e.financeRecurringCashflows, payload).then(data),
  updateRecurringCashflow: (id, payload) => api.patch(`${e.financeRecurringCashflows}${id}/`, payload).then(data),
  removeRecurringCashflow: (id) => api.delete(`${e.financeRecurringCashflows}${id}/`),

  profile: () => api.get(e.financeProfile).then(list),
  updateProfile: (id, payload) => api.patch(`${e.financeProfile}${id}/`, payload).then(data),

  habits: () => api.get(e.financeHabits).then(list),
  createHabit: (payload) => api.post(e.financeHabits, payload).then(data),
  updateHabit: (id, payload) => api.patch(`${e.financeHabits}${id}/`, payload).then(data),
  removeHabit: (id) => api.delete(`${e.financeHabits}${id}/`),

  alerts: () => api.get(e.financeAlerts).then(list),
  markAlertRead: (id) => api.post(`${e.financeAlerts}${id}/mark_read/`).then(data),
  refreshAlerts: () => api.post(e.financeAlertsRefresh).then(list),

  scenarios: () => api.get(e.financeScenarios).then(list),
  createScenario: (payload) => api.post(e.financeScenarios, payload).then(data),

  health: () => api.get(e.financeHealth).then(data),
  forecast: (months = 6) => api.get(e.financeForecast, { params: { months } }).then(data),
  scenario: (payload) => api.post(e.financeForecastScenario, payload).then(data),
  dailySummary: () => api.get(e.financeDailySummary).then(data),
  weeklyReport: () => api.get(e.financeWeeklyReport).then(data),
  monthlyReport: () => api.get(e.financeMonthlyReport).then(data),
  coach: (question) => api.post(e.financeCoach, { question }).then(data),
  ecosystem: () => api.get(e.financeEcosystem).then(data),
  contract: () => api.get(e.financeContract).then(data),

  aiInsights: (payload) => api.post(e.financeAiInsights, payload).then(data),
}
export const aiAgentApi = { plan:p=>api.post(e.aiAgentPlan,p).then(data) }
