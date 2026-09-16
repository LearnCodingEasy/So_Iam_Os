<script setup>
import { computed, onMounted, ref } from 'vue'

import { RouterLink } from 'vue-router'

import { getLearningDashboard, updateLearningProgress } from '@/services/learning'

import LearningPathEditor from '@/components/learning/LearningPathEditor.vue'

// ============================================================
// STATE
// ============================================================

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

// ============================================================
// HELPERS
// ============================================================

const normalizeList = (data) => {
  if (Array.isArray(data)) {
    return data
  }

  if (data?.results && Array.isArray(data.results)) {
    return data.results
  }

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

const formatDate = (date) => {
  if (!date) {
    return 'No activity'
  }

  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  })
}

const formatMinutes = (minutes) => {
  if (!minutes) {
    return null
  }

  if (minutes < 60) {
    return `${minutes} min`
  }

  const hours = Math.floor(minutes / 60)
  const remaining = minutes % 60

  if (!remaining) {
    return `${hours}h`
  }

  return `${hours}h ${remaining}m`
}

// ============================================================
// DASHBOARD DATA
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

// ============================================================
// GLOBAL METRICS
// ============================================================

const totalTopics = computed(() => topics.value.length)

const completedTopics = computed(() => {
  return topics.value.filter((topic) => topic.status === 'completed').length
})

const activeTopics = computed(() => {
  return topics.value.filter((topic) => topic.status === 'in_progress').length
})

const practiceCount = computed(() => {
  return progress.value.filter((item) => item.practice_completed).length
})

const passedAssessments = computed(() => {
  return attempts.value.filter((attempt) => attempt.passed).length
})

const averageProgress = computed(() => {
  if (!topics.value.length) {
    return 0
  }

  const total = topics.value.reduce((sum, topic) => sum + getTopicProgress(topic.id), 0)

  return Math.round(total / topics.value.length)
})

// ============================================================
// CURRENT LEARNING
// ============================================================

const currentTopic = computed(() => {
  const inProgress = topics.value
    .filter((topic) => topic.status === 'in_progress')
    .sort((a, b) => getTopicProgress(b.id) - getTopicProgress(a.id))

  if (inProgress.length) {
    return inProgress[0]
  }

  const pending = topics.value
    .filter((topic) => topic.status === 'pending')
    .sort((a, b) => Number(a.order || 999) - Number(b.order || 999))

  return pending[0] || null
})

const currentPath = computed(() => {
  if (!currentTopic.value) {
    return null
  }

  return getPathById(currentTopic.value.path)
})

const currentGoal = computed(() => {
  if (!currentPath.value) {
    return null
  }

  return getGoalById(currentPath.value.goal)
})

const currentTopicProgress = computed(() => {
  if (!currentTopic.value) {
    return 0
  }

  return getTopicProgress(currentTopic.value.id)
})

// ============================================================
// GOAL PROGRESS
// ============================================================

const getGoalProgress = (goalId) => {
  const goalPaths = paths.value.filter((path) => Number(path.goal) === Number(goalId))

  const goalTopics = topics.value.filter((topic) =>
    goalPaths.some((path) => Number(path.id) === Number(topic.path)),
  )

  if (!goalTopics.length) {
    return 0
  }

  const total = goalTopics.reduce((sum, topic) => sum + getTopicProgress(topic.id), 0)

  return Math.round(total / goalTopics.length)
}

// ============================================================
// ROADMAP
// ============================================================

const pathTopics = (pathId) => {
  return topics.value
    .filter((topic) => Number(topic.path) === Number(pathId))
    .sort((a, b) => Number(a.order || 0) - Number(b.order || 0))
}

// ============================================================
// FILTERS
// ============================================================

const filteredTopics = computed(() => {
  let result = [...topics.value]

  if (activeFilter.value !== 'all') {
    result = result.filter((topic) => topic.status === activeFilter.value)
  }

  return result.sort((a, b) => Number(a.order || 0) - Number(b.order || 0))
})

// ============================================================
// RECENT ACTIVITY
// ============================================================

const recentTopics = computed(() => {
  return [...topics.value]
    .sort((a, b) => {
      const aDate = getProgressForTopic(a.id)?.last_activity_at || ''

      const bDate = getProgressForTopic(b.id)?.last_activity_at || ''

      return new Date(bDate) - new Date(aDate)
    })
    .slice(0, 5)
})

// ============================================================
// PROGRESS MODAL
// ============================================================

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
  if (updatingProgress.value) {
    return
  }

  showProgressModal.value = false
  selectedTopic.value = null
}

