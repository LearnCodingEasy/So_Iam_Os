import api from '@/services/api'
import { endpoints } from './endpoints'

// ===================================================
// Helpers
// ===================================================

const normalizeList = (data) => {
  if (Array.isArray(data)) {
    return data
  }

  if (Array.isArray(data?.results)) {
    return data.results
  }

  return []
}

const getErrorMessage = (error, fallback = 'Something went wrong.') => {
  return (
    error?.response?.data?.detail ||
    error?.response?.data?.message ||
    error?.response?.data?.error ||
    fallback
  )
}

// ===================================================
// Dashboard
// ===================================================

export async function getLearningDashboard() {
  const [
    skillsResponse,
    goalsResponse,
    pathsResponse,
    topicsResponse,
    progressResponse,
    assessmentsResponse,
    attemptsResponse,
    applicationsResponse,
    revisionsResponse,
  ] = await Promise.all([
    api.get(endpoints.learning.skills),
    api.get(endpoints.learning.goals),
    api.get(endpoints.learning.paths),
    api.get(endpoints.learning.topics),
    api.get(endpoints.learning.progress),
    api.get(endpoints.learning.assessments),
    api.get(endpoints.learning.assessmentAttempts),
    api.get(endpoints.learning.applications),
    api.get(endpoints.learning.revisions),
  ])

  return {
    skills: normalizeList(skillsResponse.data),
    goals: normalizeList(goalsResponse.data),
    paths: normalizeList(pathsResponse.data),
    topics: normalizeList(topicsResponse.data),
    progress: normalizeList(progressResponse.data),
    assessments: normalizeList(assessmentsResponse.data),
    attempts: normalizeList(attemptsResponse.data),
    applications: normalizeList(applicationsResponse.data),
    revisions: normalizeList(revisionsResponse.data),
  }
}

// ===================================================
// Topic
// ===================================================

export async function getLearningTopic(topicId) {
  const response = await api.get(endpoints.learning.topic(topicId))

  return response.data
}

export async function createLearningTopic(payload) {
  const response = await api.post(endpoints.learning.topics, payload)

  return response.data
}

export async function updateLearningTopic(topicId, payload) {
  const response = await api.patch(endpoints.learning.topic(topicId), payload)

  return response.data
}

export async function deleteLearningTopic(topicId) {
  await api.delete(endpoints.learning.topic(topicId))
}

export async function startLearningTopic(topicId) {
  const response = await api.post(endpoints.learning.topicStart(topicId))
  return response.data
}

export async function completeLearningTopic(topicId) {
  const response = await api.post(endpoints.learning.topicComplete(topicId))
  return response.data
}

export async function skipLearningTopic(topicId) {
  const response = await api.post(endpoints.learning.topicSkip(topicId))
  return response.data
}

export async function generateLearningGoals(payload = {}) {
  return (await api.post(endpoints.learning.goalsGenerate, payload)).data
}

export async function getLearningGoalDashboard(params = {}) {
  return (await api.get(endpoints.learning.goalDashboard, { params })).data
}

// ===================================================
// Learning Path
// ===================================================

export async function getLearningPath(pathId) {
  const response = await api.get(endpoints.learning.path(pathId))

  return response.data
}

export async function createLearningPath(payload) {
  const response = await api.post(endpoints.learning.paths, payload)

  return response.data
}

export async function updateLearningPath(pathId, payload) {
  const response = await api.patch(endpoints.learning.path(pathId), payload)

  return response.data
}

export async function deleteLearningPath(pathId) {
  await api.delete(endpoints.learning.path(pathId))
}

export async function reorderLearningTopics(pathId, topicIds) {
  const response = await api.post(endpoints.learning.pathReorderTopics(pathId), {
    topic_ids: topicIds,
  })

  return response.data
}

export async function startLearningPath(pathId) {
  const response = await api.post(endpoints.learning.pathStart(pathId))
  return response.data
}

export async function completeLearningPath(pathId) {
  const response = await api.post(endpoints.learning.pathComplete(pathId))
  return response.data
}

export async function pauseLearningPath(pathId) {
  const response = await api.post(endpoints.learning.pathPause(pathId))
  return response.data
}

// ===================================================
// Goals
// ===================================================

