<script setup>
import { computed, onMounted, ref } from 'vue'

import { RouterLink, useRoute } from 'vue-router'

import {
  getLearningTopic,
  updateLearningProgress,
  createLearningNote,
  getLearningNotes,
  createKnowledgeItem,
  createKnowledgeApplication,
  updateKnowledgeApplication,
  submitKnowledgeApplication,
  reviewKnowledgeApplication,
  getAssessmentQuestions,
  getAssessmentChoices,
  generateLearningTopicContent,
} from '@/services/learning'

import ApplicationComposer from '@/components/learning/ApplicationComposer.vue'
import AIReviewPanel from '@/components/learning/AIReviewPanel.vue'

const route = useRoute()

// ==================================================
// STATE
// ==================================================

const loading = ref(true)
const error = ref('')

const topic = ref(null)

const activeApplication = ref(null)
const activeReference = ref(null)

const lessonCompleted = ref(false)
const quickCheckStarted = ref(false)
const quickCheckCompleted = ref(false)
const finalAssessmentCompleted = ref(false)

const personalNote = ref('')
const personalNoteId = ref(null)
const noteSaved = ref(false)

const showCompletePanel = ref(false)
const showKnowledgePreview = ref(false)

const imagePrompt = ref('')
const imagePromptCopied = ref(false)

const activeStep = ref('lesson')

const generatingContent = ref(false)
const generationError = ref('')

// Assessment
const assessmentQuestions = ref([])
const assessmentChoices = ref([])
const assessmentLoading = ref(false)
const assessmentAnswers = ref({})
const assessmentScore = ref(null)

// Application
const applicationSaving = ref(false)
const applicationSubmitting = ref(false)
const applicationReviewing = ref(false)

// Knowledge
const knowledgeSaving = ref(false)

// ==================================================
// LOAD
// ==================================================

const loadTopic = async () => {
  loading.value = true
  error.value = ''

  try {
    const topicData = await getLearningTopic(Number(route.params.topicId))

    topic.value = topicData

    activeApplication.value = topic.value?.applications?.[0] || null

    const progress = topic.value?.progress || {}

    lessonCompleted.value = Boolean(progress.lesson_completed)

    quickCheckCompleted.value = Boolean(progress.quick_check_completed)

    finalAssessmentCompleted.value = Boolean(progress.assessment_completed)

    personalNote.value = progress.notes || ''

    await loadPersonalNote()
    await loadAssessment()
  } catch (err) {
    console.error('Topic load error:', err)

    error.value =
      err?.response?.data?.detail || err?.response?.data?.message || 'Unable to load this topic.'
  } finally {
    loading.value = false
  }
}

// ==================================================
// PROGRESS
// ==================================================

const progress = computed(() => {
  return topic.value?.progress?.progress_percent ?? 0
})

const mastery = computed(() => {
  return topic.value?.progress?.mastery_level || 'not_started'
})

// ==================================================
// generate Topic Content
// ==================================================

const generateTopicContent = async () => {
  if (!topic.value?.id || generatingContent.value) {
    return
  }

  generatingContent.value = true
  generationError.value = ''
  error.value = ''

  try {
    const result = await generateLearningTopicContent(topic.value.id, {
      provider: 'ollama',
      model: '',
    })

    if (!result?.success) {
      throw new Error(result?.error || 'Unable to generate topic content.')
    }

    topic.value = result.topic

    activeApplication.value = topic.value?.applications?.[0] || null

    const progress = topic.value?.progress || {}

    lessonCompleted.value = Boolean(progress.lesson_completed)

    quickCheckCompleted.value = Boolean(progress.quick_check_completed)

    finalAssessmentCompleted.value = Boolean(progress.assessment_completed)

    personalNote.value = progress.notes || ''

    await loadPersonalNote()
    await loadAssessment()
  } catch (err) {
    console.error('Topic content generation error:', err)

    generationError.value =
      err?.response?.data?.error ||
      err?.response?.data?.detail ||
      err?.message ||
      'Unable to generate topic content.'
  } finally {
    generatingContent.value = false
  }
}

// ==================================================
// TOPIC DATA
// ==================================================

const path = computed(() => {
  return topic.value?.path || null
})

const lesson = computed(() => {
  return topic.value?.lesson || null
})

const resources = computed(() => {
  return topic.value?.resources || []
})

const notes = computed(() => {
  return topic.value?.notes || []
})

const assessments = computed(() => {
  return topic.value?.assessments || []
})

const knowledgeItem = computed(() => {
  return topic.value?.knowledge_item || null
})

const review = computed(() => {
  return activeApplication.value?.review || activeApplication.value?.latest_review || null
})

const images = computed(() => topic.value?.images ?? [])

const references = computed(() => topic.value?.references ?? [])

// ==================================================
// APPLICATION
// ==================================================

const applicationSubmitted = computed(() => {
  return Boolean(
    activeApplication.value && ['submitted', 'reviewed'].includes(activeApplication.value.status),
  )
})

const applicationReviewed = computed(() => {
  return Boolean(review.value)
})

// ==================================================
// LEARNING STEPS
// ==================================================

const learningSteps = computed(() => {
  return [
    {
      key: 'lesson',
      number: '01',
      title: 'Learn',
      label: 'Read the lesson',
      completed: lessonCompleted.value,
    },
    {
      key: 'check',
      number: '02',
      title: 'Check',
      label: 'Test your understanding',
      completed: quickCheckCompleted.value,
    },
    {
      key: 'reflect',
      number: '03',
      title: 'Reflect',
      label: 'Write what you understood',
      completed: Boolean(personalNote.value.trim()),
    },
    {
      key: 'apply',
      number: '04',
      title: 'Apply',
      label: 'Use the knowledge',
      completed: applicationSubmitted.value,
    },
    {
      key: 'review',
      number: '05',
      title: 'Review',
      label: 'Get AI feedback',
      completed: applicationReviewed.value,
    },
    {
      key: 'assess',
      number: '06',
      title: 'Assess',
      label: 'Pass the assessment',
      completed: finalAssessmentCompleted.value,
    },
  ]
})

const completedSteps = computed(() => {
  return learningSteps.value.filter((step) => step.completed).length
})

const learningCycleProgress = computed(() => {
  if (!learningSteps.value.length) {
    return 0
  }

  return Math.round((completedSteps.value / learningSteps.value.length) * 100)
})

const canCompleteTopic = computed(() => {
  return learningSteps.value.every((step) => step.completed)
})

// ==================================================
// NEXT STEP
// ==================================================

const nextStep = computed(() => {
  return learningSteps.value.find((step) => !step.completed) || null
})

const goToStep = (step) => {
  activeStep.value = step

  const element = document.getElementById(`learning-${step}`)

  if (element) {
    element.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
    })
  }
}

// ==================================================
// LESSON
// ==================================================

const markLessonCompleted = async () => {
  if (!topic.value) {
    return
  }

  try {
    const result = await updateLearningProgress({
      topic: topic.value.id,
      progress_percent: Math.max(Number(progress.value), 15),
      lesson_completed: true,
    })

    topic.value.progress = result

    lessonCompleted.value = true

    goToStep('check')
  } catch (err) {
    error.value = err?.response?.data?.detail || 'Unable to mark lesson as completed.'
  }
}

