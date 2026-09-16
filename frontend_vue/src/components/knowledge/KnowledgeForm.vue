<script setup>
import { reactive, ref, watch, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: null,
  },

  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['submit', 'cancel'])

// ============================================================
// Form
// ============================================================

const form = reactive({
  title: '',
  description: '',
  content: '',
  knowledge_type: 'note',
  source_url: '',
  source_name: '',
  tags: [],
  visibility: 'private',
})

// ============================================================
// Tags
// ============================================================

const tagsInput = ref('')

// ============================================================
// Files
// ============================================================

const selectedFiles = ref([])

const fileInput = ref(null)

const isDragging = ref(false)

// File types supported by KnowledgeFile backend
const acceptedFileTypes = [
  '.pdf',
  '.doc',
  '.docx',
  '.xls',
  '.xlsx',
  '.ppt',
  '.pptx',
  '.md',
  '.txt',
  '.jpg',
  '.jpeg',
  '.png',
  '.gif',
  '.webp',
  '.svg',
  '.mp3',
  '.wav',
  '.ogg',
  '.mp4',
  '.webm',
  '.mov',
  '.py',
  '.js',
  '.ts',
  '.vue',
  '.html',
  '.css',
  '.scss',
  '.json',
  '.xml',
  '.yaml',
  '.yml',
  '.sql',
  '.sh',
  '.bat',
]

const acceptedFileTypesString = acceptedFileTypes.join(',')

// ============================================================
// Knowledge Types
// ============================================================

const knowledgeTypes = [
  {
    value: 'note',
    label: 'Note',
  },
  {
    value: 'document',
    label: 'Document',
  },
  {
    value: 'article',
    label: 'Article',
  },
  {
    value: 'documentation',
    label: 'Documentation',
  },
  {
    value: 'idea',
    label: 'Idea',
  },
  {
    value: 'project',
    label: 'Project',
  },
  {
    value: 'learning',
    label: 'Learning',
  },
  {
    value: 'reference',
    label: 'Reference',
  },
  {
    value: 'other',
    label: 'Other',
  },
]

// ============================================================
// Existing files
// ============================================================

const existingFiles = computed(() => {
  if (!props.modelValue?.files) {
    return []
  }

  return Array.isArray(props.modelValue.files) ? props.modelValue.files : []
})

// ============================================================
// Form Reset
// ============================================================

const resetForm = () => {
  form.title = ''
  form.description = ''
  form.content = ''
  form.knowledge_type = 'note'
  form.source_url = ''
  form.source_name = ''
  form.tags = []
  form.visibility = 'private'

  tagsInput.value = ''

  selectedFiles.value = []

  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// ============================================================
// Fill Form
// ============================================================

const fillForm = (knowledge) => {
  form.title = knowledge?.title || ''
  form.description = knowledge?.description || ''
  form.content = knowledge?.content || ''

  form.knowledge_type = knowledge?.knowledge_type || 'note'

  form.source_url = knowledge?.source_url || ''

  form.source_name = knowledge?.source_name || ''

  form.tags = Array.isArray(knowledge?.tags) ? [...knowledge.tags] : []

  form.visibility = knowledge?.visibility || 'private'

  tagsInput.value = form.tags.join(', ')

  // New files selected for this form session
  selectedFiles.value = []
}

// ============================================================
// Watch Edit/Create
// ============================================================

watch(
  () => props.modelValue,
  (value) => {
    if (value) {
      fillForm(value)
    } else {
      resetForm()
    }
  },
  {
    immediate: true,
  },
)

// ============================================================
// Open File Picker
// ============================================================

const openFilePicker = () => {
  fileInput.value?.click()
}

// ============================================================
// File Validation
// ============================================================

const isValidFile = (file) => {
  const extension = `.${file.name.split('.').pop()?.toLowerCase()}`

  return acceptedFileTypes.includes(extension)
}

// ============================================================
// Add Files
// ============================================================

const addFiles = (files) => {
  if (!files) {
    return
  }

  const incomingFiles = Array.from(files)

  incomingFiles.forEach((file) => {
    // Ignore unsupported files
    if (!isValidFile(file)) {
      return
    }

    // Prevent duplicate files
    const alreadyExists = selectedFiles.value.some(
      (existingFile) =>
        existingFile.name === file.name &&
        existingFile.size === file.size &&
        existingFile.lastModified === file.lastModified,
    )

    if (alreadyExists) {
      return
    }

    selectedFiles.value.push(file)
  })
}

// ============================================================
// File Input
// ============================================================

const handleFileChange = (event) => {
  addFiles(event.target.files)

  // Allow selecting the same file again later
  event.target.value = ''
}

// ============================================================
// Drag & Drop
// ============================================================

const handleDragOver = (event) => {
  event.preventDefault()

  isDragging.value = true
}

const handleDragLeave = (event) => {
  event.preventDefault()

  isDragging.value = false
}

const handleDrop = (event) => {
  event.preventDefault()

  isDragging.value = false

  addFiles(event.dataTransfer?.files)
}

// ============================================================
// Remove Selected File
// ============================================================

const removeSelectedFile = (index) => {
  selectedFiles.value.splice(index, 1)
}

// ============================================================
// File Size
// ============================================================

const formatFileSize = (size) => {
  if (!size) {
    return '0 B'
  }

  const units = ['B', 'KB', 'MB', 'GB']

  const unitIndex = Math.floor(Math.log(size) / Math.log(1024))

  const safeIndex = Math.min(unitIndex, units.length - 1)

  const value = size / Math.pow(1024, safeIndex)

  return `${value.toFixed(safeIndex === 0 ? 0 : 1)} ${units[safeIndex]}`
}

// ============================================================
// File Type Icon
// ============================================================

const getFileIcon = (file) => {
  const extension = file.name.split('.').pop()?.toLowerCase()

  if (extension === 'pdf') {
    return 'fa-solid fa-file-pdf'
  }

  if (['doc', 'docx'].includes(extension)) {
    return 'fa-solid fa-file-word'
  }

  if (['xls', 'xlsx'].includes(extension)) {
    return 'fa-solid fa-file-excel'
  }

  if (['ppt', 'pptx'].includes(extension)) {
    return 'fa-solid fa-file-powerpoint'
  }

  if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(extension)) {
    return 'fa-solid fa-file-image'
  }

  if (['mp3', 'wav', 'ogg'].includes(extension)) {
    return 'fa-solid fa-file-audio'
  }

  if (['mp4', 'webm', 'mov'].includes(extension)) {
    return 'fa-solid fa-file-video'
  }

  if (
    [
      'py',
      'js',
      'ts',
      'vue',
      'html',
      'css',
      'scss',
      'json',
      'xml',
      'yaml',
      'yml',
      'sql',
      'sh',
      'bat',
    ].includes(extension)
  ) {
    return 'fa-solid fa-file-code'
  }

  if (extension === 'md') {
    return 'fa-brands fa-markdown'
  }

  return 'fa-solid fa-file'
}