const saveProgress = async () => {
  if (!selectedTopic.value) {
    return
  }

  updatingProgress.value = true

  try {
    const payload = {
      topic: selectedTopic.value.id,

      progress_percent: Number(progressForm.value.progress_percent),

      practice_completed: progressForm.value.practice_completed,

      notes: progressForm.value.notes,
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
      const percentage = Number(progressForm.value.progress_percent)

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

// ============================================================
// LIFECYCLE
// ============================================================

onMounted(() => {
  loadLearningDashboard()
})
</script>

<template>
  <div class="learning-page">
    <!-- ======================================================
         HEADER
    ======================================================= -->

    <header class="page-header">
      <div class="header-copy">
        <div class="eyebrow">PERSONAL LEARNING OS</div>

        <h1>
          Keep learning.
          <span>Keep moving.</span>
        </h1>

        <p>Your learning system adapts around what you learn, practice and apply.</p>
      </div>

      <button class="refresh-button" :disabled="loading || refreshing" @click="refreshDashboard">
        <span class="refresh-icon" :class="{ spinning: refreshing }"> ↻ </span>

        {{ refreshing ? 'Refreshing' : 'Refresh' }}
      </button>
    </header>

    <!-- ======================================================
         ERROR
    ======================================================= -->

    <div v-if="error" class="error-banner">
      <div class="error-icon">!</div>

      <div>
        <strong> Something went wrong </strong>

        <span>
          {{ error }}
        </span>
      </div>

      <button @click="refreshDashboard">Try again</button>
    </div>

    <!-- ======================================================
         LOADING
    ======================================================= -->

    <div v-if="loading" class="loading-screen">
      <div class="loading-orbit">
        <span></span>
      </div>

      <h3>Building your learning space</h3>

      <p>Loading goals, topics and progress...</p>
    </div>

    <template v-else>
      <!-- ====================================================
           CONTINUE LEARNING
      ===================================================== -->

      <section class="hero-grid">
        <article class="continue-card">
          <div class="card-glow"></div>

          <div class="continue-content">
            <div class="section-label light">CONTINUE LEARNING</div>

            <template v-if="currentTopic">
              <div class="continue-meta">
                <span>
                  {{ currentPath?.title || 'Learning path' }}
                </span>

                <span class="dot"> • </span>

                <span>
                  {{ statusLabel(currentTopic.status) }}
                </span>
              </div>

              <h2>
                {{ currentTopic.title }}
              </h2>

              <p>
                {{
                  currentTopic.description || 'Continue building your understanding of this topic.'
                }}
              </p>

              <div class="continue-progress">
                <div class="progress-info">
                  <span> {{ currentTopicProgress }}% complete </span>

                  <strong>
                    {{ formatMinutes(currentTopic.estimated_minutes) }}
                  </strong>
                </div>

                <div class="progress-track dark">
                  <div
                    class="progress-value"
                    :style="{
                      width: currentTopicProgress + '%',
                    }"
                  ></div>
                </div>
              </div>

              <RouterLink
                :to="{
                  name: 'learning-topic',
                  params: {
                    topicId: currentTopic.id,
                  },
                }"
                class="primary-action"
              >
                Continue learning

                <span> → </span>
              </RouterLink>
            </template>

            <template v-else>
              <h2>Your learning journey starts here.</h2>

              <p>Create a goal and build your first learning path.</p>
            </template>
          </div>

          <div class="continue-number">
            <span>
              {{ currentTopic ? 'NEXT' : 'START' }}
            </span>

            <strong>
              {{ currentTopic ? String(currentTopic.order || 1).padStart(2, '0') : '01' }}
            </strong>
          </div>
        </article>

        <!-- OVERVIEW -->

        <article class="overview-card">
          <div class="overview-top">
            <div>
              <div class="section-label">OVERALL PROGRESS</div>

              <span class="overview-caption"> Across all learning topics </span>
            </div>

            <div class="overview-ring">
              <svg viewBox="0 0 100 100">
                <circle class="ring-background" cx="50" cy="50" r="42" />

                <circle
                  class="ring-progress"
                  cx="50"
                  cy="50"
                  r="42"
                  :style="{
                    strokeDasharray: `${averageProgress * 2.64} 264`,
                  }"
                />
              </svg>

              <strong> {{ averageProgress }}% </strong>
            </div>
          </div>

          <div class="overview-stats">
            <div>
              <strong>
                {{ totalTopics }}
              </strong>

              <span> Topics </span>
            </div>

            <div>
              <strong>
                {{ completedTopics }}
              </strong>

              <span> Completed </span>
            </div>

            <div>
              <strong>
                {{ practiceCount }}
              </strong>

              <span> Practiced </span>
            </div>
          </div>
        </article>
      </section>

      <!-- ====================================================
           GOALS
      ===================================================== -->

      <section class="section-block">
        <div class="section-heading">
          <div>
            <div class="section-label">DIRECTION</div>

            <h2>What are you building toward?</h2>
          </div>

          <span class="section-count"> {{ goals.length }} goals </span>
        </div>

        <div v-if="goals.length" class="goal-list">
          <article v-for="goal in goals" :key="goal.id" class="goal-card">
            <div class="goal-icon">◎</div>

            <div class="goal-content">
              <div class="goal-header">
                <h3>
                  {{ goal.title }}
                </h3>

                <span class="status-pill" :class="goal.status">
                  {{ statusLabel(goal.status) }}
                </span>
              </div>

              <p>
                {{ goal.description || 'No description available.' }}
              </p>

              <div class="goal-progress">
                <div class="goal-progress-top">
                  <span> {{ getGoalProgress(goal.id) }}% progress </span>

                  <span>
                    {{ goal.target_level || 'Target not set' }}
                  </span>
                </div>

                <div class="progress-track">
                  <div
                    class="progress-value"
                    :style="{
                      width: getGoalProgress(goal.id) + '%',
                    }"
                  ></div>
                </div>
              </div>
            </div>

            <div class="goal-side">
              <span v-if="goal.target_date">
                Target
                <strong>
                  {{ formatDate(goal.target_date) }}
                </strong>
              </span>

              <span v-if="goal.skill">
                Skill
                <strong>
                  {{ getSkillById(goal.skill)?.name || `#${goal.skill}` }}
                </strong>
              </span>
            </div>
          </article>
        </div>

        <div v-else class="empty-card">
          <div class="empty-symbol">+</div>

          <h3>No learning goals yet</h3>

          <p>Your goals will become the direction of your learning system.</p>
        </div>
      </section>

      <!-- ====================================================
           ROADMAP
      ===================================================== -->

      <section class="section-block roadmap-section">
        <div class="section-heading">
          <div>
            <div class="section-label">ROADMAP</div>

            <h2>Your learning path</h2>

            <p>Follow the sequence, or reshape it around your needs.</p>
          </div>

          <button class="secondary-action" @click="showRoadmapEditor = !showRoadmapEditor">
            {{ showRoadmapEditor ? 'Close editor' : 'Edit roadmap' }}
          </button>
        </div>

        <!-- EDITOR -->

        <div v-if="showRoadmapEditor" class="roadmap-editor-wrapper">
          <LearningPathEditor
            :paths="paths"
            :topics="topics"
            :progress="progress"
            @refresh="refreshDashboard"
          />
        </div>

        <!-- ROADMAP -->

        <div v-if="paths.length" class="roadmap-list">
          <article v-for="path in paths" :key="path.id" class="roadmap-card">
            <div class="roadmap-number">
              {{ String(path.id).padStart(2, '0') }}
            </div>

            <div class="roadmap-main">
              <div class="roadmap-header">
                <div>
                  <span class="path-status">
                    {{ statusLabel(path.status) }}
                  </span>

                  <h3>
                    {{ path.title }}
                  </h3>
                </div>

                <span class="topic-count">
                  {{ pathTopics(path.id).length }}
                  topics
                </span>
              </div>

              <p>
                {{ path.description || 'Learning path without a description.' }}
              </p>

              <!-- TOPIC TIMELINE -->

              <div class="topic-timeline">
                <RouterLink
                  v-for="(topic, index) in pathTopics(path.id)"
                  :key="topic.id"
                  :to="{
                    name: 'learning-topic',
                    params: {
                      topicId: topic.id,
                    },
                  }"
                  class="timeline-topic"
                  :class="{
                    completed: topic.status === 'completed',
                    active: topic.status === 'in_progress',
                  }"
                >
                  <div class="timeline-node">
                    <span v-if="topic.status === 'completed'"> ✓ </span>

                    <span v-else>
                      {{ index + 1 }}
                    </span>
                  </div>

                  <div class="timeline-content">
                    <strong>
                      {{ topic.title }}
                    </strong>

                    <span> {{ getTopicProgress(topic.id) }}% </span>
                  </div>
                </RouterLink>
              </div>
            </div>
          </article>
        </div>

        <div v-else class="empty-card">
          <div class="empty-symbol">+</div>

          <h3>No learning paths yet</h3>

          <p>Your paths will organize the journey from goal to practical mastery.</p>
        </div>
      </section>

      <!-- ====================================================
           TOPICS
      ===================================================== -->

      <section class="section-block">
        <div class="section-heading topics-heading">
          <div>
            <div class="section-label">LEARN + PRACTICE</div>

            <h2>Your topics</h2>
          </div>

          <div class="filter-tabs">
            <button :class="{ active: activeFilter === 'all' }" @click="activeFilter = 'all'">
              All
            </button>

            <button
              :class="{ active: activeFilter === 'in_progress' }"
              @click="activeFilter = 'in_progress'"
            >
              In progress
            </button>

            <button
              :class="{ active: activeFilter === 'pending' }"
              @click="activeFilter = 'pending'"
            >
              Upcoming
            </button>

            <button
              :class="{ active: activeFilter === 'completed' }"
              @click="activeFilter = 'completed'"
            >
              Completed
            </button>
          </div>
        </div>

        <div v-if="filteredTopics.length" class="topic-list">
          <article v-for="topic in filteredTopics" :key="topic.id" class="learning-topic-card">
            <div class="topic-order">
              {{ String(topic.order || topic.id).padStart(2, '0') }}
            </div>

            <div class="topic-body">
              <div class="topic-top">
                <div class="topic-info">
                  <div class="topic-meta">
                    <span class="status-dot" :class="topic.status"></span>

                    {{ statusLabel(topic.status) }}

                    <span v-if="topic.estimated_minutes">
                      · {{ formatMinutes(topic.estimated_minutes) }}
                    </span>
                  </div>

                  <h3>
                    {{ topic.title }}
                  </h3>

                  <p>
                    {{ topic.description || 'Start exploring this topic.' }}
                  </p>
                </div>

                <div class="topic-percent">{{ getTopicProgress(topic.id) }}%</div>
              </div>

              <div class="topic-progress">
                <div class="progress-track">
                  <div
                    class="progress-value"
                    :style="{
                      width: getTopicProgress(topic.id) + '%',
                    }"
                  ></div>
                </div>
              </div>

              <div class="topic-footer">
                <span v-if="topic.skill" class="skill-chip">
                  {{ getSkillById(topic.skill)?.name || `Skill #${topic.skill}` }}
                </span>

                <div class="topic-actions">
                  <button class="ghost-action" @click="openProgressModal(topic)">
                    Update progress
                  </button>

                  <RouterLink
                    :to="{
                      name: 'learning-topic',
                      params: {
                        topicId: topic.id,
                      },
                    }"
                    class="topic-open"
                  >
                    Open topic
                    <span>→</span>
                  </RouterLink>
                </div>
              </div>
            </div>
          </article>
        </div>

        <div v-else class="empty-card">
          <h3>Nothing here yet</h3>

          <p>Topics matching this filter will appear here.</p>
        </div>
      </section>

      <!-- ====================================================
           PRACTICE / APPLICATION
      ===================================================== -->

      <section class="practice-banner">
        <div class="practice-copy">
          <div class="section-label light">APPLY KNOWLEDGE</div>

          <h2>
            Don't just learn it.
            <span>Use it.</span>
          </h2>

          <p>
            Turn what you studied into a real application, project or explanation. Your learning
            system can review what you produce and identify what needs more attention.
          </p>
        </div>

        <div class="practice-flow">
          <div class="flow-step">
            <span>01</span>
            Learn
          </div>

          <div class="flow-arrow">→</div>

          <div class="flow-step active">
            <span>02</span>
            Apply
          </div>

          <div class="flow-arrow">→</div>

          <div class="flow-step">
            <span>03</span>
            Review
          </div>
        </div>

        <RouterLink
          v-if="currentTopic"
          :to="{
            name: 'learning-topic',
            params: {
              topicId: currentTopic.id,
            },
          }"
          class="practice-action"
        >
          Start application
          <span>→</span>
        </RouterLink>
      </section>

      <!-- ====================================================
           INSIGHTS
      ===================================================== -->

      <section class="bottom-grid">
        <!-- RECENT -->

        <article class="activity-card">
          <div class="section-heading compact">
            <div>
              <div class="section-label">ACTIVITY</div>

              <h2>Recent learning</h2>
            </div>
          </div>

          <div v-if="recentTopics.length" class="activity-list">
            <RouterLink
              v-for="topic in recentTopics"
              :key="topic.id"
              :to="{
                name: 'learning-topic',
                params: {
                  topicId: topic.id,
                },
              }"
              class="activity-item"
            >
              <div class="activity-dot" :class="topic.status"></div>

              <div class="activity-info">
                <strong>
                  {{ topic.title }}
                </strong>

                <span>
                  {{
                    getProgressForTopic(topic.id)?.last_activity_at
                      ? formatDate(getProgressForTopic(topic.id).last_activity_at)
                      : 'No activity'
                  }}
                </span>
              </div>

              <strong class="activity-percent"> {{ getTopicProgress(topic.id) }}% </strong>
            </RouterLink>
          </div>

          <div v-else class="small-empty">Start learning to see your activity here.</div>
        </article>

        <!-- ASSESSMENTS -->

        <article class="assessment-summary-card">
          <div class="section-heading compact">
            <div>
              <div class="section-label">EVALUATION</div>

              <h2>Assessments</h2>
            </div>

            <strong class="assessment-number">
              {{ passedAssessments }}
            </strong>
          </div>

          <div class="assessment-stat">
            <div class="assessment-circle">
              <span>
                {{ assessments.length }}
              </span>

              <small> total </small>
            </div>

            <div>
              <strong>
                {{ passedAssessments }}
                passed
              </strong>

              <p>Your assessment results will feed back into your learning progress.</p>
            </div>
          </div>
        </article>
      </section>
    </template>

    <!-- ======================================================
         PROGRESS MODAL
    ======================================================= -->

    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showProgressModal" class="modal-backdrop" @click.self="closeProgressModal">
          <div class="progress-modal">
            <div class="modal-top">
              <div>
                <span class="section-label"> UPDATE LEARNING </span>

                <h2>
                  {{ selectedTopic?.title }}
                </h2>
              </div>

              <button class="modal-close" @click="closeProgressModal">×</button>
            </div>

            <div class="modal-progress">
              <div class="modal-progress-header">
                <span> How far are you? </span>

                <strong> {{ progressForm.progress_percent }}% </strong>
              </div>

              <input
                v-model.number="progressForm.progress_percent"
                type="range"
                min="0"
                max="100"
                step="5"
                class="progress-slider"
              />
            </div>

            <label class="practice-check">
              <input v-model="progressForm.practice_completed" type="checkbox" />

              <span class="check-box"> ✓ </span>

              <span>
                <strong> I practiced this topic </strong>

                <small> Mark this when you've actually applied what you learned. </small>
              </span>
            </label>

            <div class="notes-field">
              <label> Learning notes </label>

              <textarea
                v-model="progressForm.notes"
                rows="5"
                placeholder="What did you understand? What was difficult? What should you revisit?"
              ></textarea>
            </div>

            <div class="modal-actions">
              <button class="modal-cancel" :disabled="updatingProgress" @click="closeProgressModal">
                Cancel
              </button>

              <button class="modal-save" :disabled="updatingProgress" @click="saveProgress">
                {{ updatingProgress ? 'Saving...' : 'Save progress' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
/* ============================================================
   BASE
============================================================ */

.learning-page {
  --ink: #171717;
  --muted: #747474;
  --soft: #a0a0a0;
  --line: #e8e8e8;
  --surface: #ffffff;
  --surface-soft: #f7f7f5;
  --accent: #111111;
  --success: #2f7d5a;
  --warning: #a9792e;

  min-height: 100%;
  padding: 42px;
  background: radial-gradient(circle at 85% 0%, rgba(0, 0, 0, 0.035), transparent 28%), #fafaf8;

  color: var(--ink);
}

/* ============================================================
   HEADER
============================================================ */

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 30px;
  margin-bottom: 38px;
}

.header-copy {
  max-width: 760px;
}

.eyebrow,
.section-label {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.18em;
  color: #8b8b8b;
}

.header-copy h1 {
  margin: 10px 0 8px;
  font-size: clamp(38px, 5vw, 68px);
  line-height: 0.95;
  letter-spacing: -0.055em;
  font-weight: 800;
}

.header-copy h1 span {
  color: #969696;
}

.header-copy p {
  margin: 0;
  max-width: 650px;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.7;
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 9px;
  height: 42px;
  padding: 0 17px;
  border: 1px solid #dededb;
  border-radius: 10px;
  background: #fff;
  color: #333;
  cursor: pointer;
  transition: 0.2s ease;
}

.refresh-button:hover:not(:disabled) {
  transform: translateY(-1px);
  border-color: #bdbdb8;
}

.refresh-button:disabled {
  opacity: 0.55;
  cursor: wait;
}

.refresh-icon {
  font-size: 18px;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

/* ============================================================
   ERROR
============================================================ */

.error-banner {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 25px;
  padding: 15px 18px;
  border: 1px solid #eaded8;
  border-radius: 14px;
  background: #fff9f6;
}

.error-icon {
  display: grid;
  width: 32px;
  height: 32px;
  place-items: center;
  border-radius: 50%;
  background: #ead4c9;
  color: #714b3d;
  font-weight: 800;
}

.error-banner div:nth-child(2) {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 3px;
}

.error-banner span {
  color: #8b756b;
  font-size: 13px;
}

.error-banner button {
  border: 0;
  background: transparent;
  text-decoration: underline;
  cursor: pointer;
}

/* ============================================================
   HERO
============================================================ */

.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) minmax(300px, 0.8fr);
  gap: 16px;
  margin-bottom: 65px;
}

