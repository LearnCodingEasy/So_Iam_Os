<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

import { RouterLink } from 'vue-router'
import { dashboardService } from '@/services/dashboard'

/*
|--------------------------------------------------------------------------
| SIDEBAR
|--------------------------------------------------------------------------
*/

const sidebarOpen = ref(true)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const closeSidebarOnMobile = () => {
  if (window.innerWidth <= 900) {
    sidebarOpen.value = false
  }
}

/*
|--------------------------------------------------------------------------
| NAVIGATION
|--------------------------------------------------------------------------
*/

const menuItems = [
  {
    name: 'Dashboard',
    icon: '⌂',
    route: '/',
  },
  {
    name: 'Projects',
    icon: '▣',
    route: '/projects',
  },
  {
    name: 'Tasks',
    icon: '✓',
    route: '/tasks',
  },
  {
    name: 'Goals',
    icon: '◎',
    route: '/goals',
  },
  {
    name: 'Learning',
    icon: '◇',
    route: '/learning',
  },
  {
    name: 'Knowledge',
    icon: '▤',
    route: '/knowledge',
  },
  {
    name: 'Memory',
    icon: '◈',
    route: '/memory',
  },
  {
    name: 'Social',
    icon: '♟',
    route: '/social',
  },
  {
    name: 'AI Assistant',
    icon: '✦',
    route: '/ai',
  },
  {
    name: 'Settings',
    icon: '⚙',
    route: '/settings',
  },
]

/*
|--------------------------------------------------------------------------
| DASHBOARD STATE
|--------------------------------------------------------------------------
*/

const dashboard = ref(null)
const loading = ref(true)
const error = ref(null)

/*
|--------------------------------------------------------------------------
| LOAD DASHBOARD
|--------------------------------------------------------------------------
*/

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
|--------------------------------------------------------------------------
| USER
|--------------------------------------------------------------------------
*/

const userName = computed(() => {
  return dashboard.value?.user?.name || 'User'
})

const userEmail = computed(() => {
  return dashboard.value?.user?.email || 'Personal Account'
})

const userInitials = computed(() => {
  const name = userName.value.trim()

  if (!name) {
    return 'U'
  }

  const parts = name.split(/\s+/)

  if (parts.length === 1) {
    return parts[0].slice(0, 2).toUpperCase()
  }

  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
})

/*
|--------------------------------------------------------------------------
| GREETING
|--------------------------------------------------------------------------
*/

const greeting = computed(() => {
  const hour = new Date().getHours()

  if (hour >= 5 && hour < 12) {
    return 'Good Morning'
  }

  if (hour >= 12 && hour < 17) {
    return 'Good Afternoon'
  }

  if (hour >= 17 && hour < 22) {
    return 'Good Evening'
  }

  return 'Good Night'
})

/*
|--------------------------------------------------------------------------
| DATE / TIME
|--------------------------------------------------------------------------
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
|--------------------------------------------------------------------------
| STATS
|--------------------------------------------------------------------------
*/

const stats = computed(() => {
  const data = dashboard.value?.stats || {}

  return [
    {
      title: 'Projects',
      value: data.projects?.total ?? 0,
      description:
        `${data.projects?.active ?? 0} active • ` + `${data.projects?.completed ?? 0} completed`,
      icon: '▣',
      type: 'purple',
      route: '/projects',
    },

    {
      title: 'Tasks',
      value: data.tasks?.total ?? 0,
      description:
        `${data.tasks?.pending ?? 0} pending • ` + `${data.tasks?.completed ?? 0} completed`,
      icon: '✓',
      type: 'green',
      route: '/tasks',
    },

    {
      title: 'Goals',
      value: data.goals?.total ?? 0,
      description:
        `${data.goals?.in_progress ?? 0} in progress • ` +
        `${data.goals?.completed ?? 0} completed`,
      icon: '◎',
      type: 'orange',
      route: '/goals',
    },

    {
      title: 'Knowledge',
      value: data.knowledge?.total ?? 0,
      description: `${data.knowledge?.files ?? 0} files`,
      icon: '▤',
      type: 'blue',
      route: '/knowledge',
    },
  ]
})