// ==================================================
// NOTES
// ==================================================

const loadPersonalNote = async () => {
  if (!topic.value?.id) {
    return
  }

  try {
    const data = await getLearningNotes({
      topic: topic.value.id,
    })

    const topicNotes = Array.isArray(data) ? data : []

    const reflection = topicNotes.find((note) => note.note_type === 'reflection') || topicNotes[0]

    if (reflection) {
      personalNote.value = reflection.content || ''

      personalNoteId.value = reflection.id
    }
  } catch (err) {
    console.warn('Unable to load learning notes:', err)
  }
}

const savePersonalNote = async () => {
  if (!topic.value || !personalNote.value.trim()) {
    return
  }

  try {
    if (personalNoteId.value) {
      // Existing note update can be added here
      // when editing an existing reflection.
    } else {
      const note = await createLearningNote({
        topic: topic.value.id,
        lesson: lesson.value?.id || null,
        note_type: 'reflection',
        title: `Reflection: ${topic.value.title}`,
        content: personalNote.value.trim(),
      })

      personalNoteId.value = note.id
    }

    const result = await updateLearningProgress({
      topic: topic.value.id,
      progress_percent: Math.max(Number(progress.value), 25),
      notes: personalNote.value.trim(),
    })

    topic.value.progress = result

    noteSaved.value = true

    setTimeout(() => {
      noteSaved.value = false
    }, 2200)

    goToStep('apply')
  } catch (err) {
    console.error('Note save error:', err)

    error.value = err?.response?.data?.detail || 'Unable to save your reflection.'
  }
}

// ==================================================
// QUICK CHECK / ASSESSMENT
// ==================================================

const loadAssessment = async () => {
  if (!topic.value?.id) {
    return
  }

  assessmentLoading.value = true

  try {
    const currentAssessments = assessments.value

    if (!currentAssessments.length) {
      return
    }

    const assessment = currentAssessments[0]

    const questions = await getAssessmentQuestions({
      assessment: assessment.id,
    })

    assessmentQuestions.value = questions

    if (questions.length) {
      const questionIds = questions.map((question) => question.id)

      const choices = await getAssessmentChoices({
        question__in: questionIds.join(','),
      })

      assessmentChoices.value = choices
    }
  } catch (err) {
    console.error('Assessment loading error:', err)
  } finally {
    assessmentLoading.value = false
  }
}

const getQuestionChoices = (questionId) => {
  return assessmentChoices.value.filter((choice) => Number(choice.question) === Number(questionId))
}

const selectAssessmentAnswer = (questionId, choiceId) => {
  assessmentAnswers.value[questionId] = choiceId
}

const finishQuickCheck = async () => {
  const assessment = assessments.value[0]

  if (!assessment) {
    return
  }

  try {
    assessmentLoading.value = true

    /*
     * The current backend submit action accepts
     * the attempt score.
     *
     * The UI calculates the score from the
     * answer choices that are exposed by the
     * serializer.
     */

    let correct = 0
    let total = 0

    assessmentQuestions.value.forEach((question) => {
      const selected = assessmentAnswers.value[question.id]

      const choices = getQuestionChoices(question.id)

      const selectedChoice = choices.find((choice) => Number(choice.id) === Number(selected))

      if (selectedChoice && selectedChoice.is_correct) {
        correct += Number(question.points || 1)
      }

      total += Number(question.points || 1)
    })

    const score = total > 0 ? Math.round((correct / total) * 100) : 0

    const result = await import('@/services/learning').then((module) =>
      module.submitAssessment(assessment.id, {
        score,
        feedback: `Assessment completed with score ${score}%.`,
      }),
    )

    assessmentScore.value = result?.score ?? score

    quickCheckCompleted.value = true

    const progressResult = await updateLearningProgress({
      topic: topic.value.id,
      progress_percent: Math.max(Number(progress.value), 40),
      quick_check_completed: true,
    })

    topic.value.progress = progressResult

    goToStep('reflect')
  } catch (err) {
    console.error('Assessment submission error:', err)

    error.value =
      err?.response?.data?.detail ||
      err?.response?.data?.message ||
      'Unable to submit the assessment.'
  } finally {
    assessmentLoading.value = false
  }
}

// ==================================================
// APPLICATION
// ==================================================

const handleApplicationUpdated = (application) => {
  activeApplication.value = application

  if (!topic.value) {
    return
  }

  const applications = topic.value.applications || []

  const index = applications.findIndex((item) => Number(item.id) === Number(application.id))

  if (index >= 0) {
    applications[index] = application
  } else {
    applications.unshift(application)
  }

  topic.value.applications = applications
}

const submitApplication = async () => {
  if (!activeApplication.value) {
    return
  }

  applicationSubmitting.value = true

  try {
    const result = await submitKnowledgeApplication(activeApplication.value.id)

    activeApplication.value = result

    handleApplicationUpdated(result)

    const progressResult = await updateLearningProgress({
      topic: topic.value.id,
      progress_percent: Math.max(Number(progress.value), 60),
      practice_completed: true,
    })

    topic.value.progress = progressResult

    goToStep('review')
  } catch (err) {
    console.error('Application submit error:', err)

    error.value =
      err?.response?.data?.detail ||
      err?.response?.data?.message ||
      'Unable to submit your application.'
  } finally {
    applicationSubmitting.value = false
  }
}

// ==================================================
// AI REVIEW
// ==================================================

const requestApplicationReview = async () => {
  if (!activeApplication.value) {
    return
  }

  applicationReviewing.value = true

  try {
    const result = await reviewKnowledgeApplication(activeApplication.value.id)

    activeApplication.value = {
      ...activeApplication.value,
      ...result,
    }

    handleApplicationUpdated(activeApplication.value)

    const progressResult = await updateLearningProgress({
      topic: topic.value.id,
      progress_percent: Math.max(Number(progress.value), 75),
    })

    topic.value.progress = progressResult

    await loadTopic()

    goToStep('assess')
  } catch (err) {
    console.error('AI review error:', err)

    error.value =
      err?.response?.data?.detail ||
      err?.response?.data?.message ||
      'Unable to review the application.'
  } finally {
    applicationReviewing.value = false
  }
}

// ==================================================
// VISUAL PROMPT
// ==================================================

const generateImagePrompt = () => {
  if (!topic.value) {
    return
  }

  imagePrompt.value = `
Create a clean educational visual explaining "${topic.value.title}".

Context:
${topic.value.description || 'Educational explanation of the topic.'}

Requirements:
- educational
- technically accurate
- visually clear
- easy to understand
- minimal visual noise
- suitable for a personal knowledge system
- highlight the main concepts and relationships
- use clear labels where useful
- avoid decorative elements that do not support learning

The visual should help a learner understand the topic rather than simply illustrate it.
  `.trim()
}

