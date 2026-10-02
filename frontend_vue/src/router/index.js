import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'

import LoginView from '../views/Authentication/LoginView.vue'
import ProfileView from '../views/Account/ProfileView.vue'
import AuthCallback from '../views/Authentication/AuthCallback.vue'

import KnowledgeView from '../views/knowledge/KnowledgeView.vue'

import LearningView from '../views/learning/LearningView.vue'

import Dashboard from '../views/Dashboard/DashboardView.vue'

import AIChat from '@/views/AI/AIChat.vue'
import AIControl from '@/views/AI/AI.vue'
import SettingsView from '@/views/Settings/Settings.vue'
import GoalsView from '@/views/Goals/Goals.vue'
import TodayTasksView from '@/views/Tasks/TodayTasks.vue'
import TasksCalendar from '@/views/Tasks/TasksCalendar.vue'
import SocialView from '@/views/Social/SocialView.vue'
import NotificationsView from '@/views/Notifications/NotificationsView.vue'
import MyProgressView from '@/views/Progress/MyProgress.vue'
import JobsView from '@/views/jobs/JobsView.vue'
import CodexView from '@/views/Codex/CodexView.vue'

// Automation
import Automation from '../views/Automation/AutomationView.vue'
import automation_Dashboard from '../views/Automation/DashboardAutomationView.vue'
import ProgramList from '../views/Automation/ProgramList.vue'
import ProgramCreate from '../views/Automation/ProgramCreate.vue'
import ProgramEdit from '../views/Automation/ProgramEdit.vue'
import TaskCreate from '../views/Automation/TaskCreate.vue'
import TaskEditor from '../views/Automation/TaskEditor.vue'

// 404 catchall Page Not Found
import NotFound from '../views/Page_Not_Found/Page_Not_Found.vue'

import { useUserStore } from '@/stores/user'

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
    },

    {
      path: '/About',
      name: 'About',
      component: AboutView,
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
      component: KnowledgeView,
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
      component: () => import('@/views/learning/LearningTopic.vue'),
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
      path: '/tasks',
      name: 'tasks',
      component: TasksCalendar,
      meta: { requiresAuth: true },
    },

    { path: '/codex', name: 'codex', component: CodexView, meta: { requiresAuth: true } },
    { path: '/social', name: 'social', component: SocialView, meta: { requiresAuth: true } },
    {
      path: '/notifications',
      name: 'notifications',
      component: NotificationsView,
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
    // AI Chat
    // ==============================
    {
      path: '/ai',
      name: 'ai-chat',
      component: AIChat,
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

// ==========================================
// Authentication Guard
// ==========================================

router.beforeEach(async (to) => {
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

export default router