.continue-card {
  position: relative;
  min-height: 355px;
  overflow: hidden;
  display: flex;
  justify-content: space-between;
  border-radius: 25px;
  background: #151515;
  color: white;
}

.card-glow {
  position: absolute;
  width: 400px;
  height: 400px;
  right: -120px;
  top: -180px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  filter: blur(1px);
}

.continue-content {
  position: relative;
  z-index: 2;
  max-width: 670px;
  padding: 42px;
}

.section-label.light {
  color: #7e7e7e;
}

.continue-card .section-label.light {
  color: #777;
}

.continue-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 22px;
  color: #898989;
  font-size: 12px;
}

.continue-meta .dot {
  color: #555;
}

.continue-content h2 {
  margin: 12px 0 12px;
  font-size: clamp(28px, 3.5vw, 46px);
  line-height: 1;
  letter-spacing: -0.045em;
}

.continue-content p {
  max-width: 600px;
  margin: 0;
  color: #a2a2a2;
  font-size: 14px;
  line-height: 1.7;
}

.continue-progress {
  margin-top: 30px;
  max-width: 560px;
}

.progress-info,
.goal-progress-top,
.modal-progress-header {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 9px;
  font-size: 11px;
}

.progress-info span {
  color: #999;
}

.progress-info strong {
  color: #ddd;
}

