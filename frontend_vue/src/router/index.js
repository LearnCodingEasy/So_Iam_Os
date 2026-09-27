import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'

import LoginView from '../views/Authentication/LoginView.vue'
import ProfileView from '../views/Account/ProfileView.vue'
import AuthCallback from '../views/Authentication/AuthCallback.vue'

import KnowledgeView from '@/views/knowledge/KnowledgeView.vue'

import LearningView from '@/views/learning/LearningView.vue'

import Dashboard from '../views/Dashboard/DashboardView.vue'

import AIChat from '@/views/AI/AIChat.vue'
import AIControl from '@/views/AI/AI.vue'
import SettingsView from '@/views/Settings/Settings.vue'
import GoalsView from '@/views/Goals/Goals.vue'
import TodayTasksView from '@/views/Tasks/TodayTasks.vue'

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
      path: '/tasks',
      name: 'tasks',
      redirect: { name: 'today-tasks' },
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
      path: '/dashboard/',
      name: 'dashboard',
      component: Dashboard,

      meta: {
        requiresAuth: true,
      },
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
