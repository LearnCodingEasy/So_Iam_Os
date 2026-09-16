<script setup>
import { computed, onMounted, ref } from 'vue'

import {
  faBrain,
  faFilter,
  faMagnifyingGlass,
  faPlus,
  faRotate,
  faXmark,
} from '@fortawesome/free-solid-svg-icons'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { knowledgeService } from '@/services/knowledge'

import KnowledgeCard from '@/components/knowledge/KnowledgeCard.vue'
import KnowledgeEmptyState from '@/components/knowledge/KnowledgeEmptyState.vue'
import KnowledgeForm from '@/components/knowledge/KnowledgeForm.vue'

const knowledgeItems = ref([])

const loading = ref(false)
const saving = ref(false)

const error = ref('')
const successMessage = ref('')

const searchQuery = ref('')
const selectedType = ref('all')

const showForm = ref(false)
const editingKnowledge = ref(null)

const knowledgeTypes = [
  {
    value: 'note',
    label: 'Notes',
  },
  {
    value: 'document',
    label: 'Documents',
  },
  {
    value: 'article',
    label: 'Articles',
  },
  {
    value: 'documentation',
    label: 'Documentation',
  },
  {
    value: 'idea',
    label: 'Ideas',
  },
  {
    value: 'project',
    label: 'Projects',
  },
  {
    value: 'learning',
    label: 'Learning',
  },
  {
    value: 'reference',
    label: 'References',
  },
  {
    value: 'other',
    label: 'Other',
  },
]

const loadKnowledge = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await knowledgeService.getAll()

    knowledgeItems.value = Array.isArray(response) ? response : response.results || []
  } catch (err) {
    console.error('Failed to load knowledge:', err)

    error.value = err.response?.data?.detail || 'Failed to load your knowledge.'
  } finally {
    loading.value = false
  }
}

const filteredKnowledge = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()

  return knowledgeItems.value.filter((item) => {
    const matchesType = selectedType.value === 'all' || item.knowledge_type === selectedType.value

    if (!query) {
      return matchesType
    }

    const searchableText = [
      item.title,
      item.description,
      item.content,
      item.source_name,
      ...(item.tags || []),
    ]
      .join(' ')
      .toLowerCase()

    return matchesType && searchableText.includes(query)
  })
})

const totalKnowledge = computed(() => knowledgeItems.value.length)

const openCreateForm = () => {
  editingKnowledge.value = null
  showForm.value = true
  successMessage.value = ''
  error.value = ''
}

const openEditForm = (knowledge) => {
  editingKnowledge.value = knowledge
  showForm.value = true
  successMessage.value = ''
  error.value = ''
}

const closeForm = () => {
  showForm.value = false
  editingKnowledge.value = null
}

const saveKnowledge = async (data) => {
  saving.value = true
  error.value = ''

  try {
    if (editingKnowledge.value) {
      const updated = await knowledgeService.update(editingKnowledge.value.id, data)

      const index = knowledgeItems.value.findIndex((item) => item.id === editingKnowledge.value.id)

      if (index !== -1) {
        knowledgeItems.value[index] = updated
      }

      successMessage.value = 'Knowledge updated successfully.'
    } else {
      const created = await knowledgeService.create(data)

      knowledgeItems.value.unshift(created)

      successMessage.value = 'Knowledge created successfully.'
    }

    closeForm()
  } catch (err) {
    console.error('Failed to save knowledge:', err)

    error.value = err.response?.data?.detail || 'Failed to save knowledge.'
  } finally {
    saving.value = false
  }
}

const archiveKnowledge = async (knowledge) => {
  const confirmed = window.confirm(`Archive "${knowledge.title}"?`)

  if (!confirmed) {
    return
  }

  error.value = ''

  try {
    await knowledgeService.archive(knowledge.id)

    knowledgeItems.value = knowledgeItems.value.filter((item) => item.id !== knowledge.id)

    successMessage.value = 'Knowledge archived successfully.'
  } catch (err) {
    console.error('Failed to archive knowledge:', err)

    error.value = err.response?.data?.detail || 'Failed to archive knowledge.'
  }
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedType.value = 'all'
}

onMounted(() => {
  loadKnowledge()
})
</script>

