/**
 * Canonical API and WebSocket URL configuration for SO_IAM_OS.
 *
 * Accepts either VITE_API_BASE_URL (with or without /api) or VITE_API_URL
 * so development and production environments resolve one consistent origin
 * without duplicating /api.
 */

const DEFAULT_API_ORIGIN = 'http://127.0.0.1:8000'

function stripTrailingSlashes(value) {
  return String(value || '').trim().replace(/\/+$/, '')
}

export function resolveApiRoot(rawBase = import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL) {
  const cleaned = stripTrailingSlashes(rawBase)
  if (!cleaned) return DEFAULT_API_ORIGIN
  return cleaned.replace(/\/api$/i, '') || DEFAULT_API_ORIGIN
}

export function resolveApiBaseUrl(rawBase = import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL) {
  const cleaned = stripTrailingSlashes(rawBase)
  if (!cleaned) return `${DEFAULT_API_ORIGIN}/api`
  if (/^\/api$/i.test(cleaned)) return '/api'
  return /\/api$/i.test(cleaned) ? cleaned : `${cleaned}/api`
}

export function resolveWsBaseUrl(apiRoot = API_ROOT_URL) {
  const explicitWs = stripTrailingSlashes(import.meta.env.VITE_WS_BASE_URL)
  if (explicitWs) return explicitWs
  const debugWs = stripTrailingSlashes(import.meta.env.VITE_DEBUG_WS_URL)
  if (debugWs) {
    try {
      const parsed = new URL(debugWs)
      return `${parsed.protocol}//${parsed.host}`
    } catch {
      /* fall through to HTTP-derived WS origin */
    }
  }
  if (/^https?:/i.test(apiRoot)) {
    return apiRoot.replace(/^http/i, 'ws')
  }
  if (typeof window !== 'undefined' && window.location?.host) {
    const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    return `${proto}//${window.location.host}`
  }
  return 'ws://127.0.0.1:8000'
}

export const API_ROOT_URL = resolveApiRoot()
export const API_BASE_URL = resolveApiBaseUrl()
export const WS_BASE_URL = resolveWsBaseUrl(API_ROOT_URL)
export const DEBUG_WS_URL =
  stripTrailingSlashes(import.meta.env.VITE_DEBUG_WS_URL) || `${WS_BASE_URL}/ws/debug/`
