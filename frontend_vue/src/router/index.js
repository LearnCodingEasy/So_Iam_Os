import { createRouter, createWebHistory } from 'vue-router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

const HomeView = () => import('../views/shared/HomeView.vue')
const AboutView = () => import('../views/shared/AboutView.vue')

const LoginView = () => import('../views/Accounts/LoginView.vue')
const ProfileView = () => import('../views/Accounts/ProfileView.vue')
const AuthCallback = () => import('../views/Accounts/AuthCallback.vue')

const LearningView = () => import('../views/Learning/LearningView.vue')

const Dashboard = () => import('../views/Core/DashboardView.vue')
const SettingsView = () => import('@/views/Core/Settings.vue')
const MyProgressView = () => import('@/views/Core/MyProgress.vue')

const ScraperView = () => import('@/views/Scraper/ScraperView.vue')

const GoalsView = () => import('@/views/goals/Goals.vue')
const TodayTasksView = () => import('@/views/tasks/TodayTasks.vue')
const TasksCalendar = () => import('@/views/tasks/TasksCalendar.vue')
const SocialView = () => import('@/views/social/SocialView.vue')
const NotificationsView = () => import('@/views/notifications/NotificationsView.vue')
const JobsView = () => import('@/views/jobs/JobsView.vue')
const CodexView = () => import('@/views/codex/CodexView.vue')
const ProjectsView = () => import('@/views/projects/ProjectsView.vue')
const ChallengesView = () => import('@/views/challenges/ChallengesView.vue')
const FinanceView = () => import('@/views/finance/FinanceView.vue')
const MemoryView = () => import('@/views/Memory/MemoryView.vue')

// Ai
const AgentPlanner = () => import('@/views/Ai/AgentPlanner.vue')
const AIChat = () => import('@/views/Ai/AIChat.vue')
const AIControl = () => import('@/views/Ai/AIControl.vue')

const FrontendEnhancementCenter = () => import('@/components/core/FrontendEnhancementCenter.vue')

// Automation
const Automation = () => import('../views/Automation/AutomationView.vue')
const automation_Dashboard = () => import('../views/Automation/DashboardAutomationView.vue')
const ProgramList = () => import('../views/Automation/ProgramList.vue')
const ProgramCreate = () => import('../views/Automation/ProgramCreate.vue')
const ProgramEdit = () => import('../views/Automation/ProgramEdit.vue')
const TaskCreate = () => import('../views/Automation/TaskCreate.vue')
const TaskEditor = () => import('../views/Automation/TaskEditor.vue')

// 404 catchall Page Not Found
const NotFound = () => import('../views/shared/Page_Not_Found.vue')