<template>
  <section class="min-h-screen bg-slate-50 px-4 py-6 dark:bg-slate-950">
    <div class="mx-auto max-w-7xl">
      <!-- Header -->
      <header class="mb-8">
        <div class="flex flex-col justify-between gap-5 md:flex-row md:items-center">
          <div>
            <div class="mb-2 flex items-center gap-3">
              <div
                class="flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-sm"
              >
                <FontAwesomeIcon :icon="faBrain" />
              </div>

              <span
                class="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-600 dark:text-indigo-400"
              >
                So_Iam_OS
              </span>
            </div>

            <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
              Knowledge
            </h1>

            <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-500 dark:text-slate-400">
              Capture, organize, and build the knowledge that will later help your AI understand you
              and your work.
            </p>
          </div>

          <button
            type="button"
            class="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-700"
            @click="openCreateForm"
          >
            <FontAwesomeIcon :icon="faPlus" />
            Add knowledge
          </button>
        </div>
      </header>

      <!-- Stats -->
      <div class="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div
          class="rounded-2xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900"
        >
          <p class="text-xs font-medium uppercase tracking-wide text-slate-400">Total knowledge</p>

          <p class="mt-2 text-3xl font-bold text-slate-900 dark:text-white">
            {{ totalKnowledge }}
          </p>
        </div>

        <div
          class="rounded-2xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900"
        >
          <p class="text-xs font-medium uppercase tracking-wide text-slate-400">Visible now</p>

          <p class="mt-2 text-3xl font-bold text-slate-900 dark:text-white">
            {{ filteredKnowledge.length }}
          </p>
        </div>
      </div>

      <!-- Messages -->
      <div
        v-if="successMessage"
        class="mb-5 flex items-center justify-between rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700 dark:border-emerald-900/50 dark:bg-emerald-950/30 dark:text-emerald-300"
      >
        <span>{{ successMessage }}</span>

        <button type="button" @click="successMessage = ''">
          <FontAwesomeIcon :icon="faXmark" />
        </button>
      </div>

      <div
        v-if="error"
        class="mb-5 flex items-center justify-between rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-300"
      >
        <span>{{ error }}</span>

        <button type="button" @click="error = ''">
          <FontAwesomeIcon :icon="faXmark" />
        </button>
      </div>

      <!-- Filters -->
      <div
        class="mb-6 rounded-2xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900"
      >
        <div class="flex flex-col gap-3 lg:flex-row">
          <div class="relative flex-1">
            <FontAwesomeIcon
              :icon="faMagnifyingGlass"
              class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
            />

            <input
              v-model="searchQuery"
              type="search"
              placeholder="Search your knowledge..."
              class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-11 pr-4 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
            />
          </div>

          <div class="flex gap-3">
            <div class="relative">
              <FontAwesomeIcon
                :icon="faFilter"
                class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
              />

              <select
                v-model="selectedType"
                class="min-w-[190px] rounded-xl border border-slate-200 bg-slate-50 py-3 pl-11 pr-8 text-sm outline-none focus:border-indigo-500 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
              >
                <option value="all">All types</option>

                <option v-for="type in knowledgeTypes" :key="type.value" :value="type.value">
                  {{ type.label }}
                </option>
              </select>
            </div>

            <button
              type="button"
              class="rounded-xl border border-slate-200 px-4 text-slate-500 transition hover:bg-slate-100 dark:border-slate-700 dark:hover:bg-slate-800"
              title="Clear filters"
              @click="clearFilters"
            >
              <FontAwesomeIcon :icon="faRotate" />
            </button>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        <div
          v-for="item in 6"
          :key="item"
          class="h-64 animate-pulse rounded-2xl bg-slate-200 dark:bg-slate-800"
        />
      </div>

      <!-- Empty -->
      <KnowledgeEmptyState
        v-else-if="filteredKnowledge.length === 0 && !searchQuery && selectedType === 'all'"
        @create="openCreateForm"
      />

      <!-- No results -->
      <div
        v-else-if="filteredKnowledge.length === 0"
        class="rounded-2xl border border-slate-200 bg-white p-12 text-center dark:border-slate-800 dark:bg-slate-900"
      >
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white">No knowledge found</h3>

        <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">
          Try changing your search or filters.
        </p>
      </div>

      <!-- Knowledge Grid -->
      <div v-else class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        <KnowledgeCard
          v-for="knowledge in filteredKnowledge"
          :key="knowledge.id"
          :knowledge="knowledge"
          @edit="openEditForm"
          @archive="archiveKnowledge"
        />
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <div
        v-if="showForm"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 p-4 backdrop-blur-sm"
        @click.self="closeForm"
      >
        <div
          class="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-2xl bg-white shadow-2xl dark:bg-slate-900"
        >
          <div
            class="sticky top-0 z-10 flex items-center justify-between border-b border-slate-100 bg-white px-6 py-5 dark:border-slate-800 dark:bg-slate-900"
          >
            <div>
              <h2 class="text-lg font-bold text-slate-900 dark:text-white">
                {{ editingKnowledge ? 'Edit knowledge' : 'Create knowledge' }}
              </h2>

              <p class="mt-1 text-xs text-slate-400">
                Store information that So_Iam_OS can understand later.
              </p>
            </div>

            <button
              type="button"
              class="rounded-lg p-2 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
              @click="closeForm"
            >
              <FontAwesomeIcon :icon="faXmark" />
            </button>
          </div>

          <div class="p-6">
            <KnowledgeForm
              :model-value="editingKnowledge"
              :loading="saving"
              @submit="saveKnowledge"
              @cancel="closeForm"
            />
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>