const copyImagePrompt = async () => {
  if (!imagePrompt.value) {
    return
  }

  try {
    await navigator.clipboard.writeText(imagePrompt.value)

    imagePromptCopied.value = true

    setTimeout(() => {
      imagePromptCopied.value = false
    }, 2000)
  } catch (err) {
    console.error('Unable to copy image prompt', err)
  }
}

// ==================================================
// RESOURCES
// ==================================================

const openReference = (resource) => {
  activeReference.value = resource
}

const closeReference = () => {
  activeReference.value = null
}

// ==================================================
// COMPLETE
// ==================================================

const openCompletePanel = () => {
  showCompletePanel.value = true
}

const closeCompletePanel = () => {
  showCompletePanel.value = false
}

const completeTopic = async () => {
  if (!topic.value || !canCompleteTopic.value) {
    return
  }

  try {
    const result = await updateLearningProgress({
      topic: topic.value.id,
      progress_percent: 100,
      practice_completed: true,
      lesson_completed: true,
      quick_check_completed: true,
      assessment_completed: true,
    })

    topic.value.progress = result

    showCompletePanel.value = false

    await loadTopic()
  } catch (err) {
    console.error('Complete topic error:', err)

    error.value = err?.response?.data?.detail || 'Unable to complete this topic.'
  }
}

// ==================================================
// KNOWLEDGE
// ==================================================

const openKnowledgePreview = () => {
  showKnowledgePreview.value = true
}

const closeKnowledgePreview = () => {
  showKnowledgePreview.value = false
}

const saveToKnowledge = async () => {
  if (!topic.value) {
    return
  }

  knowledgeSaving.value = true

  try {
    const content = personalNote.value || lesson.value?.content || topic.value.description || ''

    const item = await createKnowledgeItem({
      title: topic.value.title,
      description: `Knowledge captured from learning topic: ${topic.value.title}`,
      content,
      knowledge_type: 'learning',
      metadata: {
        source: 'learning',
        learning_topic: topic.value.id,
        mastery: mastery.value,
      },
      tags: ['learning', 'captured'],
      visibility: 'private',
    })

    showKnowledgePreview.value = false

    return item
  } catch (err) {
    console.error('Knowledge save error:', err)

    error.value = err?.response?.data?.detail || 'Unable to save this knowledge.'
  } finally {
    knowledgeSaving.value = false
  }
}

// ==================================================
// MOUNT
// ==================================================

onMounted(loadTopic)
</script>