.progress-track {
  height: 5px;
  overflow: hidden;
  border-radius: 20px;
  background: #e9e9e7;
}

.progress-track.dark {
  background: #292929;
}

.progress-value {
  height: 100%;
  border-radius: inherit;
  background: #222;
  transition: width 0.5s ease;
}

.dark .progress-value,
.progress-track.dark .progress-value {
  background: #f1f1f1;
}

.primary-action,
.practice-action {
  display: inline-flex;
  align-items: center;
  gap: 25px;
  margin-top: 27px;
  padding: 13px 16px;
  border-radius: 10px;
  background: white;
  color: #111;
  font-size: 12px;
  font-weight: 750;
  text-decoration: none;
  transition: 0.2s ease;
}

.primary-action:hover,
.practice-action:hover {
  transform: translateY(-2px);
  gap: 31px;
}

.continue-number {
  position: relative;
  z-index: 2;
  align-self: flex-end;
  padding: 0 34px 34px 0;
  text-align: right;
}

.continue-number span {
  display: block;
  margin-bottom: 4px;
  color: #696969;
  font-size: 9px;
  letter-spacing: 0.16em;
}

.continue-number strong {
  font-size: 58px;
  line-height: 1;
  color: #292929;
}

/* ============================================================
   OVERVIEW
============================================================ */

