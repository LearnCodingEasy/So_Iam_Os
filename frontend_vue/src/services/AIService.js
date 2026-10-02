// services/AIService.js
import api from './api'

export default {
  chatStream(messages, model = 'phi', onChunk) {
    return api.post(
      'ai/chat/stream/',
      { messages, model },
      {
        responseType: 'text',
        headers: {
          Accept: 'text/event-stream',
        },
        onDownloadProgress: (progressEvent) => {
          const rawResponse = progressEvent.event.target.responseText
          const rawText = progressEvent.event.target.responseText
          onChunk(rawText)
          console.log('rawResponse: ', rawResponse)
        },
      },
    )
  },

  listModels() {
    return api.get('ai/models/')
  },
}
