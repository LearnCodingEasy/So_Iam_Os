<script setup>
defineProps({
  topic: {
    type: Object,
    required: true,
  },

  progress: {
    type: Number,
    default: 0,
  },
})

const statusLabel = (status) => {
  const labels = {
    pending: 'Pending',
    in_progress: 'In Progress',
    completed: 'Completed',
    skipped: 'Skipped',
  }

  return labels[status] || status
}
</script>

<template>
  <article class="topic-editor-card">
    <div class="drag-handle" title="Drag to reorder">⋮⋮</div>

    <div class="topic-editor-number">
      {{ String(topic.order || 1).padStart(2, '0') }}
    </div>

    <div class="topic-editor-content">
      <div class="topic-editor-meta">
        <span class="topic-status" :class="topic.status">
          {{ statusLabel(topic.status) }}
        </span>

        <span v-if="topic.estimated_minutes"> {{ topic.estimated_minutes }} min </span>
      </div>

      <h3>
        {{ topic.title }}
      </h3>

      <p>
        {{ topic.description || 'No description.' }}
      </p>

      <div class="topic-editor-progress">
        <div class="topic-progress-track">
          <div class="topic-progress-fill" :style="{ width: `${progress}%` }" />
        </div>

        <strong> {{ progress }}% </strong>
      </div>
    </div>

    <div class="topic-editor-arrow">→</div>
  </article>
</template>
