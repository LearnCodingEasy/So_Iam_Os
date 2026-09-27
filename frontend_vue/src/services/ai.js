import api from './api'
import { endpoints } from './endpoints'

// ============================================================
// SEND MESSAGE
// ============================================================

export const sendMessage = async ({
  message,
  conversation_id = null,
  provider = null,
  model = '',
}) => {
  const payload = {
    message,
  }

  if (conversation_id !== null) {
    payload.conversation_id = conversation_id
  }

  if (provider) {
    payload.provider = provider
  }

  if (model) {
    payload.model = model
  }

  const response = await api.post(endpoints.ai.chat, payload)

  return response.data
}

// ============================================================
// CONVERSATIONS
// ============================================================

export const getConversations = async () => {
  const response = await api.get(endpoints.ai.conversations)

  return response.data
}

export const getConversation = async (conversationId) => {
  const response = await api.get(endpoints.ai.conversation(conversationId))

  return response.data
}

export const createConversation = async ({ title = '', provider = null, model = '' } = {}) => {
  const payload = {
    title,
  }

  if (provider) {
    payload.provider = provider
  }

  if (model) {
    payload.model = model
  }

  const response = await api.post(endpoints.ai.conversations, payload)

  return response.data
}

export const deleteConversation = async (conversationId) => {
  await api.delete(endpoints.ai.conversation(conversationId))

  return true
}

export default {
  sendMessage,
  getConversations,
  getConversation,
  createConversation,
  deleteConversation,
}
