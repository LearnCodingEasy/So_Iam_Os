<script setup>
import { computed, ref } from 'vue'

import { RouterLink } from 'vue-router'

import draggable from 'vuedraggable'

import LearningTopicCard from './LearningTopicCard.vue'

import {
  createLearningTopic,
  updateLearningTopic,
  deleteLearningTopic,
  reorderLearningTopics,
} from '@/services/learning'

const props = defineProps({
  paths: {
    type: Array,
    default: () => [],
  },

  topics: {
    type: Array,
    default: () => [],
  },

  progress: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['refresh'])

const selectedPathId = ref(props.paths[0]?.id || null)

const savingOrder = ref(false)

const savingTopic = ref(false)

const deletingTopic = ref(false)

const error = ref('')

const showTopicModal = ref(false)

const editingTopic = ref(null)

const topicForm = ref({
  title: '',
  description: '',
  estimated_minutes: 30,
  status: 'pending',
  skill: null,
})

const selectedPath = computed(() => {
  return props.paths.find((path) => path.id === selectedPathId.value)
})

const pathTopics = computed(() => {
  return props.topics
    .filter((topic) => topic.path === selectedPathId.value)
    .sort((a, b) => Number(a.order || 0) - Number(b.order || 0))
})

const getProgress = (topicId) => {
  const item = props.progress.find((entry) => entry.topic === topicId)

  return item?.progress_percent ?? 0
}

const selectPath = (pathId) => {
  selectedPathId.value = pathId
}

const openCreateTopic = () => {
  editingTopic.value = null

  topicForm.value = {
    title: '',
    description: '',
    estimated_minutes: 30,
    status: 'pending',
    skill: null,
  }

  error.value = ''

  showTopicModal.value = true
}

const openEditTopic = (topic) => {
  editingTopic.value = topic

  topicForm.value = {
    title: topic.title || '',
    description: topic.description || '',
    estimated_minutes: topic.estimated_minutes || 30,
    status: topic.status || 'pending',
    skill: topic.skill || null,
  }

  error.value = ''

  showTopicModal.value = true
}

const closeTopicModal = () => {
  if (savingTopic.value) {
    return
  }

  showTopicModal.value = false
  editingTopic.value = null
}

const saveTopic = async () => {
  if (!selectedPathId.value) {
    return
  }

  if (!topicForm.value.title.trim()) {
    error.value = 'Topic title is required.'
    return
  }

  savingTopic.value = true
  error.value = ''

  try {
    if (editingTopic.value) {
      await updateLearningTopic(editingTopic.value.id, {
        title: topicForm.value.title,
        description: topicForm.value.description,
        estimated_minutes: Number(topicForm.value.estimated_minutes),
        status: topicForm.value.status,
        skill: topicForm.value.skill,
      })
    } else {
      await createLearningTopic({
        path: selectedPathId.value,

        title: topicForm.value.title,

        description: topicForm.value.description,

        estimated_minutes: Number(topicForm.value.estimated_minutes),

        status: topicForm.value.status,

        skill: topicForm.value.skill,

        order: pathTopics.value.length + 1,
      })
    }

    closeTopicModal()

    emit('refresh')
  } catch (err) {
    console.error('Save topic error:', err)

    error.value = err?.response?.data?.detail || 'Unable to save topic.'
  } finally {
    savingTopic.value = false
  }
}

const removeTopic = async (topic) => {
  const confirmed = window.confirm(`Delete "${topic.title}"?`)

  if (!confirmed) {
    return
  }

  deletingTopic.value = true
  error.value = ''

  try {
    await deleteLearningTopic(topic.id)

    emit('refresh')
  } catch (err) {
    console.error('Delete topic error:', err)

    error.value = err?.response?.data?.detail || 'Unable to delete topic.'
  } finally {
    deletingTopic.value = false
  }
}

const saveOrder = async () => {
  if (!selectedPathId.value) {
    return
  }

  savingOrder.value = true
  error.value = ''

  try {
    const topicIds = pathTopics.value.map((topic) => topic.id)

    await reorderLearningTopics(selectedPathId.value, topicIds)

    emit('refresh')
  } catch (err) {
    console.error('Reorder topics error:', err)

    error.value = err?.response?.data?.detail || 'Unable to reorder topics.'
  } finally {
    savingOrder.value = false
  }
}
</script>

<template>
  <section class="path-editor">
    <!-- Header -->
    <header class="path-editor-header">
      <div>
        <span class="section-kicker"> LEARNING PATH EDITOR </span>

        <h2>Build your roadmap</h2>

        <p>Arrange topics in the order that makes sense for your learning.</p>
      </div>

      <div class="path-editor-actions">
        <button class="secondary-btn" @click="openCreateTopic" :disabled="!selectedPathId">
          + Add Topic
        </button>

        <button class="primary-btn" @click="saveOrder" :disabled="savingOrder">
          {{ savingOrder ? 'Saving...' : 'Save Order' }}
        </button>
      </div>
    </header>

    <!-- Error -->
    <div v-if="error" class="editor-error">
      {{ error }}
    </div>

    <div class="path-editor-layout">
      <!-- Paths -->
      <aside class="path-selector">
        <div class="path-selector-title">Learning Paths</div>

        <button
          v-for="path in paths"
          :key="path.id"
          class="path-selector-item"
          :class="{
            active: selectedPathId === path.id,
          }"
          @click="selectPath(path.id)"
        >
          <span>
            {{ path.title }}
          </span>

          <small>
            {{ topics.filter((topic) => topic.path === path.id).length }}
            topics
          </small>
        </button>

        <div v-if="!paths.length" class="empty-editor">No learning paths.</div>
      </aside>

      <!-- Topics -->
      <main class="path-topics-editor">
        <div v-if="selectedPath" class="selected-path-heading">
          <div>
            <span> PATH </span>

            <h3>
              {{ selectedPath.title }}
            </h3>

            <p>
              {{ selectedPath.description || 'No description available.' }}
            </p>
          </div>

          <strong> {{ pathTopics.length }} Topics </strong>
        </div>

        <draggable
          v-if="pathTopics.length"
          :list="pathTopics"
          item-key="id"
          handle=".drag-handle"
          ghost-class="topic-drag-ghost"
          class="topic-sort-list"
        >
          <template #item="{ element }">
            <div class="topic-sort-item">
              <RouterLink
                :to="{
                  name: 'learning-topic',
                  params: {
                    topicId: element.id,
                  },
                }"
                class="topic-card-link"
              >
                <LearningTopicCard :topic="element" :progress="getProgress(element.id)" />
              </RouterLink>

              <div class="topic-actions">
                <button @click.prevent="openEditTopic(element)">Edit</button>

                <button
                  class="danger-action"
                  :disabled="deletingTopic"
                  @click.prevent="removeTopic(element)"
                >
                  Delete
                </button>
              </div>
            </div>
          </template>
        </draggable>

        <div v-else-if="selectedPath" class="empty-editor large">
          <strong> This path has no topics yet. </strong>

          <p>Add your first learning topic.</p>

          <button class="primary-btn" @click="openCreateTopic">+ Add Topic</button>
        </div>
      </main>
    </div>

    <!-- Topic Modal -->
    <div v-if="showTopicModal" class="editor-modal-overlay" @click.self="closeTopicModal">
      <div class="editor-modal">
        <header class="editor-modal-header">
          <div>
            <span class="section-kicker">
              {{ editingTopic ? 'EDIT TOPIC' : 'NEW TOPIC' }}
            </span>

            <h3>
              {{ editingTopic ? 'Edit learning topic' : 'Add learning topic' }}
            </h3>
          </div>

          <button class="modal-close" @click="closeTopicModal">×</button>
        </header>

        <div class="editor-form">
          <label>
            Title

            <input v-model="topicForm.title" type="text" placeholder="e.g. Django Authentication" />
          </label>

          <label>
            Description

            <textarea v-model="topicForm.description" rows="4" placeholder="What will you learn?" />
          </label>

          <label>
            Estimated minutes

            <input v-model.number="topicForm.estimated_minutes" type="number" min="1" />
          </label>

          <label>
            Status

            <select v-model="topicForm.status">
              <option value="pending">Pending</option>

              <option value="in_progress">In Progress</option>

              <option value="completed">Completed</option>

              <option value="skipped">Skipped</option>
            </select>
          </label>
        </div>

        <footer class="editor-modal-actions">
          <button class="secondary-btn" :disabled="savingTopic" @click="closeTopicModal">
            Cancel
          </button>

          <button class="primary-btn" :disabled="savingTopic" @click="saveTopic">
            {{ savingTopic ? 'Saving...' : 'Save Topic' }}
          </button>
        </footer>
      </div>
    </div>
  </section>
