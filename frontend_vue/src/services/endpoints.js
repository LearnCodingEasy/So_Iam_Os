/**
 * Canonical API endpoint builders.
 *
 * Keep endpoint paths in one place so Vue services cannot silently drift from
 * the Django router/action contract.
 */

export const endpoints = {
  core: {
    dashboard: '/core/dashboard/',
  },

  users: {
    signup: '/users/signup/',
    login: '/users/login/',
    refresh: '/users/refresh/',
    me: '/users/me/',
    profile: (id) => `/users/profile/${id}/`,
    editProfile: '/users/editprofile/',
    editPassword: '/users/editpassword/',
  },

  goals: {
    list: '/goals/',
    detail: (id) => `/goals/${id}/`,
    complete: (id) => `/goals/${id}/complete/`,
    pause: (id) => `/goals/${id}/pause/`,
    resume: (id) => `/goals/${id}/resume/`,
    progress: (id) => `/goals/${id}/progress/`,
  },

  tasks: {
    list: '/tasks/',
    today: '/tasks/today/',
    detail: (id) => `/tasks/${id}/`,
    complete: (id) => `/tasks/${id}/complete/`,
    postpone: (id) => `/tasks/${id}/postpone/`,
  },

  learning: {
    skills: '/learning/skills/',
    goals: '/learning/goals/',
    goalsGenerate: '/learning/goals/generate/',
    goal: (id) => `/learning/goals/${id}/`,
    goalDashboard: '/learning/goals/dashboard/',
    goalComplete: (id) => `/learning/goals/${id}/complete/`,
    goalPause: (id) => `/learning/goals/${id}/pause/`,
    goalResume: (id) => `/learning/goals/${id}/resume/`,

    paths: '/learning/paths/',
    path: (id) => `/learning/paths/${id}/`,
    pathStart: (id) => `/learning/paths/${id}/start/`,
    pathComplete: (id) => `/learning/paths/${id}/complete/`,
    pathPause: (id) => `/learning/paths/${id}/pause/`,
    pathReorderTopics: (id) => `/learning/paths/${id}/reorder-topics/`,

    topics: '/learning/topics/',
    topic: (id) => `/learning/topics/${id}/`,
    topicStart: (id) => `/learning/topics/${id}/start/`,
    topicComplete: (id) => `/learning/topics/${id}/complete/`,
    topicSkip: (id) => `/learning/topics/${id}/skip/`,
    topicGenerateContent: (id) => `/learning/topics/${id}/generate-content/`,

    lessons: '/learning/lessons/',
    lesson: (id) => `/learning/lessons/${id}/`,
    resources: '/learning/resources/',
    resource: (id) => `/learning/resources/${id}/`,
    notes: '/learning/notes/',
    note: (id) => `/learning/notes/${id}/`,

    progress: '/learning/progress/',
    progressUpdate: '/learning/progress/update-progress/',
    sessions: '/learning/sessions/',
    session: (id) => `/learning/sessions/${id}/`,
    sessionFinish: (id) => `/learning/sessions/${id}/finish/`,

    assessments: '/learning/assessments/',
    assessment: (id) => `/learning/assessments/${id}/`,
    assessmentLearner: (id) => `/learning/assessments/${id}/learner/`,
    assessmentStart: (id) => `/learning/assessments/${id}/start/`,
    assessmentSubmit: (id) => `/learning/assessments/${id}/submit/`,
    assessmentQuestions: '/learning/assessment-questions/',
    assessmentChoices: '/learning/assessment-choices/',
    assessmentAttempts: '/learning/assessment-attempts/',
    assessmentResponses: '/learning/assessment-responses/',
    assessmentResponse: (id) => `/learning/assessment-responses/${id}/`,

    applications: '/learning/applications/',
    application: (id) => `/learning/applications/${id}/`,
    applicationSubmit: (id) => `/learning/applications/${id}/submit/`,
    applicationReview: (id) => `/learning/applications/${id}/review/`,
    applicationHistory: (id) => `/learning/applications/${id}/history/`,
    applicationSubmissions: '/learning/application-submissions/',
    applicationSubmission: (id) => `/learning/application-submissions/${id}/`,
    applicationReviews: '/learning/application-reviews/',
    applicationReviewDetail: (id) => `/learning/application-reviews/${id}/`,

    revisions: '/learning/revisions/',
    revision: (id) => `/learning/revisions/${id}/`,
    revisionStart: (id) => `/learning/revisions/${id}/start/`,
    revisionComplete: (id) => `/learning/revisions/${id}/complete/`,
    revisionSkip: (id) => `/learning/revisions/${id}/skip/`,
  },

  knowledge: {
    items: '/knowledge/items/',
    item: (id) => `/knowledge/items/${id}/`,
    archive: (id) => `/knowledge/items/${id}/archive/`,
    restore: (id) => `/knowledge/items/${id}/restore/`,
    connectTopic: (id) => `/knowledge/items/${id}/connect-topic/`,
    disconnectTopic: (id) => `/knowledge/items/${id}/disconnect-topic/`,
    itemFiles: (id) => `/knowledge/items/${id}/files/`,
    uploadFile: (id) => `/knowledge/items/${id}/upload-file/`,
    files: '/knowledge/files/',
    file: (id) => `/knowledge/files/${id}/`,
    archiveAll: '/knowledge/items/archive-all/',
  },

  jobs: {
    sources: '/jobs/sources/',
    source: (id) => `/jobs/sources/${id}/`,
    sourceTest: (id) => `/jobs/sources/${id}/test/`,
    opportunities: '/jobs/opportunities/',
    opportunity: (id) => `/jobs/opportunities/${id}/`,
    refreshMatch: (id) => `/jobs/opportunities/${id}/refresh_match/`,
    apply: (id) => `/jobs/opportunities/${id}/apply/`,
    matches: '/jobs/matches/',
    refreshMatches: '/jobs/matches/refresh/',
    applications: '/jobs/applications/',
  },

  ai: {
    settings: '/ai/settings/',
    credentials: '/ai/credentials/',
    credential: (provider) => `/ai/credentials/${provider}/`,
    providerModels: (provider) => `/ai/providers/${provider}/models/`,
    prompts: '/ai/prompts/',
    prompt: (id) => `/ai/prompts/${id}/`,
    chat: '/ai/chat/',
    conversations: '/ai/conversations/',
    conversation: (id) => `/ai/conversations/${id}/`,
    learningPreview: '/ai/learning/preview/',
    learningApprove: '/ai/learning/approve/',
    learningAsync: '/ai/learning/async/',
    taskStatus: (id) => `/ai/tasks/${id}/`,
  },
}
