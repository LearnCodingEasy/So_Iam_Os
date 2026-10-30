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
  completeLearningTopic,
  topicChat,
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
const showTopicChat = ref(false)
const chatMessage = ref('')
const chatMessages = ref([])
const chatLoading = ref(false)

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
console.log('applicationSaving: ', applicationSaving)
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
    await loadTopicChat()
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
const sourceLessonContent = computed(
  () => lesson.value?.content || knowledgeItem.value?.content || '',
)

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
    const result = await completeLearningTopic(topic.value.id)
    topic.value = result
    showCompletePanel.value = false
    await loadTopic()
  } catch (err) {
    console.error('Complete topic error:', err)

    error.value = err?.response?.data?.detail || 'Unable to complete this topic.'
  }
}

const loadTopicChat = async () => {
  try {
    const stored = localStorage.getItem(`topic_chat_${topic.value?.id}`)
    if (!stored) return
    const data = (
      await (await import('@/services/api')).default.get(`/ai/conversations/${stored}/`)
    ).data
    chatMessages.value = (data.messages || [])
      .filter((m) => ['user', 'assistant'].includes(m.role))
      .map((m) => ({ role: m.role, content: m.content }))
  } catch {}
}

const sendTopicChat = async () => {
  const message = chatMessage.value.trim()
  if (!message || !topic.value || chatLoading.value) return
  chatMessages.value.push({ role: 'user', content: message })
  chatMessage.value = ''
  chatLoading.value = true
  try {
    const result = await topicChat({
      topic_id: topic.value.id,
      message,
      conversation_id: localStorage.getItem(`topic_chat_${topic.value.id}`) || undefined,
    })
    if (result.conversation_id)
      localStorage.setItem(`topic_chat_${topic.value.id}`, result.conversation_id)
    chatMessages.value.push({ role: 'assistant', content: result.message?.content || '' })
  } catch (err) {
    error.value = err?.response?.data?.error || 'Unable to answer this topic question.'
  } finally {
    chatLoading.value = false
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

        <prime_button type="button" class="primary-button" @click="loadTopic"
          >Try again</prime_button
        >
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

            <div class="" v-if="topic.skill">
              <span v-if="topic.skill"> Skill # </span>
              <prime_tag
                v-if="topic.skill.name"
                :value="topic.skill.name"
                :severity="topic.skill.name"
                rounded
                class="class_name"
              />
              <prime_tag
                v-if="topic.skill.description"
                :value="topic.skill.description"
                :severity="topic.skill.description"
                rounded
                class="class_name"
              />
              <prime_tag
                v-if="topic.skill.category"
                :value="topic.skill.category"
                :severity="topic.skill.category"
                rounded
                class="class_name"
              />
              <prime_tag
                v-if="topic.skill.created_at"
                :value="topic.skill.created_at"
                :severity="topic.skill.created_at"
                rounded
                class="class_name"
              />
              <prime_tag
                v-if="topic.skill.updated_at"
                :value="topic.skill.updated_at"
                :severity="topic.skill.updated_at"
                rounded
                class="class_name"
              />
            </div>
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
              <prime_button
                type="button"
                class="primary-button"
                :disabled="generatingContent"
                @click="generateTopicContent"
              >
                {{ generatingContent ? 'Generating...' : 'Generate learning content' }}
              </prime_button>
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
            <div v-if="!lesson && knowledgeItem" class="content-placeholder source-ready">
              <span class="placeholder-number">K</span>
              <div>
                <h3>Knowledge source is ready</h3>
                <p>
                  {{ knowledgeItem.title }} is the primary source for this topic. Use it directly or
                  ask AI to explain it.
                </p>
                <pre class="source-content">{{ knowledgeItem.content }}</pre>
              </div>
            </div>
            <div v-else-if="!lesson" class="content-placeholder">
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

                <prime_button
                  type="button"
                  class="primary-button"
                  :disabled="generatingContent"
                  @click="generateTopicContent"
                >
                  {{ generatingContent ? 'Generating content...' : 'Generate learning content' }}
                </prime_button>
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
                  <prime_button
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
                  </prime_button>
                </div>
              </div>

              <!-- References -->
              <div v-if="references.length" class="lesson-references">
                <div class="subsection-heading">
                  <span class="section-kicker"> REFERENCES </span>

                  <h3>Explore further</h3>
                </div>

                <div class="reference-list">
                  <prime_button
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
                  </prime_button>
                </div>
              </div>

              <!-- Complete lesson -->
              <div class="lesson-footer">
                <div>
                  <strong> Finished studying? </strong>

                  <p>Mark the lesson as completed to continue to the knowledge check.</p>
                </div>

                <prime_button
                  type="button"
                  class="primary-button"
                  :disabled="lessonCompleted"
                  @click="markLessonCompleted"
                >
                  {{ lessonCompleted ? 'Lesson completed ✓' : 'Mark lesson completed' }}
                </prime_button>
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

            <prime_button type="button" class="primary-button" @click="goToStep(nextStep.key)">
              Continue
              <span>→</span>
            </prime_button>
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
              <prime_button
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
              </prime_button>
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

              <prime_button type="button" class="secondary-button" @click="generateImagePrompt">
                Create visual prompt
              </prime_button>
            </div>

            <!-- IMAGE PROMPT -->

            <div v-if="imagePrompt" class="prompt-panel">
              <div class="prompt-header">
                <div>
                  <span class="section-kicker"> AI VISUAL </span>

                  <h3>Prompt for image generation</h3>
                </div>

                <prime_button type="button" class="icon-button" @click="imagePrompt = ''"
                  >×</prime_button
                >
              </div>

              <prime_textarea v-model="imagePrompt" rows="8" />

              <div class="prompt-actions">
                <prime_button type="button" class="secondary-button" @click="generateImagePrompt">
                  Regenerate
                </prime_button>

                <prime_button type="button" class="primary-button" @click="copyImagePrompt">
                  {{ imagePromptCopied ? 'Copied' : 'Copy prompt' }}
                </prime_button>
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
              <prime_button
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
              </prime_button>
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

              <prime_button type="button" class="primary-button" @click="startQuickCheck">
                Start check
              </prime_button>
            </div>

            <div v-else-if="!quickCheckCompleted" class="quiz-placeholder">
              <span class="section-kicker"> KNOWLEDGE CHECK </span>

              <h3>Interactive questions will appear here</h3>

              <p>This area is ready for the backend assessment engine.</p>

              <prime_button type="button" class="primary-button" @click="finishQuickCheck">
                Complete demo check
              </prime_button>
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

            <prime_textarea
              v-model="personalNote"
              class="personal-note"
              placeholder="Explain the idea in your own words. What became clear? What is still confusing?"
              rows="8"
            />

            <div class="notes-footer">
              <span> Your own explanation becomes part of your personal knowledge. </span>

              <prime_button
                type="button"
                class="primary-button"
                :disabled="!personalNote.trim()"
                @click="savePersonalNote"
              >
                {{ noteSaved ? 'Saved ✓' : 'Save reflection' }}
              </prime_button>
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

                  <prime_button type="button" class="secondary-button">Start</prime_button>
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
              <prime_button
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
              </prime_button>
            </div>
          </div>

          <!-- ===============================================
               AI
          ================================================ -->

          <div class="sidebar-card ai-card">
            <span class="section-kicker"> AI ASSISTANT </span>

            <h3>Stuck on something?</h3>

            <p>Ask questions about this lesson without leaving the learning workspace.</p>

            <prime_button
              type="button"
              class="secondary-button full-width"
              @click="showTopicChat = true"
            >
              Ask about this topic
            </prime_button>
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

            <prime_button
              type="button"
              class="primary-button full-width"
              :disabled="!canCompleteTopic"
              @click="openCompletePanel"
            >
              {{ canCompleteTopic ? 'Complete topic' : 'Finish learning first' }}
            </prime_button>
          </div>
        </aside>
      </section>
    </template>

    <div v-if="showTopicChat" class="modal-backdrop" @click.self="showTopicChat = false">
      <div class="modal-card chat-modal">
        <prime_button type="button" class="modal-close" @click="showTopicChat = false"
          >×</prime_button
        ><span class="section-kicker">TOPIC CHAT</span>
        <h2>{{ topic?.title }}</h2>
        <div class="chat-messages">
          <div v-for="(m, i) in chatMessages" :key="i" :class="['chat-message', m.role]">
            <b>{{ m.role === 'user' ? 'You' : 'AI' }}</b>
            <p>{{ m.content }}</p>
          </div>
          <div v-if="chatLoading" class="chat-message assistant"><p>Thinking...</p></div>
        </div>
        <form @submit.prevent="sendTopicChat" class="chat-form">
          <prime_input_text
            v-model="chatMessage"
            placeholder="Ask about this topic..."
          /><prime_button class="primary-button"> Send </prime_button>
        </form>
      </div>
    </div>

    <!-- ============================================
    REFERENCE MODAL
    ============================================= -->

    <div v-if="activeReference" class="modal-backdrop" @click.self="closeReference">
      <div class="modal-card">
        <prime_button type="button" class="modal-close" @click="closeReference">×</prime_button>

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
        <prime_button type="button" class="modal-close" @click="closeCompletePanel">×</prime_button>

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
          <prime_button type="button" class="secondary-button" @click="closeCompletePanel">
            Continue
          </prime_button>

          <prime_button type="button" class="primary-button" @click="completeTopic">
            Confirm completion
          </prime_button>
        </div>
      </div>
    </div>

    <!-- ============================================
    KNOWLEDGE MODAL
    ============================================= -->

    <div v-if="showKnowledgePreview" class="modal-backdrop" @click.self="closeKnowledgePreview">
      <div class="modal-card knowledge-modal">
        <prime_button type="button" class="modal-close" @click="closeKnowledgePreview"
          >×</prime_button
        >

        <span class="section-kicker"> KNOWLEDGE </span>

        <h2>Capture what you learned</h2>

        <p>This is where the learning result becomes permanent knowledge.</p>

        <div class="knowledge-preview">
          <label> Title </label>

          <prime_input_text :value="topic.title" readonly />

          <label> Source </label>

          <prime_input_text value="Learning Topic" readonly />

          <label> Mastery </label>

          <prime_input_text :value="mastery" readonly />

          <label> Knowledge </label>

          <prime_textarea
            :value="personalNote || lesson?.content || topic.description || ''"
            rows="8"
            readonly
          />
        </div>

        <div class="modal-actions">
          <prime_button type="button" class="secondary-button" @click="closeKnowledgePreview">
            Cancel
          </prime_button>

          <prime_button
            type="button"
            class="primary-button"
            :disabled="knowledgeSaving"
            @click="saveToKnowledge"
          >
            {{ knowledgeSaving ? 'Saving...' : 'Save to Knowledge' }}
          </prime_button>
        </div>
      </div>
    </div>
  </div>
</template>
