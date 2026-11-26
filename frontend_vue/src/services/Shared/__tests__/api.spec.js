import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import axios from 'axios'
import { resolveApiBaseUrl, resolveApiRoot, resolveWsBaseUrl } from '../apiConfig'
import api, { getValidAccessToken } from '../api'
import axiosInstanceAlias from '../axiosInstance'

function makeJwt(expOffsetSeconds) {
  const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }))
  const payload = btoa(JSON.stringify({ exp: Math.floor(Date.now() / 1000) + expOffsetSeconds }))
  return `${header}.${payload}.sig`
}

describe('apiConfig and shared api client', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.restoreAllMocks()
  })

  afterEach(() => {
    localStorage.clear()
    vi.restoreAllMocks()
  })

  it('normalizes api root, /api baseURL, and websocket URL without duplicating /api', () => {
    expect(resolveApiRoot('http://127.0.0.1:8000')).toBe('http://127.0.0.1:8000')
    expect(resolveApiRoot('http://127.0.0.1:8000/api/')).toBe('http://127.0.0.1:8000')
    expect(resolveApiBaseUrl('http://127.0.0.1:8000')).toBe('http://127.0.0.1:8000/api')
    expect(resolveApiBaseUrl('http://127.0.0.1:8000/api/')).toBe('http://127.0.0.1:8000/api')
    expect(resolveWsBaseUrl('https://os.example.com')).toBe('wss://os.example.com')
  })

  it('aliases axiosInstance directly to the canonical api client', () => {
    expect(axiosInstanceAlias).toBe(api)
  })

  it('attaches Bearer token for authenticated requests and omits it when unauthenticated', async () => {
    const adapter = vi.fn(async (config) => ({
      data: { ok: true },
      status: 200,
      statusText: 'OK',
      headers: {},
      config,
    }))

    await api.get('/goals/', { adapter })
    expect(adapter.mock.calls[0][0].headers.Authorization).toBeUndefined()

    const access = makeJwt(600)
    localStorage.setItem('user.access', access)
    await api.get('/goals/', { adapter })
    expect(adapter.mock.calls[1][0].headers.Authorization).toBe(`Bearer ${access}`)
  })

  it('deduplicates concurrent refreshes and persists rotated access + refresh tokens', async () => {
    const expired = makeJwt(-30)
    const freshAccess = makeJwt(900)
    const freshRefresh = makeJwt(86400)
    localStorage.setItem('user.access', expired)
    localStorage.setItem('user.refresh', 'old-refresh')

    const postSpy = vi.spyOn(axios, 'post').mockResolvedValue({
      data: { access: freshAccess, refresh: freshRefresh },
    })

    const [t1, t2] = await Promise.all([getValidAccessToken(), getValidAccessToken()])
    expect(t1).toBe(freshAccess)
    expect(t2).toBe(freshAccess)
    expect(postSpy).toHaveBeenCalledTimes(1)
    expect(localStorage.getItem('user.access')).toBe(freshAccess)
    expect(localStorage.getItem('user.refresh')).toBe(freshRefresh)
  })

  it('clears tokens and emits so-iam-auth-expired when refresh fails', async () => {
    localStorage.setItem('user.access', makeJwt(-30))
    localStorage.setItem('user.refresh', 'bad-refresh')

    const expiredListener = vi.fn()
    window.addEventListener('so-iam-auth-expired', expiredListener)
    vi.spyOn(axios, 'post').mockRejectedValue(new Error('401'))

    const token = await getValidAccessToken()
    expect(token).toBeNull()
    expect(localStorage.getItem('user.access')).toBeNull()
    expect(localStorage.getItem('user.refresh')).toBeNull()
    expect(expiredListener).toHaveBeenCalledTimes(1)
    window.removeEventListener('so-iam-auth-expired', expiredListener)
  })
})