// ============================================================
// Submit
// ============================================================

const submit = () => {
  const tags = tagsInput.value
    .split(',')
    .map((tag) => tag.trim())
    .filter(Boolean)

  emit('submit', {
    title: form.title.trim(),
    description: form.description.trim(),
    content: form.content.trim(),
    knowledge_type: form.knowledge_type,
    source_url: form.source_url.trim(),
    source_name: form.source_name.trim(),
    tags,
    visibility: form.visibility,

    // New files
    files: [...selectedFiles.value],
  })
}
</script>

<template>
  <form class="space-y-5" @submit.prevent="submit">
    <!-- ===================================================== -->
    <!-- Title -->
    <!-- ===================================================== -->

    <div>
      <label class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-200">
        Title
      </label>

      <input
        v-model="form.title"
        type="text"
        required
        placeholder="e.g. Django Signals"
        class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
      />
    </div>

    <!-- ===================================================== -->
    <!-- Type -->
    <!-- ===================================================== -->

    <div>
      <label class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-200">
        Knowledge type
      </label>

      <select
        v-model="form.knowledge_type"
        class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
      >
        <option v-for="type in knowledgeTypes" :key="type.value" :value="type.value">
          {{ type.label }}
        </option>
      </select>
    </div>

    <!-- ===================================================== -->
    <!-- Description -->
    <!-- ===================================================== -->

    <div>
      <label class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-200">
        Description
      </label>

      <textarea
        v-model="form.description"
        rows="3"
        placeholder="Short description..."
        class="w-full resize-none rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
      />
    </div>

    <!-- ===================================================== -->
    <!-- Content -->
    <!-- ===================================================== -->

    <div>
      <label class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-200">
        Content
      </label>

      <textarea
        v-model="form.content"
        rows="8"
        placeholder="Write your knowledge here..."
        class="w-full resize-y rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm leading-6 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
      />
    </div>

    <!-- ===================================================== -->
    <!-- Files -->
    <!-- ===================================================== -->

    <div>
      <div class="mb-2 flex items-center justify-between">
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-200"> Files </label>

        <span v-if="selectedFiles.length" class="text-xs text-slate-400">
          {{ selectedFiles.length }} selected
        </span>
      </div>

      <!-- Hidden input -->

      <input
        ref="fileInput"
        type="file"
        multiple
        :accept="acceptedFileTypesString"
        class="hidden"
        @change="handleFileChange"
      />

      <!-- Drop Zone -->

      <div
        class="rounded-2xl border-2 border-dashed p-6 text-center transition"
        :class="
          isDragging
            ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-950/30'
            : 'border-slate-200 bg-slate-50 hover:border-indigo-400 dark:border-slate-700 dark:bg-slate-900/50'
        "
        @dragover="handleDragOver"
        @dragleave="handleDragLeave"
        @drop="handleDrop"
      >
        <div
          class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-100 text-indigo-600 dark:bg-indigo-950 dark:text-indigo-400"
        >
          <i class="fa-solid fa-cloud-arrow-up text-xl"></i>
        </div>

        <p class="text-sm font-medium text-slate-700 dark:text-slate-200">Drag & drop files here</p>

        <p class="mt-1 text-xs text-slate-400">or</p>

        <button
          type="button"
          class="mt-3 rounded-xl bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-indigo-700"
          @click="openFilePicker"
        >
          <i class="fa-solid fa-folder-open mr-2"></i>

          Choose files
        </button>

        <p class="mt-3 text-xs leading-5 text-slate-400">
          PDF, Word, Excel, PowerPoint, Markdown, Text, Images, Audio, Video and Code files.
        </p>
      </div>

      <!-- Selected Files -->

      <div v-if="selectedFiles.length" class="mt-4 space-y-2">
        <div
          v-for="(file, index) in selectedFiles"
          :key="`${file.name}-${file.lastModified}-${index}`"
          class="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 dark:border-slate-700 dark:bg-slate-950"
        >
          <!-- Icon -->

          <div
            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300"
          >
            <i :class="getFileIcon(file)"></i>
          </div>

          <!-- Info -->

          <div class="min-w-0 flex-1">
            <p
              class="truncate text-sm font-medium text-slate-700 dark:text-slate-200"
              :title="file.name"
            >
              {{ file.name }}
            </p>

            <p class="mt-0.5 text-xs text-slate-400">
              {{ formatFileSize(file.size) }}
            </p>
          </div>

          <!-- Remove -->

          <button
            type="button"
            class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-slate-400 transition hover:bg-red-50 hover:text-red-500 dark:hover:bg-red-950/30"
            title="Remove file"
            @click="removeSelectedFile(index)"
          >
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>

      <!-- Existing Files -->

      <div v-if="existingFiles.length" class="mt-4">
        <p class="mb-2 text-xs font-medium uppercase tracking-wide text-slate-400">
          Existing files
        </p>

        <div class="space-y-2">
          <a
            v-for="file in existingFiles"
            :key="file.id"
            :href="file.file_url || file.file"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 transition hover:border-indigo-300 dark:border-slate-700 dark:bg-slate-950"
          >
            <div
              class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300"
            >
              <i class="fa-solid fa-file"></i>
            </div>

            <div class="min-w-0 flex-1">
              <p class="truncate text-sm font-medium text-slate-700 dark:text-slate-200">
                {{ file.original_name }}
              </p>

              <p class="mt-0.5 text-xs text-slate-400">
                {{ formatFileSize(file.file_size) }}
              </p>
            </div>

            <i class="fa-solid fa-arrow-up-right-from-square text-xs text-slate-400"></i>
          </a>
        </div>
      </div>
    </div>

    <!-- ===================================================== -->
    <!-- Tags -->
    <!-- ===================================================== -->

    <div>
      <label class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-200">
        Tags
      </label>

      <input
        v-model="tagsInput"
        type="text"
        placeholder="django, python, backend"
        class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
      />

      <p class="mt-1 text-xs text-slate-400">Separate tags with commas.</p>
    </div>

    <!-- ===================================================== -->
    <!-- Source -->
    <!-- ===================================================== -->

    <div class="grid gap-4 md:grid-cols-2">
      <div>
        <label class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-200">
          Source name
        </label>

        <input
          v-model="form.source_name"
          type="text"
          placeholder="Django Documentation"
          class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
        />
      </div>

      <div>
        <label class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-200">
          Source URL
        </label>

        <input
          v-model="form.source_url"
          type="url"
          placeholder="https://..."
          class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
        />
      </div>
    </div>

    <!-- ===================================================== -->
    <!-- Visibility -->
    <!-- ===================================================== -->

    <div>
      <label class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-200">
        Visibility
      </label>

      <select
        v-model="form.visibility"
        class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
      >
        <option value="private">Private</option>

        <option value="shared">Shared</option>
      </select>
    </div>

    <!-- ===================================================== -->
    <!-- Actions -->
    <!-- ===================================================== -->

    <div class="flex justify-end gap-3 border-t border-slate-100 pt-5 dark:border-slate-800">
      <button
        type="button"
        class="rounded-xl px-5 py-2.5 text-sm font-medium text-slate-600 transition hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
        @click="emit('cancel')"
      >
        Cancel
      </button>

      <button
        type="submit"
        :disabled="loading"
        class="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        <i v-if="loading" class="fa-solid fa-spinner fa-spin mr-2"></i>

        {{ loading ? 'Saving...' : modelValue ? 'Update knowledge' : 'Create knowledge' }}
      </button>
    </div>
  </form>
</template>
