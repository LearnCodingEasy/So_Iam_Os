import axios from 'axios'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
})

const getAccessToken = () => localStorage.getItem('user.access')
const getRefreshToken = () => localStorage.getItem('user.refresh')

const clearAuthStorage = () => {
  localStorage.removeItem('user.access')
  localStorage.removeItem('user.refresh')
  localStorage.removeItem('user.info')
}

const notifyAuthExpired = () => {
  window.dispatchEvent(new CustomEvent('so-iam-auth-expired'))
}

let refreshPromise = null

async function refreshAccessToken() {
  const refreshToken = getRefreshToken()
  if (!refreshToken) return null

  if (!refreshPromise) {
    refreshPromise = axios
      .post(
        `${API_BASE_URL}/users/refresh/`,
        { refresh: refreshToken },
        {
          headers: { 'Content-Type': 'application/json' },
          timeout: 30000,
        },
      )
      .then((response) => {
        const accessToken = response.data?.access
        if (!accessToken) return null
        localStorage.setItem('user.access', accessToken)
        api.defaults.headers.common.Authorization = `Bearer ${accessToken}`
        return accessToken
      })
      .catch((error) => {
        if (import.meta.env.DEV) {
          console.warn('⚠️ JWT refresh failed:', error?.response?.data || error.message)
        }
        return null
      })
      .finally(() => {
        refreshPromise = null
      })
  }

  return refreshPromise
}

api.interceptors.request.use(
  (config) => {
    const accessToken = getAccessToken()
    if (accessToken) {
      config.headers = config.headers || {}
      config.headers.Authorization = `Bearer ${accessToken}`
    }

    if (import.meta.env.DEV) {
      console.group('🔐 API REQUEST')
      console.log('➡️ Method:', config.method?.toUpperCase())
      console.log('🌐 URL:', `${config.baseURL || ''}${config.url || ''}`)
      console.log('🔑 Has Access Token:', Boolean(accessToken))
      console.log('🪪 Authorization:', config.headers?.Authorization ? 'Bearer ********' : '❌ Missing')
      console.groupEnd()
    }

    return config
  },
  (error) => Promise.reject(error),
)

api.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.group('📥 API RESPONSE')
      console.log('✅ Status:', response.status)
      console.log('🌐 URL:', response.config?.url)
      console.log('📦 Data:', response.data)
      console.groupEnd()
    }
    return response
  },
  async (error) => {
    const status = error.response?.status
    const originalRequest = error.config

    if (import.meta.env.DEV) {
      console.group('🚨 API ERROR')
      console.log('❌ Status:', status)
      console.log('🌐 URL:', originalRequest?.url)
      console.error('📦 Response:', error.response?.data)
      console.groupEnd()
    }

    if (status === 401 && originalRequest && !originalRequest._retry) {
      originalRequest._retry = true

      const accessToken = await refreshAccessToken()
      if (accessToken) {
        originalRequest.headers = originalRequest.headers || {}
        originalRequest.headers.Authorization = `Bearer ${accessToken}`
        return api(originalRequest)
      }

      clearAuthStorage()
      notifyAuthExpired()
    }

    if (status === 403 && import.meta.env.DEV) {
      console.warn('🚫 Forbidden request:', originalRequest?.url)
    }

    if (error.code === 'ECONNABORTED' && import.meta.env.DEV) {
      console.warn('⏱️ API request timed out:', originalRequest?.url)
    }

    if (!error.response && error.code !== 'ECONNABORTED' && import.meta.env.DEV) {
      console.warn('🌐 Network error. Make sure Django API is running.')
    }

    return Promise.reject(error)
  },
)

export default api
