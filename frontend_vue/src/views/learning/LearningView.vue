<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { getLearningDashboard, updateLearningProgress, pauseLearningGoal, resumeLearningGoal } from '@/services/learning'
import LearningPathEditor from '@/components/learning/LearningPathEditor.vue'

// ==================================================
// STATE
// ==================================================
const loading = ref(true)
const refreshing = ref(false)
const error = ref('')

const skills = ref([])
const goals = ref([])
const paths = ref([])
const topics = ref([])
const progress = ref([])
const assessments = ref([])
const attempts = ref([])
const applications = ref([])
const revisions = ref([])

const activeFilter = ref('all')
const showProgressModal = ref(false)
const selectedTopic = ref(null)
const updatingProgress = ref(false)
const showRoadmapEditor = ref(false)

const progressForm = ref({
  progress_percent: 0,
  practice_completed: false,
  notes: '',
})

const filterOptions = [
  { label: 'All', value: 'all' },
  { label: 'In progress', value: 'in_progress' },
  { label: 'Upcoming', value: 'pending' },
  { label: 'Completed', value: 'completed' },
]

// ============================================================
// HELPERS & API ACTIONS
// ============================================================
const normalizeList = (data) => {
  if (Array.isArray(data)) return data
  if (data?.results && Array.isArray(data.results)) return data.results
  return []
}

const getProgressForTopic = (topicId) => {
  return progress.value.find((item) => Number(item.topic) === Number(topicId)) || null
}

const getTopicProgress = (topicId) => {
  return getProgressForTopic(topicId)?.progress_percent ?? 0
}

const getPathById = (pathId) => {
  return paths.value.find((path) => Number(path.id) === Number(pathId)) || null
}

const getGoalById = (goalId) => {
  return goals.value.find((goal) => Number(goal.id) === Number(goalId)) || null
}

const getSkillById = (skillId) => {
  return skills.value.find((skill) => Number(skill.id) === Number(skillId)) || null
}

const statusLabel = (status) => {
  const labels = {
    pending: 'Not started',
    in_progress: 'In progress',
    completed: 'Completed',
    skipped: 'Skipped',
    active: 'Active',
    paused: 'Paused',
    archived: 'Archived',
  }
  return labels[status] || status || 'Unknown'
}

const getTagSeverity = (status) => {
  switch (status) {
    case 'completed':
    case 'active':
      return 'success'
    case 'in_progress':
      return 'info'
    case 'paused':
    case 'pending':
      return 'warn'
    default:
      return 'secondary'
  }
}