/*
|--------------------------------------------------------------------------
| RECENT KNOWLEDGE
|--------------------------------------------------------------------------
*/

const recentKnowledge = computed(() => {
  return dashboard.value?.recent?.knowledge || []
})

/*
|--------------------------------------------------------------------------
| TASKS
|--------------------------------------------------------------------------
*/

const tasks = computed(() => {
  return dashboard.value?.tasks || []
})

/*
|--------------------------------------------------------------------------
| QUICK ACTIONS
|--------------------------------------------------------------------------
*/

const quickActions = [
  {
    title: 'Add a new project',
    icon: '▣',
    route: '/projects',
  },
  {
    title: 'Create a task',
    icon: '✓',
    route: '/tasks',
  },
  {
    title: 'Set a goal',
    icon: '◎',
    route: '/goals',
  },
  {
    title: 'Start learning',
    icon: '◇',
    route: '/learning',
  },
  {
    title: 'Search knowledge',
    icon: '⌕',
    route: '/knowledge',
  },
  {
    title: 'Open memory',
    icon: '◈',
    route: '/memory',
  },
  {
    title: 'Ask AI Assistant',
    icon: '✦',
    route: '/ai',
  },
]

/*
|--------------------------------------------------------------------------
| AI
|--------------------------------------------------------------------------
*/

const openAI = () => {
  window.location.href = '/ai'
}

