import api from './api'
import { endpoints } from './endpoints'

const list = (data) => (Array.isArray(data) ? data : data?.results || [])
const dataOf = async (request) => (await request).data

export const listJobs = async (params = {}) => list(await dataOf(api.get(endpoints.jobs.opportunities, { params })))
export const getJob = async (id) => dataOf(api.get(endpoints.jobs.opportunity(id)))
export const createJob = async (payload) => dataOf(api.post(endpoints.jobs.opportunities, payload))
export const updateJob = async (id, payload) => dataOf(api.patch(endpoints.jobs.opportunity(id), payload))
export const deleteJob = async (id) => { await api.delete(endpoints.jobs.opportunity(id)); return true }
export const refreshJobMatch = async (id) => dataOf(api.post(endpoints.jobs.refreshMatch(id)))
export const analyzeJob = async (id) => dataOf(api.post(endpoints.jobs.analyze(id)))
export const getReadiness = async (id) => dataOf(api.get(endpoints.jobs.readiness(id)))
export const listSimilarJobs = async (id) => list(await dataOf(api.get(endpoints.jobs.similar(id))))
export const compareJobs = async (ids) => list(await dataOf(api.get(endpoints.jobs.workspaceCompare, { params: { ids: ids.join(',') } })))
export const listMatches = async (params = {}) => list(await dataOf(api.get(endpoints.jobs.matches, { params })))
export const refreshMatches = async () => list(await dataOf(api.post(endpoints.jobs.refreshMatches)))
export const applyToJob = async (id, payload = {}) => dataOf(api.post(endpoints.jobs.apply(id), payload))

export const listApplications = async (params = {}) => list(await dataOf(api.get(endpoints.jobs.applications, { params })))
export const updateApplication = async (id, payload) => dataOf(api.patch(endpoints.jobs.application(id), payload))
export const applicationTimeline = async (id) => list(await dataOf(api.get(endpoints.jobs.applicationTimeline(id))))
export const addApplicationEvent = async (id, payload) => dataOf(api.post(endpoints.jobs.applicationEvent(id), payload))

export const listSources = async () => list(await dataOf(api.get(endpoints.jobs.sources)))
export const createSource = async (payload) => dataOf(api.post(endpoints.jobs.sources, payload))
export const updateSource = async (id, payload) => dataOf(api.patch(endpoints.jobs.source(id), payload))
export const deleteSource = async (id) => { await api.delete(endpoints.jobs.source(id)); return true }
export const testSource = async (id) => dataOf(api.post(endpoints.jobs.sourceTest(id)))
export const syncSource = async (id) => dataOf(api.post(endpoints.jobs.sourceSync(id)))

export const getPreferences = async () => dataOf(api.get(endpoints.jobs.preferences))
export const updatePreferences = async (payload) => dataOf(api.patch(endpoints.jobs.preferencesUpdate, payload))
export const listSavedSearches = async () => list(await dataOf(api.get(endpoints.jobs.savedSearches)))
export const createSavedSearch = async (payload) => dataOf(api.post(endpoints.jobs.savedSearches, payload))
export const runSavedSearch = async (id) => list(await dataOf(api.post(endpoints.jobs.savedSearchRun(id))))

export const listSkillGaps = async (params = {}) => list(await dataOf(api.get(endpoints.jobs.skillGaps, { params })))
export const startSkillLearning = async (id) => dataOf(api.post(endpoints.jobs.skillGapLearning(id)))
export const listReadiness = async () => list(await dataOf(api.get(endpoints.jobs.readiness)))
export const refreshReadiness = async () => list(await dataOf(api.post(endpoints.jobs.readinessRefresh)))

export const listRecommendations = async () => list(await dataOf(api.get(endpoints.jobs.recommendations)))
export const refreshRecommendations = async () => list(await dataOf(api.post(endpoints.jobs.recommendationsRefresh)))
export const saveRecommendation = async (id) => dataOf(api.post(endpoints.jobs.recommendationSave(id)))
export const dismissRecommendation = async (id) => dataOf(api.post(endpoints.jobs.recommendationDismiss(id)))
export const markRecommendationSeen = async (id) => dataOf(api.post(endpoints.jobs.recommendationSeen(id)))

export const listCompanies = async () => list(await dataOf(api.get(endpoints.jobs.companies)))
export const toggleCompanyFollow = async (id) => dataOf(api.post(endpoints.jobs.companyFollow(id)))
export const toggleCompanyBlacklist = async (id) => dataOf(api.post(endpoints.jobs.companyBlacklist(id)))
export const listResumes = async () => list(await dataOf(api.get(endpoints.jobs.resumes)))
export const createResume = async (payload) => dataOf(api.post(endpoints.jobs.resumes, payload))
export const makeResumeDefault = async (id) => dataOf(api.post(endpoints.jobs.resumeDefault(id)))
export const listCoverLetters = async () => list(await dataOf(api.get(endpoints.jobs.coverLetters)))
export const listInterviews = async () => list(await dataOf(api.get(endpoints.jobs.interviews)))
export const listAlerts = async () => list(await dataOf(api.get(endpoints.jobs.alerts)))
export const listAnalytics = async () => list(await dataOf(api.get(endpoints.jobs.analytics)))

export const getDashboard = async () => dataOf(api.get(endpoints.jobs.dashboard))
export const getFeatureCatalog = async () => dataOf(api.get(endpoints.jobs.features))
export const refreshAll = async () => dataOf(api.post(endpoints.jobs.refreshAll))