export async function createLearningGoal(payload) {
  const response = await api.post(endpoints.learning.goals, payload)

  return response.data
}

export async function updateLearningGoal(goalId, payload) {
  const response = await api.patch(endpoints.learning.goal(goalId), payload)

  return response.data
}

export async function deleteLearningGoal(goalId) {
  await api.delete(endpoints.learning.goal(goalId))
}

export async function completeLearningGoal(goalId) {
  const response = await api.post(endpoints.learning.goalComplete(goalId))
  return response.data
}

export async function pauseLearningGoal(goalId) {
  const response = await api.post(endpoints.learning.goalPause(goalId))
  return response.data
}

export async function resumeLearningGoal(goalId) {
  const response = await api.post(endpoints.learning.goalResume(goalId))
  return response.data
}

// ===================================================
// Progress
// ===================================================

export async function updateLearningProgress(payload) {
  const response = await api.post(endpoints.learning.progressUpdate, payload)

  return response.data
}

export async function getLearningProgressSummary(params = {}) {
  return (await api.get(endpoints.learning.progressSummary, { params })).data
}

// ===================================================
// AI Topic Content
// ===================================================

export async function generateLearningTopicContent(topicId, payload = {}) {
  const response = await api.post(endpoints.learning.topicGenerateContent(topicId), payload)

  return response.data
}

export async function getLearningSessions(params = {}) {
  return normalizeList((await api.get(endpoints.learning.sessions, { params })).data)
}

export async function getLearningSession(sessionId) {
  return (await api.get(endpoints.learning.session(sessionId))).data
}

// ===================================================
// Sessions
// ===================================================

export async function createLearningSession(payload) {
  const response = await api.post(endpoints.learning.sessions, payload)

  return response.data
}

export async function updateLearningSession(sessionId, payload) {
  const response = await api.patch(endpoints.learning.session(sessionId), payload)

  return response.data
}

export async function finishLearningSession(sessionId, payload = {}) {
  const response = await api.post(endpoints.learning.sessionFinish(sessionId), payload)
  return response.data
}

export async function deleteLearningSession(sessionId) {
  await api.delete(endpoints.learning.session(sessionId))
}

// ===================================================
// Lessons
// ===================================================

export async function getLessons(params = {}) {
  const response = await api.get(endpoints.learning.lessons, { params })

  return normalizeList(response.data)
}

export async function getLearningLesson(lessonId) {
  const response = await api.get(endpoints.learning.lesson(lessonId))

  return response.data
}

export async function createLearningLesson(payload) {
  return (await api.post(endpoints.learning.lessons, payload)).data
}

export async function updateLearningLesson(lessonId, payload) {
  return (await api.patch(endpoints.learning.lesson(lessonId), payload)).data
}

export async function deleteLearningLesson(lessonId) {
  await api.delete(endpoints.learning.lesson(lessonId))
}

export async function markLearningLessonComplete(lessonId) {
  return (await api.post(endpoints.learning.lessonMarkComplete(lessonId))).data
}

// ===================================================
// Resources
// ===================================================

export async function getLearningResources(params = {}) {
  const response = await api.get(endpoints.learning.resources, { params })

  return normalizeList(response.data)
}

export async function getLearningResource(resourceId) {
  const response = await api.get(endpoints.learning.resource(resourceId))

  return response.data
}

export async function createLearningResource(payload) {
  return (await api.post(endpoints.learning.resources, payload)).data
}

export async function updateLearningResource(resourceId, payload) {
  return (await api.patch(endpoints.learning.resource(resourceId), payload)).data
}

export async function deleteLearningResource(resourceId) {
  await api.delete(endpoints.learning.resource(resourceId))
}

// ===================================================
// Notes
// ===================================================

export async function getLearningNotes(params = {}) {
  const response = await api.get(endpoints.learning.notes, { params })

  return normalizeList(response.data)
}

export async function createLearningNote(payload) {
  const response = await api.post(endpoints.learning.notes, payload)

  return response.data
}

export async function updateLearningNote(noteId, payload) {
  const response = await api.patch(endpoints.learning.note(noteId), payload)

  return response.data
}

export async function deleteLearningNote(noteId) {
  await api.delete(endpoints.learning.note(noteId))
}

export async function getLearningNote(noteId) {
  return (await api.get(endpoints.learning.note(noteId))).data
}