<template>
  <div class="topic-page">
    <!-- ============================================
    LOADING
    ============================================= -->

    <div v-if="loading" class="topic-loading">
      <div class="loader"></div>

      <p>Preparing your learning space...</p>
    </div>

    <!-- ============================================
    ERROR
    ============================================= -->

    <div v-else-if="error" class="topic-error">
      <div class="error-card">
        <span class="section-kicker"> LEARNING </span>

        <h2>Something went wrong</h2>

        <p>
          {{ error }}
        </p>

        <button type="button" class="primary-button" @click="loadTopic">Try again</button>
      </div>
    </div>

    <!-- ============================================
    TOPIC
    ============================================= -->

    <template v-else-if="topic">
      <!-- ==========================================
      BREADCRUMB
      =========================================== -->

      <nav class="topic-breadcrumb">
        <RouterLink to="/learning"> Learning </RouterLink>

        <span>/</span>

        <span>
          <span>
            {{ topic.path?.title || 'Learning path' }}
          </span>
        </span>

        <span>/</span>

        <strong>
          {{ topic.title }}
        </strong>
      </nav>

      <!-- ==========================================
      HERO
      =========================================== -->

      <header class="topic-hero">
        <div class="hero-main">
          <div class="topic-kicker">TOPIC {{ topic.order }}</div>

          <h1>
            {{ topic.title }}
          </h1>

          <p class="hero-description">
            {{
              topic.description ||
              'Learn the concept, practice it, test your understanding, and turn it into knowledge.'
            }}
          </p>

          <div class="hero-meta">
            <span>
              {{ topic.status }}
            </span>

            <span v-if="topic.estimated_minutes"> {{ topic.estimated_minutes }} min </span>

            <span v-if="topic.skill"> Skill #{{ topic.skill }} </span>
          </div>
        </div>

        <!-- HERO PROGRESS -->

        <div class="hero-progress">
          <div class="progress-top">
            <span> LEARNING CYCLE </span>

            <strong> {{ learningCycleProgress }}% </strong>
          </div>

          <div class="progress-track">
            <div
              class="progress-fill"
              :style="{
                width: `${learningCycleProgress}%`,
              }"
            />
          </div>

          <div class="progress-bottom">
            <span>
              {{ completedSteps }}/{{ learningSteps.length }}
              steps
            </span>

            <span>
              {{ mastery }}
            </span>
          </div>
        </div>
      </header>

      <!-- ==========================================
      MAIN WORKSPACE
      =========================================== -->

      <section class="learning-layout">
        <!-- ========================================
        MAIN
        ========================================= -->

        <main class="learning-main">
          <div class="hero-ai-status">
            <span class="ai-status-dot" :class="`status-${topic.ai?.status || 'empty'}`" />
            <div v-if="!topic.ai?.content_available" class="hero-actions">
              <button
                type="button"
                class="primary-button"
                :disabled="generatingContent"
                @click="generateTopicContent"
              >
                {{ generatingContent ? 'Generating...' : 'Generate learning content' }}
              </button>
            </div>
            <span v-if="topic.ai?.content_available"> AI content ready </span>

            <span v-else> Content not generated </span>
          </div>
          <section id="learning-lesson" class="workspace-section lesson-section">
            <div class="section-heading">
              <div>
                <span class="section-kicker"> 01 · LEARN </span>

                <h2>
                  {{ lesson?.title || 'Lesson' }}
                </h2>
              </div>

              <span v-if="lesson?.estimated_minutes"> {{ lesson.estimated_minutes }} min </span>
            </div>

            <!-- No content -->
            <div v-if="!lesson" class="content-placeholder">
              <span class="placeholder-number"> L </span>

              <div>
                <h3>Your lesson is not ready yet</h3>

                <p>
                  Generate the learning content for this topic to create the lesson, visuals,
                  references, and supporting material.
                </p>

                <div v-if="generationError" class="error-message">
                  {{ generationError }}
                </div>

                <button
                  type="button"
                  class="primary-button"
                  :disabled="generatingContent"
                  @click="generateTopicContent"
                >
                  {{ generatingContent ? 'Generating content...' : 'Generate learning content' }}
                </button>
              </div>
            </div>

            <!-- Lesson exists -->
            <template v-else>
              <div v-if="lesson.content" class="lesson-body" v-html="lesson.content" />

              <div v-else class="content-placeholder">
                <h3>This lesson has no content yet</h3>

                <p>The lesson record exists, but no content was returned by the API.</p>
              </div>

              <!-- Images -->
              <div v-if="images.length" class="lesson-visuals">
                <div class="subsection-heading">
                  <span class="section-kicker"> VISUALS </span>

                  <h3>See the concept</h3>
                </div>

                <div class="visual-grid">
                  <article v-for="image in images" :key="image.id" class="visual-card">
                    <img :src="image.image" :alt="image.title || topic.title" />

                    <div>
                      <h4 v-if="image.title">
                        {{ image.title }}
                      </h4>

                      <p v-if="image.caption">
                        {{ image.caption }}
                      </p>
                    </div>
                  </article>
                </div>
              </div>

              <!-- Resources -->
              <div v-if="resources.length" class="lesson-resources">
                <div class="subsection-heading">
                  <span class="section-kicker"> RESOURCES </span>

                  <h3>Study resources</h3>
                </div>

                <div class="reference-list">
                  <button
                    v-for="resource in resources"
                    :key="resource.id"
                    type="button"
                    class="reference-row"
                    @click="openReference(resource)"
                  >
                    <div class="reference-icon">
                      {{
                        resource.reference_type === 'file'
                          ? 'F'
                          : resource.reference_type === 'url'
                            ? 'W'
                            : resource.reference_type === 'content'
                              ? 'N'
                              : 'R'
                      }}
                    </div>

                    <div class="reference-content">
                      <span>
                        {{ resource.reference_type }}
                      </span>

                      <h3>
                        {{ resource.title }}
                      </h3>

                      <p>
                        {{
                          resource.description ||
                          resource.caption ||
                          'Learning resource connected to this topic.'
                        }}
                      </p>
                    </div>

                    <span class="reference-arrow"> → </span>
                  </button>
                </div>
              </div>

              <!-- References -->
              <div v-if="references.length" class="lesson-references">
                <div class="subsection-heading">
                  <span class="section-kicker"> REFERENCES </span>

                  <h3>Explore further</h3>
                </div>

                <div class="reference-list">
                  <button
                    v-for="reference in references"
                    :key="reference.id"
                    type="button"
                    class="reference-row"
                    @click="openReference(reference)"
                  >
                    <div class="reference-icon">
                      {{
                        reference.reference_type === 'file'
                          ? 'F'
                          : reference.reference_type === 'note'
                            ? 'N'
                            : 'W'
                      }}
                    </div>

                    <div class="reference-content">
                      <span>
                        {{ reference.reference_type }}
                      </span>

                      <h3>
                        {{ reference.title }}
                      </h3>

                      <p>
                        {{ reference.description || 'Reference material connected to this topic.' }}
                      </p>
                    </div>

                    <span class="reference-arrow"> → </span>
                  </button>
                </div>
              </div>

              <!-- Complete lesson -->
              <div class="lesson-footer">
                <div>
                  <strong> Finished studying? </strong>

                  <p>Mark the lesson as completed to continue to the knowledge check.</p>
                </div>

                <button
                  type="button"
                  class="primary-button"
                  :disabled="lessonCompleted"
                  @click="markLessonCompleted"
                >
                  {{ lessonCompleted ? 'Lesson completed ✓' : 'Mark lesson completed' }}
                </button>
              </div>
            </template>
          </section>

          <!-- ======================================
          NEXT ACTION
          ======================================= -->

          <section v-if="nextStep" class="next-action">
            <div>
              <span class="section-kicker"> NEXT STEP </span>

              <h2>
                {{ nextStep.title }}
              </h2>

              <p>
                {{ nextStep.label }}
              </p>
            </div>

            <button type="button" class="primary-button" @click="goToStep(nextStep.key)">
              Continue
              <span>→</span>
            </button>
          </section>

          <!-- ======================================
          LESSON
          ======================================= -->

          <section class="workspace-section">
            <div class="section-heading">
              <div>
                <span class="section-kicker"> RESOURCES </span>
                <h2>Study resources</h2>
              </div>

              <span> {{ resources.length }} resources </span>
            </div>

            <div v-if="resources.length" class="reference-list">
              <button
                v-for="resource in resources"
                :key="resource.id"
                type="button"
                class="reference-row"
                @click="openReference(resource)"
              >
                <div class="reference-icon">
                  {{
                    resource.reference_type === 'file'
                      ? 'F'
                      : resource.reference_type === 'url'
                        ? 'W'
                        : resource.reference_type === 'content'
                          ? 'N'
                          : 'R'
                  }}
                </div>

                <div class="reference-content">
                  <span>
                    {{ resource.reference_type }}
                  </span>

                  <h3>
                    {{ resource.title }}
                  </h3>

                  <p>
                    {{
                      resource.description ||
                      resource.caption ||
                      'Learning resource connected to this topic.'
                    }}
                  </p>
                </div>

                <span class="reference-arrow"> → </span>
              </button>
            </div>

            <div v-else class="visual-empty">
              <div class="empty-symbol">◇</div>

              <div class="empty-copy">
                <strong> No resources yet </strong>

                <p>
                  Websites, files, notes and learning material connected to this topic will appear
                  here.
                </p>
              </div>
            </div>
          </section>
          <!-- ======================================
          VISUALS
          ======================================= -->

          <section class="workspace-section">
            <div class="section-heading">
              <div>
                <span class="section-kicker"> VISUALS </span>

                <h2>See the concept</h2>
              </div>

              <span> {{ images.length }} visuals </span>
            </div>

            <div v-if="images.length" class="visual-grid">
              <article v-for="image in images" :key="image.id" class="visual-card">
                <img :src="image.image" :alt="image.title || topic.title" />

                <div>
                  <h3>
                    {{ image.title }}
                  </h3>

                  <p v-if="image.caption">
                    {{ image.caption }}
                  </p>
                </div>
              </article>
            </div>
            <div v-else class="visual-empty">
              <div class="empty-symbol">◇</div>

              <div class="empty-copy">
                <strong> No visual yet </strong>

                <p>
                  Add a diagram, screenshot, or generated visual to make this topic easier to
                  understand.
                </p>
              </div>

              <button type="button" class="secondary-button" @click="generateImagePrompt">
                Create visual prompt
              </button>
            </div>

            <!-- IMAGE PROMPT -->

            <div v-if="imagePrompt" class="prompt-panel">
              <div class="prompt-header">
                <div>
                  <span class="section-kicker"> AI VISUAL </span>

                  <h3>Prompt for image generation</h3>
                </div>

                <button type="button" class="icon-button" @click="imagePrompt = ''">×</button>
              </div>

              <textarea v-model="imagePrompt" rows="8" />

              <div class="prompt-actions">
                <button type="button" class="secondary-button" @click="generateImagePrompt">
                  Regenerate
                </button>

                <button type="button" class="primary-button" @click="copyImagePrompt">
                  {{ imagePromptCopied ? 'Copied' : 'Copy prompt' }}
                </button>
              </div>

              <small>
                Generate the visual externally and then attach it to this topic as a reference.
              </small>
            </div>
          </section>

          <!-- ======================================
          REFERENCES
          ======================================= -->

          <section class="workspace-section">
            <div class="section-heading">
              <div>
                <span class="section-kicker"> REFERENCES </span>

                <h2>Explore further</h2>
              </div>

              <span> {{ references.length }} sources </span>
            </div>

            <div v-if="references.length" class="reference-list">
              <button
                v-for="reference in references"
                :key="reference.id"
                type="button"
                class="reference-row"
                @click="openReference(reference)"
              >
                <div class="reference-icon">
                  {{
                    reference.reference_type === 'file'
                      ? 'F'
                      : reference.reference_type === 'note'
                        ? 'N'
                        : 'W'
                  }}
                </div>

                <div class="reference-content">
                  <span>
                    {{ reference.reference_type }}
                  </span>

                  <h3>
                    {{ reference.title }}
                  </h3>

                  <p>
                    {{ reference.description || 'Reference material connected to this topic.' }}
                  </p>
                </div>

                <span class="reference-arrow"> → </span>
              </button>
            </div>

            <div v-else class="content-placeholder">
              <span class="placeholder-number"> R </span>

              <div>
                <h3>Build your source library</h3>

                <p>
                  Websites, uploaded files, notes, documentation, and personal references can all
                  live here.
                </p>
              </div>
            </div>
          </section>

          <!-- ======================================
          QUICK CHECK
          ======================================= -->

          <section id="learning-check" class="workspace-section check-section">
            <div class="section-heading">
              <div>
                <span class="section-kicker"> 02 · CHECK </span>

                <h2>Do you really understand it?</h2>
              </div>

              <span v-if="quickCheckCompleted" class="done-badge"> ✓ Completed </span>
            </div>

            <div v-if="!quickCheckStarted" class="action-card">
              <div class="action-card-icon">?</div>

              <div class="action-card-copy">
                <h3>Quick knowledge check</h3>

                <p>Answer a few short questions before moving to practical application.</p>
              </div>

              <button type="button" class="primary-button" @click="startQuickCheck">
                Start check
              </button>
            </div>

            <div v-else-if="!quickCheckCompleted" class="quiz-placeholder">
              <span class="section-kicker"> KNOWLEDGE CHECK </span>

              <h3>Interactive questions will appear here</h3>

              <p>This area is ready for the backend assessment engine.</p>

              <button type="button" class="primary-button" @click="finishQuickCheck">
                Complete demo check
              </button>
            </div>

            <div v-else class="success-card">
              ✓
              <div>
                <strong> Knowledge check completed </strong>

                <p>You can now move to reflection.</p>
              </div>
            </div>
          </section>

          <!-- ======================================
          NOTES
          ======================================= -->

          <section id="learning-reflect" class="workspace-section">
            <div class="section-heading">
              <div>
                <span class="section-kicker"> 03 · REFLECT </span>

                <h2>What did you understand?</h2>
              </div>
            </div>

            <textarea
              v-model="personalNote"
              class="personal-note"
              placeholder="Explain the idea in your own words. What became clear? What is still confusing?"
              rows="8"
            />

            <div class="notes-footer">
              <span> Your own explanation becomes part of your personal knowledge. </span>

              <button
                type="button"
                class="primary-button"
                :disabled="!personalNote.trim()"
                @click="savePersonalNote"
              >
                {{ noteSaved ? 'Saved ✓' : 'Save reflection' }}
              </button>
            </div>
          </section>

          <!-- ======================================
          KNOWLEDGE
          ======================================= -->
          <section class="workspace-section">
            <div class="section-heading">
              <div>
                <span class="section-kicker"> KNOWLEDGE </span>

                <h2>Connected knowledge</h2>
              </div>

              <span>
                {{ knowledgeItem ? '1 item' : 'None' }}
              </span>
            </div>

            <div v-if="knowledgeItem" class="knowledge-grid">
              <article class="knowledge-card">
                <span>
                  {{ knowledgeItem.knowledge_type }}
                </span>

                <h3>
                  {{ knowledgeItem.title }}
                </h3>

                <p>
                  {{ knowledgeItem.description || knowledgeItem.content || 'Knowledge item' }}
                </p>
              </article>
            </div>

            <div v-else class="content-placeholder">
              <span class="placeholder-number"> K </span>

              <div>
                <h3>No knowledge connected yet</h3>

                <p>Knowledge items connected to this topic will appear here.</p>
              </div>
            </div>
          </section>
          <!-- ======================================
          APPLICATION
          ======================================= -->

          <section id="learning-apply" class="workspace-section application-section">
            <div class="section-heading">
              <div>
                <span class="section-kicker"> 04 · APPLY </span>

                <h2>Show that you can use it</h2>
              </div>

              <span v-if="applicationSubmitted" class="done-badge"> ✓ Submitted </span>
            </div>

            <p class="section-description">
              Reading gives you information. Applying it turns that information into usable
              knowledge.
            </p>

            <ApplicationComposer
              :topic-id="topic.id"
              :application="activeApplication"
              @updated="handleApplicationUpdated"
            />
          </section>

          <!-- ======================================
          AI REVIEW
          ======================================= -->

          <section v-if="review" id="learning-review" class="workspace-section">
            <div class="section-heading">
              <div>
                <span class="section-kicker"> 05 · REVIEW </span>

                <h2>Understand your gaps</h2>
              </div>

              <span class="done-badge"> AI reviewed </span>
            </div>

            <AIReviewPanel :review="review" />
          </section>

          <!-- ======================================
          FINAL ASSESSMENT
          ======================================= -->

          <section id="learning-assess" class="workspace-section assessment-section">
            <div class="section-heading">
              <div>
                <span class="section-kicker"> 06 · ASSESS </span>

                <h2>Test your mastery</h2>
              </div>

              <span v-if="finalAssessmentCompleted" class="done-badge"> ✓ Passed </span>
            </div>

            <div v-if="assessments.length" class="assessment-list">
              <article
                v-for="assessment in assessments"
                :key="assessment.id"
                class="assessment-row"
              >
                <div>
                  <span>
                    {{ assessment.assessment_type }}
                  </span>

                  <h3>
                    {{ assessment.title }}
                  </h3>

                  <p>
                    {{ assessment.description || 'Test your understanding of this topic.' }}
                  </p>
                </div>

                <div class="assessment-side">
                  <strong> {{ assessment.passing_score }}% </strong>

                  <small> passing </small>

                  <button type="button" class="secondary-button">Start</button>
                </div>
              </article>
            </div>

            <div v-else class="action-card">
              <div class="action-card-icon">✓</div>

              <div class="action-card-copy">
                <h3>Final assessment</h3>

                <p>No assessment has been created for this topic yet.</p>
              </div>
            </div>
          </section>
        </main>

        <!-- ========================================
        SIDEBAR
        ========================================= -->

        <aside class="topic-sidebar">
          <!-- ======================================
          PROGRESS
          ======================================= -->

          <div class="sidebar-card">
            <div class="sidebar-label">YOUR PROGRESS</div>

            <div class="sidebar-progress-number">{{ learningCycleProgress }}%</div>

            <div class="progress-track">
              <div
                class="progress-fill"
                :style="{
                  width: `${learningCycleProgress}%`,
                }"
              />
            </div>

            <div class="sidebar-meta">
              <span>
                {{ completedSteps }} of
                {{ learningSteps.length }}
              </span>

              <strong>
                {{ mastery }}
              </strong>
            </div>
          </div>

          <!-- ===============================================
               LEARNING PATH
          ================================================ -->

          <div class="sidebar-card">
            <div class="sidebar-card-title">Learning path</div>

            <div class="step-list">
              <button
                v-for="step in learningSteps"
                :key="step.key"
                type="button"
                class="step-item"
                :class="{
                  completed: step.completed,
                  active: activeStep === step.key,
                }"
                @click="goToStep(step.key)"
              >
                <span class="step-number">
                  {{ step.completed ? '✓' : step.number }}
                </span>

                <span class="step-copy">
                  <strong>
                    {{ step.title }}
                  </strong>

                  <small>
                    {{ step.label }}
                  </small>
                </span>
              </button>
            </div>
          </div>

          <!-- ===============================================
               AI
          ================================================ -->

          <div class="sidebar-card ai-card">
            <span class="section-kicker"> AI ASSISTANT </span>

            <h3>Stuck on something?</h3>

            <p>Ask questions about this lesson without leaving the learning workspace.</p>

            <button type="button" class="secondary-button full-width">Ask about this topic</button>
          </div>

          <!-- ===============================================
               COMPLETE
          ================================================ -->

          <div class="sidebar-card finish-card">
            <span class="section-kicker"> FINISH </span>

            <h3>Complete topic</h3>

            <p v-if="canCompleteTopic">
              Your learning cycle is complete. Capture the result as knowledge.
            </p>

            <p v-else>Finish the remaining learning steps before completing this topic.</p>

            <button
              type="button"
              class="primary-button full-width"
              :disabled="!canCompleteTopic"
              @click="openCompletePanel"
            >
              {{ canCompleteTopic ? 'Complete topic' : 'Finish learning first' }}
            </button>
          </div>
        </aside>
      </section>
    </template>

    <!-- ============================================
    REFERENCE MODAL
    ============================================= -->

    <div v-if="activeReference" class="modal-backdrop" @click.self="closeReference">
      <div class="modal-card">
        <button type="button" class="modal-close" @click="closeReference">×</button>

        <span class="section-kicker"> REFERENCE </span>

        <h2>
          {{ activeReference.title }}
        </h2>

        <p>
          {{ activeReference.description }}
        </p>

        <a
          v-if="activeReference.url"
          :href="activeReference.url"
          target="_blank"
          rel="noopener noreferrer"
          class="primary-button modal-link"
        >
          Open website →
        </a>

        <a
          v-else-if="activeReference.file"
          :href="activeReference.file"
          target="_blank"
          rel="noopener noreferrer"
          class="primary-button modal-link"
        >
          Open file →
        </a>

        <div v-else-if="activeReference.content" class="reference-text">
          {{ activeReference.content }}
        </div>
      </div>
    </div>

    <!-- ============================================
    COMPLETE MODAL
    ============================================= -->

    <div v-if="showCompletePanel" class="modal-backdrop" @click.self="closeCompletePanel">
      <div class="modal-card completion-modal">
        <button type="button" class="modal-close" @click="closeCompletePanel">×</button>

        <div class="completion-symbol">✓</div>

        <span class="section-kicker"> LEARNING COMPLETE </span>

        <h2>You completed the learning cycle</h2>

        <p>The next step is to preserve what you learned inside your personal knowledge system.</p>

        <div class="completion-list">
          <div v-for="step in learningSteps" :key="step.key">
            <span>
              {{ step.completed ? '✓' : '○' }}
            </span>

            {{ step.label }}
          </div>
        </div>

        <div class="modal-actions">
          <button type="button" class="secondary-button" @click="closeCompletePanel">
            Continue
          </button>

          <button type="button" class="primary-button" @click="completeTopic">
            Confirm completion
          </button>
        </div>
      </div>
    </div>

    <!-- ============================================
    KNOWLEDGE MODAL
    ============================================= -->

    <div v-if="showKnowledgePreview" class="modal-backdrop" @click.self="closeKnowledgePreview">
      <div class="modal-card knowledge-modal">
        <button type="button" class="modal-close" @click="closeKnowledgePreview">×</button>

        <span class="section-kicker"> KNOWLEDGE </span>

        <h2>Capture what you learned</h2>

        <p>This is where the learning result becomes permanent knowledge.</p>

        <div class="knowledge-preview">
          <label> Title </label>

          <input :value="topic.title" readonly />

          <label> Source </label>

          <input value="Learning Topic" readonly />

          <label> Mastery </label>

          <input :value="mastery" readonly />

          <label> Knowledge </label>

          <textarea
            :value="personalNote || lesson?.content || topic.description || ''"
            rows="8"
            readonly
          />
        </div>

        <div class="modal-actions">
          <button type="button" class="secondary-button" @click="closeKnowledgePreview">
            Cancel
          </button>

          <button
            type="button"
            class="primary-button"
            :disabled="knowledgeSaving"
            @click="saveToKnowledge"
          >
            {{ knowledgeSaving ? 'Saving...' : 'Save to Knowledge' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.topic-page {
  width: 100%;
  max-width: 1320px;
  margin: 0 auto;
  padding: 28px 28px 100px;
}

/* =========================================================
   LOADING / ERROR
========================================================= */

.topic-loading,
.topic-error {
  min-height: 500px;
  display: grid;
  place-items: center;
}

.topic-loading {
  color: inherit;
  opacity: 0.6;
}

.loader {
  width: 28px;
  height: 28px;
  border: 2px solid rgba(127, 127, 127, 0.2);
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 14px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-card {
  width: min(500px, 100%);
  padding: 30px;
  border: 1px solid rgba(127, 127, 127, 0.18);
  border-radius: 20px;
}

/* =========================================================
   BREADCRUMB
========================================================= */

.topic-breadcrumb {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-bottom: 30px;
  font-size: 12px;
  opacity: 0.55;
}

.topic-breadcrumb a {
  color: inherit;
  text-decoration: none;
}

.topic-breadcrumb strong {
  opacity: 1;
}

/* =========================================================
   HERO
========================================================= */

.topic-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 310px;
  gap: 50px;
  padding-bottom: 42px;
  border-bottom: 1px solid rgba(127, 127, 127, 0.16);
}

.topic-kicker,
.section-kicker {
  display: block;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  opacity: 0.5;
}

.hero-main h1 {
  max-width: 900px;
  margin: 9px 0 16px;
  font-size: clamp(38px, 6vw, 68px);
  line-height: 0.98;
  letter-spacing: -0.045em;
}

.hero-description {
  max-width: 760px;
  margin: 0;
  font-size: 16px;
  line-height: 1.8;
  opacity: 0.62;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 22px;
}

.hero-meta span {
  padding: 7px 11px;
  border-radius: 999px;
  background: rgba(127, 127, 127, 0.08);
  font-size: 11px;
  text-transform: capitalize;
}

.hero-progress {
  align-self: start;
  padding: 22px;
  border: 1px solid rgba(127, 127, 127, 0.18);
  border-radius: 20px;
}

.progress-top,
.progress-bottom,
.sidebar-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.progress-top span {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.1em;
  opacity: 0.5;
}

.progress-top strong {
  font-size: 32px;
}

.progress-track {
  height: 7px;
  margin-top: 16px;
  overflow: hidden;
  border-radius: 99px;
  background: rgba(127, 127, 127, 0.12);
}

.progress-fill {
  height: 100%;
  background: currentColor;
  border-radius: inherit;
  transition: width 0.4s ease;
}

.progress-bottom {
  margin-top: 13px;
  font-size: 11px;
  opacity: 0.55;
}

/* =========================================================
   LAYOUT
========================================================= */

.learning-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 290px;
  gap: 34px;
  margin-top: 34px;
}

.learning-main {
  min-width: 0;
}

.topic-sidebar {
  align-self: start;
  position: sticky;
  top: 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* =========================================================
   NEXT ACTION
========================================================= */

.next-action {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  margin-bottom: 28px;
  padding: 22px;
  border: 1px solid rgba(127, 127, 127, 0.18);
  border-radius: 20px;
}

.next-action h2 {
  margin: 5px 0 3px;
}

.next-action p {
  margin: 0;
  opacity: 0.55;
}

/* =========================================================
   SECTIONS
========================================================= */

.workspace-section {
  scroll-margin-top: 30px;
  margin-bottom: 34px;
  padding: 28px;
  border: 1px solid rgba(127, 127, 127, 0.15);
  border-radius: 22px;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 20px;
  margin-bottom: 22px;
}

.section-heading h2 {
  margin: 6px 0 0;
  font-size: 25px;
  letter-spacing: -0.025em;
}

.section-heading > span {
  font-size: 11px;
  opacity: 0.5;
}

/* =========================================================
   LESSON
========================================================= */

.lesson-content {
  white-space: pre-wrap;
  font-size: 16px;
  line-height: 1.9;
  opacity: 0.82;
}

.content-placeholder {
  display: flex;
  align-items: flex-start;
  gap: 18px;
  padding: 25px;
  border-radius: 16px;
  background: rgba(127, 127, 127, 0.05);
}

.placeholder-number {
  flex: 0 0 auto;
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(127, 127, 127, 0.2);
  border-radius: 50%;
  font-size: 11px;
  font-weight: 800;
}

.content-placeholder h3 {
  margin: 2px 0 6px;
}

.content-placeholder p {
  margin: 0;
  line-height: 1.65;
  opacity: 0.58;
}

.section-footer,
.notes-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 18px;
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid rgba(127, 127, 127, 0.12);
}

.section-footer > span,
.notes-footer > span {
  max-width: 520px;
  font-size: 11px;
  line-height: 1.5;
  opacity: 0.5;
}

.done-badge {
  color: inherit;
  font-size: 11px !important;
  font-weight: 700;
}

.completed-state {
  font-size: 12px;
  font-weight: 700;
  opacity: 0.7;
}

/* =========================================================
   VISUALS
========================================================= */

.visual-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.visual-card {
  overflow: hidden;
  border: 1px solid rgba(127, 127, 127, 0.15);
  border-radius: 16px;
}

.visual-card img {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 10;
  object-fit: cover;
}

.visual-card > div {
  padding: 15px;
}

.visual-card h3 {
  margin: 0 0 5px;
}

.visual-card p {
  margin: 0;
  line-height: 1.55;
  font-size: 12px;
  opacity: 0.55;
}

.visual-empty {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 25px;
  border: 1px dashed rgba(127, 127, 127, 0.25);
  border-radius: 16px;
}

.empty-symbol {
  width: 42px;
  height: 42px;
  flex: 0 0 auto;
  display: grid;
  place-items: center;
  border: 1px solid rgba(127, 127, 127, 0.18);
  border-radius: 50%;
  font-size: 20px;
}

.empty-copy {
  flex: 1;
}

.empty-copy strong {
  display: block;
}

.empty-copy p {
  margin: 5px 0 0;
  font-size: 12px;
  line-height: 1.55;
  opacity: 0.55;
}

/* =========================================================
   PROMPT
========================================================= */

.prompt-panel {
  margin-top: 16px;
  padding: 20px;
  border-radius: 16px;
  background: rgba(127, 127, 127, 0.05);
}

.prompt-header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 15px;
}

