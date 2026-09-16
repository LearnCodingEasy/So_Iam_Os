<script setup>
import { computed, onMounted, ref } from 'vue'

import { RouterLink, useRoute } from 'vue-router'

import { getLearningTopic } from '@/services/learning'

import ApplicationComposer from '@/components/learning/ApplicationComposer.vue'

import AIReviewPanel from '@/components/learning/AIReviewPanel.vue'

const route = useRoute()

const loading = ref(true)

const error = ref('')

const topic = ref(null)

const activeApplication = ref(null)

const loadTopic = async () => {
  loading.value = true
  error.value = ''

  try {
    topic.value = await getLearningTopic(Number(route.params.topicId))

    const applications = topic.value?.applications || []

    activeApplication.value = applications[0] || null
  } catch (err) {
    console.error('Topic load error:', err)

    error.value = err?.response?.data?.detail || 'Unable to load this topic.'
  } finally {
    loading.value = false
  }
}

const handleApplicationUpdated = (application) => {
  activeApplication.value = application

  if (!topic.value) {
    return
  }

  const applications = topic.value.applications || []

  const index = applications.findIndex((item) => item.id === application.id)

  if (index >= 0) {
    applications[index] = application
  } else {
    applications.unshift(application)
  }

  topic.value.applications = applications
}

const progress = computed(() => {
  return topic.value?.progress?.progress_percent ?? 0
})

const mastery = computed(() => {
  return topic.value?.progress?.mastery_level || 'not_started'
})

const review = computed(() => {
  return activeApplication.value?.review || null
})

const knowledgeItems = computed(() => {
  return topic.value?.knowledge_items || []
})

const assessments = computed(() => {
  return topic.value?.assessments || []
})

onMounted(loadTopic)
</script>

<template>
  <div class="topic-page">
    <!-- Loading -->
    <div v-if="loading" class="topic-loading">
      <div class="loader"></div>

      <p>Loading topic...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="topic-error">
      {{ error }}
    </div>

    <template v-else-if="topic">
      <!-- Breadcrumb -->
      <nav class="topic-breadcrumb">
        <RouterLink to="/learning"> Learning </RouterLink>

        <span> / </span>

        <span>
          {{ topic.path?.title }}
        </span>

        <span> / </span>

        <strong>
          {{ topic.title }}
        </strong>
      </nav>

      <!-- Hero -->
      <header class="topic-hero">
        <div class="topic-hero-main">
          <div class="topic-kicker">TOPIC {{ topic.order }}</div>

          <h1>
            {{ topic.title }}
          </h1>

          <p>
            {{ topic.description || 'No description available.' }}
          </p>

          <div class="topic-meta-row">
            <span>
              {{ topic.status }}
            </span>

            <span v-if="topic.estimated_minutes">
              {{ topic.estimated_minutes }}
              minutes
            </span>

            <span v-if="topic.skill"> Skill #{{ topic.skill }} </span>
          </div>
        </div>

        <!-- Progress -->
        <div class="topic-progress-card">
          <span> PROGRESS </span>

          <strong> {{ progress }}% </strong>

          <div class="topic-progress-track">
            <div
              class="topic-progress-fill"
              :style="{
                width: `${progress}%`,
              }"
            />
          </div>

          <small>
            Mastery:
            {{ mastery }}
          </small>
        </div>
      </header>

      <!-- Learning -->
      <section class="workspace-section">
        <div class="workspace-section-header">
          <div>
            <span class="section-kicker"> KNOWLEDGE </span>

            <h2>What you're learning</h2>
          </div>

          <span>
            {{ knowledgeItems.length }}
            items
          </span>
        </div>

        <div v-if="knowledgeItems.length" class="knowledge-grid">
          <article v-for="item in knowledgeItems" :key="item.id" class="knowledge-card">
            <span>
              {{ item.knowledge_type }}
            </span>

            <h3>
              {{ item.title }}
            </h3>

            <p>
              {{ item.description || item.content || 'No content.' }}
            </p>

            <div v-if="item.tags?.length" class="knowledge-tags">
              <span v-for="tag in item.tags" :key="tag"> #{{ tag }} </span>
            </div>
          </article>
        </div>

        <div v-else class="workspace-empty">No knowledge items connected to this topic yet.</div>
      </section>

      <!-- Application -->
      <ApplicationComposer
        :topic-id="topic.id"
        :application="activeApplication"
        @updated="handleApplicationUpdated"
      />

      <!-- AI -->
      <AIReviewPanel v-if="review" :review="review" />

      <!-- Assessments -->
      <section class="workspace-section">
        <div class="workspace-section-header">
          <div>
            <span class="section-kicker"> TEST </span>

            <h2>Assessments</h2>
          </div>

          <span>
            {{ assessments.length }}
          </span>
        </div>

        <div v-if="assessments.length" class="assessment-list">
          <article v-for="assessment in assessments" :key="assessment.id" class="assessment-row">
            <div>
              <span>
                {{ assessment.assessment_type }}
              </span>

              <h3>
                {{ assessment.title }}
              </h3>

              <p>
                {{ assessment.description || 'No description.' }}
              </p>
            </div>

            <strong>
              Passing:
              {{ assessment.passing_score }}%
            </strong>
          </article>
        </div>

        <div v-else class="workspace-empty">No assessments for this topic.</div>
      </section>
    </template>
  </div>