.overview-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 355px;
  padding: 31px;
  border: 1px solid var(--line);
  border-radius: 25px;
  background: #fff;
}

.overview-top {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.overview-caption {
  display: block;
  margin-top: 7px;
  color: #9a9a9a;
  font-size: 11px;
}

.overview-ring {
  position: relative;
  width: 95px;
  height: 95px;
  flex: 0 0 95px;
}

.overview-ring svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.ring-background,
.ring-progress {
  fill: none;
  stroke-width: 6;
}

.ring-background {
  stroke: #ededeb;
}

.ring-progress {
  stroke: #222;
  stroke-linecap: round;
  transition: stroke-dasharray 0.6s ease;
}

.overview-ring strong {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  font-size: 20px;
  letter-spacing: -0.04em;
}

.overview-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.overview-stats > div {
  padding-top: 17px;
  border-top: 1px solid var(--line);
}

.overview-stats strong,
.overview-stats span {
  display: block;
}

.overview-stats strong {
  font-size: 22px;
}

.overview-stats span {
  margin-top: 4px;
  color: #999;
  font-size: 10px;
}

/* ============================================================
   SECTIONS
============================================================ */

.section-block {
  margin-bottom: 72px;
}

.section-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 25px;
  margin-bottom: 22px;
}

.section-heading h2 {
  margin: 7px 0 0;
  font-size: 25px;
  letter-spacing: -0.035em;
}

