<!-- ============================================================
  🧠 AIChat.vue
  بيستخدم نفس naming convention الـ main.js (prime_xxx)
  ============================================================ -->

<template>
  <div class="ai-chat-wrapper">
    <!-- ════════════════════════════════════════════
      🔧 SIDEBAR — إعدادات متقدمة
    ════════════════════════════════════════════ -->
    <prime_drawer
      :visible="showSettings"
      header="⚙️ إعدادات المحادثة"
      position="right"
      style="width: 420px"
    >
      <!-- 🤖 تعريف دور الـ AI -->
      <prime_divider align="left">
        <span class="section-label">🤖 تعريف دور الـ AI</span>
      </prime_divider>

      <!-- 📋 قوالب جاهزة -->
      <div class="templates-grid">
        <prime_chip
          v-for="tpl in systemTemplates"
          :key="tpl.label"
          :label="tpl.label"
          :icon="tpl.icon"
          class="template-chip"
          @click="applyTemplate(tpl)"
          v-tooltip.top="tpl.preview"
        />
      </div>

      <!-- ✏️ System Prompt يدوي -->
      <prime_textarea
        v-model="systemPrompt"
        rows="5"
        placeholder="مثال: أنت مطور Vue.js خبير. أجب بشكل مختصر ومنظم مع أمثلة كود..."
        class="w-full mt-3"
        :auto-resize="true"
      />

      <!-- 🏗️ Prompt Engineering Builder -->
      <prime_divider align="left" class="mt-4">
        <span class="section-label">🏗️ بناء Prompt احترافي</span>
      </prime_divider>

      <div class="prompt-builder">
        <prime_float_label class="w-full mb-3">
          <prime_input_text id="role-input" v-model="promptBuilder.role" class="w-full" />
          <label for="role-input">👤 الدور (Act as...)</label>
        </prime_float_label>

        <prime_float_label class="w-full mb-3">
          <prime_input_text id="task-input" v-model="promptBuilder.task" class="w-full" />
          <label for="task-input">🎯 المطلوب (Task)</label>
        </prime_float_label>

        <prime_float_label class="w-full mb-3">
          <prime_textarea
            id="context-input"
            v-model="promptBuilder.context"
            rows="2"
            class="w-full"
          />
          <label for="context-input">📌 السياق (Context)</label>
        </prime_float_label>

        <prime_float_label class="w-full mb-3">
          <prime_input_text id="structure-input" v-model="promptBuilder.structure" class="w-full" />
          <label for="structure-input">📐 الهيكل (Structure)</label>
        </prime_float_label>

        <prime_button
          label="🪄 ابنيلي الـ Prompt"
          severity="secondary"
          class="w-full"
          @click="buildPrompt"
        />

        <div v-if="builtPrompt" class="built-prompt mt-3">
          <p class="built-label">✅ Prompt جاهز للإرسال:</p>
          <pre class="built-text">{{ builtPrompt }}</pre>
          <prime_button label="📋 انسخ وأرسل" size="small" @click="sendBuiltPrompt" />
        </div>
      </div>

      <!-- 🛡️ إعدادات إضافية -->
      <prime_divider align="left" class="mt-4">
        <span class="section-label">🛡️ إعدادات إضافية</span>
      </prime_divider>

      <div class="extra-settings">
        <label class="setting-label">🌡️ الإبداعية (Temperature): {{ temperature }}</label>
        <prime_slider v-model="temperature" :min="0" :max="1" :step="0.1" class="w-full mb-3" />

        <label class="setting-label">🧠 احتفظ بسياق المحادثة كاملاً</label>
        <prime_toggle_switch v-model="keepFullHistory" class="mb-3" />

        <prime_button
          label="💾 صدّر المحادثة JSON"
          severity="contrast"
          outlined
          size="small"
          class="w-full"
          @click="exportChat"
        />
      </div>
    </prime_drawer>

    <!-- ════════════════════════════════════════════
      📌 HEADER
    ════════════════════════════════════════════ -->
    <div class="chat-header">
      <div class="header-left">
        <i class="pi pi-bolt header-icon" />
        <span class="header-title">Ollama AI Chat</span>
        <prime_tag :value="selectedModel" severity="info" rounded />
      </div>
      <div class="header-right">
        <prime_badge
          :value="isConnected ? 'متصل' : 'غير متصل'"
          :severity="isConnected ? 'success' : 'danger'"
          class="connection-badge"
        />
        <prime_button
          icon="pi pi-sliders-h"
          text
          rounded
          severity="secondary"
          v-tooltip.bottom="'الإعدادات المتقدمة'"
          @click="showSettings = true"
        />
        <prime_button
          icon="pi pi-trash"
          text
          rounded
          severity="danger"
          v-tooltip.bottom="'مسح المحادثة'"
          @click="clearChat"
        />
      </div>
    </div>

    <!-- ════════════════════════════════════════════
      💬 MESSAGES AREA
    ════════════════════════════════════════════ -->
    <div class="messages-area" ref="messagesContainer">
      <div v-if="systemPrompt" class="system-indicator">
        <i class="pi pi-cog" />
        <span
          >System: {{ systemPrompt.slice(0, 80) }}{{ systemPrompt.length > 80 ? '...' : '' }}</span
        >
        <prime_button icon="pi pi-eye" text size="small" @click="showSettings = true" />
      </div>

      <div v-if="messages.length === 0" class="empty-state">
        <i class="pi pi-comments empty-icon" />
        <p>ابدأ محادثتك مع الـ AI 👋</p>
        <div class="quick-prompts">
          <prime_chip
            v-for="qp in quickPrompts"
            :key="qp"
            :label="qp"
            class="quick-chip"
            @click="useQuickPrompt(qp)"
          />
        </div>
      </div>

      <div v-for="(msg, i) in messages" :key="i" :class="['message-bubble', msg.role]">
        <div class="role-avatar" :class="msg.role">
          <i :class="roleIcon(msg.role)" />
        </div>
        <div class="bubble-content">
          <div class="bubble-header">
            <prime_tag
              :value="roleLabel(msg.role)"
              :severity="roleSeverity(msg.role)"
              size="small"
            />
            <span class="timestamp">{{ msg.time }}</span>
          </div>
          <div class="message-text" v-html="formatMessage(msg.content)" />
        </div>
      </div>

      <!-- 🔄 Streaming -->
      <div v-if="isLoading || currentResponse" class="message-bubble assistant streaming-bubble">
        <div class="role-avatar assistant">
          <i class="pi pi-bolt" />
        </div>
        <div class="bubble-content">
          <div class="bubble-header">
            <prime_tag value="AI" severity="info" size="small" />
            <prime_progress_spinner
              v-if="isLoading"
              style="width: 16px; height: 16px"
              strokeWidth="4"
            />
          </div>
          <div class="message-text" v-html="formatMessage(currentResponse)" />
          <span v-if="isLoading" class="cursor-blink">▋</span>
        </div>
      </div>
    </div>

    <!-- ════════════════════════════════════════════
      ✍️ INPUT AREA
    ════════════════════════════════════════════ -->
    <div class="input-area">
      <div class="tools-row">
        <prime_select
          v-model="selectedModel"
          :options="availableModels"
          optionLabel="label"
          optionValue="value"
          placeholder="اختار الموديل"
          class="model-select"
        >
          <template #option="{ option }">
            <div class="model-option">
              <i class="pi pi-microchip-ai" />
              <span>{{ option.label }}</span>
              <prime_tag :value="option.speed" :severity="option.speedSeverity" size="small" />
            </div>
          </template>
        </prime_select>

        <prime_select_button
          v-model="currentRole"
          :options="roleOptions"
          optionLabel="label"
          optionValue="value"
          class="role-selector"
        />

        <prime_button
          icon="pi pi-sliders-h"
          text
          rounded
          severity="secondary"
          @click="showSettings = true"
          v-tooltip.top="'إعدادات متقدمة'"
        />
      </div>

      <div class="input-row">
        <prime_textarea
          v-model="input"
          :placeholder="inputPlaceholder"
          rows="1"
          :auto-resize="true"
          class="main-input"
          @keydown="handleKeydown"
        />
        <prime_button
          :icon="isLoading ? 'pi pi-stop-circle' : 'pi pi-send'"
          :severity="isLoading ? 'danger' : 'primary'"
          rounded
          class="send-btn"
          @click="isLoading ? stopStream() : send()"
          v-tooltip.top="isLoading ? 'إيقاف' : 'إرسال (Ctrl+Enter)'"
        />
      </div>

      <div class="input-hint">
        <span>Ctrl+Enter للإرسال</span>
        <span v-if="error" class="error-hint">
          <i class="pi pi-exclamation-triangle" /> {{ error }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import { useAI } from '@/composables/useAI'

const { response: currentResponse, isLoading, error, chatStream, stopStream } = useAI()

const messages = ref([])
const input = ref('')
const selectedModel = ref('phi')
const currentRole = ref('user')
const showSettings = ref(false)
const messagesContainer = ref(null)
const isConnected = ref(true)
const keepFullHistory = ref(true)
const temperature = ref(0.7)
const builtPrompt = ref('')
const systemPrompt = ref('')
const promptBuilder = ref({ role: '', task: '', context: '', structure: '' })

const availableModels = ref([
  { label: 'phi', value: 'phi', speed: 'سريع', speedSeverity: 'success' },
  { label: 'gemma3:4b', value: 'gemma3:4b', speed: 'متوسط', speedSeverity: 'warn' },
  { label: 'llama3', value: 'llama3', speed: 'قوي', speedSeverity: 'info' },
])
const roleOptions = [
  { label: '👤 User', value: 'user' },
  { label: '🤖 Assistant', value: 'assistant' },
  { label: '⚙️ System', value: 'system' },
]
const systemTemplates = [
  {
    label: '🧑‍💻 Vue Expert',
    icon: 'pi pi-code',
    preview: 'مطور Vue.js خبير',
    prompt:
      'You are a Senior Vue.js expert. Always respond with Composition API code examples. Be concise.',
  },
  {
    label: '🐍 Django Dev',
    icon: 'pi pi-server',
    preview: 'مطور Django/DRF/Celery',
    prompt:
      'You are a Django/DRF expert. Focus on best practices and security. Always include code examples.',
  },
  {
    label: '🎬 Script Writer',
    icon: 'pi pi-video',
    preview: 'كاتب سكريبت تعليمي',
    prompt:
      'You are a technical content writer. Structure: Intro → Explanation → Code Demo → Summary.',
  },
  {
    label: '📋 Code Reviewer',
    icon: 'pi pi-check-square',
    preview: 'مراجع كود يكشف الأخطاء',
    prompt: 'You are a strict code reviewer. Structure: Issues Found → Improvements → Fixed Code.',
  },
]
const quickPrompts = [
  '⚡ اشرحلي Vue 3 Lifecycle Hooks',
  '🔍 راجعلي الكود ده',
  '📝 اكتبلي script لفيديو عن Django REST',
  '🐛 فين الـ bug في الكود ده؟',
]

const inputPlaceholder = computed(
  () =>
    ({
      user: '💬 اكتب سؤالك هنا...',
      assistant: '🤖 أدخل رداً يدوياً...',
      system: '⚙️ أدخل تعليمة System...',
    })[currentRole.value] || 'اكتب هنا...',
)

const apiMessages = computed(() => {
  const msgs = []
  if (systemPrompt.value.trim()) msgs.push({ role: 'system', content: systemPrompt.value.trim() })
  const history = keepFullHistory.value ? messages.value : messages.value.slice(-10)
  msgs.push(...history.map((m) => ({ role: m.role, content: m.content })))
  return msgs
})

async function send() {
  if (!input.value.trim() || isLoading.value) return
  messages.value.push({
    role: currentRole.value,
    content: input.value.trim(),
    time: new Date().toLocaleTimeString('ar-EG', { hour: '2-digit', minute: '2-digit' }),
  })
  input.value = ''
  await nextTick()
  scrollToBottom()
  await chatStream(apiMessages.value, selectedModel.value)
  if (currentResponse.value) {
    messages.value.push({
      role: 'assistant',
      content: currentResponse.value,
      time: new Date().toLocaleTimeString('ar-EG', { hour: '2-digit', minute: '2-digit' }),
    })
  }
  await nextTick()
  scrollToBottom()
}

function handleKeydown(e) {
  if (e.ctrlKey && e.key === 'Enter') {
    e.preventDefault()
    send()
  }
}
function applyTemplate(tpl) {
  systemPrompt.value = tpl.prompt
}
function useQuickPrompt(p) {
  input.value = p
  send()
}
function clearChat() {
  messages.value = []
  currentResponse.value = ''
}
function scrollToBottom() {
  if (messagesContainer.value)
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
}

function buildPrompt() {
  const p = promptBuilder.value
  builtPrompt.value = [
    p.role && `Act as: ${p.role}`,
    p.task && `Task: ${p.task}`,
    p.context && `Context: ${p.context}`,
    p.structure && `Structure: ${p.structure}`,
  ]
    .filter(Boolean)
    .join('\n')
}
function sendBuiltPrompt() {
  input.value = builtPrompt.value
  builtPrompt.value = ''
  showSettings.value = false
  send()
}

function exportChat() {
  const a = Object.assign(document.createElement('a'), {
    href: URL.createObjectURL(
      new Blob(
        [
          JSON.stringify(
            {
              model: selectedModel.value,
              systemPrompt: systemPrompt.value,
              messages: messages.value,
            },
            null,
            2,
          ),
        ],
        { type: 'application/json' },
      ),
    ),
    download: `chat-${Date.now()}.json`,
  })
  a.click()
  URL.revokeObjectURL(a.href)
}

const roleIcon = (r) =>
  ({ user: 'pi pi-user', assistant: 'pi pi-bolt', system: 'pi pi-cog' })[r] || 'pi pi-circle'
const roleLabel = (r) => ({ user: 'أنت', assistant: 'AI', system: 'System' })[r] || r
const roleSeverity = (r) =>
  ({ user: 'secondary', assistant: 'info', system: 'warn' })[r] || 'secondary'

function formatMessage(text) {
  if (!text) return ''
  return text
    .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre class="code-block"><code>$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
    .replace(/\n/g, '<br>')
}

onMounted(async () => {
  try {
    const data = await (await fetch('/api/ai/models/')).json()
    if (data.models?.length)
      availableModels.value = data.models.map((m) => ({
        label: m,
        value: m,
        speed: 'متاح',
        speedSeverity: 'success',
      }))
    isConnected.value = true
  } catch {
    isConnected.value = false
  }
})
</script>

<style scoped>
.ai-chat-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--p-surface-ground);
  font-family: 'Cairo', 'Segoe UI', sans-serif;
  direction: rtl;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
  background: var(--p-surface-card);
  border-bottom: 1px solid var(--p-surface-border);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
