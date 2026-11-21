import AIService from './AIService'
import api from '../Shared/api'
import { endpoints } from '../Shared/endpoints'

export const sendMessage = async ({ message, conversation_id = null, provider = null, model = '', ...options }) => {
  return AIService.chat([{ role: 'user', content: message }], model, {
    conversationId: conversation_id,
    provider,
    ...options,
  })
}

export const streamMessage = async ({ message, conversation_id = null, provider = null, model = '', onChunk, signal, ...options }) => {
  return AIService.chatStream([{ role: 'user', content: message }], model, onChunk, {
    conversationId: conversation_id,
    provider,
    signal,
    ...options,
  })
}

export const getConversations = async () => (await api.get(endpoints.ai.conversations)).data
export const getConversation = async (id) => (await api.get(endpoints.ai.conversation(id))).data
export const createConversation = async (payload = {}) => (await api.post(endpoints.ai.conversations, payload)).data
export const deleteConversation = async (id) => { await api.delete(endpoints.ai.conversation(id)); return true }
export const getAIHealth = async () => (await api.get(endpoints.ai.health)).data
export const getAICapabilities = async () => (await api.get(endpoints.ai.capabilities)).data

export default { sendMessage, streamMessage, getConversations, getConversation, createConversation, deleteConversation, getAIHealth, getAICapabilities }