.section-heading p {
  margin: 7px 0 0;
  color: #8c8c8c;
  font-size: 12px;
}

.section-count {
  color: #9b9b9b;
  font-size: 11px;
}

/* ============================================================
   GOALS
============================================================ */

.goal-list {
  display: grid;
  gap: 10px;
}

.goal-card {
  display: grid;
  grid-template-columns: 48px minmax(0, 1fr) 150px;
  gap: 22px;
  align-items: center;
  padding: 23px;
  border: 1px solid var(--line);
  border-radius: 17px;
  background: #fff;
  transition: 0.2s ease;
}

.goal-card:hover {
  border-color: #d3d3d0;
  transform: translateY(-1px);
}

.goal-icon {
  display: grid;
  width: 45px;
  height: 45px;
  place-items: center;
  border: 1px solid #ddd;
  border-radius: 12px;
  color: #555;
  font-size: 21px;
}

.goal-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.goal-header h3 {
  margin: 0;
  font-size: 16px;
  letter-spacing: -0.02em;
}

.goal-content p {
  margin: 7px 0 15px;
  color: #8d8d8d;
  font-size: 12px;
}

.status-pill {
  padding: 5px 8px;
  border-radius: 999px;
  background: #f0f0ee;
  color: #666;
  font-size: 9px;
  font-weight: 700;
}

.status-pill.active {
  background: #edf5f0;
  color: #397056;
}

.goal-progress-top {
  color: #888;
}

.goal-side {
  display: flex;
  flex-direction: column;
  gap: 12px;
  text-align: right;
}

.goal-side span {
  display: flex;
  flex-direction: column;
  color: #aaa;
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.goal-side strong {
  margin-top: 3px;
  color: #333;
  font-size: 11px;
  text-transform: none;
  letter-spacing: 0;
}

/* ============================================================
   EMPTY
============================================================ */

.empty-card {
  padding: 65px 30px;
  border: 1px dashed #d8d8d5;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.5);
  text-align: center;
}

.empty-symbol {
  display: grid;
  width: 42px;
  height: 42px;
  margin: 0 auto 15px;
  place-items: center;
  border: 1px solid #ddd;
  border-radius: 50%;
  color: #777;
  font-size: 20px;
}

.empty-card h3 {
  margin: 0 0 6px;
  font-size: 16px;
}

.empty-card p {
  margin: 0;
  color: #999;
  font-size: 12px;
}

/* ============================================================
   ROADMAP
============================================================ */

.roadmap-section {
  position: relative;
}

.secondary-action {
  height: 38px;
  padding: 0 14px;
  border: 1px solid #dcdcd8;
  border-radius: 9px;
  background: #fff;
  color: #444;
  font-size: 11px;
  cursor: pointer;
  transition: 0.2s ease;
}

.secondary-action:hover {
  border-color: #bdbdb8;
}

.roadmap-editor-wrapper {
  margin-bottom: 15px;
  padding: 20px;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: white;
}

.roadmap-list {
  display: grid;
  gap: 12px;
}

.roadmap-card {
  display: grid;
  grid-template-columns: 58px minmax(0, 1fr);
  gap: 22px;
  padding: 25px;
  border: 1px solid var(--line);
  border-radius: 19px;
  background: #fff;
}

.roadmap-number {
  font-size: 22px;
  font-weight: 800;
  color: #d2d2cf;
  letter-spacing: -0.04em;
}

.roadmap-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}

.path-status {
  color: #999;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.13em;
  text-transform: uppercase;
}

.roadmap-header h3 {
  margin: 6px 0 0;
  font-size: 18px;
  letter-spacing: -0.025em;
}

.topic-count {
  color: #999;
  font-size: 10px;
}

.roadmap-main > p {
  margin: 8px 0 20px;
  color: #8d8d8d;
  font-size: 12px;
}

.topic-timeline {
  display: flex;
  overflow-x: auto;
  padding: 7px 0 5px;
}

.timeline-topic {
  position: relative;
  min-width: 150px;
  flex: 1;
  padding-right: 15px;
  text-decoration: none;
  color: inherit;
}

.timeline-topic:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 15px;
  left: 31px;
  right: 15px;
  height: 1px;
  background: #dededb;
}

.timeline-node {
  position: relative;
  z-index: 2;
  display: grid;
  width: 30px;
  height: 30px;
  place-items: center;
  margin-bottom: 9px;
  border: 1px solid #ddd;
  border-radius: 50%;
  background: #fff;
  color: #999;
  font-size: 9px;
  font-weight: 800;
}

.timeline-topic.completed .timeline-node {
  border-color: #333;
  background: #333;
  color: white;
}

.timeline-topic.active .timeline-node {
  border-color: #333;
  box-shadow: 0 0 0 4px #f0f0ed;
}

.timeline-content {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding-right: 10px;
}

.timeline-content strong {
  font-size: 11px;
  line-height: 1.35;
}

.timeline-content span {
  color: #999;
  font-size: 9px;
}

/* ============================================================
   TOPICS
============================================================ */

.topics-heading {
  align-items: center;
}

.filter-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  padding: 4px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: #f3f3f1;
}

.filter-tabs button {
  padding: 7px 11px;
  border: 0;
  border-radius: 7px;
  background: transparent;
  color: #8d8d8d;
  font-size: 10px;
  cursor: pointer;
}

.filter-tabs button.active {
  background: #fff;
  color: #222;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.topic-list {
  display: grid;
  gap: 10px;
}