// ===================================================
// Assessments
// ===================================================

export async function getAssessments(params = {}) {
  const response = await api.get(endpoints.learning.assessments, { params })

  return normalizeList(response.data)
}

export async function getAssessment(assessmentId) {
  const response = await api.get(endpoints.learning.assessment(assessmentId))

  return response.data
}

export async function getLearnerAssessment(assessmentId) {
  const response = await api.get(endpoints.learning.assessmentLearner(assessmentId))
  return response.data
}

export async function startAssessment(assessmentId) {
  const response = await api.post(endpoints.learning.assessmentStart(assessmentId))
  return response.data
}

export async function submitAssessment(assessmentId, payload = {}) {
  const response = await api.post(endpoints.learning.assessmentSubmit(assessmentId), payload)

  return response.data
}

export async function createAssessment(payload) {
  return (await api.post(endpoints.learning.assessments, payload)).data
}

export async function updateAssessment(assessmentId, payload) {
  return (await api.patch(endpoints.learning.assessment(assessmentId), payload)).data
}

export async function deleteAssessment(assessmentId) {
  await api.delete(endpoints.learning.assessment(assessmentId))
}

export async function getAssessmentAnalytics(assessmentId) {
  return (await api.get(endpoints.learning.assessmentAnalytics(assessmentId))).data
}

// ===================================================
// Assessment Questions
// ===================================================

export async function getAssessmentQuestions(params = {}) {
  const response = await api.get(endpoints.learning.assessmentQuestions, { params })

  return normalizeList(response.data)
}

// ===================================================
// Assessment Choices
// ===================================================

export async function getAssessmentChoices(params = {}) {
  const response = await api.get(endpoints.learning.assessmentChoices, { params })

  return normalizeList(response.data)
}

export async function createAssessmentQuestion(payload) {
  return (await api.post(endpoints.learning.assessmentQuestions, payload)).data
}

export async function updateAssessmentQuestion(questionId, payload) {
  return (await api.patch(endpoints.learning.assessmentQuestion(questionId), payload)).data
}

export async function deleteAssessmentQuestion(questionId) {
  await api.delete(endpoints.learning.assessmentQuestion(questionId))
}

export async function createAssessmentChoice(payload) {
  return (await api.post(endpoints.learning.assessmentChoices, payload)).data
}

export async function updateAssessmentChoice(choiceId, payload) {
  return (await api.patch(endpoints.learning.assessmentChoice(choiceId), payload)).data
}

export async function deleteAssessmentChoice(choiceId) {
  await api.delete(endpoints.learning.assessmentChoice(choiceId))
}

// ===================================================
// Assessment Attempts
// ===================================================

export async function getAssessmentAttempts(params = {}) {
  const response = await api.get(endpoints.learning.assessmentAttempts, { params })

  return normalizeList(response.data)
}

// ===================================================
// Assessment Responses
// ===================================================

export async function createAssessmentResponse(payload) {
  const response = await api.post(endpoints.learning.assessmentResponses, payload)

  return response.data
}

export async function updateAssessmentResponse(responseId, payload) {
  const response = await api.patch(endpoints.learning.assessmentResponse(responseId), payload)

  return response.data
}

export async function getAssessmentResponses(params = {}) {
  return normalizeList((await api.get(endpoints.learning.assessmentResponses, { params })).data)
}

export async function getAssessmentResponse(responseId) {
  return (await api.get(endpoints.learning.assessmentResponse(responseId))).data
}

export async function deleteAssessmentResponse(responseId) {
  await api.delete(endpoints.learning.assessmentResponse(responseId))
}

// ===================================================
// 🧠 Knowledge Applications
// ===================================================

export async function getKnowledgeApplications(params = {}) {
  const response = await api.get(endpoints.learning.applications, {
    params,
  })

  return normalizeList(response.data)
}

export async function getKnowledgeApplication(applicationId) {
  const response = await api.get(`/learning/applications/${applicationId}/`)

  return response.data
}

export async function createKnowledgeApplication(payload) {
  const response = await api.post(endpoints.learning.applications, payload)

  return response.data
}

export async function updateKnowledgeApplication(applicationId, payload) {
  const response = await api.patch(`/learning/applications/${applicationId}/`, payload)

  return response.data
}

