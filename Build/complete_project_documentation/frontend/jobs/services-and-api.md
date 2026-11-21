# jobs services and API

Service files found under services/Jobs. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Jobs/jobs.js
L4: const list = (data) => (Array.isArray(data) ? data : data?.results || [])
L5: const dataOf = async (request) => (await request).data
L7: export const listJobs = async (params = {}) =>
L9: export const getJob = async (id) => dataOf(api.get(endpoints.jobs.opportunity(id)))
L10: export const createJob = async (payload) => dataOf(api.post(endpoints.jobs.opportunities, payload))
L11: export const updateJob = async (id, payload) =>
L13: export const deleteJob = async (id) => {
L17: export const refreshJobMatch = async (id) => dataOf(api.post(endpoints.jobs.refreshMatch(id)))
L18: export const analyzeJob = async (id) => dataOf(api.post(endpoints.jobs.analyze(id)))
L19: export const getReadiness = async (id) => dataOf(api.get(endpoints.jobs.opportunityReadiness(id)))
L20: export const listSimilarJobs = async (id) => list(await dataOf(api.get(endpoints.jobs.similar(id))))
L21: export const compareJobs = async (ids) =>
L23: export const listMatches = async (params = {}) =>
L25: export const refreshMatches = async () =>
L27: export const applyToJob = async (id, payload = {}) =>
L29: export const generateCoverLetter = async (id, payload = {}) =>
L31: export const createCoverLetter = async (payload) =>
L33: export const updateCoverLetter = async (id, payload) =>
L36: export const listApplications = async (params = {}) =>
L38: export const updateApplication = async (id, payload) =>
L40: export const applicationTimeline = async (id) =>
L42: export const addApplicationEvent = async (id, payload) =>
L45: export const listSources = async () => list(await dataOf(api.get(endpoints.jobs.sources)))
L46: export const createSource = async (payload) => dataOf(api.post(endpoints.jobs.sources, payload))
L47: export const updateSource = async (id, payload) =>
L49: export const deleteSource = async (id) => {
L53: export const testSource = async (id) => dataOf(api.post(endpoints.jobs.sourceTest(id)))
L54: export const previewSource = async (id) => dataOf(api.post(endpoints.jobs.sourcePreview(id)))
L55: export const syncAllSources = async () => dataOf(api.post(endpoints.jobs.sourcesSyncAll))
L56: export const syncSource = async (id) => dataOf(api.post(endpoints.jobs.sourceSync(id)))
L58: export const getPreferences = async () => dataOf(api.get(endpoints.jobs.preferences))
L59: export const updatePreferences = async (payload) =>
L61: export const listSavedSearches = async () =>
L63: export const createSavedSearch = async (payload) =>
L65: export const runSavedSearch = async (id) =>
L68: export const listSkillGaps = async (params = {}) =>
L70: export const startSkillLearning = async (id) =>
L72: export const listReadiness = async () => list(await dataOf(api.get(endpoints.jobs.readiness)))
L73: export const refreshReadiness = async () =>
L76: export const listRecommendations = async () =>
L78: export const refreshRecommendations = async () =>
L80: export const saveRecommendation = async (id) =>
L82: export const dismissRecommendation = async (id) =>
L84: export const markRecommendationSeen = async (id) =>
L87: export const listCompanies = async () => list(await dataOf(api.get(endpoints.jobs.companies)))
L88: export const toggleCompanyFollow = async (id) => dataOf(api.post(endpoints.jobs.companyFollow(id)))
L89: export const toggleCompanyBlacklist = async (id) =>
L91: export const listResumes = async () => list(await dataOf(api.get(endpoints.jobs.resumes)))
L92: export const createResume = async (payload) => dataOf(api.post(endpoints.jobs.resumes, payload))
L93: export const makeResumeDefault = async (id) => dataOf(api.post(endpoints.jobs.resumeDefault(id)))
L94: export const listCoverLetters = async () => list(await dataOf(api.get(endpoints.jobs.coverLetters)))
L95: export const listInterviews = async () => list(await dataOf(api.get(endpoints.jobs.interviews)))
L96: export const listAlerts = async () => list(await dataOf(api.get(endpoints.jobs.alerts)))
L97: export const listAnalytics = async () => list(await dataOf(api.get(endpoints.jobs.analytics)))
L99: export const getDashboard = async () => dataOf(api.get(endpoints.jobs.dashboard))
L100: export const getFeatureCatalog = async () => dataOf(api.get(endpoints.jobs.features))
L101: export const refreshAll = async () => dataOf(api.post(endpoints.jobs.refreshAll))


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
