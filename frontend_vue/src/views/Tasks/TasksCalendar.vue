<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import {
  listTasks,
  createTask,
  completeTask,
  postponeTask,
  generateTodayTasks,
} from '@/services/tasks'

// =====================================================
// State
// =====================================================
const cursor = ref(new Date())
const view = ref('week')

const tasks = ref([])
const loading = ref(false)
const generating = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const busyTaskIds = ref(new Set())
const requestId = ref(0)

let messageTimer = null

// =====================================================
// Date utilities
// استخدم التاريخ المحلي لتجنب انزياح اليوم بسبب UTC
// =====================================================
const pad = (value) => String(value).padStart(2, '0')

const formatDateKey = (date) => {
  const d = new Date(date)

  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

const parseDateKey = (value) => {
  if (!value) return null

  const match = String(value).match(/^(\d{4})-(\d{2})-(\d{2})$/)

  if (!match) return null

  const date = new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3]))

  return formatDateKey(date) === value ? date : null
}

const startOfWeek = (date) => {
  const d = new Date(date)
  d.setHours(0, 0, 0, 0)
  d.setDate(d.getDate() - d.getDay())
  return d
}

const monthNames = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
]

const currentMonthYear = computed(() => {
  return `${monthNames[cursor.value.getMonth()]} ${cursor.value.getFullYear()}`
})

const rangeStart = computed(() => {
  if (view.value === 'month') {
    return new Date(cursor.value.getFullYear(), cursor.value.getMonth(), 1)
  }

  return startOfWeek(cursor.value)
})

const rangeEnd = computed(() => {
  if (view.value === 'month') {
    return new Date(cursor.value.getFullYear(), cursor.value.getMonth() + 1, 0)
  }

  const end = new Date(rangeStart.value)
  end.setDate(end.getDate() + 6)
  return end
})

const days = computed(() => {
  const result = []
  const base = new Date(rangeStart.value)
  const count = view.value === 'month' ? rangeEnd.value.getDate() : 7

  for (let i = 0; i < count; i += 1) {
    const day = new Date(base)
    day.setDate(base.getDate() + i)
    result.push(day)
  }

  return result
})

const todayKey = computed(() => formatDateKey(new Date()))

// =====================================================
// Response normalization
// يدعم المصفوفة المباشرة وشكل DRF Pagination
// =====================================================
const normalizeTaskList = (response) => {
  let data = response

  // يدعم Axios response إذا كانت الخدمة تعيد الاستجابة كاملة
  if (data && !Array.isArray(data) && data.data !== undefined) {
    data = data.data
  }

  // Django REST Framework pagination
  if (data && !Array.isArray(data) && Array.isArray(data.results)) {
    return data.results
  }

  // بعض APIs تعيد النتائج داخل items
  if (data && !Array.isArray(data) && Array.isArray(data.items)) {
    return data.items
  }

  return Array.isArray(data) ? data : []
}

const getErrorMessage = (error, fallback) => {
  const data = error?.response?.data

  if (typeof data?.detail === 'string') {
    return data.detail
  }

  if (typeof data?.message === 'string') {
    return data.message
  }

  if (data && typeof data === 'object') {
    const firstKey = Object.keys(data)[0]
    const firstValue = firstKey ? data[firstKey] : null

    if (typeof firstValue === 'string') {
      return firstValue
    }

    if (Array.isArray(firstValue) && firstValue.length) {
      return String(firstValue[0])
    }
  }

  return error?.message || fallback
}

const showSuccess = (message) => {
  successMessage.value = message
  errorMessage.value = ''

  if (messageTimer) clearTimeout(messageTimer)

  messageTimer = setTimeout(() => {
    successMessage.value = ''
  }, 3500)
}

const showError = (error, fallback) => {
  errorMessage.value = typeof error === 'string' ? error : getErrorMessage(error, fallback)

  successMessage.value = ''
}

