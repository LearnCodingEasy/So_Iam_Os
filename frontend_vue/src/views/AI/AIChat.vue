<template>
  <div class="ai-page">
    <!-- =====================================================
         SIDEBAR
    ====================================================== -->
    <aside class="ai-sidebar" :class="{ collapsed: sidebarCollapsed }">
      <!-- Sidebar Header -->
      <div class="sidebar-header">
        <div v-if="!sidebarCollapsed" class="brand">
          <div class="brand-icon">🤖</div>

          <div>
            <h2>AI Core</h2>
            <span>So_Iam_OS</span>
          </div>
        </div>

        <button class="icon-button" type="button" @click="sidebarCollapsed = !sidebarCollapsed">
          {{ sidebarCollapsed ? '→' : '←' }}
        </button>
      </div>

      <!-- New Conversation -->
      <button
        v-if="!sidebarCollapsed"
        class="new-chat-button"
        type="button"
        @click="startNewConversation"
      >
        <span>＋</span>
        New Conversation
      </button>

      <!-- Conversations -->
      <div v-if="!sidebarCollapsed" class="conversations">
        <div class="section-title">Conversations</div>

        <!-- Loading -->
        <div v-if="loadingConversations" class="empty-state">Loading...</div>

        <!-- Empty -->
        <div v-else-if="conversations.length === 0" class="empty-state">No conversations yet.</div>

        <!-- Conversation List -->
        <button
          v-for="conversation in conversations"
          :key="conversation.id"
          type="button"
          class="conversation-item"
          :class="{
            active: conversation.id === activeConversationId,
          }"
          @click="selectConversation(conversation.id)"
        >
          <div class="conversation-main">
            <span class="conversation-icon"> 💬 </span>

            <span class="conversation-title">
              {{ conversation.title || `Conversation #${conversation.id}` }}
            </span>
          </div>

          <span
            class="delete-button"
            title="Archive conversation"
            @click.stop="archiveConversation(conversation.id)"
          >
            ×
          </span>
        </button>
      </div>
    </aside>

    <!-- =====================================================
         MAIN CHAT
    ====================================================== -->
    <main class="chat-container">
      <!-- Header -->
      <header class="chat-header">
        <div class="chat-header-info">
          <div class="ai-avatar">🤖</div>

          <div>
            <h1>
              {{ activeConversationTitle }}
            </h1>

            <span class="status">
              <span class="status-dot"></span>
              AI Core Online
            </span>
          </div>
        </div>

        <button class="header-button" type="button" @click="startNewConversation">
          ＋ New Chat
        </button>
      </header>

      <!-- =====================================================
           MESSAGES
      ====================================================== -->
      <section ref="messagesContainer" class="messages-container">
        <!-- Welcome -->
        <div v-if="messages.length === 0 && !sending" class="welcome">
          <div class="welcome-icon">🤖</div>

          <h2>How can I help you?</h2>

          <p>
            أنا الـ AI Core الخاص بـ So_Iam_OS.
            <br />
            اسألني عن التعلم، البرمجة، المشاريع، التخطيط أو أي شيء تحتاجه.
          </p>

          <div class="suggestions">
            <button type="button" @click="useSuggestion('عايز أتعلم Django')">
              📚 عايز أتعلم Django
            </button>

            <button type="button" @click="useSuggestion('ساعدني أعمل خطة لتعلم Python')">
              🐍 خطة تعلم Python
            </button>

            <button type="button" @click="useSuggestion('ساعدني في تطوير مشروعي')">
              🚀 تطوير مشروعي
            </button>
          </div>
        </div>

        <!-- =====================================================
             MESSAGE LIST
        ====================================================== -->
        <div
          v-for="message in messages"
          :key="message.id || `${message.role}-${message.content}`"
          class="message-row"
          :class="message.role"
        >
          <!-- Assistant Avatar -->
          <div v-if="message.role === 'assistant'" class="message-avatar">🤖</div>

          <div class="message-content">
            <div class="message-role">
              {{ message.role === 'assistant' ? 'AI Core' : 'You' }}
            </div>

            <div class="message-bubble">
              {{ message.content }}
            </div>

            <div v-if="message.model" class="message-meta">
              {{ message.provider }} · {{ message.model }}
            </div>
          </div>
        </div>

        <!-- =====================================================
             LEARNING ACTION RESULT
        ====================================================== -->
        <div v-if="learningAction" class="learning-action-card">
          <div class="learning-action-icon">📚</div>

          <div class="learning-action-content">
            <h3>Learning Plan Created</h3>

            <p v-if="learningResult">
              تم إنشاء خطة تعلم
              <strong>
                {{ learningResult.skill?.name || 'جديدة' }}
              </strong>
              بنجاح.
            </p>

            <p v-else>تم تنفيذ إجراء التعلم بنجاح.</p>

            <RouterLink to="/learning" class="learning-action-button"> افتح Learning → </RouterLink>
          </div>
        </div>

        <!-- =====================================================
             SENDING
        ====================================================== -->
        <div v-if="sending" class="message-row assistant">
          <div class="message-avatar">🤖</div>

          <div class="message-content">
            <div class="message-role">AI Core</div>

            <div class="message-bubble typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </section>

      <!-- =====================================================
           ERROR
      ====================================================== -->
      <div v-if="errorMessage" class="error-box">
        <span>⚠️</span>

        {{ errorMessage }}

        <button type="button" @click="errorMessage = ''">×</button>
      </div>

      <!-- =====================================================
           INPUT
      ====================================================== -->
      <form class="chat-input-area" @submit.prevent="send">
        <!-- ⭐ هنا المكان اللي بتكتب فيه -->
        <textarea
          v-model="inputMessage"
          :disabled="sending"
          placeholder="اكتب ما تحتاجه هنا..."
          rows="1"
          @keydown.enter.exact.prevent="send"
          @keydown.enter.shift.exact.stop
        ></textarea>
        <div class="ai-controls">
          <!-- Provider -->
          <select v-model="selectedProvider">
            <option
              v-for="provider in providerOptions"
              :key="provider.value"
              :value="provider.value"
            >
              {{ provider.icon }}
              {{ provider.label }}
            </option>
          </select>

          <!-- Model -->
          <select v-model="selectedModel">
            <option v-for="model in availableModels" :key="model.value" :value="model.value">
              {{ model.label }}
            </option>
          </select>

          <!-- Status -->
          <span
            class="ai-source"
            :class="{
              local: isLocalAI,
              cloud: !isLocalAI,
            }"
          >
            {{ isLocalAI ? '🟢 Local' : '🔵 Cloud' }}
          </span>
        </div>
        <button class="send-button" type="submit" :disabled="sending || !inputMessage.trim()">
          {{ sending ? '...' : '➤' }}
        </button>
      </form>

      <div class="input-hint">Enter للإرسال · Shift + Enter لسطر جديد</div>
    </main>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'