</template>

<style scoped>
.path-editor {
  margin-top: 32px;
}

.path-editor-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 24px;
}

.path-editor-header h2 {
  margin: 6px 0;
}

.path-editor-header p {
  margin: 0;
  opacity: 0.65;
}

.path-editor-actions {
  display: flex;
  gap: 10px;
}

.path-editor-layout {
  display: grid;
  grid-template-columns: 250px minmax(0, 1fr);
  gap: 20px;
}

.path-selector {
  border: 1px solid rgba(127, 127, 127, 0.2);
  border-radius: 16px;
  padding: 12px;
}

.path-selector-title {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.12em;
  opacity: 0.5;
  padding: 10px;
}

.path-selector-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  border: 0;
  background: transparent;
  padding: 13px;
  border-radius: 10px;
  cursor: pointer;
  text-align: left;
}

.path-selector-item:hover,
.path-selector-item.active {
  background: rgba(127, 127, 127, 0.1);
}

.path-selector-item span {
  font-weight: 700;
}

.path-selector-item small {
  margin-top: 4px;
  opacity: 0.55;
}

.selected-path-heading {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 18px;
}

.selected-path-heading span {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.12em;
  opacity: 0.5;
}

.selected-path-heading h3 {
  margin: 5px 0;
  font-size: 22px;
}