// =====================================================
// Load tasks
// ملاحظة: يفترض أن views.py يدعم date_from/date_to
// =====================================================
const loadTasks = async () => {
  const currentRequest = ++requestId.value
  loading.value = true
  errorMessage.value = ''

  try {
    const params = {
      date_from: formatDateKey(rangeStart.value),
      date_to: formatDateKey(rangeEnd.value),
    }

    const response = await listTasks(params)

    // تجاهل أي استجابة قديمة وصلت بعد طلب أحدث
    if (currentRequest !== requestId.value) return

    const result = normalizeTaskList(response)

    // حماية إضافية في حالة إرجاع الخدمة بيانات غير متوقعة
    tasks.value = result.filter((task) => task && task.id !== undefined && task.id !== null)
  } catch (error) {
    if (currentRequest === requestId.value) {
      showError(error, 'Unable to load calendar tasks.')
    }
  } finally {
    if (currentRequest === requestId.value) {
      loading.value = false
    }
  }
}

// =====================================================
// Navigation
// =====================================================
const prevPeriod = () => {
  const date = new Date(cursor.value)

  if (view.value === 'month') {
    // تثبيت اليوم الأول لتجنب تجاوز الشهر عند يوم 29–31
    date.setDate(1)
    date.setMonth(date.getMonth() - 1)
  } else {
    date.setDate(date.getDate() - 7)
  }

  cursor.value = date
}

const nextPeriod = () => {
  const date = new Date(cursor.value)

  if (view.value === 'month') {
    date.setDate(1)
    date.setMonth(date.getMonth() + 1)
  } else {
    date.setDate(date.getDate() + 7)
  }

  cursor.value = date
}

const goToToday = () => {
  cursor.value = new Date()
}

// تحميل تلقائي عند تغيير الشهر أو الأسبوع أو نمط العرض
watch(
  [rangeStart, rangeEnd, view],
  () => {
    loadTasks()
  },
  { deep: true },
)

// =====================================================
// Task helpers
// =====================================================
const getTaskDate = (task) => {
  const value = task?.scheduled_date

  if (!value) return ''

  // يدعم YYYY-MM-DD وكذلك التاريخ المصحوب بوقت
  return String(value).slice(0, 10)
}

const getTasksByDay = (date) => {
  const key = formatDateKey(date)

  return tasks.value
    .filter((task) => getTaskDate(task) === key)
    .sort((a, b) => {
      const orderDifference = Number(a.sort_order ?? 0) - Number(b.sort_order ?? 0)

      if (orderDifference !== 0) return orderDifference

      const startA = a.scheduled_start || ''
      const startB = b.scheduled_start || ''

      return String(startA).localeCompare(String(startB))
    })
}

const isCompleted = (task) => task?.status === 'completed'

const isBusy = (task) => busyTaskIds.value.has(task.id)

const setTaskBusy = (taskId, busy) => {
  const next = new Set(busyTaskIds.value)

  if (busy) {
    next.add(taskId)
  } else {
    next.delete(taskId)
  }

  busyTaskIds.value = next
}

const updateTaskInList = (updatedTask) => {
  if (!updatedTask || updatedTask.id == null) return

  const index = tasks.value.findIndex((task) => String(task.id) === String(updatedTask.id))

  if (index === -1) {
    tasks.value = [...tasks.value, updatedTask]
  } else {
    const next = [...tasks.value]
    next[index] = { ...next[index], ...updatedTask }
    tasks.value = next
  }
}

// =====================================================
// Status styling
// =====================================================
const getStatusBadgeClass = (status) => {
  switch (status) {
    case 'completed':
      return 'bg-green-500/10 text-green-700 border-green-500/30 dark:bg-green-500/20 dark:text-green-300'

    case 'in_progress':
      return 'bg-blue-500/10 text-blue-700 border-blue-500/30 dark:bg-blue-500/20 dark:text-blue-300'

    case 'postponed':
      return 'bg-amber-500/10 text-amber-700 border-amber-500/30 dark:bg-amber-500/20 dark:text-amber-300'

    case 'cancelled':
      return 'bg-red-500/10 text-red-700 border-red-500/30 dark:bg-red-500/20 dark:text-red-300'

    case 'pending':
    default:
      return 'bg-surface-500/10 text-surface-700 border-surface-500/20 dark:bg-surface-800 dark:text-surface-300'
  }
}