/*
|--------------------------------------------------------------------------
| LIFECYCLE
|--------------------------------------------------------------------------
*/

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
  <div
    class="app"
    :class="{
      'sidebar-collapsed': !sidebarOpen,
    }"
  >
    <!-- =====================================================
         SIDEBAR OVERLAY - MOBILE
    ====================================================== -->

    <div v-if="sidebarOpen" class="sidebar-overlay" @click="toggleSidebar"></div>

    <!-- ===========================================
    SIDEBAR
    ============================================ -->

    <aside
      class="sidebar"
      :class="{
        open: sidebarOpen,
        collapsed: !sidebarOpen,
      }"
    >
      <!-- BRAND -->

      <div class="brand">
        <div class="brand-logo">✦</div>

        <div class="brand-info">
          <h1>So Iam OS</h1>

          <span> Your Personal AI Operating System </span>
        </div>
      </div>

      <!-- SIDEBAR TOGGLE -->

      <button
        class="sidebar-toggle"
        type="button"
        @click="toggleSidebar"
        :aria-label="sidebarOpen ? 'Close sidebar' : 'Open sidebar'"
      >
        <span v-if="sidebarOpen"> ‹ </span>

        <span v-else> › </span>
      </button>

      <!-- NAVIGATION -->

      <nav class="navigation">
        <RouterLink
          v-for="item in menuItems"
          :key="item.name"
          :to="item.route"
          class="nav-item"
          active-class="active"
          @click="closeSidebarOnMobile"
        >
          <span class="nav-icon">
            {{ item.icon }}
          </span>

          <span class="nav-name">
            {{ item.name }}
          </span>

          <span v-if="item.badge" class="badge">
            {{ item.badge }}
          </span>
        </RouterLink>
      </nav>

      <!-- PROFILE -->

      <div class="sidebar-bottom">
        <div class="profile">
          <div class="avatar">
            {{ userInitials }}
          </div>

          <div class="profile-info">
            <strong>
              {{ userName }}
            </strong>

            <span>
              {{ userEmail }}
            </span>
          </div>

          <span class="profile-arrow"> ⌄ </span>
        </div>
      </div>
    </aside>

    <!-- =====================================================
         MAIN
    ====================================================== -->

    <main class="main">
      <!-- =====================================================
           HEADER
      ====================================================== -->

      <header class="header">
        <!-- SIDEBAR BUTTON -->

        <button
          class="header-menu-button"
          type="button"
          @click="toggleSidebar"
          :aria-label="sidebarOpen ? 'Close sidebar' : 'Open sidebar'"
        >
          ☰
        </button>

        <!-- SEARCH -->

        <div class="search">
          <span> ⌕ </span>

          <input type="text" placeholder="Search anything... (projects, tasks, knowledge, etc.)" />
        </div>

        <!-- HEADER ACTIONS -->

        <div class="header-actions">
          <button class="header-button" type="button">♧</button>

          <button class="header-button" type="button">☼</button>

          <div class="date">
            <strong>
              {{ formattedDate }}
            </strong>

            <span>
              {{ formattedTime }}
            </span>
          </div>

          <div class="header-avatar">
            {{ userInitials }}
          </div>
        </div>
      </header>

      <!-- =====================================================
           CONTENT
      ====================================================== -->

      <section class="content">
        <!-- =====================================================
             ERROR
        ====================================================== -->

        <div v-if="error" class="dashboard-error">
          <strong> Dashboard API Error </strong>

          <span>
            {{ error }}
          </span>

          <button type="button" @click="loadDashboard">Try again</button>
        </div>

        <!-- =====================================================
             HERO
        ====================================================== -->

        <section class="hero">
          <div class="hero-content">
            <h2>
              {{ greeting }},
              {{ userName }}
              <span>👋</span>
            </h2>

            <p>Your goals, projects and dreams are now part of a smarter system.</p>

            <p>Let's build your future together.</p>

            <div class="hero-actions">
              <button type="button">⚡ Focus</button>

              <button type="button">♻ Build</button>

              <button type="button">🎓 Learn</button>

              <button type="button">★ Grow</button>

              <button type="button">✦ Be Better</button>
            </div>
          </div>

          <div class="hero-quote">
            <span class="quote-mark"> “ </span>

            <p>Small steps every day lead to big results.</p>

            <small> So_Iam_OS ✦ </small>
          </div>
        </section>

        <!-- =====================================================
             STATS
        ====================================================== -->

        <section class="stats-grid">
          <RouterLink
            v-for="stat in stats"
            :key="stat.title"
            :to="stat.route"
            class="stat-card"
            :class="stat.type"
          >
            <div class="stat-icon">
              {{ stat.icon }}
            </div>

            <div class="stat-content">
              <span class="stat-title">
                {{ stat.title }}
              </span>

              <strong>
                {{ stat.value }}
              </strong>

              <small>
                {{ stat.description }}
              </small>
            </div>

            <span class="card-arrow"> › </span>
          </RouterLink>
        </section>

        <!-- =====================================================
             DASHBOARD GRID
        ====================================================== -->

        <section class="dashboard-grid">
          <!-- ===================================================
               TASKS
          ==================================================== -->

          <article class="panel tasks-panel">
            <div class="panel-header">
              <div>
                <span class="panel-icon"> ▣ </span>

                <h3>Today's Tasks</h3>
              </div>

              <RouterLink to="/tasks" class="panel-link"> View all → </RouterLink>
            </div>

            <div class="tasks-list">
              <div v-if="loading" class="empty-state">Loading tasks...</div>

              <div v-else-if="tasks.length === 0" class="empty-state">
                <span> ✓ </span>

                <p>No tasks for today.</p>

                <RouterLink to="/tasks" class="panel-link"> Create a task → </RouterLink>
              </div>

              <div v-else v-for="task in tasks" :key="task.id || task.title" class="task">
                <span
                  class="task-check"
                  :class="{
                    completed: task.completed,
                  }"
                >
                  <span v-if="task.completed"> ✓ </span>
                </span>

                <span
                  class="task-title"
                  :class="{
                    done: task.completed,
                  }"
                >
                  {{ task.title }}
                </span>

                <span class="task-time">
                  {{ task.time || '' }}
                </span>
              </div>
            </div>
          </article>

          <!-- ===================================================
               PROGRESS
          ==================================================== -->

          <article class="panel progress-panel">
            <div class="panel-header">
              <div>
                <span class="panel-icon green-icon"> ▥ </span>

                <h3>My Progress</h3>
              </div>

              <select>
                <option>This week</option>

                <option>This month</option>

                <option>This year</option>
              </select>
            </div>

            <div class="chart">
              <div class="y-axis">
                <span>10</span>
                <span>8</span>
                <span>6</span>
                <span>4</span>
                <span>2</span>
                <span>0</span>
              </div>

              <div class="chart-area">
                <div class="grid-line"></div>
                <div class="grid-line"></div>
                <div class="grid-line"></div>
                <div class="grid-line"></div>
                <div class="grid-line"></div>

                <svg class="chart-svg" viewBox="0 0 500 180" preserveAspectRatio="none">
                  <polyline
                    points="0,145 80,120 160,110 240,75 320,82 400,55 500,30"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="3"
                  />

                  <polyline
                    points="0,160 80,150 160,148 240,120 320,120 400,105 500,75"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="3"
                  />

                  <polyline
                    points="0,170 80,160 160,158 240,155 320,150 400,140 500,120"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="3"
                  />
                </svg>
              </div>
            </div>

            <div class="chart-legend">
              <span>
                <i class="legend-project"></i>
                Projects
              </span>

              <span>
                <i class="legend-task"></i>
                Tasks
              </span>

              <span>
                <i class="legend-learning"></i>
                Learning
              </span>
            </div>
          </article>

          <!-- ===================================================
               AI
          ==================================================== -->

          <article class="panel ai-panel">
            <div class="panel-header">
              <div>
                <span class="panel-icon"> ✦ </span>

                <h3>AI Assistant</h3>
              </div>

              <RouterLink to="/ai" class="panel-link"> Open AI → </RouterLink>
            </div>

            <div class="ai-content">
              <div class="ai-message">
                Hi {{ userName }} 👋
                <br />
                What can I help you with today?
              </div>

              <RouterLink to="/ai" class="ai-input">
                <span> Ask me anything... </span>

                <button type="button" @click.prevent="openAI">➤</button>
              </RouterLink>

              <div class="ai-actions">
                <RouterLink to="/ai" class="ai-action-button"> ♧ Plan my day </RouterLink>

                <RouterLink to="/ai" class="ai-action-button"> ◇ Explain a concept </RouterLink>

                <RouterLink to="/ai" class="ai-action-button"> ⚙ Help with code </RouterLink>

                <RouterLink to="/ai" class="ai-action-button"> ✦ Suggest ideas </RouterLink>
              </div>
            </div>
          </article>

          <!-- ===================================================
               QUICK ACCESS
          ==================================================== -->

          <article class="panel quick-panel">
            <div class="panel-header">
              <div>
                <span class="panel-icon"> ϟ </span>

                <h3>Quick Access</h3>
              </div>
            </div>

            <div class="quick-list">
              <RouterLink
                v-for="action in quickActions"
                :key="action.title"
                :to="action.route"
                class="quick-item"
              >
                <span class="quick-icon">
                  {{ action.icon }}
                </span>

                <span>
                  {{ action.title }}
                </span>

                <b> › </b>
              </RouterLink>
            </div>
          </article>

          <!-- ===================================================
               RECENT KNOWLEDGE
          ==================================================== -->

          <article class="panel knowledge-panel">
            <div class="panel-header">
              <div>
                <span class="panel-icon"> ▤ </span>

                <h3>Recent Knowledge</h3>
              </div>

              <RouterLink to="/knowledge" class="panel-link"> View all → </RouterLink>
            </div>

            <div v-if="loading" class="knowledge-empty">Loading knowledge...</div>

            <div v-else-if="recentKnowledge.length === 0" class="knowledge-empty">
              <span> ▤ </span>

              <p>No knowledge yet.</p>

              <RouterLink to="/knowledge" class="panel-link">
                Add your first knowledge →
              </RouterLink>
            </div>

            <div v-else class="quick-list">
              <RouterLink
                v-for="item in recentKnowledge"
                :key="item.id"
                to="/knowledge"
                class="quick-item"
              >
                <span class="quick-icon"> ▤ </span>

                <span>
                  {{ item.title }}
                </span>

                <small>
                  {{ item.files_count || 0 }}
                  files
                </small>

                <b> › </b>
              </RouterLink>
            </div>
          </article>
        </section>
      </section>
    </main>
  </div>
</template>