import { useUserStore } from '@/stores/accounts/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    // ==============================
    // Public
    // ==============================

    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        requiresAuth: true,
      },
    },

    {
      path: '/About',
      name: 'About',
      component: AboutView,
      meta: {
        requiresAuth: true,
      },
    },

    // ==============================
    // Authentication
    // ==============================

    {
      path: '/login',
      name: 'login',
      component: LoginView,

      meta: {
        requiresGuest: true,
      },
    },

    {
      path: '/auth-callback',
      name: 'AuthCallback',
      component: AuthCallback,
    },

    // ==============================
    // Account
    // ==============================

    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView,

      meta: {
        requiresAuth: true,
      },
    },

    // ==============================
    // Knowledge
    // ==============================
    {
      path: '/knowledge',
      name: 'knowledge',
      component: () => import('../views/knowledge/knowledgeView.vue'),
      meta: {
        requiresAuth: true,
      },
    },

    // ==============================
    // Learning
    // ==============================
    {
      path: '/learning',
      name: 'learning',
      component: LearningView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/learning/topics/:topicId',
      name: 'learning-topic',
      component: () => import('@/views/Learning/LearningTopic.vue'),
      meta: {
        requiresAuth: true,
      },
    },
    // ==============================
    // Planning / Execution
    // ==============================
    {
      path: '/goals',
      name: 'goals',
      component: GoalsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/tasks/today',
      name: 'today-tasks',
      component: TodayTasksView,
      meta: { requiresAuth: true },
    },
    {
      path: '/progress',
      name: 'progress',
      component: MyProgressView,
      meta: { requiresAuth: true },
    },
    {
      path: '/jobs',
      name: 'jobs',
      component: JobsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/scraper',
      name: 'scraper',
      component: ScraperView,
      meta: { requiresAuth: true },
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: TasksCalendar,
      meta: { requiresAuth: true },
    },

    { path: '/codex', name: 'codex', component: CodexView, meta: { requiresAuth: true } },
    { path: '/projects', name: 'projects', component: ProjectsView, meta: { requiresAuth: true } },
    {
      path: '/challenges',
      name: 'challenges',
      component: ChallengesView,
      meta: { requiresAuth: true },
    },
    { path: '/finance', name: 'finance', component: FinanceView, meta: { requiresAuth: true } },
    { path: '/memory', name: 'memory', component: MemoryView, meta: { requiresAuth: true } },
    {
      path: '/ai/agents',
      name: 'ai-agents',
      component: AgentPlanner,
      meta: { requiresAuth: true },
    },
    { path: '/social', name: 'social', component: SocialView, meta: { requiresAuth: true } },
    {
      path: '/notifications',
      name: 'notifications',
      component: NotificationsView,
      meta: { requiresAuth: true },
    },

    // ==============================
    // Frontend Engineering Center
    // ==============================
    {
      path: '/system/frontend',
      name: 'frontend-enhancements',
      component: FrontendEnhancementCenter,
      meta: { requiresAuth: true },
    },

    // ==============================
    // Settings
    // ==============================
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView,
      meta: { requiresAuth: true },
    },

    // ==============================
    // AI Chat & Control Center
    // ==============================
    {
      path: '/ai',
      name: 'ai-chat',
      component: AIChat,
      meta: { requiresAuth: true },
    },
    {
      path: '/ai/control',
      name: 'ai-control',
      component: AIControl,
      meta: { requiresAuth: true },
    },
    {
      path: '/ai/operations',
      name: 'ai-operations',
      component: () => import('@/views/Ai/AIOperationsView.vue'),
      meta: { requiresAuth: true },
    },

    // ==============================
    // Dashboard
    // ==============================
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: {
        requiresAuth: true,
      },
    },
    // Automation
    {
      path: '/automation',
      name: 'automation',
      component: Automation,
      meta: { requiresAuth: true },
    },
    {
      path: '/automation_Dashboard',
      name: 'automation_Dashboard',
      component: automation_Dashboard,
      meta: { requiresAuth: true },
    },
    {
      path: '/automation_ProgramList',
      name: 'automation_ProgramList',
      component: ProgramList,
      meta: { requiresAuth: true },
    },
    {
      path: '/automation_programs_create',
      name: 'automation_programs_create',
      component: ProgramCreate,
      meta: { requiresAuth: true },
    },
    {
      path: '/automation/:id',
      name: 'automation_programs_edit',
      component: ProgramEdit,
      meta: { requiresAuth: true },
    },
    {
      path: '/automation_TaskCreate',
      name: 'automation_TaskCreate',
      component: TaskCreate,
      meta: { requiresAuth: true },
    },
    {
      path: '/automation_TaskEditor',
      name: 'automation_TaskEditor',
      component: TaskEditor,
      meta: { requiresAuth: true },
    },
    //////////////////////////////////////////////////
    ////////////////////// 404 ///////////////////////
    //////////////////////////////////////////////////
    // 404 catchall Page Not Found
    {
      path: '/:catchAll(.*)',
      name: 'NotFound',
      component: NotFound,
    },
  ],
})

// Keep route access synchronized when the central Axios client determines
// that both the access token and refresh token are no longer usable.
if (typeof window !== 'undefined') {
  window.addEventListener('so-iam-auth-expired', () => {
    const current = router.currentRoute.value
    if (current.name !== 'login') {
      router.replace({
        name: 'login',
        query: current.fullPath ? { redirect: current.fullPath } : {},
      })
    }
  })
}

// ==========================================
// Authentication Guard
// ==========================================

router.beforeEach(async (to) => {
  NProgress.start()
  const userStore = useUserStore()

  // Initialize authentication state
  if (!userStore.initialized) {
    await userStore.initStore()
  }

  const isAuthenticated = userStore.isLoggedIn

  // Protected route
  if (to.meta.requiresAuth && !isAuthenticated) {
    return {
      name: 'login',
      query: {
        redirect: to.fullPath,
      },
    }
  }

  // Guest-only route
  if (to.meta.requiresGuest && isAuthenticated) {
    return {
      name: 'home',
    }
  }

  return true
})

router.afterEach(() => NProgress.done())
router.onError(() => NProgress.done())

export default router