const getStatusLabel = (task) => {
  return task?.status_display || task?.status || 'Unknown'
}

// =====================================================
// Create task
// =====================================================
const handleAddQuickTask = async (date) => {
  const title = window.prompt('Enter task title:')

  if (title === null) return

  const cleanTitle = title.trim()

  if (!cleanTitle) {
    showError('Task title is required.')
    return
  }

  try {
    const payload = {
      title: cleanTitle,
      scheduled_date: formatDateKey(date),
      estimated_minutes: 30,
      priority: 'medium',
      description: '',
    }

    const response = await createTask(payload)
    const createdTask = response?.data !== undefined ? response.data : response

    if (createdTask?.id != null) {
      updateTaskInList(createdTask)
    } else {
      await loadTasks()
    }

    showSuccess('Task created successfully.')
  } catch (error) {
    showError(error, 'Unable to create task.')
  }
}

// =====================================================
// Generate daily tasks
// =====================================================
const handleGenerateTasks = async () => {
  if (generating.value) return

  generating.value = true
  errorMessage.value = ''

  try {
    const response = await generateTodayTasks({
      count: 3,
      async: false,
    })

    // بعض إعدادات DRF تعيد البيانات داخل data
    const result = normalizeTaskList(response)

    if (result.length) {
      const merged = new Map(tasks.value.map((task) => [String(task.id), task]))

      result.forEach((task) => {
        if (task?.id != null) {
          merged.set(String(task.id), task)
        }
      })

      tasks.value = [...merged.values()]
    }

    await loadTasks()
    showSuccess('Task generation request completed.')
  } catch (error) {
    showError(error, 'Unable to generate tasks.')
  } finally {
    generating.value = false
  }
}

// =====================================================
// Complete task
// =====================================================
const handleComplete = async (task) => {
  if (!task?.id || isCompleted(task) || isBusy(task)) return

  setTaskBusy(task.id, true)

  try {
    const actualMinutes =
      Number.isFinite(Number(task.actual_minutes)) && Number(task.actual_minutes) >= 0
        ? Number(task.actual_minutes)
        : Number(task.estimated_minutes) || 30

    const response = await completeTask(task.id, actualMinutes)
    const updatedTask = response?.data !== undefined ? response.data : response

    if (updatedTask && typeof updatedTask === 'object') {
      updateTaskInList(updatedTask)
    } else {
      await loadTasks()
    }

    showSuccess('Task completed successfully.')
  } catch (error) {
    showError(error, 'Unable to complete task.')
  } finally {
    setTaskBusy(task.id, false)
  }
}

// =====================================================
// Postpone task
// =====================================================
const handlePostpone = async (task) => {
  if (!task?.id || isBusy(task)) return

  const newDate = window.prompt(
    'Postpone until (YYYY-MM-DD):',
    task.scheduled_date || todayKey.value,
  )

  if (newDate === null) return

  const cleanDate = newDate.trim()
  const parsedDate = parseDateKey(cleanDate)

  if (!parsedDate) {
    showError('Enter a valid date in YYYY-MM-DD format.')
    return
  }

  // هذا الفحص يمنع التاريخ غير الصحيح فقط؛
  // قواعد السماح بالتأجيل تظل مسؤولية الـ Backend.
  setTaskBusy(task.id, true)

  try {
    const response = await postponeTask(task.id, cleanDate)
    const updatedTask = response?.data !== undefined ? response.data : response

    if (updatedTask && typeof updatedTask === 'object') {
      updateTaskInList(updatedTask)
    }

    // قد تنتقل المهمة خارج النطاق الحالي
    await loadTasks()

    showSuccess('Task postponed successfully.')
  } catch (error) {
    showError(error, 'Unable to postpone task.')
  } finally {
    setTaskBusy(task.id, false)
  }
}

onMounted(() => {
  loadTasks()
})
</script>

