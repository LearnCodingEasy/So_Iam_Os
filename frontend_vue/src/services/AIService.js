import api from './api'
import { endpoints } from './endpoints'

/**
 * The backend currently exposes a JSON chat endpoint, not an SSE endpoint.
 * Keep the historical chatStream method name for callers, but make no claim
 * that the response is streamed; it resolves when the real API returns.
 */
export default {
  async chat(messages, model = '', { conversationId = null, systemPrompt = '', temperature, signal } = {}) {
    const history = Array.isArray(messages) ? messages : []
    const latestUser = [...history].reverse().find((item) => item?.role === 'user' && item?.content?.trim())
    if (!latestUser) throw new Error('Enter a user message before sending.')

    const payload = { message: latestUser.content.trim() }
    if (conversationId !== null) payload.conversation_id = conversationId
    if (model) { payload.model = model; payload.provider = 'ollama' }
    const systemMessage = history.find((item) => item?.role === 'system' && item?.content?.trim())
    if (systemPrompt || systemMessage?.content) payload.system_prompt = (systemPrompt || systemMessage.content).slice(0, 8000)
    if (Number.isFinite(Number(temperature))) payload.temperature = Math.min(2, Math.max(0, Number(temperature)))

    const { data } = await api.post(endpoints.ai.chat, payload, { timeout: 120000, signal })
    if (data?.success === false) throw new Error(data.error || 'AI request failed.')
    return data
  },

  async chatStream(messages, model = '', onChunk, options = {}) {
    const data = await this.chat(messages, model, options)
    const content = data?.message?.content || ''
    if (typeof onChunk === 'function') onChunk(content)
    return data
  },

  listModels(provider = 'ollama') {
    return api.get(endpoints.ai.providerModels(provider))
  },
}