.header-left,
.header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.header-icon {
  font-size: 1.4rem;
  color: var(--p-primary-color);
}
.header-title {
  font-size: 1.1rem;
  font-weight: 700;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  scroll-behavior: smooth;
}
.system-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--p-yellow-100);
  border: 1px dashed var(--p-yellow-400);
  border-radius: 8px;
  font-size: 0.82rem;
  color: var(--p-yellow-700);
}
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  gap: 1rem;
  color: var(--p-text-muted-color);
}
.empty-icon {
  font-size: 3rem;
  opacity: 0.3;
}
.quick-prompts {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}
.quick-chip,
.template-chip {
  cursor: pointer;
  transition: transform 0.15s;
}
.quick-chip:hover,
.template-chip:hover {
  transform: translateY(-2px);
}

.message-bubble {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  animation: fadeInUp 0.25s ease;
}
.message-bubble.user {
  flex-direction: row-reverse;
}
.message-bubble.system {
  justify-content: center;
  opacity: 0.75;
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.role-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 0.9rem;
}
.role-avatar.user {
  background: var(--p-primary-100);
  color: var(--p-primary-color);
}
.role-avatar.assistant {
  background: var(--p-blue-100);
  color: var(--p-blue-600);
}
.role-avatar.system {
  background: var(--p-yellow-100);
  color: var(--p-yellow-700);
}

