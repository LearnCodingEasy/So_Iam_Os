// composables/useAI.js
import { ref } from 'vue'
import AIService from '@/services/AIService'

export function useAI() {
  const response = ref('')
  const isLoading = ref(false)
  const error = ref(null)

  async function chatStream(messages, model = 'phi') {
    response.value = ''
    isLoading.value = true
    error.value = null

    try {
      await AIService.chatStream(messages, model, (fullText) => {
        // 1. نقسم النص لأسطر
        const lines = fullText.split('\n')
        let combinedContent = ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6).trim()
            if (dataStr === '[DONE]') continue

            try {
              const parsed = JSON.parse(dataStr)
              if (parsed.token) combinedContent += parsed.token
              if (parsed.error) throw new Error(parsed.error)
            } catch (e) {
              console.log('e: ', e)
              // تجاهل الأسطر غير المكتملة في الـ Stream
            }
          }
        }
        response.value = combinedContent
      })
    } catch (e) {
      error.value = e.response?.data?.error || e.message
      console.error('AI Error:', e)
    } finally {
      isLoading.value = false
    }
  }

  return { response, isLoading, error, chatStream }
}
