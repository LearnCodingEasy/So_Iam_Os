<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { RouterLink } from 'vue-router'
import { dashboardService } from '@/services/dashboard'

import Button from 'primevue/button'
import Tag from 'primevue/tag'
import ProgressBar from 'primevue/progressbar'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

/*
|-----------------------------------------------------
| SIDEBAR STATE & NAVIGATION
|-----------------------------------------------------
*/
const sidebarOpen = ref(true)

// eslint-disable-next-line no-unused-vars
const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

/*
|-----------------------------------------------------
| DASHBOARD STATE (REAL DATA API)
|-----------------------------------------------------
*/
const dashboard = ref(null)
const loading = ref(true)
const error = ref(null)

const loadDashboard = async () => {
  loading.value = true
  error.value = null

  try {
    const data = await dashboardService.get()
    console.log('Dashboard API response:', data)
    dashboard.value = data
  } catch (err) {
    console.error('Dashboard API error:', err)
    error.value =
      err?.response?.data?.detail ||
      err?.response?.data?.message ||
      err?.message ||
      'Unable to load dashboard data.'
  } finally {
    loading.value = false
  }
}

/*
|-----------------------------------------------------
| USER & COMPUTED METRICS
|-----------------------------------------------------
*/
const userName = computed(() => dashboard.value?.user?.name || 'User')

const userInitials = computed(() => {
  const name = userName.value.trim()
  if (!name) return 'U'
  const parts = name.split(/\s+/)
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
})

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour >= 5 && hour < 12) return 'Good Morning'
  if (hour >= 12 && hour < 17) return 'Good Afternoon'
  if (hour >= 17 && hour < 22) return 'Good Evening'
  return 'Good Night'
})

/*
|-----------------------------------------------------
| CLOCK TIMER
|-----------------------------------------------------
*/
const currentDate = ref(new Date())
let clockTimer = null

const updateClock = () => {
  currentDate.value = new Date()
}

const formattedDate = computed(() => {
  return currentDate.value.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
})

const formattedTime = computed(() => {
  return currentDate.value.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  })
})

/*
|-----------------------------------------------------
| REAL STATS DATA FROM API
|-----------------------------------------------------
*/
const statsList = computed(() => {
  const data = dashboard.value?.stats || {}
  return [
    {
      title: 'Cumulative Projects',
      value: data.projects?.total ?? 0,
      activeText: `${data.projects?.active ?? 0} active`,
      completedText: `${data.projects?.completed ?? 0} completed`,
      icon: 'pi pi-folder',
      route: '/projects',
      tagValue: 'Active',
      tagSeverity: 'success',
    },
    {
      title: 'Task Velocity',
      value: data.tasks?.total ?? 0,
      activeText: `${data.tasks?.pending ?? 0} pending`,
      completedText: `${data.tasks?.completed ?? 0} completed`,
      icon: 'pi pi-check-circle',
      route: '/tasks',
      tagValue: 'In Flight',
      tagSeverity: 'info',
    },
    {
      title: 'Active Objectives',
      value: data.goals?.total ?? 0,
      activeText: `${data.goals?.in_progress ?? 0} in progress`,
      completedText: `${data.goals?.completed ?? 0} completed`,
      icon: 'pi pi-target',
      route: '/goals',
      tagValue: 'Milestones',
      tagSeverity: 'warn',
    },
    {
      title: 'Knowledge Base',
      value: data.knowledge?.total ?? 0,
      activeText: `${data.knowledge?.files ?? 0} files indexed`,
      completedText: 'Ready',
      icon: 'pi pi-book',
      route: '/knowledge',
      tagValue: 'Synced',
      tagSeverity: 'success',
    },
  ]
})

/*
|-----------------------------------------------------
| REAL TASKS & KNOWLEDGE FROM API
|-----------------------------------------------------
*/
const tasks = computed(() => dashboard.value?.tasks || [])
const recentKnowledge = computed(() => dashboard.value?.recent?.knowledge || [])

// UI Controls State
const selectedTimeframe = ref('This Week')
const timeframes = ['Today', 'This Week', 'This Month', 'Custom']
const selectedChartView = ref('Weekly')
const chartViews = ['Daily', 'Weekly', 'Sprint']