.prompt-header h3 {
  margin: 5px 0 0;
}

.prompt-panel textarea,
.personal-note,
.knowledge-preview textarea,
.knowledge-preview input {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid rgba(127, 127, 127, 0.2);
  border-radius: 12px;
  background: transparent;
  color: inherit;
  padding: 14px;
  outline: none;
  resize: vertical;
  font: inherit;
  line-height: 1.6;
}

.prompt-actions {
  display: flex;
  justify-content: flex-end;
  gap: 9px;
  margin-top: 12px;
}

.prompt-panel small {
  display: block;
  margin-top: 12px;
  opacity: 0.45;
}

/* =========================================================
   REFERENCES
========================================================= */

.reference-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.reference-row {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 15px;
  text-align: left;
  padding: 16px;
  border: 1px solid rgba(127, 127, 127, 0.14);
  border-radius: 14px;
  background: transparent;
  color: inherit;
  cursor: pointer;
  transition:
    transform 0.15s ease,
    background 0.15s ease;
}

.reference-row:hover {
  transform: translateY(-1px);
  background: rgba(127, 127, 127, 0.04);
}

.reference-icon {
  width: 36px;
  height: 36px;
  flex: 0 0 auto;
  display: grid;
  place-items: center;
  border: 1px solid rgba(127, 127, 127, 0.18);
  border-radius: 10px;
  font-size: 10px;
  font-weight: 800;
}

