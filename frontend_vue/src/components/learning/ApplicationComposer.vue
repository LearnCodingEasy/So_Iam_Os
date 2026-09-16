<script setup>
import { computed, ref } from 'vue'

import {
  createKnowledgeApplication,
  updateKnowledgeApplication,
  submitKnowledgeApplication,
  reviewKnowledgeApplication,
} from '@/services/learning'

const props = defineProps({
  topicId: {
    type: Number,
    required: true,
  },

  application: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['updated'])

const title = ref(props.application?.title || '')

const content = ref(props.application?.content || '')

const saving = ref(false)

const submitting = ref(false)

const reviewing = ref(false)

const error = ref('')

const currentApplication = ref(props.application)

const isReviewed = computed(() => {
  return Boolean(currentApplication.value?.review)
})
console.log('isReviewed: ', isReviewed)

const saveApplication = async () => {
  if (!title.value.trim()) {
    error.value = 'Application title is required.'
    return null
  }

  if (!content.value.trim()) {
    error.value = 'Describe what you actually applied.'
    return null
  }

  saving.value = true
  error.value = ''

  try {
    let result

    if (currentApplication.value?.id) {
      result = await updateKnowledgeApplication(currentApplication.value.id, {
        title: title.value,
        content: content.value,
      })
    } else {
      result = await createKnowledgeApplication({
        topic: props.topicId,
        title: title.value,
        content: content.value,
      })
    }

    currentApplication.value = result

    emit('updated', result)

    return result
  } catch (err) {
    console.error('Save application error:', err)

    error.value = err?.response?.data?.detail || 'Unable to save application.'

    return null
  } finally {
    saving.value = false
  }
}

const submitApplication = async () => {
  submitting.value = true
  error.value = ''

  try {
    let application = currentApplication.value

    if (!application) {
      application = await saveApplication()
    }

    if (!application) {
      return
    }

    const result = await submitKnowledgeApplication(application.id)

    currentApplication.value = result

    emit('updated', result)
  } catch (err) {
    console.error('Submit application error:', err)

    error.value = err?.response?.data?.detail || 'Unable to submit application.'
  } finally {
    submitting.value = false
  }
}

const runReview = async () => {
  if (!currentApplication.value) {
    return
  }

  reviewing.value = true
  error.value = ''

  try {
    const review = await reviewKnowledgeApplication(currentApplication.value.id)

    currentApplication.value = {
      ...currentApplication.value,
      review,
      status: 'reviewed',
    }

    emit('updated', currentApplication.value)
  } catch (err) {
    console.error('AI review error:', err)

    error.value = err?.response?.data?.detail || 'Unable to review application.'
  } finally {
    reviewing.value = false
  }
}
</script>

<template>
  <section class="application-composer">
    <header class="application-header">
      <div>
        <span class="section-kicker"> PRACTICE </span>

        <h2>Apply what you learned</h2>

        <p>
          Don't just describe the theory. Show what you actually built, solved, tested, or
          practiced.
        </p>
      </div>

      <span v-if="currentApplication" class="application-status">
        {{ currentApplication.status }}
      </span>
    </header>

    <div v-if="error" class="application-error">
      {{ error }}
    </div>

    <div class="application-form">
      <label>
        Application title

        <input v-model="title" type="text" placeholder="e.g. I built a JWT authentication API" />
      </label>

      <label>
        What did you actually do?

        <textarea
          v-model="content"
          rows="10"
          placeholder="Describe your implementation, experiment, project, problem solving, or practical work..."
        />
      </label>

      <div class="application-actions">
        <button
          class="secondary-btn"
          :disabled="saving || submitting || reviewing"
          @click="saveApplication"
        >
          {{ saving ? 'Saving...' : 'Save Draft' }}
        </button>

        <button
          class="primary-btn"
          :disabled="saving || submitting || reviewing"
          @click="submitApplication"
        >
          {{ submitting ? 'Submitting...' : 'Submit Application' }}
        </button>

        <button
          v-if="
            currentApplication?.status === 'submitted' || currentApplication?.status === 'reviewed'
          "
          class="review-btn"
          :disabled="reviewing || submitting"
          @click="runReview"
        >
          {{ reviewing ? 'Analyzing...' : 'AI Review' }}
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.application-composer {
  margin-top: 28px;
  border: 1px solid rgba(127, 127, 127, 0.18);
  border-radius: 18px;
  padding: 24px;
}

.application-header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}

.application-header h2 {
  margin: 5px 0;
}

.application-header p {
  margin: 0;
  opacity: 0.6;
  max-width: 700px;
}

.application-status {
  height: fit-content;
  padding: 6px 10px;
  border-radius: 20px;
  background: rgba(127, 127, 127, 0.1);
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
}

.application-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.application-form label {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
}

.application-form input,
.application-form textarea {
  box-sizing: border-box;
  width: 100%;
  border: 1px solid rgba(127, 127, 127, 0.25);
  border-radius: 10px;
  padding: 12px;
  background: transparent;
  color: inherit;
  font: inherit;
  resize: vertical;
}

.application-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 10px;
}

.primary-btn,
.secondary-btn,
.review-btn {
  border: 0;
  border-radius: 9px;
  padding: 11px 16px;
  font-weight: 700;
  cursor: pointer;
}

.primary-btn {
  background: currentColor;
  color: white;
}

.secondary-btn {
  background: rgba(127, 127, 127, 0.12);
  color: inherit;
}

.review-btn {
  background: rgba(80, 130, 220, 0.15);
  color: inherit;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.application-error {
  margin-bottom: 16px;
  padding: 12px;
  border-radius: 10px;
  background: rgba(200, 50, 50, 0.1);
  color: #c44;
}
</style>