.selected-path-heading p {
  margin: 0;
  opacity: 0.6;
}

.topic-sort-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.topic-sort-item {
  position: relative;
}

.topic-card-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.topic-editor-card {
  display: grid;
  grid-template-columns: 36px 48px minmax(0, 1fr) 30px;
  align-items: center;
  gap: 12px;
  border: 1px solid rgba(127, 127, 127, 0.18);
  border-radius: 14px;
  padding: 16px;
  background: rgba(127, 127, 127, 0.03);
  transition: transform 0.2s ease;
}

.topic-editor-card:hover {
  transform: translateY(-1px);
}

.drag-handle {
  cursor: grab;
  font-size: 20px;
  opacity: 0.4;
  user-select: none;
}

.drag-handle:active {
  cursor: grabbing;
}

.topic-editor-number {
  font-size: 18px;
  font-weight: 800;
  opacity: 0.4;
}

.topic-editor-meta {
  display: flex;
  gap: 10px;
  font-size: 11px;
  opacity: 0.6;
}

.topic-status {
  font-weight: 800;
}

.topic-editor-content h3 {
  margin: 5px 0;
}

.topic-editor-content p {
  margin: 0 0 10px;
  opacity: 0.6;
}

.topic-editor-progress {
  display: flex;
  align-items: center;
  gap: 10px;
}

.topic-progress-track {
  flex: 1;
  height: 5px;
  border-radius: 10px;
  overflow: hidden;
  background: rgba(127, 127, 127, 0.15);
}

.topic-progress-fill {
  height: 100%;
  background: currentColor;
}

.topic-editor-progress strong {
  font-size: 11px;
}

.topic-editor-arrow {
  opacity: 0.35;
}

.topic-actions {
  display: flex;
  gap: 8px;
  margin-top: 7px;
  justify-content: flex-end;
}

.topic-actions button {
  border: 0;
  background: transparent;
  cursor: pointer;
  font-size: 12px;
  opacity: 0.65;
}

.topic-actions button:hover {
  opacity: 1;
}

.danger-action {
  color: #c44;
}

.topic-drag-ghost {
  opacity: 0.4;
}

.primary-btn,
.secondary-btn {
  border: 0;
  border-radius: 9px;
  padding: 10px 15px;
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

.primary-btn:disabled,
.secondary-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.editor-error {
  margin-bottom: 15px;
  padding: 12px 14px;
  border-radius: 10px;
  background: rgba(200, 50, 50, 0.1);
  color: #c44;
}

.empty-editor {
  padding: 30px 15px;
  text-align: center;
  opacity: 0.6;
}

.empty-editor.large {
  padding: 70px 20px;
  border: 1px dashed rgba(127, 127, 127, 0.25);
  border-radius: 14px;
}

.empty-editor p {
  margin: 8px 0 18px;
}

.editor-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.55);
}

.editor-modal {
  width: min(620px, 100%);
  border-radius: 18px;
  padding: 24px;
  background: var(--bg, white);
  box-shadow: 0 20px 70px rgba(0, 0, 0, 0.3);
}

.editor-modal-header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.editor-modal-header h3 {
  margin: 5px 0 20px;
}

.modal-close {
  border: 0;
  background: transparent;
  font-size: 26px;
  cursor: pointer;
}

.editor-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.editor-form label {
  display: flex;
  flex-direction: column;
  gap: 7px;
  font-size: 13px;
  font-weight: 700;
}

.editor-form input,
.editor-form textarea,
.editor-form select {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid rgba(127, 127, 127, 0.25);
  border-radius: 9px;
  padding: 11px;
  background: transparent;
  color: inherit;
  font: inherit;
}

.editor-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 22px;
}

@media (max-width: 800px) {
  .path-editor-header {
    flex-direction: column;
    align-items: stretch;
  }

  .path-editor-layout {
    grid-template-columns: 1fr;
  }
}
</style>