.reference-content {
  min-width: 0;
  flex: 1;
}

.reference-content > span {
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  opacity: 0.45;
}

.reference-content h3 {
  margin: 4px 0;
}

.reference-content p {
  margin: 0;
  font-size: 12px;
  opacity: 0.55;
}

.reference-arrow {
  opacity: 0.45;
}

/* =========================================================
   CHECK / ACTION CARDS
========================================================= */

.action-card {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 24px;
  border-radius: 16px;
  background: rgba(127, 127, 127, 0.05);
}

.action-card-icon {
  width: 42px;
  height: 42px;
  flex: 0 0 auto;
  display: grid;
  place-items: center;
  border: 1px solid rgba(127, 127, 127, 0.2);
  border-radius: 50%;
  font-weight: 800;
}

.action-card-copy {
  flex: 1;
}

.action-card-copy h3 {
  margin: 0 0 5px;
}

.action-card-copy p {
  margin: 0;
  font-size: 12px;
  opacity: 0.55;
}

.quiz-placeholder {
  padding: 28px;
  border-radius: 16px;
  background: rgba(127, 127, 127, 0.05);
}

.quiz-placeholder h3 {
  margin: 8px 0;
}

.quiz-placeholder p {
  margin: 0 0 18px;
  opacity: 0.55;
}

