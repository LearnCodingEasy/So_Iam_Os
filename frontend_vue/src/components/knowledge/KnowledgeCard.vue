<script setup>
import {
  faArchive,
  faArrowUpRightFromSquare,
  faBook,
  faCode,
  faFileLines,
  faLightbulb,
  faPen,
} from '@fortawesome/free-solid-svg-icons'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

defineProps({
  knowledge: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['edit', 'archive'])

const typeIcons = {
  note: faPen,
  document: faFileLines,
  article: faBook,
  documentation: faCode,
  idea: faLightbulb,
  project: faCode,
  learning: faBook,
  reference: faBook,
  other: faFileLines,
}

const getIcon = (type) => {
  return typeIcons[type] || faFileLines
}

const getTypeLabel = (type) => {
  const labels = {
    note: 'Note',
    document: 'Document',
    article: 'Article',
    documentation: 'Documentation',
    idea: 'Idea',
    project: 'Project',
    learning: 'Learning',
    reference: 'Reference',
    other: 'Other',
  }

  return labels[type] || type
}

const formatDate = (date) => {
  if (!date) {
    return ''
  }

  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(date))
}
</script>

<template>
  <article
    class="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md dark:border-slate-700 dark:bg-slate-900"
  >
    <!-- Header -->
    <div class="mb-4 flex items-start justify-between gap-4">
      <div class="flex min-w-0 items-center gap-3">
        <div
          class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600 dark:bg-indigo-500/10 dark:text-indigo-400"
        >
          <FontAwesomeIcon :icon="getIcon(knowledge.knowledge_type)" />
        </div>

        <div class="min-w-0">
          <h3 class="truncate text-base font-semibold text-slate-900 dark:text-white">
            {{ knowledge.title }}
          </h3>

          <span class="text-xs font-medium uppercase tracking-wide text-slate-400">
            {{ getTypeLabel(knowledge.knowledge_type) }}
          </span>
        </div>
      </div>

      <button
        type="button"
        class="rounded-lg p-2 text-slate-400 opacity-0 transition hover:bg-slate-100 hover:text-slate-700 group-hover:opacity-100 dark:hover:bg-slate-800 dark:hover:text-white"
        title="Archive"
        @click="emit('archive', knowledge)"
      >
        <FontAwesomeIcon :icon="faArchive" />
      </button>
    </div>

    <!-- Description -->
    <p
      v-if="knowledge.description"
      class="mb-4 line-clamp-3 text-sm leading-6 text-slate-600 dark:text-slate-300"
    >
      {{ knowledge.description }}
    </p>

    <!-- Tags -->
    <div v-if="knowledge.tags?.length" class="mb-4 flex flex-wrap gap-2">
      <span
        v-for="tag in knowledge.tags"
        :key="tag"
        class="rounded-full bg-slate-100 px-2.5 py-1 text-xs text-slate-600 dark:bg-slate-800 dark:text-slate-300"
      >
        #{{ tag }}
      </span>
    </div>

    <!-- Footer -->
    <div
      class="flex items-center justify-between border-t border-slate-100 pt-4 dark:border-slate-800"
    >
      <span class="text-xs text-slate-400">
        {{ formatDate(knowledge.updated_at) }}
      </span>

      <div class="flex items-center gap-2">
        <a
          v-if="knowledge.source_url"
          :href="knowledge.source_url"
          target="_blank"
          rel="noopener noreferrer"
          class="rounded-lg p-2 text-slate-400 transition hover:bg-slate-100 hover:text-indigo-600 dark:hover:bg-slate-800"
          title="Open source"
        >
          <FontAwesomeIcon :icon="faArrowUpRightFromSquare" />
        </a>

        <button
          type="button"
          class="rounded-lg p-2 text-slate-400 transition hover:bg-slate-100 hover:text-indigo-600 dark:hover:bg-slate-800"
          title="Edit"
          @click="emit('edit', knowledge)"
        >
          <FontAwesomeIcon :icon="faPen" />
        </button>
      </div>
    </div>
  </article>
</template>
