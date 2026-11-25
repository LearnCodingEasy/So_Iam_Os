<template>
  <section class="enhancement-center" :class="{ 'reduced-motion': prefersReducedMotion }">
    <header class="enhancement-center__header">
      <div>
        <span class="eyebrow">SO_IAM_OS / FRONTEND</span>
        <h1>{{ t('enhancements.title') }}</h1>
        <p>{{ t('enhancements.subtitle') }}</p>
      </div>
      <div class="enhancement-center__actions">
        <button v-tooltip="'Switch application language'" type="button" @click="toggleLocale">
          {{ locale === 'ar' ? 'EN' : 'عربي' }}
        </button>
        <button v-tooltip="'Trigger a real toast notification'" type="button" @click="notify">
          {{ t('enhancements.notify') }}
        </button>
      </div>
    </header>

    <div class="enhancement-grid">
      <article class="enhancement-card">
        <div class="card-heading">
          <span>01</span>
          <h2>{{ t('enhancements.cache') }}</h2>
        </div>
        <p v-if="query.isPending">Loading server state…</p>
        <p v-else-if="query.isError">Backend unavailable: {{ query.error?.message }}</p>
        <p v-else>API health request completed at {{ query.data?.timestamp || '—' }}.</p>
        <small>TanStack Vue Query · {{ query.isFetching ? 'refreshing' : 'cached' }}</small>
      </article>

      <article class="enhancement-card enhancement-card--wide">
        <div class="card-heading">
          <span>02</span>
          <h2>{{ t('enhancements.editor') }}</h2>
        </div>
        <EditorContent v-if="editor" :editor="editor" class="tiptap-surface" />
      </article>

      <article class="enhancement-card">
        <div class="card-heading">
          <span>03</span>
          <h2>{{ t('enhancements.files') }}</h2>
        </div>
        <input ref="fileInput" type="file" multiple />
        <small
          >FilePond is configured as an upload intake UI; submission remains
          backend-controlled.</small
        >
      </article>

      <article class="enhancement-card">
        <div class="card-heading">
          <span>04</span>
          <h2>{{ t('enhancements.theme') }}</h2>
        </div>
        <label class="switch-row">
          <input v-model="isDark" type="checkbox" />
          <span>{{ isDark ? 'Dark' : 'Light' }}</span>
        </label>
        <small>VueUse · useDark</small>
      </article>

      <article class="enhancement-card enhancement-card--wide">
        <div class="card-heading">
          <span>05</span>
          <h2>{{ t('enhancements.reorder') }}</h2>
        </div>
        <VueDraggable v-model="cards" class="draggable-list" :animation="180" handle=".drag-handle">
          <div v-for="card in cards" :key="card.id" class="draggable-item">
            <span class="drag-handle" aria-hidden="true">⋮⋮</span>
            <strong>{{ card.title }}</strong>
            <span>{{ card.description }}</span>
          </div>
        </VueDraggable>
      </article>

      <article class="enhancement-card enhancement-card--wide">
        <div class="card-heading">
          <span>06</span>
          <h2>{{ t('enhancements.virtualization') }}</h2>
        </div>
        <DynamicScroller
          class="activity-scroller"
          :items="activity"
          :min-item-size="42"
          key-field="id"
        >
          <template #default="{ item, active }">
            <DynamicScrollerItem :item="item" :active="active" :size-dependencies="[item.message]">
              <div class="activity-row">
                <span>{{ item.id }}</span>
                <span>{{ item.message }}</span>
              </div>
            </DynamicScrollerItem>
          </template>
        </DynamicScroller>
      </article>
    </div>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useDark, usePreferredReducedMotion } from '@vueuse/core'
import { useQuery } from '@tanstack/vue-query'
import { EditorContent, useEditor } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import { VueDraggable } from 'vue-draggable-plus'
import { DynamicScroller, DynamicScrollerItem } from 'vue-virtual-scroller'
import { toast } from 'vue-sonner'
import { create } from 'filepond'
import 'filepond/dist/filepond.min.css'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'

import api from '@/services/Shared/api'

const { t, locale } = useI18n()
const isDark = useDark({
  selector: 'html',
  attribute: 'class',
  valueDark: 'p-dark',
  valueLight: '',
})
const prefersReducedMotion = computed(() => usePreferredReducedMotion().value === 'reduce')

