import api from '@/services/api'

// ============================================================
// Helpers
// ============================================================

const normalizeList = (data) => {
  if (Array.isArray(data)) {
    return data
  }

  if (Array.isArray(data?.results)) {
    return data.results
  }

  return []
}

// ============================================================
// Dashboard
// ============================================================

export async function getLearningDashboard() {
  const [
    skillsResponse,
    goalsResponse,
    pathsResponse,
    topicsResponse,
    progressResponse,
    assessmentsResponse,
    attemptsResponse,
  ] = await Promise.all([
    api.get('/learning/skills/'),
    api.get('/learning/goals/'),
    api.get('/learning/paths/'),
    api.get('/learning/topics/'),
    api.get('/learning/progress/'),
    api.get('/learning/assessments/'),
    api.get('/learning/assessment-attempts/'),
  ])

  return {
    skills: normalizeList(skillsResponse.data),
    goals: normalizeList(goalsResponse.data),
    paths: normalizeList(pathsResponse.data),
    topics: normalizeList(topicsResponse.data),
    progress: normalizeList(progressResponse.data),
    assessments: normalizeList(assessmentsResponse.data),
    attempts: normalizeList(attemptsResponse.data),
  }
}

// ============================================================
// Progress
// ============================================================

export async function updateLearningProgress(payload) {
  const response = await api.post(
    '/learning/progress/update-progress/',
    payload,
  )

  return response.data
}

// ============================================================
// Topic
// ============================================================

export async function getLearningTopic(topicId) {
  const response = await api.get(
    `/learning/topics/${topicId}/detail/`,
  )

  return response.data
}

// ============================================================
// Topic CRUD
// ============================================================

export async function createLearningTopic(payload) {
  const response = await api.post(
    '/learning/topics/',
    payload,
  )

  return response.data
}

export async function updateLearningTopic(topicId, payload) {
  const response = await api.patch(
    `/learning/topics/${topicId}/`,
    payload,
  )

  return response.data
}

export async function deleteLearningTopic(topicId) {
  await api.delete(
    `/learning/topics/${topicId}/`,
  )
}

// ============================================================
// Path
// ============================================================

export async function getLearningPath(pathId) {
  const response = await api.get(
    `/learning/paths/${pathId}/`,
  )

  return response.data
}

export async function updateLearningPath(pathId, payload) {
  const response = await api.patch(
    `/learning/paths/${pathId}/`,
    payload,
  )

  return response.data
}

export async function reorderLearningTopics(
  pathId,
  topicIds,
) {
  const response = await api.post(
    `/learning/paths/${pathId}/reorder-topics/`,
    {
      topic_ids: topicIds,
    },
  )

  return response.data
}

// ============================================================
// Applications
// ============================================================

export async function createKnowledgeApplication(payload) {
  const response = await api.post(
    '/learning/applications/',
    payload,
  )

  return response.data
}

export async function updateKnowledgeApplication(
  applicationId,
  payload,
) {
  const response = await api.patch(
    `/learning/applications/${applicationId}/`,
    payload,
  )

  return response.data
}

export async function submitKnowledgeApplication(
  applicationId,
) {
  const response = await api.post(
    `/learning/applications/${applicationId}/submit/`,
  )

  return response.data
}

// ============================================================
// AI Review
// ============================================================

export async function reviewKnowledgeApplication(
  applicationId,
) {
  const response = await api.post(
    `/learning/applications/${applicationId}/review/`,
  )

  return response.data
}

// ============================================================
// Knowledge
// ============================================================

export async function createKnowledgeItem(payload) {
  const response = await api.post(
    '/knowledge/items/',
    payload,
  )

  return response.data
}