// Creates immutable ApplicationSubmission
export async function submitKnowledgeApplication(applicationId) {
  const response = await api.post(`/learning/applications/${applicationId}/submit/`)

  return response.data
}

// ===================================================
// Application Submissions
// ===================================================

export async function getApplicationSubmissions(params = {}) {
  const response = await api.get(endpoints.learning.applicationSubmissions, { params })

  return normalizeList(response.data)
}

export async function getApplicationSubmission(submissionId) {
  const response = await api.get(endpoints.learning.applicationSubmission(submissionId))

  return response.data
}

export async function getApplicationHistory(applicationId) {
  return (await api.get(endpoints.learning.applicationHistory(applicationId))).data
}

// ===================================================
// AI Review
// ===================================================

export async function reviewKnowledgeApplication(applicationId) {
  const response = await api.post(`/learning/applications/${applicationId}/review/`)

  return response.data
}

// ===================================================
// Application Reviews
// ===================================================

export async function getApplicationReviews(params = {}) {
  const response = await api.get(endpoints.learning.applicationReviews, { params })

  return normalizeList(response.data)
}

export async function getApplicationReview(reviewId) {
  const response = await api.get(endpoints.learning.applicationReviewDetail(reviewId))

  return response.data
}

// ===================================================
// Revisions
// ===================================================

export async function getLearningRevisions(params = {}) {
  const response = await api.get(endpoints.learning.revisions, { params })

  return normalizeList(response.data)
}

export async function getLearningRevision(revisionId) {
  const response = await api.get(`/learning/revisions/${revisionId}/`)

  return response.data
}

export async function updateLearningRevision(revisionId, payload) {
  const response = await api.patch(`/learning/revisions/${revisionId}/`, payload)

  return response.data
}

export async function startLearningRevision(revisionId) {
  return (await api.post(endpoints.learning.revisionStart(revisionId))).data
}

export async function completeLearningRevision(revisionId) {
  return (await api.post(endpoints.learning.revisionComplete(revisionId))).data
}

export async function skipLearningRevision(revisionId) {
  return (await api.post(endpoints.learning.revisionSkip(revisionId))).data
}

// ===================================================
// Knowledge
// ===================================================

export async function getKnowledgeItems(params = {}) {
  const response = await api.get(endpoints.knowledge.items, { params })

  return normalizeList(response.data)
}

export async function getKnowledgeItem(itemId) {
  const response = await api.get(endpoints.knowledge.item(itemId))

  return response.data
}

export async function createKnowledgeItem(payload) {
  const response = await api.post(endpoints.knowledge.items, payload)

  return response.data
}

export async function updateKnowledgeItem(itemId, payload) {
  const response = await api.patch(endpoints.knowledge.item(itemId), payload)

  return response.data
}

export async function archiveKnowledgeItem(itemId) {
  const response = await api.post(endpoints.knowledge.archive(itemId))

  return response.data
}

export async function restoreKnowledgeItem(itemId) {
  const response = await api.post(endpoints.knowledge.restore(itemId))

  return response.data
}

export async function connectKnowledgeToTopic(knowledgeId, topicId) {
  const response = await api.post(endpoints.knowledge.connectTopic(knowledgeId), {
    topic_id: topicId,
  })

  return response.data
}

export async function disconnectKnowledgeFromTopic(knowledgeId, topicId) {
  const response = await api.post(endpoints.knowledge.disconnectTopic(knowledgeId), {
    topic_id: topicId,
  })

  return response.data
}

// ===================================================
// Knowledge Files
// ===================================================

export async function getKnowledgeFiles(params = {}) {
  const response = await api.get(endpoints.knowledge.files, { params })

  return normalizeList(response.data)
}

export async function uploadKnowledgeFile(knowledgeId, file, extra = {}) {
  const formData = new FormData()

  formData.append('knowledge', knowledgeId)
  formData.append('file', file)

  Object.entries(extra).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      formData.append(key, value)
    }
  })

  const response = await api.post(endpoints.knowledge.uploadFile(knowledgeId), formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

// ===================================================
// Error helper
// ===================================================

export { normalizeList, getErrorMessage }

export async function topicChat(payload) {
  return (await api.post('/ai/topic-chat/', payload)).data
}