const daysLabels = [
  { text: 'Mon 23', x: 75, active: false },
  { text: 'Tue 24', x: 180, active: false },
  { text: 'Wed 25 (Peak)', x: 290, active: true },
  { text: 'Thu 26', x: 400, active: false },
  { text: 'Fri 27', x: 510, active: false },
  { text: 'Sat 28', x: 620, active: false },
  { text: 'Sun 29', x: 720, active: false },
]

const learningTracks = ref([
  {
    title: 'RAG Pipelines & Vector Search',
    subtitle: 'AI Engineering • 14/18 modules',
    tag: 'High',
    tagSeverity: 'danger',
    progress: 78,
    target: 'Nov 15',
  },
  {
    title: 'Nuxt 3 SSR Cache & Edge Runtime',
    subtitle: 'Frontend Arch • 22/25 modules',
    tag: 'Active',
    tagSeverity: 'success',
    progress: 88,
    target: 'Nov 08',
  },
])

const habits = ref([
  { name: 'Deep Work (4h+)', status: ['✓', '✓', '★', '✓', '✓', '—', '—'] },
  { name: 'Code Kata & Refactor', status: ['✓', '✓', '✓', '✓', '✓', '✓', '—'] },
  { name: 'Cardio & Resistance', status: ['✓', '—', '✓', '—', '✓', '✓', '✓'] },
])

const telemetryLogs = ref([
  {
    timestamp: '14:18:22 UTC',
    component: 'Core Kernel::TaskEngine',
    context: 'System Dashboard synchronized successfully',
    score: '99.1% Flow',
    status: 'Optimal',
  },
  {
    timestamp: '13:45:00 UTC',
    component: 'BioSense::Biometrics',
    context: 'Session telemetry updated from database',
    score: 'Normal Baseline',
    status: 'Active',
  },
])

onMounted(() => {
  loadDashboard()
  clockTimer = window.setInterval(updateClock, 1000)
})

onBeforeUnmount(() => {
  if (clockTimer) {
    window.clearInterval(clockTimer)
    clockTimer = null
  }
})
</script>