.learning-topic-card {
  display: grid;
  grid-template-columns: 60px minmax(0, 1fr);
  gap: 18px;
  padding: 24px;
  border: 1px solid var(--line);
  border-radius: 17px;
  background: #fff;
  transition: 0.2s ease;
}

.learning-topic-card:hover {
  border-color: #cfcfcb;
  transform: translateY(-1px);
}

.topic-order {
  color: #c4c4c1;
  font-size: 22px;
  font-weight: 800;
}

.topic-top {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.topic-meta {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 6px;
  color: #999;
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #bbb;
}

.status-dot.in_progress {
  background: #444;
  box-shadow: 0 0 0 4px #eeeeeb;
}

.status-dot.completed {
  background: var(--success);
}

.topic-info h3 {
  margin: 0;
  font-size: 16px;
  letter-spacing: -0.02em;
}

.topic-info p {
  margin: 7px 0 0;
  color: #8d8d8d;
  font-size: 12px;
}

.topic-percent {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.04em;
}

.topic-progress {
  margin-top: 20px;
}

.topic-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  margin-top: 17px;
}

.skill-chip {
  padding: 5px 8px;
  border: 1px solid #e4e4e1;
  border-radius: 7px;
  color: #888;
  font-size: 9px;
}

.topic-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ghost-action,
.topic-open {
  border: 0;
  background: transparent;
  color: #777;
  font-size: 10px;
  cursor: pointer;
  text-decoration: none;
}

.topic-open {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #222;
  font-weight: 750;
}

.topic-open span {
  transition: 0.2s ease;
}

.topic-open:hover span {
  transform: translateX(3px);
}

/* ============================================================
   PRACTICE
============================================================ */

.practice-banner {
  position: relative;
  display: grid;
  grid-template-columns: 1.5fr 1fr auto;
  align-items: center;
  gap: 35px;
  margin-bottom: 70px;
  padding: 36px;
  overflow: hidden;
  border-radius: 23px;
  background: #151515;
  color: white;
}

.practice-banner::after {
  content: '';
  position: absolute;
  width: 300px;
  height: 300px;
  right: -120px;
  bottom: -200px;
  border-radius: 50%;
  border: 1px solid #333;
}

.practice-copy {
  position: relative;
  z-index: 2;
}

.practice-copy h2 {
  margin: 8px 0 10px;
  font-size: 30px;
  line-height: 1;
  letter-spacing: -0.04em;
}

.practice-copy h2 span {
  color: #777;
}

.practice-copy p {
  max-width: 580px;
  margin: 0;
  color: #999;
  font-size: 12px;
  line-height: 1.7;
}

.practice-flow {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #777;
}

.flow-step {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 10px;
}

.flow-step span {
  color: #555;
  font-size: 8px;
}

.flow-step.active {
  color: white;
}

.flow-step.active span {
  color: #999;
}

.flow-arrow {
  color: #555;
}

.practice-action {
  position: relative;
  z-index: 2;
  margin: 0;
  white-space: nowrap;
}

/* ============================================================
   BOTTOM
============================================================ */

.bottom-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 15px;
  margin-bottom: 40px;
}

.activity-card,
.assessment-summary-card {
  padding: 26px;
  border: 1px solid var(--line);
  border-radius: 19px;
  background: white;
}

.section-heading.compact {
  margin-bottom: 18px;
}

.section-heading.compact h2 {
  font-size: 20px;
}

.activity-list {
  display: grid;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px 0;
  border-top: 1px solid #eeeeec;
  text-decoration: none;
  color: inherit;
}

.activity-dot {
  width: 7px;
  height: 7px;
  flex: 0 0 7px;
  border-radius: 50%;
  background: #bbb;
}

.activity-dot.in_progress {
  background: #333;
}

.activity-dot.completed {
  background: var(--success);
}

.activity-info {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 3px;
}

.activity-info strong {
  font-size: 11px;
}

.activity-info span {
  color: #aaa;
  font-size: 9px;
}

.activity-percent {
  font-size: 11px;
}

.small-empty {
  padding: 20px 0;
  color: #999;
  font-size: 11px;
}

.assessment-number {
  font-size: 20px;
}

.assessment-stat {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-top: 15px;
}

.assessment-circle {
  display: flex;
  width: 80px;
  height: 80px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid #ddd;
  border-radius: 50%;
}

.assessment-circle span {
  font-size: 20px;
  font-weight: 800;
}

.assessment-circle small {
  color: #999;
  font-size: 8px;
}

.assessment-stat > div:last-child {
  flex: 1;
}

.assessment-stat strong {
  font-size: 13px;
}

.assessment-stat p {
  margin: 7px 0 0;
  color: #999;
  font-size: 11px;
  line-height: 1.6;
}

/* ============================================================
   MODAL
============================================================ */

.modal-backdrop {
  position: fixed;
  z-index: 1000;
  inset: 0;
  display: grid;
  place-items: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.48);
  backdrop-filter: blur(7px);
}

.progress-modal {
  width: min(560px, 100%);
  padding: 29px;
  border-radius: 22px;
  background: #fff;
  box-shadow: 0 30px 90px rgba(0, 0, 0, 0.22);
}

.modal-top {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 32px;
}

.modal-top h2 {
  margin: 7px 0 0;
  max-width: 420px;
  font-size: 24px;
  letter-spacing: -0.035em;
}

.modal-close {
  width: 34px;
  height: 34px;
  border: 1px solid #e2e2df;
  border-radius: 50%;
  background: white;
  color: #555;
  font-size: 20px;
  cursor: pointer;
}