const query = useQuery({
  queryKey: ['frontend-enhancement-center', 'health'],
  queryFn: async () => {
    const response = await api.get('/ai/health/')
    return response.data
  },
  staleTime: 30_000,
  retry: 1,
})

const editor = useEditor({
  content: '<p>Write a note, decision or implementation brief…</p>',
  extensions: [StarterKit],
})

const cards = ref([
  { id: 1, title: 'AI', description: 'Provider-aware generation' },
  { id: 2, title: 'Knowledge', description: 'Searchable context' },
  { id: 3, title: 'Learning', description: 'Progress and review' },
  { id: 4, title: 'Automation', description: 'Workflow execution' },
])

const activity = Array.from({ length: 250 }, (_, index) => ({
  id: index + 1,
  message: `Activity event #${index + 1} — rendered through the virtualized stream.`,
}))

const fileInput = ref(null)
let pond

onMounted(() => {
  if (fileInput.value) {
    pond = create(fileInput.value, {
      allowMultiple: true,
      credits: false,
      instantUpload: false,
    })
  }
})

onBeforeUnmount(() => {
  pond?.destroy()
  editor.value?.destroy()
})

function toggleLocale() {
  locale.value = locale.value === 'ar' ? 'en' : 'ar'
  localStorage.setItem('so-iam-locale', locale.value)
}

function notify() {
  toast.success(locale.value === 'ar' ? 'تم تنفيذ الإجراء بنجاح' : 'Action completed successfully')
}
</script>

<style scoped lang="scss">
.enhancement-center {
  padding: 2rem;
}
.enhancement-center__header {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}
.eyebrow {
  font-size: 0.72rem;
  letter-spacing: 0.16em;
  opacity: 0.65;
}
.enhancement-center h1 {
  margin: 0.25rem 0 0.5rem;
  font-size: clamp(1.8rem, 3vw, 2.8rem);
}
.enhancement-center__header p {
  max-width: 760px;
  opacity: 0.75;
}
.enhancement-center__actions {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}
.enhancement-center__actions button {
  border: 1px solid var(--surface-border);
  background: var(--surface-card);
  color: inherit;
  border-radius: 10px;
  padding: 0.65rem 0.9rem;
  cursor: pointer;
}
.enhancement-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}
.enhancement-card {
  min-height: 180px;
  padding: 1.25rem;
  border: 1px solid var(--surface-border);
  border-radius: 18px;
  background: color-mix(in srgb, var(--surface-card) 94%, transparent);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
}
.enhancement-card--wide {
  grid-column: span 2;
}
.card-heading {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-bottom: 1rem;
}
.card-heading > span {
  opacity: 0.5;
  font-variant-numeric: tabular-nums;
}
.card-heading h2 {
  margin: 0;
  font-size: 1rem;
}
.tiptap-surface :deep(.tiptap) {
  min-height: 120px;
  outline: none;
  padding: 1rem;
  border: 1px solid var(--surface-border);
  border-radius: 12px;
}
.draggable-list {
  display: grid;
  gap: 0.5rem;
}
.draggable-item {
  display: grid;
  grid-template-columns: auto 120px 1fr;
  gap: 0.75rem;
  align-items: center;
  padding: 0.75rem;
  border: 1px solid var(--surface-border);
  border-radius: 10px;
  background: var(--surface-ground);
}
.drag-handle {
  cursor: grab;
  opacity: 0.6;
}
.activity-scroller {
  height: 240px;
  border: 1px solid var(--surface-border);
  border-radius: 12px;
}
.activity-row {
  display: grid;
  grid-template-columns: 56px 1fr;
  gap: 0.75rem;
  padding: 0.65rem 0.8rem;
  border-bottom: 1px solid color-mix(in srgb, var(--surface-border) 50%, transparent);
}
.switch-row {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}
@media (max-width: 900px) {
  .enhancement-center__header {
    flex-direction: column;
  }
  .enhancement-grid {
    grid-template-columns: 1fr;
  }
  .enhancement-card--wide {
    grid-column: span 1;
  }
  .draggable-item {
    grid-template-columns: auto 1fr;
  }
}
</style>