<template>
  <div class="w-full min-h-screen px-6 py-6 antialiased font-sans dashboard-page">
    <div class="flex flex-col w-full gap-6 pb-8">
      <!-- ========= ERROR NOTIFICATION ========= -->
      <div
        v-if="error"
        class="p-4 rounded-xl border flex items-center justify-between error-banner"
      >
        <span><strong>Dashboard API Error:</strong> {{ error }}</span>
        <Button label="Try again" @click="loadDashboard" severity="danger" size="small" />
      </div>

      <!-- ======= TOP HEADER / ACTION BAR ======= -->
      <div
        class="flex flex-col xl:flex-row xl:items-center justify-between gap-4 p-6 rounded-xl shadow-sm border header-card"
      >
        <div class="flex flex-col gap-1 max-w-2xl">
          <div class="flex items-center gap-2 flex-wrap">
            <h1 class="text-2xl font-semibold tracking-tight">{{ greeting }}, {{ userName }} 👋</h1>
            <span
              class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full font-mono text-[11px] font-semibold system-badge"
            >
              <span class="w-2 h-2 rounded-full animate-pulse status-dot"></span>
              System Active • SO Iam OS v2.4
            </span>
          </div>
          <p class="text-sm">
            Your goals, projects, and active database telemetry synthesis in real-time.
          </p>
        </div>

        <!-- Controls & Actions -->
        <div class="flex flex-wrap items-center gap-3">
          <div class="flex items-center p-1 rounded-lg gap-1 border control-group">
            <button
              v-for="tf in timeframes"
              :key="tf"
              @click="selectedTimeframe = tf"
              :class="[
                'px-3 py-1 rounded-md text-xs transition-all font-medium timeframe-btn',
                selectedTimeframe === tf ? 'active' : '',
              ]"
            >
              {{ tf }}
            </button>
          </div>

          <div class="flex items-center gap-2">
            <Button
              label="Export Data"
              icon="pi pi-download"
              severity="secondary"
              outlined
              class="!text-xs !py-1.5 !px-3"
            />
            <RouterLink to="/ai">
              <Button
                label="Ask AI Assistant"
                icon="pi pi-sparkles"
                class="!text-xs !py-1.5 !px-3"
              />
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- ================= QUICK KPI TELEMETRY STRIP (REAL DB STATS) ================= -->
      <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <RouterLink
          v-for="stat in statsList"
          :key="stat.title"
          :to="stat.route"
          class="flex flex-col justify-between p-5 rounded-xl shadow-sm hover:shadow-md transition-shadow border group stat-card"
        >
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs uppercase tracking-wider font-semibold stat-title">{{
              stat.title
            }}</span>
            <div
              class="w-8 h-8 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform icon-wrapper"
            >
              <i :class="[stat.icon, 'text-base']"></i>
            </div>
          </div>
          <div class="flex items-baseline justify-between mt-1">
            <span class="text-3xl font-semibold tracking-tight font-mono stat-value">
              {{ loading ? '...' : stat.value }}
            </span>
            <Tag :value="stat.tagValue" :severity="stat.tagSeverity" class="!text-[11px] !py-0.5" />
          </div>
          <div class="mt-3 flex items-center justify-between font-mono text-[11px] stat-footer">
            <span>{{ stat.activeText }}</span>
            <span class="font-semibold secondary-text">{{ stat.completedText }}</span>
          </div>
        </RouterLink>
      </div>

      <!-- ================= BENTO SECTION 1: MOMENTUM CHART + LEARNING MATRIX ================= -->
      <div class="grid grid-cols-1 xl:grid-cols-12 gap-6 items-start">
        <!-- Bento Card 1: Productivity Momentum Chart (8 cols) -->
        <div class="xl:col-span-8 flex flex-col rounded-xl p-6 shadow-sm border bento-card">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
            <div class="flex flex-col gap-0.5">
              <div class="flex items-center gap-2">
                <h2 class="text-lg font-semibold">Productivity & Velocity Momentum</h2>
                <span
                  class="px-2 py-0.5 rounded font-mono text-[11px] font-semibold telemetry-badge"
                  >Telemetry V2</span
                >
              </div>
              <p class="text-xs">Focus Hours (Area) mapped against Task Delivery Velocity (Line)</p>
            </div>

            <div class="flex items-center gap-4 flex-wrap">
              <div class="flex items-center gap-3 font-mono text-xs">
                <div class="flex items-center gap-1.5">
                  <span class="w-3 h-3 rounded-sm legend-box focus-box"></span>
                  <span class="text-[11px]">Focus Hours</span>
                </div>
                <div class="flex items-center gap-1.5">
                  <span class="w-3 h-1 rounded-full legend-line velocity-line"></span>
                  <span class="text-[11px]">Task Velocity</span>
                </div>
              </div>
              <div class="flex items-center p-0.5 rounded-lg gap-0.5 border view-toggle">
                <button
                  v-for="v in chartViews"
                  :key="v"
                  @click="selectedChartView = v"
                  :class="[
                    'px-2 py-0.5 rounded text-[11px] font-medium transition-all view-btn',
                    selectedChartView === v ? 'active' : '',
                  ]"
                >
                  {{ v }}
                </button>
              </div>
            </div>
          </div>

          <!-- Interactive SVG Chart -->
          <div class="relative w-full h-72 sm:h-80 select-none">
            <svg
              class="w-full h-full overflow-visible chart-svg"
              viewBox="0 0 760 300"
              preserveAspectRatio="none"
            >
              <defs>
                <linearGradient id="focusGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" class="stop-focus-top" />
                  <stop offset="100%" class="stop-focus-bottom" />
                </linearGradient>
                <linearGradient id="velocityLineGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" class="stop-velocity-start" />
                  <stop offset="100%" class="stop-velocity-end" />
                </linearGradient>
              </defs>

              <line
                v-for="y in [40, 100, 160, 220]"
                :key="y"
                x1="40"
                :y1="y"
                x2="740"
                :y2="y"
                class="grid-line"
                stroke-dasharray="4 4"
                stroke-width="1"
              />
              <line x1="40" y1="270" x2="740" y2="270" class="baseline-line" stroke-width="1" />

              <path
                d="M75,270 L75,136 Q130,110 180,94 T290,64 T400,106 T510,73 T620,157 T720,175 L720,270 Z"
                fill="url(#focusGradient)"
              />
              <path
                d="M75,136 Q130,110 180,94 T290,64 T400,106 T510,73 T620,157 T720,175"
                fill="none"
                class="focus-path"
                stroke-width="2.5"
              />
              <path
                d="M75,160 C120,140 150,125 180,118 C230,108 260,60 290,52 C330,46 370,130 400,138 C435,145 480,85 510,78 C545,72 585,185 620,192 C660,198 690,202 720,204"
                fill="none"
                stroke="url(#velocityLineGrad)"
                stroke-width="2.75"
              />

              <circle
                cx="290"
                cy="52"
                r="5"
                class="chart-point point-secondary"
                stroke-width="2.5"
              />
              <circle cx="290" cy="64" r="5" class="chart-point point-primary" stroke-width="2.5" />

              <text
                v-for="(day, idx) in daysLabels"
                :key="idx"
                :x="day.x"
                y="290"
                font-family="monospace"
                font-size="11"
                text-anchor="middle"
                :font-weight="day.active ? 'bold' : 'normal'"
                class="chart-label"
              >
                {{ day.text }}
              </text>
            </svg>
          </div>
        </div>

        <!-- Bento Card 2: Learning Matrix Progress (4 cols) -->
        <div
          class="xl:col-span-4 flex flex-col justify-between rounded-xl p-6 shadow-sm border bento-card"
        >
          <div>
            <div class="flex items-center justify-between mb-4">
              <div class="flex flex-col">
                <h2 class="text-lg font-semibold">Learning Matrix</h2>
                <span class="text-xs muted-text">Active competencies Q4</span>
              </div>
              <RouterLink to="/learning">
                <Button
                  label="View All"
                  icon="pi pi-arrow-right"
                  iconPos="right"
                  text
                  class="!text-xs !p-0"
                />
              </RouterLink>
            </div>

            <div class="flex flex-col gap-3">
              <div
                v-for="track in learningTracks"
                :key="track.title"
                class="flex flex-col gap-1.5 p-3 rounded-lg track-item transition-colors"
              >
                <div class="flex items-start justify-between gap-2">
                  <div class="flex flex-col">
                    <span class="text-sm font-semibold">{{ track.title }}</span>
                    <span class="font-mono text-[11px] muted-text">{{ track.subtitle }}</span>
                  </div>
                  <Tag
                    :value="track.tag"
                    :severity="track.tagSeverity"
                    class="!text-[10px] !py-0.2"
                  />
                </div>
                <ProgressBar
                  :value="track.progress"
                  :showValue="false"
                  class="!h-2 custom-progressbar"
                />
                <div class="flex items-center justify-between text-[11px] font-mono muted-text">
                  <span>Progress: {{ track.progress }}%</span>
                  <span>Target: {{ track.target }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ================= BENTO SECTION 2: TASKS, HABITS, RECENT KNOWLEDGE ================= -->
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-12 gap-6 items-stretch">
        <!-- Bento Card 3: Real Database Tasks (4 cols) -->
        <div
          class="xl:col-span-4 flex flex-col justify-between rounded-xl p-6 shadow-sm border bento-card"
        >
          <div>
            <div class="flex items-center justify-between mb-4">
              <div class="flex flex-col">
                <h2 class="text-lg font-semibold">Today's Tasks</h2>
                <span class="text-xs muted-text">Fetched directly from database</span>
              </div>
              <RouterLink to="/tasks" class="text-xs font-semibold hover:underline link-action"
                >View all →</RouterLink
              >
            </div>

            <div class="flex flex-col gap-2 max-h-64 overflow-y-auto">
              <div v-if="loading" class="text-xs muted-text p-4 text-center font-mono">
                Loading tasks...
              </div>
              <div
                v-else-if="tasks.length === 0"
                class="text-xs muted-text p-4 text-center font-mono"
              >
                No tasks for today.
                <RouterLink to="/tasks" class="link-action underline">Create one</RouterLink>
              </div>
              <div
                v-for="task in tasks"
                :key="task.id || task.title"
                class="flex items-center gap-3 p-2.5 rounded-lg task-item transition-colors"
              >
                <span
                  :class="[
                    'w-4 h-4 rounded flex items-center justify-center text-[10px] task-checkbox',
                    task.completed ? 'completed' : '',
                  ]"
                >
                  <span v-if="task.completed">✓</span>
                </span>
                <span
                  :class="[
                    'text-xs font-medium truncate task-title',
                    task.completed ? 'line-through opacity-60' : '',
                  ]"
                >
                  {{ task.title }}
                </span>
              </div>
            </div>
          </div>

          <div
            class="mt-4 pt-3 border-t flex justify-between items-center text-xs font-mono card-footer"
          >
            <span>Total pending tasks</span>
            <span class="font-bold link-action"
              >{{ tasks.filter((t) => !t.completed).length }} remaining</span
            >
          </div>
        </div>

        <!-- Bento Card 4: Habits & Energy Matrix (5 cols) -->
        <div
          class="xl:col-span-5 flex flex-col justify-between rounded-xl p-6 shadow-sm border bento-card"
        >
          <div class="flex items-center justify-between mb-2">
            <div class="flex flex-col">
              <h2 class="text-lg font-semibold">Habits & Energy Architecture</h2>
              <span class="text-xs muted-text">Weekly cognitive stamina & ritual execution</span>
            </div>
            <Tag value="Score: 89/100" severity="success" class="!text-[11px] !py-0.5" />
          </div>

          <div class="flex flex-col gap-2 my-2 overflow-x-auto">
            <div
              class="grid grid-cols-8 text-center font-mono text-[11px] pb-1 border-b habits-header min-w-[360px]"
            >
              <span class="text-left font-semibold">Ritual Protocol</span>
              <span v-for="d in ['M', 'T', 'W', 'T', 'F', 'S', 'S']" :key="d">{{ d }}</span>
            </div>
            <div
              v-for="habit in habits"
              :key="habit.name"
              class="grid grid-cols-8 items-center text-center font-mono text-xs py-1 habit-row rounded transition-colors min-w-[360px]"
            >
              <span class="text-left truncate pr-1 font-sans text-xs">{{ habit.name }}</span>
              <span
                v-for="(val, idx) in habit.status"
                :key="idx"
                :class="val === '—' ? 'muted-symbol' : 'active-symbol font-bold'"
              >
                {{ val }}
              </span>
            </div>
          </div>
        </div>

        <!-- Bento Card 5: Recent Knowledge Database Items (3 cols) -->
        <div
          class="xl:col-span-3 flex flex-col justify-between rounded-xl p-6 shadow-sm border bento-card"
        >
          <div>
            <div class="flex items-center justify-between mb-3">
              <div class="flex flex-col">
                <h2 class="text-lg font-semibold">Recent Knowledge</h2>
                <span class="text-xs muted-text">Synced repository</span>
              </div>
              <RouterLink to="/knowledge" class="text-xs font-semibold hover:underline link-action"
                >View all →</RouterLink
              >
            </div>

            <div v-if="loading" class="text-xs muted-text text-center py-4">
              Loading knowledge...
            </div>
            <div
              v-else-if="recentKnowledge.length === 0"
              class="text-xs muted-text text-center py-4"
            >
              No knowledge files yet.
            </div>
            <div v-else class="flex flex-col gap-2">
              <RouterLink
                v-for="item in recentKnowledge"
                :key="item.id"
                to="/knowledge"
                class="flex items-center justify-between p-2 rounded-lg knowledge-item text-xs transition-colors"
              >
                <span class="font-medium truncate">{{ item.title }}</span>
                <span class="font-mono text-[10px] px-1.5 py-0.5 rounded badge-count"
                  >{{ item.files_count || 0 }} files</span
                >
              </RouterLink>
            </div>
          </div>

          <div
            class="mt-4 pt-3 border-t text-center font-mono text-[11px] card-footer secondary-text"
          >
            System Database Connected
          </div>
        </div>
      </div>

      <!-- ================= LOGS & TELEMETRY FEED ================= -->
      <div class="flex flex-col rounded-xl p-6 shadow-sm border bento-card">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center icon-wrapper">
              <i class="pi pi-code text-base"></i>
            </div>
            <div>
              <h2 class="text-lg font-semibold">Executive Telemetry Feed</h2>
              <span class="text-xs muted-text"
                >Live chronological logs of system synchronization and state transitions</span
              >
            </div>
          </div>
          <span class="font-mono text-[11px] muted-text">Stream: Latency 14ms • OK</span>
        </div>

        <DataTable :value="telemetryLogs" class="p-datatable-sm font-mono text-xs custom-table">
          <Column field="timestamp" header="Timestamp" class="col-timestamp"></Column>
          <Column
            field="component"
            header="Component"
            class="!font-semibold col-component"
          ></Column>
          <Column field="context" header="Session Context" class="col-context"></Column>
          <Column field="score" header="Efficiency Score">
            <template #body="slotProps">
              <Tag :value="slotProps.data.score" severity="success" class="!text-[11px]" />
            </template>
          </Column>
          <Column field="status" header="Status" class="text-right">
            <template #body="slotProps">
              <span class="font-bold secondary-text">{{ slotProps.data.status }}</span>
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>