.modal-progress {
  margin-bottom: 27px;
}

.modal-progress-header {
  align-items: center;
  color: #777;
}

.modal-progress-header strong {
  color: #111;
  font-size: 18px;
}

.progress-slider {
  width: 100%;
  accent-color: #222;
  cursor: pointer;
}

.practice-check {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 25px;
  padding: 15px;
  border: 1px solid #e7e7e4;
  border-radius: 12px;
  cursor: pointer;
}

.practice-check input {
  position: absolute;
  opacity: 0;
}

.check-box {
  display: grid;
  width: 20px;
  height: 20px;
  flex: 0 0 20px;
  place-items: center;
  border: 1px solid #ccc;
  border-radius: 5px;
  color: transparent;
  font-size: 12px;
}

.practice-check input:checked + .check-box {
  border-color: #222;
  background: #222;
  color: white;
}

.practice-check strong,
.practice-check small {
  display: block;
}

.practice-check strong {
  font-size: 12px;
}

.practice-check small {
  margin-top: 3px;
  color: #999;
  font-size: 10px;
  line-height: 1.5;
}

.notes-field label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-size: 10px;
  font-weight: 750;
}

.notes-field textarea {
  width: 100%;
  box-sizing: border-box;
  resize: vertical;
  padding: 13px;
  border: 1px solid #dededb;
  border-radius: 11px;
  outline: none;
  font: inherit;
  font-size: 12px;
  line-height: 1.6;
  transition: 0.2s ease;
}

.notes-field textarea:focus {
  border-color: #999;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 23px;
}

.modal-cancel,
.modal-save {
  height: 40px;
  padding: 0 17px;
  border-radius: 9px;
  font-size: 11px;
  cursor: pointer;
}

.modal-cancel {
  border: 1px solid #ddd;
  background: white;
  color: #666;
}

.modal-save {
  border: 1px solid #222;
  background: #222;
  color: white;
}

.modal-save:disabled,
.modal-cancel:disabled {
  opacity: 0.5;
  cursor: wait;
}

/* ============================================================
   TRANSITIONS
============================================================ */

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-active .progress-modal,
.modal-leave-active .progress-modal {
  transition: transform 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .progress-modal,
.modal-leave-to .progress-modal {
  transform: translateY(10px) scale(0.98);
}

/* ============================================================
   LOADING
============================================================ */

.loading-screen {
  min-height: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.loading-orbit {
  position: relative;
  width: 46px;
  height: 46px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 50%;
  animation: spin 1.4s linear infinite;
}

.loading-orbit::before {
  content: '';
  position: absolute;
  top: -3px;
  left: 50%;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #222;
  transform: translateX(-50%);
}

.loading-screen h3 {
  margin: 0 0 6px;
  font-size: 15px;
}

.loading-screen p {
  margin: 0;
  color: #999;
  font-size: 11px;
}

/* ============================================================
   RESPONSIVE
============================================================ */

@media (max-width: 1100px) {
  .learning-page {
    padding: 30px;
  }

  .hero-grid {
    grid-template-columns: 1fr;
  }

  .practice-banner {
    grid-template-columns: 1fr;
  }

  .practice-action {
    justify-self: start;
  }
}

@media (max-width: 800px) {
  .learning-page {
    padding: 22px 17px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .header-copy h1 {
    font-size: 42px;
  }

  .continue-content {
    padding: 30px 25px;
  }

  .continue-card {
    min-height: 390px;
  }

  .continue-number {
    display: none;
  }

  .goal-card {
    grid-template-columns: 42px minmax(0, 1fr);
  }

  .goal-side {
    display: none;
  }

  .goal-icon {
    width: 40px;
    height: 40px;
  }

  .bottom-grid {
    grid-template-columns: 1fr;
  }

  .topics-heading,
  .section-heading {
    align-items: flex-start;
    flex-direction: column;
  }

  .filter-tabs {
    width: 100%;
  }

  .filter-tabs button {
    flex: 1;
  }

  .topic-footer {
    align-items: flex-start;
    flex-direction: column;
  }

  .topic-actions {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 550px) {
  .overview-top {
    align-items: flex-start;
    flex-direction: column;
  }

  .overview-ring {
    align-self: flex-end;
  }

  .overview-stats {
    margin-top: 25px;
  }

  .roadmap-card {
    grid-template-columns: 1fr;
    gap: 5px;
  }

  .roadmap-number {
    font-size: 13px;
  }

  .topic-timeline {
    flex-direction: column;
    gap: 10px;
  }

  .timeline-topic {
    display: grid;
    grid-template-columns: 30px 1fr;
    min-width: 0;
    gap: 10px;
  }

  .timeline-topic:not(:last-child)::after {
    top: 30px;
    left: 14px;
    right: auto;
    width: 1px;
    height: 25px;
  }

  .timeline-node {
    margin-bottom: 0;
  }

  .practice-banner {
    padding: 28px 23px;
  }

  .practice-flow {
    display: none;
  }

  .learning-topic-card {
    grid-template-columns: 40px minmax(0, 1fr);
    padding: 20px;
  }

  .topic-order {
    font-size: 16px;
  }

  .topic-top {
    align-items: flex-start;
  }

  .topic-percent {
    font-size: 17px;
  }

  .modal-backdrop {
    align-items: flex-end;
    padding: 0;
  }

  .progress-modal {
    border-radius: 22px 22px 0 0;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