import {
  sendMessage,
  getConversations,
  getConversation,
  createConversation,
  deleteConversation,
} from '@/services/ai'

// ============================================================
// STATE
// ============================================================

const conversations = ref([])

const messages = ref([])

const activeConversationId = ref(null)

const inputMessage = ref('')

const sending = ref(false)

const loadingConversations = ref(false)

const errorMessage = ref('')

const sidebarCollapsed = ref(false)

const messagesContainer = ref(null)

// ============================================================
// LEARNING ACTION STATE
// ============================================================

const learningAction = ref(null)

const learningResult = ref(null)

const selectedProvider = ref('ollama')

const selectedModel = ref('phi:latest')

const providerOptions = [
  {
    value: 'ollama',
    label: 'Local',
    icon: '🟢',
  },
  {
    value: 'openrouter',
    label: 'Cloud',
    icon: '🔵',
  },
]

const localModels = [
  {
    value: 'phi:latest',
    label: 'Phi',
  },
  {
    value: 'gemma3:4b',
    label: 'Gemma 3 4B',
  },
]

const cloudModels = [
  {
    value: 'openai/gpt-4o-mini',
    label: 'OpenRouter Model',
  },
]

const availableModels = computed(() => {
  return selectedProvider.value === 'ollama' ? localModels : cloudModels
})

const isLocalAI = computed(() => {
  return selectedProvider.value === 'ollama'
})

// ============================================================
// COMPUTED
// ============================================================

const activeConversation = computed(() => {
  return conversations.value.find((conversation) => conversation.id === activeConversationId.value)
})

const activeConversationTitle = computed(() => {
  if (activeConversation.value?.title) {
    return activeConversation.value.title
  }

  return 'AI Core'
})

// ============================================================
// LOAD CONVERSATIONS
// ============================================================

const loadConversations = async () => {
  loadingConversations.value = true

  errorMessage.value = ''

  try {
    const data = await getConversations()

    conversations.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    console.error('Failed to load AI conversations:', error)

    errorMessage.value = error.response?.data?.detail || 'Unable to load conversations.'
  } finally {
    loadingConversations.value = false
  }
}

