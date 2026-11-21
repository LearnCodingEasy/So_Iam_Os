import axios from 'axios'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

// Telemetry receives path-only URLs: query parameters may contain tokens or
// user-supplied search/prompt data and must not be copied into debug events.
const safeLogUrl = (baseURL, requestURL) => {
  const raw = `${baseURL || ''}${requestURL || ''}`
  return raw.split('?')[0].split('#')[0]
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 180000,
})

const getAccessToken = () => localStorage.getItem('user.access')
const getRefreshToken = () => localStorage.getItem('user.refresh')

const clearAuthStorage = () => {
  localStorage.removeItem('user.access')
  localStorage.removeItem('user.refresh')
  localStorage.removeItem('user.info')
  delete api.defaults.headers.common.Authorization
}

const notifyAuthExpired = () => {
  window.dispatchEvent(new CustomEvent('so-iam-auth-expired'))
}

let refreshPromise = null
let activeRequests = 0

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
        const rotatedRefreshToken = response.data?.refresh

        if (!accessToken) return null

        // SimpleJWT is configured with ROTATE_REFRESH_TOKENS and
        // BLACKLIST_AFTER_ROTATION. Persist BOTH tokens atomically from the
        // response; keeping the previous refresh token makes the next refresh
        // fail with "Token is blacklisted".
        localStorage.setItem('user.access', accessToken)
        if (rotatedRefreshToken) {
          localStorage.setItem('user.refresh', rotatedRefreshToken)
        }

        api.defaults.headers.common.Authorization = `Bearer ${accessToken}`
        window.dispatchEvent(new CustomEvent('so-iam-token-refreshed', {
          detail: {
            access: accessToken,
            refresh: rotatedRefreshToken || getRefreshToken(),
          },
        }))
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

// Streaming fetch requests bypass Axios interceptors, so expose the same
// refresh policy without duplicating refresh-token rotation logic.
export async function getValidAccessToken() {
  const token = getAccessToken()
  if (!token) {
    if (!getRefreshToken()) return null
    const refreshed = await refreshAccessToken()
    if (refreshed) return refreshed
    clearAuthStorage()
    notifyAuthExpired()
    return null
  }

  let expiresAt = 0
  try {
    const payload = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
    const decoded = JSON.parse(atob(payload.padEnd(Math.ceil(payload.length / 4) * 4, '=')))
    expiresAt = Number(decoded.exp || 0) * 1000
  } catch {
    expiresAt = 0
  }

  if (expiresAt > Date.now() + 60_000) return token
  const refreshed = await refreshAccessToken()
  if (refreshed) return refreshed
  clearAuthStorage()
  notifyAuthExpired()
  return null
}

api.interceptors.request.use(
  (config) => {
    activeRequests += 1
    if (activeRequests === 1) NProgress.start()
    const accessToken = getAccessToken()
    if (accessToken) {
      config.headers = config.headers || {}
      config.headers.Authorization = `Bearer ${accessToken}`
    }

    config.metadata = { startedAt: performance.now() }
    window.dispatchEvent(
      new CustomEvent('so-iam-api-log', {
        detail: {
          phase: 'request',
          method: config.method?.toUpperCase(),
          url: safeLogUrl(config.baseURL, config.url),
          startedAt: Date.now(),
        },
      }),
    )

    if (import.meta.env.DEV) {
      console.group('🔐 API REQUEST')
      console.log('➡️ Method:', config.method?.toUpperCase())
      console.log('🌐 URL:', `${config.baseURL || ''}${config.url || ''}`)
      console.log('🔑 Has Access Token:', Boolean(accessToken))
      console.log(
        '🪪 Authorization:',
        config.headers?.Authorization ? 'Bearer ********' : '❌ Missing',
      )
      console.groupEnd()
    }

    return config
  },
  (error) => Promise.reject(error),
)

api.interceptors.response.use(
  (response) => {
    const duration = response.config?.metadata?.startedAt
      ? Math.round(performance.now() - response.config.metadata.startedAt)
      : null
    window.dispatchEvent(
      new CustomEvent('so-iam-api-log', {
        detail: {
          phase: 'response',
          method: response.config?.method?.toUpperCase(),
          url: safeLogUrl(response.config?.baseURL, response.config?.url),
          status: response.status,
          duration,
        },
      }),
    )
    if (import.meta.env.DEV) {
      console.group('📥 API RESPONSE')
      console.log('✅ Status:', response.status)
      console.log('🌐 URL:', response.config?.url)
      console.groupEnd()
    }
    activeRequests = Math.max(0, activeRequests - 1)
    if (activeRequests === 0) NProgress.done()
    return response
  },
  async (error) => {
    activeRequests = Math.max(0, activeRequests - 1)
    if (activeRequests === 0) NProgress.done()

    const status = error.response?.status
    const originalRequest = error.config
    const duration = originalRequest?.metadata?.startedAt
      ? Math.round(performance.now() - originalRequest.metadata.startedAt)
      : null
    window.dispatchEvent(
      new CustomEvent('so-iam-api-log', {
        detail: {
          phase: 'error',
          method: originalRequest?.method?.toUpperCase(),
          url: safeLogUrl(originalRequest?.baseURL, originalRequest?.url),
          status: status || 0,
          // Never forward response bodies or request payloads to UI telemetry.
          error: error.code === 'ECONNABORTED' ? 'Request timed out' : (error.response ? 'API request failed' : 'Network request failed'),
          duration,
        },
      }),
    )

    if (import.meta.env.DEV) {
      console.group('🚨 API ERROR')
      console.log('❌ Status:', status)
      console.log('🌐 URL:', originalRequest?.url)
      console.error('📦 Response status:', status)
      console.groupEnd()
    }

    const requestPath = String(originalRequest?.url || '').replace(/^\/+/, '')
    const isRefreshRequest = requestPath === 'users/refresh/' || requestPath.endsWith('/users/refresh/')

    // Refresh requests are sent with the bare Axios client above. Exclude any
    // explicit refresh endpoint call from the interceptor to prevent recursive
    // refresh attempts when the refresh token itself is expired/blacklisted.
    if (status === 401 && originalRequest && !originalRequest._retry && !isRefreshRequest) {
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
