# learning services and API

Service files found under services/Learning. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Learning/learning.js
L8: const normalizeList = (data) => {
L20: const getErrorMessage = (error, fallback = 'Something went wrong.') => {
L33: export async function getLearningDashboard() {
L73: export async function getLearningTopic(topicId) {
L74: const response = await api.get(endpoints.learning.topic(topicId))
L79: export async function createLearningTopic(payload) {
L80: const response = await api.post(endpoints.learning.topics, payload)
L85: export async function updateLearningTopic(topicId, payload) {
L86: const response = await api.patch(endpoints.learning.topic(topicId), payload)
L91: export async function deleteLearningTopic(topicId) {
L95: export async function startLearningTopic(topicId) {
L96: const response = await api.post(endpoints.learning.topicStart(topicId))
L100: export async function completeLearningTopic(topicId) {
L101: const response = await api.post(endpoints.learning.topicComplete(topicId))
L105: export async function skipLearningTopic(topicId) {
L106: const response = await api.post(endpoints.learning.topicSkip(topicId))
L110: export async function generateLearningGoals(payload = {}) {
L114: export async function getLearningGoalDashboard(params = {}) {
L118: export async function getLearningGoals(params = {}) {
L126: export async function getLearningPath(pathId) {
L127: const response = await api.get(endpoints.learning.path(pathId))
L132: export async function createLearningPath(payload) {
L133: const response = await api.post(endpoints.learning.paths, payload)
L138: export async function updateLearningPath(pathId, payload) {
L139: const response = await api.patch(endpoints.learning.path(pathId), payload)
L144: export async function deleteLearningPath(pathId) {
L148: export async function reorderLearningTopics(pathId, topicIds) {
L149: const response = await api.post(endpoints.learning.pathReorderTopics(pathId), {
L156: export async function startLearningPath(pathId) {
L157: const response = await api.post(endpoints.learning.pathStart(pathId))
L161: export async function completeLearningPath(pathId) {
L162: const response = await api.post(endpoints.learning.pathComplete(pathId))
L166: export async function pauseLearningPath(pathId) {
L167: const response = await api.post(endpoints.learning.pathPause(pathId))
L175: export async function createLearningGoal(payload) {
L176: const response = await api.post(endpoints.learning.goals, payload)
L181: export async function updateLearningGoal(goalId, payload) {
L182: const response = await api.patch(endpoints.learning.goal(goalId), payload)
L187: export async function deleteLearningGoal(goalId) {
L191: export async function completeLearningGoal(goalId) {
L192: const response = await api.post(endpoints.learning.goalComplete(goalId))
L196: export async function pauseLearningGoal(goalId) {
L197: const response = await api.post(endpoints.learning.goalPause(goalId))
L201: export async function resumeLearningGoal(goalId) {
L202: const response = await api.post(endpoints.learning.goalResume(goalId))
L210: const progressRequests = new Map()
L212: export async function updateLearningProgress(payload) {
L213: const topicId = Number(payload?.topic)
L218: const previous = progressRequests.get(topicId) || Promise.resolve()
L219: const request = previous
L222: const response = await api.post(endpoints.learning.progressUpdate, payload, {
L249: export async function getLearningProgressSummary(params = {}) {
L257: export async function generateLearningTopicContent(topicId, payload = {}) {
L258: const response = await api.post(endpoints.learning.topicGenerateContent(topicId), payload)
L263: export async function getLearningSessions(params = {}) {
L267: export async function getLearningSession(sessionId) {
L275: export async function createLearningSession(payload) {
L276: const response = await api.post(endpoints.learning.sessions, payload)
L281: export async function updateLearningSession(sessionId, payload) {
L282: const response = await api.patch(endpoints.learning.session(sessionId), payload)
L287: export async function finishLearningSession(sessionId, payload = {}) {
L288: const response = await api.post(endpoints.learning.sessionFinish(sessionId), payload)
L292: export async function deleteLearningSession(sessionId) {
L300: export async function getLessons(params = {}) {
L301: const response = await api.get(endpoints.learning.lessons, { params })
L306: export async function getLearningLesson(lessonId) {
L307: const response = await api.get(endpoints.learning.lesson(lessonId))
L312: export async function createLearningLesson(payload) {
L316: export async function updateLearningLesson(lessonId, payload) {
L320: export async function deleteLearningLesson(lessonId) {
L324: export async function markLearningLessonComplete(lessonId) {
L332: export async function getLearningResources(params = {}) {
L333: const response = await api.get(endpoints.learning.resources, { params })
L338: export async function getLearningResource(resourceId) {
L339: const response = await api.get(endpoints.learning.resource(resourceId))
L344: export async function createLearningResource(payload) {
L348: export async function updateLearningResource(resourceId, payload) {
L352: export async function deleteLearningResource(resourceId) {
L360: export async function getLearningNotes(params = {}) {
L361: const response = await api.get(endpoints.learning.notes, { params })
L366: export async function createLearningNote(payload) {
L367: const response = await api.post(endpoints.learning.notes, payload)
L372: export async function updateLearningNote(noteId, payload) {
L373: const response = await api.patch(endpoints.learning.note(noteId), payload)
L378: export async function deleteLearningNote(noteId) {
L382: export async function getLearningNote(noteId) {
L390: export async function getAssessments(params = {}) {
L391: const response = await api.get(endpoints.learning.assessments, { params })
L396: export async function getAssessment(assessmentId) {
L397: const response = await api.get(endpoints.learning.assessment(assessmentId))
L402: export async function getLearnerAssessment(assessmentId) {
L403: const response = await api.get(endpoints.learning.assessmentLearner(assessmentId))
L407: export async function startAssessment(assessmentId) {
L408: const response = await api.post(endpoints.learning.assessmentStart(assessmentId))
L412: export async function submitAssessment(assessmentId, payload = {}) {
L413: const response = await api.post(endpoints.learning.assessmentSubmit(assessmentId), payload)
L418: export async function createAssessment(payload) {
L422: export async function updateAssessment(assessmentId, payload) {
L426: export async function deleteAssessment(assessmentId) {
L430: export async function getAssessmentAnalytics(assessmentId) {
L438: export async function getAssessmentQuestions(params = {}) {
L439: const response = await api.get(endpoints.learning.assessmentQuestions, { params })
L448: export async function getAssessmentChoices(params = {}) {
L449: const response = await api.get(endpoints.learning.assessmentChoices, { params })
L454: export async function createAssessmentQuestion(payload) {
L458: export async function updateAssessmentQuestion(questionId, payload) {
L462: export async function deleteAssessmentQuestion(questionId) {
L466: export async function createAssessmentChoice(payload) {
L470: export async function updateAssessmentChoice(choiceId, payload) {
L474: export async function deleteAssessmentChoice(choiceId) {
L482: export async function getAssessmentAttempts(params = {}) {
L483: const response = await api.get(endpoints.learning.assessmentAttempts, { params })
L492: export async function createAssessmentResponse(payload) {
L493: const response = await api.post(endpoints.learning.assessmentResponses, payload)
L498: export async function updateAssessmentResponse(responseId, payload) {
L499: const response = await api.patch(endpoints.learning.assessmentResponse(responseId), payload)
L504: export async function getAssessmentResponses(params = {}) {
L508: export async function getAssessmentResponse(responseId) {
L512: export async function deleteAssessmentResponse(responseId) {
L520: export async function getKnowledgeApplications(params = {}) {
L521: const response = await api.get(endpoints.learning.applications, {
L528: export async function getKnowledgeApplication(applicationId) {
L529: const response = await api.get(`/learning/applications/${applicationId}/`)
L534: export async function createKnowledgeApplication(payload) {
L535: const response = await api.post(endpoints.learning.applications, payload)
L540: export async function updateKnowledgeApplication(applicationId, payload) {
L541: const response = await api.patch(`/learning/applications/${applicationId}/`, payload)
L547: export async function submitKnowledgeApplication(applicationId) {
L548: const response = await api.post(`/learning/applications/${applicationId}/submit/`)
L557: export async function getApplicationSubmissions(params = {}) {
L558: const response = await api.get(endpoints.learning.applicationSubmissions, { params })
L563: export async function getApplicationSubmission(submissionId) {
L564: const response = await api.get(endpoints.learning.applicationSubmission(submissionId))
L569: export async function getApplicationHistory(applicationId) {
L577: export async function reviewKnowledgeApplication(applicationId) {
L578: const response = await api.post(`/learning/applications/${applicationId}/review/`)
L587: export async function getApplicationReviews(params = {}) {
L588: const response = await api.get(endpoints.learning.applicationReviews, { params })
L593: export async function getApplicationReview(reviewId) {
L594: const response = await api.get(endpoints.learning.applicationReviewDetail(reviewId))
L603: export async function getLearningRevisions(params = {}) {
L604: const response = await api.get(endpoints.learning.revisions, { params })
L609: export async function getLearningRevision(revisionId) {
L610: const response = await api.get(`/learning/revisions/${revisionId}/`)
L615: export async function updateLearningRevision(revisionId, payload) {
L616: const response = await api.patch(`/learning/revisions/${revisionId}/`, payload)
L621: export async function startLearningRevision(revisionId) {
L625: export async function completeLearningRevision(revisionId) {
L629: export async function skipLearningRevision(revisionId) {
L637: export async function getKnowledgeItems(params = {}) {
L638: const response = await api.get(endpoints.knowledge.items, { params })
L643: export async function getKnowledgeItem(itemId) {
L644: const response = await api.get(endpoints.knowledge.item(itemId))
L649: export async function createKnowledgeItem(payload) {
L650: const response = await api.post(endpoints.knowledge.items, payload)
L655: export async function updateKnowledgeItem(itemId, payload) {
L656: const response = await api.patch(endpoints.knowledge.item(itemId), payload)
L661: export async function archiveKnowledgeItem(itemId) {
L662: const response = await api.post(endpoints.knowledge.archive(itemId))
L667: export async function restoreKnowledgeItem(itemId) {
L668: const response = await api.post(endpoints.knowledge.restore(itemId))
L673: export async function connectKnowledgeToTopic(knowledgeId, topicId) {
L674: const response = await api.post(endpoints.knowledge.connectTopic(knowledgeId), {
L681: export async function disconnectKnowledgeFromTopic(knowledgeId, topicId) {
L682: const response = await api.post(endpoints.knowledge.disconnectTopic(knowledgeId), {
L693: export async function getKnowledgeFiles(params = {}) {
L694: const response = await api.get(endpoints.knowledge.files, { params })
L699: export async function uploadKnowledgeFile(knowledgeId, file, extra = {}) {
L700: const formData = new FormData()
L711: const response = await api.post(endpoints.knowledge.uploadFile(knowledgeId), formData, {
L724: export { normalizeList, getErrorMessage }
L726: export async function topicChat(payload) {


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
