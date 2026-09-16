import { defineStore } from 'pinia'

import api from '@/services/api'

// ====================================================
// 🔑 Local Storage Keys
// ====================================================

const ACCESS_TOKEN_KEY = 'user.access'
const REFRESH_TOKEN_KEY = 'user.refresh'
const USER_KEY = 'user.info'

// ====================================================
// 👤 Default User
// ====================================================
const defaultUser = () => ({
  isAuthenticated: false,

  id: null,

  name: null,
  surname: null,
  full_name: null,
  email: null,

  date_of_birth: null,
  gender: null,

  avatar_url: null,
  cover_url: null,

  skills: [],

  is_online: false,

  task_count: 0,

  date_joined: null,

  access: null,
  refresh: null,
})

// ====================================================
// 👤 User Store
// ====================================================

export const useUserStore = defineStore('user', {
  // ==================================================
  // 📦 State
  // ==================================================

  state: () => ({
    user: defaultUser(),

    error: null,

    initialized: false,
  }),

  // ==================================================
  // 🎯 Getters
  // ==================================================

  getters: {
    // -----------------------------------------------
    // 🔐 Authentication Status
    // -----------------------------------------------

    isLoggedIn: (state) => {
      return Boolean(state.user.isAuthenticated && state.user.access)
    },

    // -----------------------------------------------
    // 👤 Full Name
    // -----------------------------------------------

    fullName: (state) => {
      return [state.user.name, state.user.surname].filter(Boolean).join(' ')
    },

    // -----------------------------------------------
    // 🛠 User Skills
    // -----------------------------------------------

    userSkills: (state) => {
      return Array.isArray(state.user.skills) ? state.user.skills : []
    },

    // -----------------------------------------------
    // 🔑 Access Token
    // -----------------------------------------------

    userToken: (state) => {
      return state.user.access
    },

    // -----------------------------------------------
    // 🔄 Refresh Token
    // -----------------------------------------------

    refreshToken: (state) => {
      return state.user.refresh
    },
  },

  // ==================================================
  // ⚙️ Actions
  // ==================================================

  actions: {
    // =================================================
    // 🚀 Initialize Store
    // =================================================

    async initStore() {
      if (this.initialized) {
        return
      }

      this.error = null

      const access = localStorage.getItem(ACCESS_TOKEN_KEY)

      const refresh = localStorage.getItem(REFRESH_TOKEN_KEY)

      const storedUser = localStorage.getItem(USER_KEY)

      // -----------------------------------------------
      // ❌ No Tokens
      // -----------------------------------------------

      if (!access || !refresh) {
        this.removeToken()

        this.initialized = true

        return
      }

      // -----------------------------------------------
      // 💾 Restore Tokens
      // -----------------------------------------------

      this.user.access = access
      this.user.refresh = refresh
      this.user.isAuthenticated = true

      // -----------------------------------------------
      // 👤 Restore User
      // -----------------------------------------------

      if (storedUser) {
        try {
          const parsedUser = JSON.parse(storedUser)

          this.user = {
            ...defaultUser(),
            ...parsedUser,

            access,
            refresh,

            isAuthenticated: true,
          }
        } catch (error) {
          console.error('Failed to parse stored user:', error)
        }
      }

      // -----------------------------------------------
      // 🔐 Set Authorization
      // -----------------------------------------------

      this.setAuthorizationHeader(access)

      // -----------------------------------------------
      // 👤 Validate Current User
      // -----------------------------------------------

      try {
        const response = await api.get('/users/me/')

        this.setUserInfo(response.data)
      } catch (error) {
        console.warn('Access token validation failed.', error)

        // ---------------------------------------------
        // 🔄 Try Refresh
        // ---------------------------------------------

        const refreshed = await this.refreshAccessToken()

        if (!refreshed) {
          this.removeToken()

          this.initialized = true

          return
        }

        // ---------------------------------------------
        // 🔁 Retry /me
        // ---------------------------------------------

        try {
          const response = await api.get('/users/me/')

          this.setUserInfo(response.data)
        } catch (meError) {
          console.error('Failed to load current user:', meError)

          this.removeToken()
        }
      }

      this.initialized = true
    },

    // =================================================
    // 🔑 Save JWT Tokens
    // =================================================

    setToken(data) {
      if (!data?.access) {
        throw new Error('Access token is missing.')
      }

      this.user.access = data.access

      if (data.refresh) {
        this.user.refresh = data.refresh
      }

      this.user.isAuthenticated = true

      // -----------------------------------------------
      // 💾 Local Storage
      // -----------------------------------------------

      localStorage.setItem(ACCESS_TOKEN_KEY, data.access)

      if (data.refresh) {
        localStorage.setItem(REFRESH_TOKEN_KEY, data.refresh)
      }

      // -----------------------------------------------
      // 🔐 Authorization
      // -----------------------------------------------

      this.setAuthorizationHeader(data.access)
    },

    // =================================================
    // 👤 Save User Information
    // =================================================

    setUserInfo(user) {
      if (!user) {
        return
      }

      this.user = {
        ...defaultUser(),
        ...this.user,
        ...user,

        isAuthenticated: true,

        access: this.user.access,
        refresh: this.user.refresh,

        task_count: user.task_count ?? 0,

        is_online: Boolean(user.is_online),

        skills: Array.isArray(user.skills) ? user.skills : [],
      }

      localStorage.setItem(USER_KEY, JSON.stringify(this.user))
    },

    // =================================================
    // 🔐 Set Authorization Header
    // =================================================

    setAuthorizationHeader(token) {
      if (!token) {
        return
      }

      api.defaults.headers.common.Authorization = `Bearer ${token}`
    },

    // =================================================
    // 🧹 Remove Authorization Header
    // =================================================

    removeAuthorizationHeader() {
      delete api.defaults.headers.common.Authorization
    },

    // =================================================
    // 🔄 Refresh Access Token
    // =================================================

    async refreshAccessToken() {
      const refresh = this.user.refresh || localStorage.getItem(REFRESH_TOKEN_KEY)

      if (!refresh) {
        return false
      }

      try {
        const response = await api.post('/users/refresh/', {
          refresh,
        })

        const newAccess = response.data?.access

        if (!newAccess) {
          throw new Error('No access token returned.')
        }

        // ---------------------------------------------
        // 💾 Save New Access Token
        // ---------------------------------------------

        this.user.access = newAccess
        this.user.refresh = refresh
        this.user.isAuthenticated = true

        localStorage.setItem(ACCESS_TOKEN_KEY, newAccess)

        // ---------------------------------------------
        // 🔐 Update Authorization
        // ---------------------------------------------

        this.setAuthorizationHeader(newAccess)

        return true
      } catch (error) {
        console.error('Refresh token failed:', error)

        this.removeToken()

        return false
      }
    },

    // =================================================
    // 🚪 Logout
    // =================================================

    async logout() {
      // -----------------------------------------------
      // ⚠️ No backend logout endpoint yet
      // -----------------------------------------------
      //
      // Therefore logout is currently local.
      //

      this.removeToken()
    },

    // =================================================
    // 🧹 Clear Authentication
    // =================================================

    removeToken() {
      this.user = defaultUser()

      this.error = null

      localStorage.removeItem(ACCESS_TOKEN_KEY)

      localStorage.removeItem(REFRESH_TOKEN_KEY)

      localStorage.removeItem(USER_KEY)

      this.removeAuthorizationHeader()
    },

    // =================================================
    // 🔄 Reset User
    // =================================================

    resetUser() {
      this.user = defaultUser()
    },
  },
})