<template>
  <div class="h-full flex flex-col overflow-hidden text-sm bg-white dark:bg-surface-900">
    <!-- Header -->
    <header
      class="flex flex-wrap items-center justify-between px-4 py-3 border-b border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-950 shrink-0 gap-3"
    >
      <div class="flex flex-wrap items-center gap-3">
        <div class="flex items-center gap-2">
          <div
            class="w-9 h-9 relative flex items-center justify-center bg-primary rounded-lg text-white font-bold"
          >
            <i class="pi pi-calendar text-lg" aria-hidden="true"></i>
          </div>

          <span class="text-xl font-normal text-surface-800 dark:text-surface-100">
            Tasks Calendar
          </span>
        </div>

        <prime_button
          label="Today"
          variant="outlined"
          size="small"
          :disabled="loading"
          @click="goToToday"
        />

        <div class="flex items-center gap-1">
          <prime_button
            icon="pi pi-chevron-left"
            text
            rounded
            severity="secondary"
            aria-label="Previous period"
            :disabled="loading"
            @click="prevPeriod"
          />

          <prime_button
            icon="pi pi-chevron-right"
            text
            rounded
            severity="secondary"
            aria-label="Next period"
            :disabled="loading"
            @click="nextPeriod"
          />
        </div>

        <h1 class="text-xl font-normal text-surface-800 dark:text-surface-100">
          {{ currentMonthYear }}
        </h1>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <prime_button
          label="Generate AI Tasks"
          icon="pi pi-sparkles"
          severity="help"
          size="small"
          :loading="generating"
          :disabled="loading || generating"
          @click="handleGenerateTasks"
        />

        <prime_select
          v-model="view"
          :options="[
            { label: 'Week', value: 'week' },
            { label: 'Month', value: 'month' },
          ]"
          optionLabel="label"
          optionValue="value"
          class="w-32"
          :disabled="loading"
        />
      </div>
    </header>

    <!-- Feedback -->
    <div
      v-if="errorMessage"
      class="mx-3 mt-3 p-3 rounded-lg border border-red-300 bg-red-50 text-red-700 dark:bg-red-950/30 dark:text-red-300 dark:border-red-800 flex items-start justify-between gap-3"
      role="alert"
    >
      <span>{{ errorMessage }}</span>

      <prime_button
        icon="pi pi-times"
        text
        rounded
        severity="danger"
        size="small"
        aria-label="Dismiss error"
        @click="errorMessage = ''"
      />
    </div>

    <div
      v-if="successMessage"
      class="mx-3 mt-3 p-3 rounded-lg border border-green-300 bg-green-50 text-green-700 dark:bg-green-950/30 dark:text-green-300 dark:border-green-800"
      role="status"
    >
      {{ successMessage }}
    </div>

    <!-- Calendar -->
    <div class="flex flex-1 overflow-hidden relative">
      <main class="flex-1 flex flex-col h-full bg-white dark:bg-surface-900 overflow-hidden">
        <!-- Days header -->
        <div
          class="grid border-b border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-800 select-none"
          :style="{ gridTemplateColumns: `repeat(${days.length}, minmax(0,1fr))` }"
        >
          <div
            v-for="day in days"
            :key="formatDateKey(day)"
            class="text-center py-2 border-r border-surface-200 dark:border-surface-700 last:border-r-0"
          >
            <span class="block text-[11px] font-medium text-surface-500 uppercase">
              {{ day.toLocaleDateString(undefined, { weekday: 'short' }) }}
            </span>

            <span
              class="inline-flex items-center justify-center text-lg font-normal leading-none mt-1 w-8 h-8 rounded-full"
              :class="
                formatDateKey(day) === todayKey
                  ? 'bg-primary text-primary-contrast font-bold shadow-sm'
                  : 'text-surface-800 dark:text-surface-100'
              "
            >
              {{ day.getDate() }}
            </span>
          </div>
        </div>

        <!-- Days grid -->
        <div
          class="flex-1 overflow-auto grid"
          :style="{ gridTemplateColumns: `repeat(${days.length}, minmax(0,1fr))` }"
        >
          <div
            v-for="day in days"
            :key="formatDateKey(day)"
            class="min-w-0 min-h-[500px] border-r border-b border-surface-200 dark:border-surface-700 last:border-r-0 p-2 hover:bg-surface-50 dark:hover:bg-surface-800/50 transition-colors flex flex-col"
            @dblclick="handleAddQuickTask(day)"
          >
            <div class="space-y-2.5 flex-1">
              <div
                v-for="task in getTasksByDay(day)"
                :key="task.id"
                class="p-3 rounded-xl border text-xs shadow-sm transition-all flex flex-col justify-between gap-2"
                :class="getStatusBadgeClass(task.status)"
              >
                <div>
                  <div class="font-bold flex items-start justify-between gap-2">
                    <span class="break-words">{{ task.title }}</span>

                    <span
                      v-if="task.overdue"
                      class="shrink-0 text-[9px] bg-red-600 text-white px-1.5 py-0.5 rounded-full"
                    >
                      Overdue
                    </span>
                  </div>

                  <p v-if="task.description" class="text-[11px] opacity-80 mt-1 line-clamp-2">
                    {{ task.description }}
                  </p>

                  <div class="mt-2 flex flex-wrap items-center gap-1.5">
                    <span class="text-[10px] px-1.5 py-0.5 rounded border border-current/20">
                      {{ getStatusLabel(task) }}
                    </span>

                    <span
                      v-if="task.priority_display || task.priority"
                      class="text-[10px] opacity-80"
                    >
                      {{ task.priority_display || task.priority }}
                    </span>
                  </div>
                </div>

                <div
                  class="flex items-center justify-between gap-2 pt-2 border-t border-current/10 text-[10px]"
                >
                  <span class="font-medium">
                    <i class="pi pi-clock mr-1" aria-hidden="true"></i>
                    {{ task.estimated_minutes ?? 0 }}m
                  </span>

                  <div class="flex items-center gap-1">
                    <prime_button
                      v-if="!isCompleted(task) && task.status !== 'cancelled'"
                      icon="pi pi-check"
                      severity="success"
                      text
                      rounded
                      size="small"
                      title="Complete Task"
                      aria-label="Complete task"
                      :loading="isBusy(task)"
                      :disabled="isBusy(task) || loading"
                      @click.stop="handleComplete(task)"
                    />

                    <prime_button
                      v-if="task.status !== 'cancelled'"
                      icon="pi pi-calendar-clock"
                      severity="warn"
                      text
                      rounded
                      size="small"
                      title="Postpone Task"
                      aria-label="Postpone task"
                      :loading="isBusy(task)"
                      :disabled="isBusy(task) || loading"
                      @click.stop="handlePostpone(task)"
                    />
                  </div>
                </div>
              </div>

              <div
                v-if="!loading && getTasksByDay(day).length === 0"
                class="text-center text-[10px] text-surface-400 py-3"
              >
                No tasks
              </div>
            </div>

            <button
              type="button"
              class="mt-2 w-full py-2 rounded-lg border border-dashed border-surface-300 dark:border-surface-600 text-surface-500 hover:text-primary hover:border-primary transition-colors"
              :aria-label="`Add task on ${formatDateKey(day)}`"
              title="Add task"
              @click.stop="handleAddQuickTask(day)"
            >
              <i class="pi pi-plus" aria-hidden="true"></i>
              <span class="ml-1 text-xs">Add task</span>
            </button>
          </div>
        </div>

        <!-- Loading -->
        <div
          v-if="loading"
          class="p-4 text-center text-sm text-surface-500 flex items-center justify-center gap-2"
          role="status"
        >
          <prime_progress_spinner style="width: 20px; height: 20px" strokeWidth="4" />
          Loading calendar tasks...
        </div>

        <!-- Footer -->
        <div
          class="px-4 py-2 border-t border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-950 text-xs text-surface-500 flex flex-wrap justify-between items-center gap-2"
        >
          <span> Double-click a day or select Add task to create a task. </span>

          <span class="flex flex-wrap items-center gap-2">
            <span class="inline-block w-2 h-2 rounded-full bg-green-500"></span>
            Completed

            <span class="inline-block w-2 h-2 rounded-full bg-blue-500"></span>
            In Progress

            <span class="inline-block w-2 h-2 rounded-full bg-amber-500"></span>
            Postponed
          </span>
        </div>
      </main>
    </div>
  </div>
</template>
