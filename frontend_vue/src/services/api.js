




import axios from 'axios'

// ===================================================
// 🌐 API Configuration
// ===================================================

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,

  headers: {
    'Content-Type': 'application/json',
  },

  timeout: 30000,
})

// ====================================================
// 🔐 Request Interceptor
// ====================================================

api.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('user.access')

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }

    if (import.meta.env.DEV) {
      console.group('🔐 API REQUEST')

      console.log(
        '➡️ Method:',
        config.method?.toUpperCase(),
      )

      console.log(
        '🌐 URL:',
        `${config.baseURL}${config.url}`,
      )

      console.log(
        '🔑 Has Access Token:',
        Boolean(accessToken),
      )

      console.log(
        '🪪 Authorization:',
        config.headers.Authorization
          ? 'Bearer ********'
          : '❌ Missing',
      )

      console.groupEnd()
    }

    return config
  },

  (error) => {
    if (import.meta.env.DEV) {
      console.error(
        '❌ Request Interceptor Error:',
        error,
      )
    }

    return Promise.reject(error)
  },
)

// ====================================================
// 📥 Response Interceptor
// ====================================================

api.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.group('📥 API RESPONSE')

      console.log(
        '✅ Status:',
        response.status,
      )

      console.log(
        '🌐 URL:',
        response.config.url,
      )

      console.log(
        '📦 Data:',
        response.data,
      )

      console.groupEnd()
    }

    return response
  },

  (error) => {
    if (import.meta.env.DEV) {
      console.group('🚨 API ERROR')

      console.log(
        '❌ Status:',
        error.response?.status,
      )

      console.log(
        '🌐 URL:',
        error.config?.url,
      )

      console.error(
        '📦 Response:',
        error.response?.data,
      )

      console.groupEnd()
    }

    if (error.response?.status === 401) {
      console.warn(
        '🔐 Access Token Unauthorized',
      )
    }

    if (error.response?.status === 403) {
      console.warn(
        '🚫 Forbidden request',
      )
    }

    if (error.code === 'ECONNABORTED') {
      console.warn(
        '⏱️ API request timed out',
      )
    }

    return Promise.reject(error)
  },
)

export default api