.bubble-content {
  max-width: 72%;
  background: var(--p-surface-card);
  border-radius: 12px;
  padding: 0.75rem 1rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07);
}
.message-bubble.user .bubble-content {
  background: var(--p-primary-color);
  color: white;
}
.bubble-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.4rem;
}
.timestamp {
  font-size: 0.7rem;
  opacity: 0.6;
  margin-right: auto;
}
.message-text {
  font-size: 0.92rem;
  line-height: 1.7;
  word-break: break-word;
}

:deep(.code-block) {
  background: #1e1e2e;
  color: #cdd6f4;
  padding: 0.75rem;
  border-radius: 8px;
  overflow-x: auto;
  font-family: 'Fira Code', monospace;
  font-size: 0.84rem;
  margin: 0.5rem 0;
}
:deep(.inline-code) {
  background: var(--p-surface-hover);
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  font-family: 'Fira Code', monospace;
  font-size: 0.85em;
}

.streaming-bubble .bubble-content {
  border: 1px solid var(--p-primary-200);
}
.cursor-blink {
  display: inline-block;
  animation: blink 1s infinite;
  color: var(--p-primary-color);
}
@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

.input-area {
  padding: 0.75rem 1.25rem 1rem;
  background: var(--p-surface-card);
  border-top: 1px solid var(--p-surface-border);
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.tools-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.model-select {
  min-width: 160px;
}
.role-selector {
  flex: 1;
}
.input-row {
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
}
.main-input {
  flex: 1;
  resize: none;
  max-height: 160px;
}
.send-btn {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
}
.input-hint {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: var(--p-text-muted-color);
}
.error-hint {
  color: var(--p-red-500);
}
.model-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--p-text-muted-color);
}
.templates-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.prompt-builder {
  display: flex;
  flex-direction: column;
}
.built-prompt {
  background: var(--p-surface-hover);
  border-radius: 8px;
  padding: 0.75rem;
}
.built-label {
  font-size: 0.8rem;
  color: var(--p-green-600);
  margin-bottom: 0.4rem;
}
.built-text {
  font-size: 0.82rem;
  white-space: pre-wrap;
  margin-bottom: 0.5rem;
}
.extra-settings {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.setting-label {
  font-size: 0.85rem;
}
</style>