</template>

<style scoped>
.topic-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 24px 80px;
}

.topic-loading,
.topic-error {
  min-height: 400px;
  display: grid;
  place-items: center;
}

.topic-error {
  color: #c44;
}

.topic-breadcrumb {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 28px;
  font-size: 12px;
  opacity: 0.6;
}

.topic-breadcrumb a {
  color: inherit;
  text-decoration: none;
}

.topic-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: 30px;
  padding-bottom: 35px;
  border-bottom: 1px solid rgba(127, 127, 127, 0.18);
}

.topic-kicker {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.14em;
  opacity: 0.5;
}

.topic-hero h1 {
  margin: 8px 0;
  font-size: clamp(32px, 5vw, 56px);
  line-height: 1;
}

.topic-hero p {
  max-width: 750px;
  margin: 15px 0;
  font-size: 16px;
  line-height: 1.7;
  opacity: 0.65;
}

.topic-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.topic-meta-row span {
  padding: 6px 9px;
  border-radius: 20px;
  background: rgba(127, 127, 127, 0.08);
  font-size: 11px;
  text-transform: capitalize;
}

.topic-progress-card {
  align-self: start;
  border: 1px solid rgba(127, 127, 127, 0.18);
  border-radius: 16px;
  padding: 20px;
}

.topic-progress-card > span {
  display: block;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.12em;
  opacity: 0.5;
}

.topic-progress-card strong {
  display: block;
  margin: 8px 0;
  font-size: 40px;
}

.topic-progress-card small {
  display: block;
  margin-top: 12px;
  opacity: 0.55;
  text-transform: capitalize;
}

.topic-progress-track {
  height: 7px;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(127, 127, 127, 0.14);
}

.topic-progress-fill {
  height: 100%;
  background: currentColor;
}

.workspace-section {
  margin-top: 32px;
}

.workspace-section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 20px;
  margin-bottom: 18px;
}

.workspace-section-header h2 {
  margin: 5px 0 0;
}

.workspace-section-header > span {
  opacity: 0.5;
  font-size: 12px;
}

.knowledge-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.knowledge-card {
  padding: 18px;
  border: 1px solid rgba(127, 127, 127, 0.17);
  border-radius: 14px;
}

.knowledge-card > span {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.1em;
  opacity: 0.5;
  text-transform: uppercase;
}

.knowledge-card h3 {
  margin: 8px 0;
}

.knowledge-card p {
  margin: 0;
  line-height: 1.6;
  opacity: 0.65;
}

.knowledge-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 12px;
}

.knowledge-tags span {
  font-size: 10px;
  opacity: 0.5;
}

.workspace-empty {
  padding: 30px;
  text-align: center;
  border: 1px dashed rgba(127, 127, 127, 0.25);
  border-radius: 14px;
  opacity: 0.55;
}

.assessment-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.assessment-row {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 18px;
  border: 1px solid rgba(127, 127, 127, 0.17);
  border-radius: 14px;
}

.assessment-row span {
  font-size: 10px;
  text-transform: uppercase;
  font-weight: 800;
  opacity: 0.5;
}

.assessment-row h3 {
  margin: 6px 0;
}

.assessment-row p {
  margin: 0;
  opacity: 0.6;
}

.assessment-row > strong {
  white-space: nowrap;
  opacity: 0.65;
}

@media (max-width: 850px) {
  .topic-hero {
    grid-template-columns: 1fr;
  }

  .knowledge-grid {
    grid-template-columns: 1fr;
  }

  .assessment-row {
    flex-direction: column;
  }
}
</style>