.success-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px;
  border: 1px solid rgba(127, 127, 127, 0.15);
  border-radius: 14px;
}

.success-card > div {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.success-card p {
  margin: 0;
  font-size: 12px;
  opacity: 0.5;
}

/* =========================================================
   NOTES
========================================================= */

.personal-note {
  min-height: 170px;
}

.notes-footer {
  border-top: 0;
  padding-top: 10px;
}

/* =========================================================
   KNOWLEDGE
========================================================= */

.knowledge-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.knowledge-card {
  padding: 18px;
  border: 1px solid rgba(127, 127, 127, 0.15);
  border-radius: 14px;
}

.knowledge-card > span {
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  opacity: 0.45;
}

.knowledge-card h3 {
  margin: 7px 0;
}

.knowledge-card p {
  margin: 0;
  font-size: 12px;
  line-height: 1.6;
  opacity: 0.55;
}

/* =========================================================
   APPLICATION
========================================================= */

.section-description {
  margin: -8px 0 22px;
  max-width: 650px;
  font-size: 13px;
  line-height: 1.7;
  opacity: 0.55;
}

/* =========================================================
   ASSESSMENT
========================================================= */

.assessment-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.assessment-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 18px;
  border: 1px solid rgba(127, 127, 127, 0.14);
  border-radius: 14px;
}