// ============================================================
// LOAD CONVERSATION
// ============================================================

const selectConversation = async (conversationId) => {
  if (sending.value) {
    return
  }

  errorMessage.value = ''

  learningAction.value = null

  learningResult.value = null

  try {
    const conversation = await getConversation(conversationId)

    activeConversationId.value = conversation.id

    messages.value = conversation.messages || []

    await scrollToBottom()
  } catch (error) {
    console.error('Failed to load conversation:', error)

    errorMessage.value = error.response?.data?.detail || 'Unable to load conversation.'
  }
}

// ============================================================
// NEW CONVERSATION
// ============================================================

const startNewConversation = async () => {
  if (sending.value) {
    return
  }

  errorMessage.value = ''

  learningAction.value = null

  learningResult.value = null

  activeConversationId.value = null

  messages.value = []

  inputMessage.value = ''

  try {
    const conversation = await createConversation()

    conversations.value.unshift(conversation)

    activeConversationId.value = conversation.id

    messages.value = conversation.messages || []
  } catch (error) {
    console.error('Failed to create conversation:', error)

    errorMessage.value = error.response?.data?.detail || 'Unable to create a new conversation.'
  }
}

// ============================================================
// ARCHIVE CONVERSATION
// ============================================================

const archiveConversation = async (conversationId) => {
  try {
    await deleteConversation(conversationId)

    conversations.value = conversations.value.filter(
      (conversation) => conversation.id !== conversationId,
    )

    if (activeConversationId.value === conversationId) {
      activeConversationId.value = null

      messages.value = []

      learningAction.value = null

      learningResult.value = null
    }
  } catch (error) {
    console.error('Failed to archive conversation:', error)

    errorMessage.value = error.response?.data?.detail || 'Unable to archive conversation.'
  }
}

// ============================================================
// SEND MESSAGE
// ============================================================

const send = async () => {
  const message = inputMessage.value.trim()

  if (!message || sending.value) {
    return
  }

  errorMessage.value = ''

  learningAction.value = null

  learningResult.value = null

  // ----------------------------------------------------------
  // Current conversation
  // ----------------------------------------------------------

  const previousConversationId = activeConversationId.value

  // ----------------------------------------------------------
  // Temporary user message
  // ----------------------------------------------------------

  const temporaryUserMessage = {
    id: `temp-${Date.now()}`,

    role: 'user',

    content: message,
  }

  messages.value.push(temporaryUserMessage)

  inputMessage.value = ''

  sending.value = true

  await scrollToBottom()

  try {
    // --------------------------------------------------------
    // Send to Django
    // --------------------------------------------------------

    const response = await sendMessage({
      message,
      conversation_id: previousConversationId,
      provider: selectedProvider.value,
      model: selectedModel.value,
    })

    // --------------------------------------------------------
    // Conversation
    // --------------------------------------------------------

    activeConversationId.value = response.conversation_id

    // --------------------------------------------------------
    // Assistant message
    // --------------------------------------------------------

    if (response.message) {
      messages.value.push(response.message)
    }

    // --------------------------------------------------------
    // Learning Action
    // --------------------------------------------------------

    if (response.learning_action) {
      learningAction.value = response.learning_action
    }

    // --------------------------------------------------------
    // Learning Result
    // --------------------------------------------------------

    if (response.learning) {
      learningResult.value = response.learning
    }

    // --------------------------------------------------------
    // Refresh conversations
    // --------------------------------------------------------

    await loadConversations()

    await scrollToBottom()
  } catch (error) {
    console.error('AI message failed:', error)

    // Remove temporary message

    messages.value = messages.value.filter((item) => item.id !== temporaryUserMessage.id)

    errorMessage.value =
      error.response?.data?.error ||
      error.response?.data?.detail ||
      'AI Core could not process your request.'
  } finally {
    sending.value = false

    await scrollToBottom()
  }
}

// ============================================================
// SUGGESTIONS
// ============================================================

const useSuggestion = (text) => {
  inputMessage.value = text

  nextTick(() => {
    const textarea = document.querySelector('.chat-input-area textarea')

    textarea?.focus()
  })
}

// ============================================================
// SCROLL
// ============================================================

const scrollToBottom = async () => {
  await nextTick()

  const container = messagesContainer.value

  if (!container) {
    return
  }

  container.scrollTop = container.scrollHeight
}

// ============================================================
// INITIALIZATION
// ============================================================

onMounted(async () => {
  await loadConversations()
})
</script>
