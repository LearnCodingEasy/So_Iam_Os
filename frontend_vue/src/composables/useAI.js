import { ref } from 'vue'
import AIService from '@/services/AI/AIService'

export function useAI() {
  const response = ref('')
  const isLoading = ref(false)
  const error = ref(null)
  const conversationId = ref(null)
  let activeController = null

  async function chatStream(messages, model = '', options = {}) {
    response.value = ''
    isLoading.value = true
    error.value = null
    activeController = new AbortController()
    try {
      const result = await AIService.chatStream(
        messages,
        model,
        (chunk) => {
          response.value += chunk
        },
        {
          conversationId: conversationId.value,
          systemPrompt: options.systemPrompt || '',
          temperature: options.temperature,
          provider: options.provider || '',
          maxTokens: options.maxTokens,
          idempotencyKey: options.idempotencyKey || '',
          signal: activeController.signal,
        },
      )
      conversationId.value = result.conversation_id ?? conversationId.value
      if (result.message?.content && !response.value) response.value = result.message.content
      return result
    } catch (e) {
      error.value =
        e?.response?.data?.error || e?.response?.data?.detail || e.message || 'AI request failed.'
      return null
    } finally {
      isLoading.value = false
      activeController = null
    }
  }

  function stopStream() {
    if (activeController) activeController.abort()
  }

  function resetConversation() {
    stopStream()
    conversationId.value = null
    response.value = ''
    error.value = null
  }

  return { response, isLoading, error, conversationId, chatStream, stopStream, resetConversation }
}