const formatDate = (date) => {
  if (!date) return 'No activity'
  return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const formatMinutes = (minutes) => {
  if (!minutes) return null
  if (minutes < 60) return `${minutes} min`
  const hours = Math.floor(minutes / 60)
  const remaining = minutes % 60
  if (!remaining) return `${hours}h`
  return `${hours}h ${remaining}m`
}

// ============================================================
// DASHBOARD DATA LOAD
// ============================================================
const loadLearningDashboard = async (silent = false) => {
  if (silent) {
    refreshing.value = true
  } else {
    loading.value = true
  }
  error.value = ''

  try {
    const data = await getLearningDashboard()
    skills.value = normalizeList(data.skills)
    goals.value = normalizeList(data.goals)
    paths.value = normalizeList(data.paths)
    topics.value = normalizeList(data.topics)
    progress.value = normalizeList(data.progress)
    assessments.value = normalizeList(data.assessments)
    attempts.value = normalizeList(data.attempts)
    applications.value = normalizeList(data.applications)
    revisions.value = normalizeList(data.revisions)
  } catch (err) {
    console.error('Learning dashboard error:', err)
    error.value = err?.response?.data?.detail || 'Unable to load your learning system.'
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

const refreshDashboard = async () => {
  await loadLearningDashboard(true)
}

// Goal Controls (Actions API Integration)
const pauseGoal = async (goalId) => {
  try {
    await pauseLearningGoal(goalId)
    await refreshDashboard()
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Unable to pause this goal.'
  }
}

const resumeGoal = async (goalId) => {
  try {
    await resumeLearningGoal(goalId)
    await refreshDashboard()
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Unable to resume this goal.'
  }
}

// ==================================================
// COMPUTED METRICS
// ==================================================
const totalTopics = computed(() => topics.value.length)
const completedTopics = computed(() => topics.value.filter((t) => t.status === 'completed').length)
const practiceCount = computed(
  () => progress.value.filter((item) => item.practice_completed).length,
)
const passedAssessments = computed(() => attempts.value.filter((attempt) => attempt.passed).length)

const averageProgress = computed(() => {
  if (!topics.value.length) return 0
  const total = topics.value.reduce((sum, topic) => sum + getTopicProgress(topic.id), 0)
  return Math.round(total / topics.value.length)
})

const currentTopic = computed(() => {
  const inProgress = topics.value
    .filter((topic) => topic.status === 'in_progress')
    .sort((a, b) => getTopicProgress(b.id) - getTopicProgress(a.id))
  if (inProgress.length) return inProgress[0]
  const pending = topics.value
    .filter((topic) => topic.status === 'pending')
    .sort((a, b) => Number(a.order || 999) - Number(b.order || 999))
  return pending[0] || null
})

const currentPath = computed(() =>
  currentTopic.value ? getPathById(currentTopic.value.path) : null,
)
const currentTopicProgress = computed(() =>
  currentTopic.value ? getTopicProgress(currentTopic.value.id) : 0,
)

const getGoalProgress = (goalId) => {
  const goalPaths = paths.value.filter((path) => Number(path.goal) === Number(goalId))
  const goalTopics = topics.value.filter((topic) =>
    goalPaths.some((path) => Number(path.id) === Number(topic.path)),
  )
  if (!goalTopics.length) return 0
  const total = goalTopics.reduce((sum, topic) => sum + getTopicProgress(topic.id), 0)
  return Math.round(total / goalTopics.length)
}

const pathTopics = (pathId) => {
  return topics.value
    .filter((topic) => Number(topic.path) === Number(pathId))
    .sort((a, b) => Number(a.order || 0) - Number(b.order || 0))
}

const filteredTopics = computed(() => {
  let result = [...topics.value]
  if (activeFilter.value !== 'all') {
    result = result.filter((topic) => topic.status === activeFilter.value)
  }
  return result.sort((a, b) => Number(a.order || 0) - Number(b.order || 0))
})

const recentTopics = computed(() => {
  return [...topics.value]
    .sort((a, b) => {
      const aDate = getProgressForTopic(a.id)?.last_activity_at || ''
      const bDate = getProgressForTopic(b.id)?.last_activity_at || ''
      return new Date(bDate) - new Date(aDate)
    })
    .slice(0, 5)
})

// ==================================================
// PROGRESS MODAL & SAVING
// ==================================================
const openProgressModal = (topic) => {
  selectedTopic.value = topic
  const existing = getProgressForTopic(topic.id)
  progressForm.value = {
    progress_percent: existing?.progress_percent ?? 0,
    practice_completed: existing?.practice_completed ?? false,
    notes: existing?.notes ?? '',
  }
  showProgressModal.value = true
}

const closeProgressModal = () => {
  if (updatingProgress.value) return
  showProgressModal.value = false
  selectedTopic.value = null
}

const saveProgress = async () => {
  if (!selectedTopic.value) return
  updatingProgress.value = true

  try {
    const percentage = Number(progressForm.value.progress_percent)
    const payload = {
      topic: selectedTopic.value.id,
      progress_percent: percentage,
      practice_completed: progressForm.value.practice_completed,
      notes: progressForm.value.notes,
      lesson_completed: percentage >= 100 ? true : undefined,
      quick_check_completed: percentage >= 100 ? true : undefined,
      assessment_completed: percentage >= 100 ? true : undefined,
    }

    const result = await updateLearningProgress(payload)
    const existingIndex = progress.value.findIndex(
      (item) => Number(item.topic) === Number(selectedTopic.value.id),
    )

    if (existingIndex !== -1) {
      progress.value[existingIndex] = result
    } else {
      progress.value.push(result)
    }

    const topicIndex = topics.value.findIndex(
      (topic) => Number(topic.id) === Number(selectedTopic.value.id),
    )
    if (topicIndex !== -1) {
      topics.value[topicIndex] = {
        ...topics.value[topicIndex],
        status: percentage >= 100 ? 'completed' : percentage > 0 ? 'in_progress' : 'pending',
      }
    }
    closeProgressModal()
  } catch (err) {
    console.error('Progress update error:', err)
    error.value = err?.response?.data?.detail || 'Unable to update progress.'
  } finally {
    updatingProgress.value = false
  }
}

onMounted(() => {
  loadLearningDashboard()
})
</script>

<template>
  <div class="learning-page">
    <!-- HEADER -->
    <header class="page-header">
      <div class="header-copy">
        <span class="eyebrow">PERSONAL LEARNING OS</span>
        <h1>Keep learning. <span>Keep moving.</span></h1>
        <p>Your learning system adapts around what you learn, practice and apply.</p>
      </div>

      <div>
        <prime_button
          :icon="refreshing ? 'pi pi-spin pi-spinner' : 'pi pi-refresh'"
          :label="refreshing ? 'Refreshing' : 'Refresh'"
          variant="outlined"
          :disabled="loading || refreshing"
          @click="refreshDashboard"
        />
      </div>
    </header>

    <!-- ERROR BANNER -->
    <prime_message v-if="error" severity="error" class="error-banner w-full">
      <div class="flex items-center justify-between w-full gap-4">
        <div>
          <strong class="block font-semibold">Something went wrong</strong>
          <span class="text-sm">{{ error }}</span>
        </div>
        <prime_button label="Try again" variant="text" severity="error" @click="refreshDashboard" />
      </div>
    </prime_message>

    <!-- LOADING STATE -->
    <div v-if="loading" class="loading-screen">
      <div class="loading-orbit"><span></span></div>
      <h3>Building your learning space</h3>
      <p>Loading goals, topics and progress...</p>
    </div>

    <template v-else>
      <!-- HERO & OVERVIEW -->
      <section class="hero-grid">
        <prime_card class="continue-card shadow-sm border border-surface">
          <template #title>
            <div class="flex items-center justify-between">
              <span class="eyebrow light">CONTINUE LEARNING</span>
              <prime_tag
                v-if="currentTopic"
                :value="currentTopic ? String(currentTopic.order || 1).padStart(2, '0') : '01'"
                severity="secondary"
              />
            </div>
          </template>
          <template #content>
            <div v-if="currentTopic" class="continue-content space-y-4 py-2">
              <div class="continue-meta">
                <span>{{ currentPath?.title || 'Learning path' }}</span>
                <span class="dot">•</span>
                <prime_tag
                  :value="statusLabel(currentTopic.status)"
                  :severity="getTagSeverity(currentTopic.status)"
                />
              </div>

              <h2>{{ currentTopic.title }}</h2>
              <p>
                {{
                  currentTopic.description || 'Continue building your understanding of this topic.'
                }}
              </p>

              <div class="continue-progress">
                <div class="progress-info">
                  <span>{{ currentTopicProgress }}% complete</span>
                  <strong>{{ formatMinutes(currentTopic.estimated_minutes) }}</strong>
                </div>
                <div class="progress-track dark">
                  <div class="progress-value" :style="{ width: currentTopicProgress + '%' }"></div>
                </div>
              </div>
            </div>

            <div v-else class="continue-content py-8 space-y-2">
              <h2>Your learning journey starts here.</h2>
              <p>Create a goal and build your first learning path.</p>
            </div>
          </template>
          <template #footer>
            <div v-if="currentTopic" class="pt-2">
              <RouterLink :to="{ name: 'learning-topic', params: { topicId: currentTopic.id } }">
                <prime_button label="Continue learning" icon="pi pi-arrow-right" iconPos="right" />
              </RouterLink>
            </div>
          </template>
        </prime_card>

        <prime_card class="overview-card shadow-sm border border-surface">
          <template #title>
            <span class="eyebrow">OVERALL PROGRESS</span>
          </template>
          <template #subtitle>
            <span class="overview-caption">Across all learning topics</span>
          </template>
          <template #content>
            <div class="overview-top flex flex-col items-center justify-center py-6 space-y-4">
              <div class="overview-ring">
                <svg viewBox="0 0 100 100">
                  <circle class="ring-background" cx="50" cy="50" r="42" />
                  <circle
                    class="ring-progress"
                    cx="50"
                    cy="50"
                    r="42"
                    :style="{ strokeDasharray: `${averageProgress * 2.64} 264` }"
                  />
                </svg>
                <strong>{{ averageProgress }}%</strong>
              </div>

              <prime_divider />

              <div class="overview-stats">
                <div>
                  <strong>{{ totalTopics }}</strong>
                  <span>Topics</span>
                </div>
                <div>
                  <strong>{{ completedTopics }}</strong>
                  <span>Completed</span>
                </div>
                <div>
                  <strong>{{ practiceCount }}</strong>
                  <span>Practiced</span>
                </div>
              </div>
            </div>
          </template>
        </prime_card>
      </section>

      <!-- GOALS SECTION -->
      <section class="section-block">
        <div class="section-heading">
          <div>
            <span class="eyebrow">DIRECTION</span>
            <h2>What are you building toward?</h2>
          </div>
          <prime_chip :label="`${goals.length} goals`" />
        </div>

        <div v-if="goals.length" class="goal-list">
          <prime_card
            v-for="goal in goals"
            :key="goal.id"
            class="goal-card shadow-sm border border-surface"
          >
            <template #title>
              <div class="goal-header flex items-start justify-between gap-2">
                <h3>{{ goal.title }}</h3>
                <div class="flex items-center gap-2">
                  <prime_tag
                    :value="statusLabel(goal.status)"
                    :severity="getTagSeverity(goal.status)"
                  />
                  <prime_button
                    v-if="goal.status === 'active'"
                    icon="pi pi-pause"
                    size="small"
                    severity="warn"
                    variant="text"
                    @click="pauseGoal(goal.id)"
                  />
                  <prime_button
                    v-else
                    icon="pi pi-play"
                    size="small"
                    severity="success"
                    variant="text"
                    @click="resumeGoal(goal.id)"
                  />
                </div>
              </div>
            </template>
            <template #content>
              <div class="goal-content">
                <p>{{ goal.description || 'No description available.' }}</p>
                <div class="goal-progress">
                  <div class="goal-progress-top">
                    <span>{{ getGoalProgress(goal.id) }}% progress</span>
                    <span>{{ goal.target_level || 'Target not set' }}</span>
                  </div>
                  <div class="progress-track">
                    <div
                      class="progress-value"
                      :style="{ width: getGoalProgress(goal.id) + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </template>
            <template #footer>
              <div class="goal-side border-t border-surface pt-3">
                <span v-if="goal.target_date"
                  >Target <strong>{{ formatDate(goal.target_date) }}</strong></span
                >
                <span v-if="goal.skill"
                  >Skill
                  <strong>{{ getSkillById(goal.skill)?.name || `#${goal.skill}` }}</strong></span
                >
              </div>
            </template>
          </prime_card>
        </div>

        <prime_card v-else class="empty-card text-center py-8 border border-dashed border-surface">
          <template #content>
            <div class="empty-symbol">+</div>
            <h3>No learning goals yet</h3>
            <p>Your goals will become the direction of your learning system.</p>
          </template>
        </prime_card>
      </section>

      <!-- ROADMAP SECTION -->
      <section class="section-block roadmap-section">
        <div class="section-heading">
          <div>
            <span class="eyebrow">ROADMAP</span>
            <h2>Your learning path</h2>
            <p>Follow the sequence, or reshape it around your needs.</p>
          </div>
          <prime_button
            :label="showRoadmapEditor ? 'Close editor' : 'Edit roadmap'"
            :icon="showRoadmapEditor ? 'pi pi-times' : 'pi pi-pencil'"
            class="secondary-action"
            variant="outlined"
            severity="secondary"
            @click="showRoadmapEditor = !showRoadmapEditor"
          />
        </div>

        <div v-if="showRoadmapEditor" class="roadmap-editor-wrapper">
          <LearningPathEditor
            :paths="paths"
            :topics="topics"
            :progress="progress"
            @refresh="refreshDashboard"
          />
        </div>

        <div v-if="paths.length" class="roadmap-list">
          <prime_card
            v-for="path in paths"
            :key="path.id"
            class="roadmap-card shadow-sm border border-surface"
          >
            <template #title>
              <div class="roadmap-header flex items-center justify-between">
                <div>
                  <span class="path-status">{{ statusLabel(path.status) }}</span>
                  <h3>{{ path.title }}</h3>
                </div>
                <span class="topic-count">{{ pathTopics(path.id).length }} topics</span>
              </div>
            </template>
            <template #content>
              <div class="roadmap-main">
                <p>{{ path.description || 'Learning path without a description.' }}</p>
                <prime_divider />
                <div class="topic-timeline">
                  <RouterLink
                    v-for="(topic, index) in pathTopics(path.id)"
                    :key="topic.id"
                    :to="{ name: 'learning-topic', params: { topicId: topic.id } }"
                    class="timeline-topic"
                    :class="{
                      completed: topic.status === 'completed',
                      active: topic.status === 'in_progress',
                    }"
                  >
                    <div class="timeline-node">
                      <span v-if="topic.status === 'completed'">✓</span>
                      <span v-else>{{ index + 1 }}</span>
                    </div>
                    <div class="timeline-content">
                      <strong>{{ topic.title }}</strong>
                      <span>{{ getTopicProgress(topic.id) }}%</span>
                    </div>
                  </RouterLink>
                </div>
              </div>
            </template>
          </prime_card>
        </div>

        <div v-else class="empty-card text-center py-8 border border-dashed border-surface">
          <div class="empty-symbol">+</div>
          <h3>No learning paths yet</h3>
          <p>Your paths will organize the journey from goal to practical mastery.</p>
        </div>
      </section>

      <!-- TOPICS SECTION -->
      <section class="section-block">
        <div
          class="section-heading topics-heading flex flex-col md:flex-row md:items-center justify-between gap-4"
        >
          <div>
            <span class="eyebrow">LEARN + PRACTICE</span>
            <h2>Your topics</h2>
          </div>
          <div class="filter-tabs">
            <prime_select_button
              v-model="activeFilter"
              :options="filterOptions"
              optionLabel="label"
              optionValue="value"
              :allowEmpty="false"
            />
          </div>
        </div>

        <div v-if="filteredTopics.length" class="topic-list">
          <prime_card
            v-for="topic in filteredTopics"
            :key="topic.id"
            class="learning-topic-card shadow-sm border border-surface"
          >
            <template #content>
              <div class="topic-body">
                <div
                  class="topic-top flex flex-col md:flex-row md:items-center justify-between gap-4"
                >
                  <div class="topic-info flex items-start gap-4">
                    <span class="topic-order">{{
                      String(topic.order || topic.id).padStart(2, '0')
                    }}</span>
                    <div>
                      <div class="topic-meta flex items-center gap-2">
                        <span class="status-dot" :class="topic.status"></span>
                        {{ statusLabel(topic.status) }}
                        <span v-if="topic.estimated_minutes"
                          >· {{ formatMinutes(topic.estimated_minutes) }}</span
                        >
                      </div>
                      <h3>{{ topic.title }}</h3>
                      <p>{{ topic.description || 'Start exploring this topic.' }}</p>
                    </div>
                  </div>
                  <div class="topic-percent text-right">
                    <span>{{ getTopicProgress(topic.id) }}%</span>
                  </div>
                </div>

                <div class="topic-progress">
                  <div class="progress-track">
                    <div
                      class="progress-value"
                      :style="{ width: getTopicProgress(topic.id) + '%' }"
                    ></div>
                  </div>
                </div>

                <div
                  class="topic-footer flex items-center justify-between pt-4 mt-4 border-t border-surface"
                >
                  <span v-if="topic.skill" class="skill-chip">
                    {{ getSkillById(topic.skill)?.name || `Skill #${topic.skill}` }}
                  </span>
                  <div class="topic-actions flex items-center gap-2">
                    <prime_button
                      label="Update progress"
                      class="ghost-action"
                      variant="text"
                      size="small"
                      severity="secondary"
                      @click="openProgressModal(topic)"
                    />
                    <RouterLink
                      :to="{ name: 'learning-topic', params: { topicId: topic.id } }"
                      class="topic-open"
                    >
                      <prime_button
                        label="Open topic"
                        icon="pi pi-arrow-right"
                        iconPos="right"
                        size="small"
                        variant="outlined"
                      />
                    </RouterLink>
                  </div>
                </div>
              </div>
            </template>
          </prime_card>
        </div>

        <div v-else class="empty-card text-center py-8 border border-dashed border-surface">
          <h3>Nothing here yet</h3>
          <p>Topics matching this filter will appear here.</p>
        </div>
      </section>

      <!-- PRACTICE BANNER -->
      <section class="practice-banner">
        <div class="practice-copy">
          <span class="eyebrow light">APPLY KNOWLEDGE</span>
          <h2>Don't just learn it. <span>Use it.</span></h2>
          <p>
            Turn what you studied into a real application, project or explanation. Your learning
            system can review what you produce and identify what needs more attention.
          </p>
        </div>

        <div class="practice-flow">
          <div class="flow-step"><span>01</span> Learn</div>
          <div class="flow-arrow">→</div>
          <div class="flow-step active"><span>02</span> Apply</div>
          <div class="flow-arrow">→</div>
          <div class="flow-step"><span>03</span> Review</div>
        </div>

        <RouterLink
          v-if="currentTopic"
          :to="{ name: 'learning-topic', params: { topicId: currentTopic.id } }"
        >
          <prime_button
            label="Start application"
            icon="pi pi-arrow-right"
            iconPos="right"
            class="practice-action"
          />
        </RouterLink>
      </section>

      <!-- BOTTOM INSIGHTS -->
      <section class="bottom-grid">
        <article class="activity-card">
          <div class="section-heading compact">
            <div>
              <span class="eyebrow">ACTIVITY</span>
              <h2>Recent learning</h2>
            </div>
          </div>

          <div v-if="recentTopics.length" class="activity-list">
            <RouterLink
              v-for="topic in recentTopics"
              :key="topic.id"
              :to="{ name: 'learning-topic', params: { topicId: topic.id } }"
              class="activity-item"
            >
              <div class="activity-dot" :class="topic.status"></div>
              <div class="activity-info">
                <strong>{{ topic.title }}</strong>
                <span>{{
                  getProgressForTopic(topic.id)?.last_activity_at
                    ? formatDate(getProgressForTopic(topic.id).last_activity_at)
                    : 'No activity'
                }}</span>
              </div>
              <strong class="activity-percent">{{ getTopicProgress(topic.id) }}%</strong>
            </RouterLink>
          </div>
          <div v-else class="small-empty">Start learning to see your activity here.</div>
        </article>

        <article class="assessment-summary-card">
          <div class="section-heading compact">
            <div>
              <span class="eyebrow">EVALUATION</span>
              <h2>Assessments</h2>
            </div>
            <strong class="assessment-number">{{ passedAssessments }}</strong>
          </div>

          <div class="assessment-stat">
            <div class="assessment-circle">
              <span>{{ assessments.length }}</span>
              <small>total</small>
            </div>
            <div>
              <strong>{{ passedAssessments }} passed</strong>
              <p>Your assessment results will feed back into your learning progress.</p>
            </div>
          </div>
        </article>
      </section>
    </template>

    <!-- PROGRESS MODAL -->
    <prime_dialog
      v-model:visible="showProgressModal"
      modal
      :header="selectedTopic?.title || 'UPDATE LEARNING'"
      :style="{ width: '500px' }"
      :breakpoints="{ '1199px': '75vw', '575px': '90vw' }"
      @hide="closeProgressModal"
    >
      <div class="progress-modal space-y-6 pt-2">
        <div class="modal-progress space-y-2">
          <div class="modal-progress-header flex justify-between text-sm">
            <span>How far are you?</span>
            <strong>{{ progressForm.progress_percent }}%</strong>
          </div>
          <prime_slider
            v-model="progressForm.progress_percent"
            :step="5"
            class="progress-slider w-full"
          />
        </div>

        <label
          class="practice-check flex items-start gap-3 p-3 border border-surface rounded-lg cursor-pointer"
        >
          <prime_check_box v-model="progressForm.practice_completed" :binary="true" />
          <span class="check-box">✓</span>
          <span>
            <strong>I practiced this topic</strong>
            <small>Mark this when you've actually applied what you learned.</small>
          </span>
        </label>

        <div class="notes-field space-y-2">
          <label>Learning notes</label>
          <prime_textarea
            v-model="progressForm.notes"
            rows="4"
            class="w-full"
            placeholder="What did you understand? What was difficult? What should you revisit?"
          />
        </div>
      </div>

      <template #footer>
        <div class="modal-actions flex justify-end gap-2">
          <prime_button
            label="Cancel"
            class="modal-cancel"
            variant="outlined"
            severity="secondary"
            :disabled="updatingProgress"
            @click="closeProgressModal"
          />
          <prime_button
            :label="updatingProgress ? 'Saving...' : 'Save progress'"
            :icon="updatingProgress ? 'pi pi-spin pi-spinner' : 'pi pi-check'"
            class="modal-save"
            :disabled="updatingProgress"
            @click="saveProgress"
          />
        </div>
      </template>
    </prime_dialog>
  </div>
</template>
