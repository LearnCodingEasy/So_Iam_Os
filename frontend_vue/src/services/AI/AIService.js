import api, { getValidAccessToken } from '../Shared/api'
import { endpoints } from '../Shared/endpoints'
import { consumeSSEStream } from './sse'

function buildPayload(messages, model = '', options = {}) {
  const history = Array.isArray(messages) ? messages : []
  const latestUser = [...history]
    .reverse()
    .find((item) => item?.role === 'user' && item?.content?.trim())
  if (!latestUser) throw new Error('Enter a user message before sending.')
  const payload = { message: latestUser.content.trim() }
  if (options.conversationId != null) payload.conversation_id = options.conversationId
  if (model) payload.model = model
  if (options.provider) payload.provider = options.provider
  const systemMessage = history.find((item) => item?.role === 'system' && item?.content?.trim())
  if (options.systemPrompt || systemMessage?.content)
    payload.system_prompt = (options.systemPrompt || systemMessage.content).slice(0, 8000)
  if (Number.isFinite(Number(options.temperature)))
    payload.temperature = Math.min(2, Math.max(0, Number(options.temperature)))
  if (Number.isFinite(Number(options.maxTokens)))
    payload.max_tokens = Math.max(1, Math.floor(Number(options.maxTokens)))
  if (options.idempotencyKey) payload.idempotency_key = options.idempotencyKey
  // Per-request timeout (seconds). The server validates the bounds and is authoritative.
  if (Number.isFinite(Number(options.timeoutSeconds)) && Number(options.timeoutSeconds) > 0)
    payload.timeout = Math.floor(Number(options.timeoutSeconds))
  return payload
}

// Client-side HTTP timeout must outlast the server-side AI timeout (+ fallback window),
// otherwise Axios aborts a request that Django is still legitimately processing.
export function clientTimeoutMs(timeoutSeconds) {
  const t = Number(timeoutSeconds)
  return Number.isFinite(t) && t > 0 ? Math.floor(t + 45) * 1000 : 180000
}

export default {
  async chat(messages, model = '', options = {}) {
    try {
      const { data } = await api.post(endpoints.ai.chat, buildPayload(messages, model, options), {
        timeout: clientTimeoutMs(options.timeoutSeconds),
        signal: options.signal,
      })
      if (data?.success === false) {
        const error = new Error(data.error || 'AI request failed.')
        error.code = data.error_code || 'ai_request_failed'
        error.retryable = Boolean(data.retryable)
        throw error
      }
      return data
    } catch (error) {
      const body = error?.response?.data
      if (body?.error_code) error.code = body.error_code
      if (body?.retryable !== undefined) error.retryable = Boolean(body.retryable)
      throw error
    }
  },

  async chatStream(messages, model = '', onChunk, options = {}) {
    const payload = buildPayload(messages, model, options)
    const accessToken = await getValidAccessToken()
    if (!accessToken) throw new Error('انتهت جلسة الدخول. يرجى تسجيل الدخول مرة أخرى.')

    const baseURL = String(api.defaults.baseURL || '').replace(/\/+$/, '')
    const streamPath = endpoints.ai.chatStream.startsWith('/')
      ? endpoints.ai.chatStream
      : `/${endpoints.ai.chatStream}`
    const response = await fetch(`${baseURL}${streamPath}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'text/event-stream, application/json',
        Authorization: `Bearer ${accessToken}`,
        ...(payload.idempotency_key ? { 'Idempotency-Key': payload.idempotency_key } : {}),
      },
      body: JSON.stringify(payload),
      signal: options.signal,
      cache: 'no-store',
    })

    if (!response.ok) {
      let body = {}
      try {
        body = await response.json()
      } catch {
        /* response may not be JSON */
      }
      const error = new Error(
        body.error || body.detail || `AI streaming request failed (${response.status}).`,
      )
      error.status = response.status
      error.code = body.error_code || body.code || 'stream_http_error'
      error.retryable = Boolean(body.retryable)
      throw error
    }

    const contentType = response.headers.get('content-type') || ''
    if (!contentType.includes('text/event-stream') || !response.body) {
      const body = await response.json()
      if (body?.success === false) throw new Error(body.error || 'AI request failed.')
      const content = body?.message?.content || ''
      if (content && typeof onChunk === 'function') onChunk(content)
      return body
    }

    const result = {
      success: true,
      conversation_id: null,
      provider: null,
      model: null,
      message: { id: null, role: 'assistant', content: '' },
    }
    await consumeSSEStream(response.body, (event) => {
      if (event.type === 'meta') {
        result.conversation_id = event.data.conversation_id ?? result.conversation_id
        result.provider = event.data.provider ?? result.provider
        result.model = event.data.model ?? result.model
      } else if (event.type === 'delta') {
        const delta = event.data.delta || ''
        result.message.content += delta
        if (delta && typeof onChunk === 'function') onChunk(delta)
      } else if (event.type === 'done') {
        result.message.id = event.data.message_id ?? result.message.id
        if (typeof event.data.content === 'string') result.message.content = event.data.content
      } else if (event.type === 'error') {
        const error = new Error(event.data.error || 'AI streaming failed.')
        error.code = event.data.error_code || 'stream_error'
        error.retryable = Boolean(event.data.retryable)
        throw error
      }
    })

    if (!result.message.content.trim())
      throw new Error('عاد الخادم باستجابة فارغة من مزود الذكاء الاصطناعي.')
    result.message.provider = result.provider
    result.message.model = result.model
    return result
  },

  listModels(provider = 'ollama', force = false) {
    return api.get(`${endpoints.ai.providerModels(provider)}${force ? '?refresh=1' : ''}`)
  },
  health() {
    return api.get(endpoints.ai.health)
  },
  capabilities() {
    return api.get(endpoints.ai.capabilities)
  },
}