.assessment-row > div:first-child {
  min-width: 0;
}

.assessment-row span {
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  opacity: 0.45;
}

.assessment-row h3 {
  margin: 5px 0;
}

.assessment-row p {
  margin: 0;
  font-size: 12px;
  opacity: 0.55;
}

.assessment-side {
  display: flex;
  align-items: center;
  gap: 8px;
}

.assessment-side strong {
  font-size: 20px;
}

.assessment-side small {
  opacity: 0.45;
}

/* =========================================================
   SIDEBAR
========================================================= */

.sidebar-card {
  padding: 20px;
  border: 1px solid rgba(127, 127, 127, 0.15);
  border-radius: 18px;
}

.sidebar-label,
.sidebar-card-title {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  opacity: 0.5;
}

.sidebar-progress-number {
  margin: 8px 0;
  font-size: 38px;
  font-weight: 700;
}

.sidebar-meta {
  margin-top: 10px;
  font-size: 10px;
  opacity: 0.55;
}

.sidebar-meta strong {
  text-transform: capitalize;
}

/* =========================================================
   STEPS
========================================================= */

.step-list {
  display: flex;
  flex-direction: column;
  gap: 3px;
  margin-top: 13px;
}

.step-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 7px;
  border: 0;
  border-radius: 10px;
  background: transparent;
  color: inherit;
  text-align: left;
  cursor: pointer;
}

.step-item:hover,
.step-item.active {
  background: rgba(127, 127, 127, 0.06);
}

.step-number {
  width: 25px;
  height: 25px;
  flex: 0 0 auto;
  display: grid;
  place-items: center;
  border: 1px solid rgba(127, 127, 127, 0.18);
  border-radius: 50%;
  font-size: 9px;
}

.step-item.completed .step-number {
  font-weight: 800;
}

.step-copy {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.step-copy strong {
  font-size: 11px;
}

.step-copy small {
  font-size: 9px;
  opacity: 0.45;
}

/* =========================================================
   AI / FINISH
========================================================= */

.ai-card h3,
.finish-card h3 {
  margin: 7px 0;
}

.ai-card p,
.finish-card p {
  font-size: 12px;
  line-height: 1.6;
  opacity: 0.55;
}

.finish-card {
  position: relative;
}

/* =========================================================
   BUTTONS
========================================================= */

.primary-button,
.secondary-button {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  min-height: 38px;
  padding: 9px 14px;
  border-radius: 10px;
  font: inherit;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  transition:
    transform 0.15s ease,
    opacity 0.15s ease;
}

.primary-button {
  border: 1px solid currentColor;
  background: currentColor;
  color: Canvas;
}

.secondary-button {
  border: 1px solid rgba(127, 127, 127, 0.22);
  background: transparent;
  color: inherit;
}

.primary-button:hover,
.secondary-button:hover {
  transform: translateY(-1px);
}

.primary-button:disabled {
  cursor: not-allowed;
  opacity: 0.35;
  transform: none;
}

.full-width {
  width: 100%;
}

.icon-button,
.modal-close {
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(127, 127, 127, 0.18);
  border-radius: 50%;
  background: transparent;
  color: inherit;
  cursor: pointer;
  font-size: 18px;
}

/* =========================================================
   MODALS
========================================================= */

.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: grid;
  place-items: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
}

.modal-card {
  position: relative;
  width: min(600px, 100%);
  max-height: calc(100vh - 40px);
  overflow-y: auto;
  padding: 30px;
  border: 1px solid rgba(127, 127, 127, 0.2);
  border-radius: 22px;
  background: Canvas;
  color: CanvasText;
}

.modal-close {
  position: absolute;
  top: 18px;
  right: 18px;
}

.modal-card h2 {
  margin: 8px 0;
  font-size: 30px;
}

.modal-card > p {
  line-height: 1.7;
  opacity: 0.6;
}

.modal-link {
  margin-top: 15px;
  text-decoration: none;
}

.reference-text {
  margin-top: 18px;
  white-space: pre-wrap;
  line-height: 1.8;
}

.completion-modal {
  text-align: center;
}

.completion-symbol {
  width: 54px;
  height: 54px;
  display: grid;
  place-items: center;
  margin: 0 auto 16px;
  border: 1px solid rgba(127, 127, 127, 0.2);
  border-radius: 50%;
  font-size: 24px;
}

.completion-list {
  margin-top: 22px;
  padding: 15px;
  text-align: left;
  border-radius: 14px;
  background: rgba(127, 127, 127, 0.05);
}

.completion-list div {
  padding: 8px 0;
  font-size: 12px;
}

.completion-list span {
  display: inline-block;
  width: 24px;
  font-weight: 800;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 9px;
  margin-top: 22px;
}

.knowledge-preview {
  display: flex;
  flex-direction: column;
  gap: 7px;
  margin-top: 20px;
}

.knowledge-preview label {
  margin-top: 8px;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  opacity: 0.5;
}

/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 1050px) {
  .learning-layout {
    grid-template-columns: 1fr;
  }

  .topic-sidebar {
    position: static;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 850px) {
  .topic-page {
    padding: 20px 16px 70px;
  }

  .topic-hero {
    grid-template-columns: 1fr;
    gap: 25px;
  }

  .visual-grid,
  .knowledge-grid {
    grid-template-columns: 1fr;
  }

  .topic-sidebar {
    grid-template-columns: 1fr;
  }

  .next-action,
  .action-card,
  .visual-empty,
  .section-footer,
  .notes-footer {
    align-items: flex-start;
    flex-direction: column;
  }

  .assessment-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .assessment-side {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 560px) {
  .workspace-section {
    padding: 20px;
    border-radius: 17px;
  }

  .hero-main h1 {
    font-size: 40px;
  }

  .section-heading {
    align-items: flex-start;
    flex-direction: column;
  }

  .modal-card {
    padding: 23px;
  }
}
</style>
