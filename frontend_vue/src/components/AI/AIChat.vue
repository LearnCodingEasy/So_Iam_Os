<template>
  <div class="ai-chat-page" dir="rtl">
    <aside class="ai-sidebar" :class="{ 'is-collapsed': sidebarCollapsed }">
      <div class="sidebar-brand">
        <div class="brand-mark">AI</div>
        <div v-if="!sidebarCollapsed">
          <strong>AI Core</strong>
          <small>So_Iam_OS</small>
        </div>
        <button class="icon-btn" type="button" :aria-label="sidebarCollapsed ? 'فتح القائمة' : 'طي القائمة'"
          @click="sidebarCollapsed = !sidebarCollapsed">{{ sidebarCollapsed ? '☰' : '‹' }}</button>
      </div>
      <button v-if="!sidebarCollapsed" class="primary-btn full" type="button" @click="startNewConversation">
        ＋ محادثة جديدة
        <HelpButton @click="showHelp('newConversation')" />
      </button>
      <div v-if="!sidebarCollapsed" class="conversation-list">
        <div class="list-heading">المحادثات <span>{{ conversations.length }}</span>
          <HelpButton @click="showHelp('history')" />
        </div>
        <div v-if="loadingConversations" class="muted center">جارٍ تحميل المحادثات…</div>
        <div v-else-if="!conversations.length" class="muted center">لا توجد محادثات محفوظة بعد.</div>
        <div v-for="conversation in conversations" :key="conversation.id"
          class="conversation-item" :class="{ active: conversation.id === activeConversationId }">
          <button class="conversation-select" type="button" @click="selectConversation(conversation.id)">
            <span class="conversation-icon">▤</span>
            <span class="conversation-name">{{ conversation.title || `محادثة #${conversation.id}` }}</span>
          </button>
          <button class="mini-danger" type="button" title="أرشفة المحادثة"
            @click="archiveConversation(conversation.id)">×</button>
        </div>
      </div>
      <div v-if="!sidebarCollapsed" class="sidebar-footer">
        <span class="status-dot" :class="{ online: backendAvailable }"></span>
        {{ backendAvailable ? 'واجهة الخادم متاحة' : 'تعذر الاتصال بالخادم' }}
        <HelpButton @click="showHelp('backendStatus')" />
      </div>
    </aside>

    <main class="ai-main">
      <header class="topbar">
        <div class="heading-block">
          <div class="eyebrow">مساحة الذكاء الاصطناعي</div>
          <h1>{{ activeConversationTitle }}</h1>
          <p>إعداداتك تُحفظ في Backend عبر API، وليست مجرد قيم شكلية في الواجهة.</p>
        </div>
        <div class="topbar-actions">
          <span class="provider-pill">{{ providerLabel(settings.preferred_provider) }} · {{ settings.preferred_model || 'النموذج الافتراضي' }}</span>
          <button class="secondary-btn" type="button" @click="settingsOpen = true">⚙ الإعدادات
            <HelpButton @click.stop="showHelp('settings')" />
          </button>
        </div>
      </header>

      <section class="chat-stage" ref="messagesContainer">
        <div v-if="!messages.length && !sending" class="welcome-panel">
          <div class="welcome-orb">✦</div>
          <h2>أهلًا بك في AI Core</h2>
          <p>اكتب سؤالك، أو اختر اقتراحًا للبدء. يمكنك تغيير المزود والنموذج وإدارة السياق وقوالب التعليمات من الإعدادات.</p>
          <div class="suggestions">
            <button type="button" @click="useSuggestion('ساعدني في تطوير مشروع Django وVue')">تطوير Django وVue <span>↗</span></button>
            <button type="button" @click="useSuggestion('أنشئ لي خطة تعلم عملية للغة Python')">خطة تعلم Python <span>↗</span></button>
            <button type="button" @click="useSuggestion('راجع هذه الفكرة وحدد الخطوات التالية')">تخطيط الخطوات التالية <span>↗</span></button>
          </div>
        </div>

        <article v-for="message in messages" :key="message.id || `${message.role}-${message.created_at || message.content}`"
          class="message-row" :class="message.role">
          <div class="message-avatar">{{ message.role === 'assistant' ? '✦' : 'أنت' }}</div>
          <div class="message-body">
            <div class="message-meta">
              <strong>{{ message.role === 'assistant' ? 'AI Core' : message.role === 'system' ? 'تعليمات' : 'أنت' }}</strong>
              <span v-if="message.created_at">{{ formatTime(message.created_at) }}</span>
              <span v-else-if="message.time">{{ message.time }}</span>
              <span v-if="message.provider || message.model" class="model-meta">{{ message.provider || '' }} {{ message.model || '' }}</span>
              <HelpButton v-if="message.role === 'assistant'" @click="showHelp('assistantMessage')" />
            </div>
            <div class="message-bubble">{{ message.content }}</div>
          </div>
        </article>

        <article v-if="sending" class="message-row assistant">
          <div class="message-avatar">✦</div>
          <div class="message-body">
            <div class="message-meta"><strong>AI Core</strong><span class="muted">جارٍ التفكير…</span></div>
            <div class="message-bubble typing"><i></i><i></i><i></i></div>
          </div>
        </article>

        <div v-if="errorMessage" class="error-banner" role="alert">
          <span>⚠ {{ errorMessage }}</span>
          <button type="button" @click="errorMessage = ''" aria-label="إغلاق الخطأ">×</button>
        </div>
      </section>

      <footer class="composer-wrap">
        <div class="composer-controls">
          <label class="control-chip">
            <span>المزود</span>
            <select v-model="settings.preferred_provider" @change="onProviderChange">
              <option value="ollama">Ollama</option>
              <option value="openai">OpenAI</option>
              <option value="openrouter">OpenRouter</option>
            </select>
            <HelpButton @click="showHelp('provider')" />
          </label>
          <label class="control-chip model-chip">
            <span>النموذج</span>
            <select v-model="settings.preferred_model" :disabled="modelsLoading">
              <option value="">استخدم الافتراضي</option>
              <option v-for="model in availableModels" :key="model.value" :value="model.value">{{ model.label }}</option>
            </select>
            <HelpButton @click="showHelp('model')" />
          </label>
          <button class="text-btn" type="button" @click="saveSettings" :disabled="savingSettings">
            {{ savingSettings ? 'جارٍ الحفظ…' : 'حفظ الإعدادات' }}
          </button>
        </div>
        <div class="composer">
          <textarea v-model="draft" rows="1" :disabled="sending"
            placeholder="اكتب رسالتك هنا… (Enter للإرسال، Shift+Enter لسطر جديد)"
            @keydown="onComposerKeydown"></textarea>
          <button class="send-btn" type="button" :disabled="sending || !draft.trim()" @click="sendMessage">
            {{ sending ? '…' : 'إرسال ↑' }}
          </button>
        </div>
        <div class="composer-foot">
          <span>قد تحتاج بعض المزودات إلى بيانات اعتماد محفوظة في إعداداتك.</span>
          <button type="button" class="text-btn" @click="settingsOpen = true">إدارة المزودات والقوالب <HelpButton @click.stop="showHelp('providerSettings')" /></button>
        </div>
      </footer>
    </main>

    <!-- Settings drawer -->
    <div v-if="settingsOpen" class="modal-backdrop" @click.self="settingsOpen = false">
      <section class="settings-modal" role="dialog" aria-modal="true" aria-labelledby="settings-title">
        <header class="modal-header">
          <div><span class="eyebrow">تحكم متصل بالـ Backend</span><h2 id="settings-title">إعدادات AI Core</h2></div>
          <button class="icon-btn" type="button" aria-label="إغلاق" @click="settingsOpen = false">×</button>
        </header>
        <div class="settings-tabs">
          <button v-for="tab in settingsTabs" :key="tab.id" type="button"
            :class="{ selected: settingsTab === tab.id }" @click="settingsTab = tab.id">
            {{ tab.label }} <HelpButton @click.stop="showHelp(tab.help)" />
          </button>
        </div>

        <div v-if="settingsTab === 'general'" class="settings-content">
          <div class="settings-section-title"><h3>إعدادات التشغيل</h3><HelpButton @click="showHelp('generalSettings')" /></div>
          <label class="field-label">المزود الافتراضي <HelpButton @click="showHelp('provider')" />
            <select v-model="settings.preferred_provider" @change="onProviderChange">
              <option value="ollama">Ollama (محلي)</option><option value="openai">OpenAI</option><option value="gemini">Google Gemini</option><option value="deepseek">DeepSeek</option><option value="openrouter">OpenRouter</option>
            </select>
          </label>
          <label class="field-label">النموذج الافتراضي <HelpButton @click="showHelp('model')" />
            <div class="inline-field"><select v-model="settings.preferred_model"><option value="">استخدم الافتراضي</option>
              <option v-for="model in availableModels" :key="model.value" :value="model.value">{{ model.label }}</option></select>
              <button class="secondary-btn" type="button" @click="loadModels" :disabled="modelsLoading">{{ modelsLoading ? 'جارٍ الفحص…' : 'تحديث النماذج' }}</button><button class="secondary-btn" type="button" @click="testProvider" :disabled="modelsLoading">اختبار الاتصال</button></div>
          </label>
          <label class="switch-row"><span><strong>استخدام سياق التطبيق</strong><small>يسمح للخادم بإضافة سياق المستخدم المتاح له وفق الكود الحالي.</small></span>
            <input type="checkbox" v-model="settings.context_enabled" /><HelpButton @click="showHelp('context')"/>
          </label>
          <label class="field-label">الحد الأقصى لسياق التوكنز
            <HelpButton @click="showHelp('maxContextTokens')" />
            <input v-model.number="settings.max_context_tokens" type="number" min="256" max="100000" step="256" />
          </label>
          <p class="info-note">هذه هي إعدادات AISettings التي يدعمها الـ API الحالي. لا تعرض هذه الشاشة خيارات لا يوجد لها endpoint فعلي.</p>
          <button class="primary-btn" type="button" @click="saveSettings" :disabled="savingSettings">{{ savingSettings ? 'جارٍ الحفظ…' : 'حفظ الإعدادات' }}</button>
        </div>

        <div v-else-if="settingsTab === 'credentials'" class="settings-content">
          <div class="settings-section-title"><h3>بيانات اعتماد المزودين</h3><HelpButton @click="showHelp('credentials')" /></div>
          <p class="muted">يُرسل المفتاح إلى الخادم فقط. لا تتم قراءة المفتاح المحفوظ أو عرضه مرة أخرى في الواجهة.</p>
          <div class="credential-list">
            <div v-for="credential in credentials" :key="credential.provider" class="credential-item">
              <div><strong>{{ providerLabel(credential.provider) }}</strong><small>{{ credential.has_api_key ? 'مفتاح محفوظ' : 'لا يوجد مفتاح' }}</small></div>
              <button v-if="credential.has_api_key" class="danger-btn" type="button" @click="removeCredential(credential.provider)">حذف المفتاح</button>
            </div>
            <div v-if="!credentials.length" class="muted">لم يتم إعداد بيانات اعتماد بعد.</div>
          </div>
          <div class="credential-form">
            <label class="field-label">المزود
              <select v-model="credentialForm.provider"><option value="openai">OpenAI</option><option value="gemini">Google Gemini</option><option value="deepseek">DeepSeek</option><option value="openrouter">OpenRouter</option><option value="ollama">Ollama</option></select>
            </label>
            <label class="field-label">مفتاح API (يُترك فارغًا إذا لم ترد تغييره)
              <input v-model="credentialForm.api_key" type="password" autocomplete="new-password" placeholder="أدخل المفتاح الجديد" />
            </label>
            <button class="primary-btn" type="button" @click="saveCredentialAction" :disabled="!credentialForm.api_key.trim() || credentialsBusy">
              {{ credentialsBusy ? 'جارٍ الحفظ…' : 'حفظ بيانات الاعتماد' }}
            </button>
          </div>
        </div>

        <div v-else-if="settingsTab === 'prompts'" class="settings-content">
          <div class="settings-section-title"><h3>قوالب التعليمات (Prompt Profiles)</h3><HelpButton @click="showHelp('prompts')" /></div>
          <div class="prompt-list">
            <div v-for="profile in promptProfiles" :key="profile.id" class="prompt-item">
              <button class="prompt-pick" type="button" @click="editPrompt(profile)"><strong>{{ profile.name }}</strong><small>{{ profile.is_default ? 'القالب الافتراضي' : 'اضغط للتعديل' }}</small></button>
              <button class="mini-danger" type="button" title="حذف القالب" @click="deletePrompt(profile.id)">×</button>
            </div>
          </div>
          <div class="prompt-editor">
            <h4>{{ promptForm.id ? 'تعديل القالب' : 'إنشاء قالب جديد' }}</h4>
            <label class="field-label">اسم القالب <input v-model="promptForm.name" maxlength="120" /></label>
            <label class="field-label">System Prompt <HelpButton @click="showHelp('systemPrompt')" /><textarea v-model="promptForm.system_prompt" rows="4"></textarea></label>
            <label class="field-label">تعليمات السياق <textarea v-model="promptForm.context_instructions" rows="3"></textarea></label>
            <div class="two-fields">
              <label class="field-label">Temperature <input v-model.number="promptForm.temperature" type="number" min="0" max="2" step="0.1" /></label>
              <label class="field-label">Max tokens <input v-model.number="promptForm.max_tokens" type="number" min="1" /></label>
            </div>
            <label class="switch-row"><span><strong>اجعل القالب افتراضيًا</strong><small>سيستخدمه Backend عند بناء سياق المحادثة.</small></span><input type="checkbox" v-model="promptForm.is_default" /></label>
            <div class="button-row"><button class="primary-btn" type="button" @click="savePrompt" :disabled="promptsBusy || !promptForm.name.trim()">{{ promptsBusy ? 'جارٍ الحفظ…' : 'حفظ القالب' }}</button>
              <button class="secondary-btn" type="button" @click="resetPromptForm">قالب جديد</button></div>
          </div>
        </div>

        <div v-else class="settings-content">
          <div class="settings-section-title"><h3>حول الاتصال والحدود</h3><HelpButton @click="showHelp('backendStatus')" /></div>
          <div class="status-card"><span class="status-dot" :class="{ online: backendAvailable }"></span>
            <div><strong>{{ backendAvailable ? 'تم الاتصال بنجاح' : 'الاتصال غير مؤكد' }}</strong><small>{{ backendAvailable ? 'تم تحميل إعدادات AI من API.' : 'افحص تسجيل الدخول وعنوان API والخادم.' }}</small></div>
          </div>
          <p class="info-note">المحادثات والإعدادات والقوالب وبيانات الاعتماد تتعامل مع نقاط API الموجودة. مراقبة التنفيذ، حدود الميزانية، وسجل التدقيق لا يتم تمثيلها هنا كميزات فعالة لأنها تحتاج إلى endpoints إضافية في Backend.</p>
          <button class="secondary-btn" type="button" @click="refreshAll">إعادة تحميل بيانات الخادم</button>
        </div>
        <div v-if="settingsNotice" class="notice" :class="{ error: settingsNoticeType === 'error' }" role="status">{{ settingsNotice }}</div>
      </section>
    </div>

    <!-- Contextual help popup -->
    <div v-if="helpDialog.open" class="modal-backdrop help-backdrop" @click.self="helpDialog.open = false">
      <section class="help-modal" role="dialog" aria-modal="true" aria-labelledby="help-title">
        <header class="modal-header"><div><span class="eyebrow">مركز المساعدة</span><h2 id="help-title">{{ helpDialog.title }}</h2></div>
          <button class="icon-btn" type="button" aria-label="إغلاق" @click="helpDialog.open = false">×</button></header>
        <p>{{ helpDialog.body }}</p>
        <div class="info-note">التغيير لا يُعتبر محفوظًا إلا بعد نجاح طلب API وظهور رسالة نجاح.</div>
        <button class="primary-btn full" type="button" @click="helpDialog.open = false">فهمت</button>
      </section>
    </div>
    <div v-if="toast" class="toast-message" role="status">{{ toast }}</div>
  </div>
</template>

<script setup>
import { computed, defineComponent, h, onMounted, reactive, ref, nextTick } from 'vue'
import api from '@/services/api'
import aiControl from '@/services/aiControl'
import { endpoints } from '@/services/endpoints'

const HelpButton = defineComponent({
  name: 'HelpButton',
  emits: ['click'],
  setup(_, { emit }) {
    return () => h('button', {
      class: 'help-button',
      type: 'button',
      title: 'شرح هذه الخاصية',
      'aria-label': 'شرح هذه الخاصية',
      onClick: (event) => { event.preventDefault(); event.stopPropagation(); emit('click') },
    }, '?')
  },
})

const helpCopy = {
  newConversation: ['محادثة جديدة', 'ينشئ مساحة محادثة جديدة. عند إرسال أول رسالة، يقوم Backend بإنشاء سجل المحادثة وربط الرسائل بحسابك.'],
  history: ['سجل المحادثات', 'يعرض المحادثات النشطة المحفوظة على الخادم. يمكنك فتح محادثة لاستكمالها أو أرشفتها. بيانات كل مستخدم معزولة بحسب صلاحيات Backend.'],
  backendStatus: ['حالة Backend', 'هذه الحالة تعكس نجاح تحميل إعدادات AI من API، ولا تعني أن كل مزود خارجي يعمل. لاختبار المزود، حدّث قائمة النماذج من إعدادات المزود.'],
  settings: ['إعدادات AI Core', 'تتيح إدارة إعدادات AISettings، وبيانات اعتماد المزود، وقوالب التعليمات من نقاط API الموجودة في المشروع.'],
  providerSettings: ['إدارة المزودات والقوالب', 'من هنا تختار المزود الافتراضي، تحفظ مفتاح API بأمان على الخادم، وتدير Prompt Profiles. توفر الميزات يعتمد على إعدادات Backend والمزود.'],
  provider: ['مزود الذكاء الاصطناعي', 'المزود هو الخدمة التي تنفذ الطلب: Ollama محلي، OpenAI، Gemini، DeepSeek أو OpenRouter. يجب حفظ مفتاح المزود السحابي في إعدادات الاعتماد قبل اختباره أو استخدامه.'],
  model: ['النموذج', 'اسم النموذج الذي سيُطلب من المزود. قائمة النماذج تُحمّل من endpoint المزود، وقد لا تكون متاحة إن كان المزود غير مضبوط أو غير متصل.'],
  generalSettings: ['إعدادات التشغيل', 'هذه الحقول تقابل حقول AISettings في Django. اضغط حفظ الإعدادات لإرسالها عبر PATCH إلى /ai/settings/.'],
  context: ['استخدام سياق التطبيق', 'عند التفعيل، يمكن لخدمة AI الحالية تضمين سياق من بيانات التطبيق التي يسمح Backend باسترجاعها. لا يعني ذلك إرسال كل بيانات النظام بلا قيود.'],
  maxContextTokens: ['حد سياق التوكنز', 'قيمة حد السياق المخزنة في AISettings. التطبيق الفعلي لهذا الحد يعتمد على تنفيذ خدمة بناء السياق في Backend.'],
  credentials: ['بيانات اعتماد المزودين', 'أدخل مفتاح API لحفظه على الخادم. واجهة API تعيد حالة وجود المفتاح فقط ولا تعيد المفتاح نفسه. لا تضع أسرارًا في رسائل المحادثة.'],
  prompts: ['قوالب التعليمات', 'قالب Prompt Profile يتضمن اسمًا وتعليمات نظام وتعليمات سياق وTemperature وMax tokens. يمكن تعيين قالب افتراضي ليستخدمه Backend عند بناء المحادثة.'],
  systemPrompt: ['System Prompt', 'تعليمات تحدد الدور والأسلوب المطلوب من النموذج. استخدمها فقط مع بيانات تملك حق إرسالها، ولا تضع كلمات مرور أو مفاتيح API فيها.'],
  assistantMessage: ['رسالة المساعد', 'هذه هي الاستجابة المحفوظة من Backend، وقد يظهر بجانبها اسم المزود والنموذج اللذان أرجعهما الخادم.'],
}

const sidebarCollapsed = ref(false)
const settingsOpen = ref(false)
const settingsTab = ref('general')
const settingsTabs = [
  { id: 'general', label: 'عام', help: 'generalSettings' },
  { id: 'credentials', label: 'المزودات', help: 'credentials' },
  { id: 'prompts', label: 'قوالب Prompts', help: 'prompts' },
  { id: 'status', label: 'الاتصال والحدود', help: 'backendStatus' },
]
const conversations = ref([])
const activeConversationId = ref(null)
const messages = ref([])
const draft = ref('')
const sending = ref(false)
const loadingConversations = ref(false)
const savingSettings = ref(false)
const modelsLoading = ref(false)
const credentialsBusy = ref(false)
const promptsBusy = ref(false)
const backendAvailable = ref(false)
const errorMessage = ref('')
const settingsNotice = ref('')
const settingsNoticeType = ref('success')
const toast = ref('')
const messagesContainer = ref(null)
const availableModels = ref([])
const credentials = ref([])
const promptProfiles = ref([])
const settings = reactive({
  preferred_provider: 'ollama',
  preferred_model: '',
  default_prompt_profile: null,
  context_enabled: true,
  max_context_tokens: 6000,
})
const credentialForm = reactive({ provider: 'openai', api_key: '' })
const promptForm = reactive({
  id: null, name: '', system_prompt: '', context_instructions: '',
  temperature: null, max_tokens: null, is_default: false,
})
const helpDialog = reactive({ open: false, title: '', body: '' })

const activeConversationTitle = computed(() => {
  const active = conversations.value.find((item) => item.id === activeConversationId.value)
  return active?.title || 'محادثة جديدة'
})

function showHelp(key) {
  const copy = helpCopy[key] || ['شرح الخاصية', 'هذه الخاصية مرتبطة بعناصر واجهة AI Core. راجع حالة الخادم ورسالة الاستجابة لمعرفة ما إذا تم حفظ التغيير.']
  helpDialog.title = copy[0]
  helpDialog.body = copy[1]
  helpDialog.open = true
}
function providerLabel(provider) {
  return ({ ollama: 'Ollama', openai: 'OpenAI', openrouter: 'OpenRouter', gemini: 'Google Gemini', deepseek: 'DeepSeek' })[provider] || provider || 'غير محدد'
}
function normalizeList(data) {
  if (Array.isArray(data)) return data
  if (Array.isArray(data?.results)) return data.results
  if (Array.isArray(data?.models)) return data.models
  return []
}
function normalizeModel(item) {
  if (typeof item === 'string') return { value: item, label: item }
  const value = item?.id || item?.name || item?.model || item?.value
  return value ? { value, label: item.label || value } : null
}
function notify(message, type = 'success') {
  toast.value = message
  settingsNotice.value = message
  settingsNoticeType.value = type
  window.setTimeout(() => { if (toast.value === message) toast.value = '' }, 3200)
}
function formatTime(value) {
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? '' : date.toLocaleString('ar-EG', { dateStyle: 'short', timeStyle: 'short' })
}
function getErrorMessage(error, fallback) {
  const data = error?.response?.data
  if (typeof data?.detail === 'string') return data.detail
  if (typeof data?.error === 'string') return data.error
  if (typeof data === 'string' && data.trim()) return data
  return error?.message || fallback
}
async function loadSettings() {
  const data = await aiControl.getAISettings()
  Object.assign(settings, data || {})
  backendAvailable.value = true
}
async function loadConversations() {
  loadingConversations.value = true
  try {
    conversations.value = normalizeList((await api.get(endpoints.ai.conversations)).data)
    backendAvailable.value = true
  } catch (error) {
    errorMessage.value = getErrorMessage(error, 'تعذر تحميل المحادثات.')
    backendAvailable.value = false
  } finally {
    loadingConversations.value = false
  }
}
async function loadCredentials() {
  try { credentials.value = await aiControl.getCredentials() }
  catch (error) { settingsNotice.value = getErrorMessage(error, 'تعذر تحميل بيانات الاعتماد.'); settingsNoticeType.value = 'error' }
}
async function loadPrompts() {
  try { promptProfiles.value = await aiControl.listPromptProfiles() }
  catch (error) { settingsNotice.value = getErrorMessage(error, 'تعذر تحميل القوالب.'); settingsNoticeType.value = 'error' }
}
async function loadModels() {
  modelsLoading.value = true
  try {
    const data = await aiControl.getProviderModels(settings.preferred_provider)
    availableModels.value = normalizeList(data).map(normalizeModel).filter(Boolean)
    if (data?.success === false) throw new Error(data.error || 'فشل جلب النماذج.')
    if (!availableModels.value.length) notify('لم يرجع المزود قائمة نماذج. يمكنك كتابة اسم النموذج الافتراضي في إعدادات Backend.', 'error')
  } catch (error) {
    availableModels.value = []
    settingsNotice.value = getErrorMessage(error, 'تعذر تحميل النماذج لهذا المزود.')
    settingsNoticeType.value = 'error'
  } finally { modelsLoading.value = false }
}
async function testProvider() {
  modelsLoading.value = true
  try {
    const result = await aiControl.testProviderConnection(settings.preferred_provider)
    if (result?.connected) {
      availableModels.value = normalizeList({ models: result.models }).map(normalizeModel).filter(Boolean)
      notify(`الاتصال ناجح مع ${providerLabel(settings.preferred_provider)}.`, 'success')
    } else {
      throw new Error(result?.error || 'فشل الاتصال بالمزود.')
    }
  } catch (error) {
    settingsNotice.value = getErrorMessage(error, 'فشل اختبار الاتصال بالمزود.')
    settingsNoticeType.value = 'error'
  } finally { modelsLoading.value = false }
}
async function onProviderChange() {
  settings.preferred_model = ''
  await loadModels()
}
async function saveSettings() {
  savingSettings.value = true
  try {
    const payload = {
      preferred_provider: settings.preferred_provider,
      preferred_model: settings.preferred_model,
      context_enabled: Boolean(settings.context_enabled),
      max_context_tokens: Number(settings.max_context_tokens),
      default_prompt_profile: settings.default_prompt_profile || null,
    }
    const saved = await aiControl.updateAISettings(payload)
    Object.assign(settings, saved)
    notify('تم حفظ إعدادات AI على الخادم.')
  } catch (error) {
    const message = getErrorMessage(error, 'تعذر حفظ الإعدادات.')
    settingsNotice.value = message
    settingsNoticeType.value = 'error'
    errorMessage.value = message
  } finally { savingSettings.value = false }
}
async function saveCredentialAction() {
  if (!credentialForm.api_key.trim()) return
  credentialsBusy.value = true
  try {
    await aiControl.saveCredential({ provider: credentialForm.provider, api_key: credentialForm.api_key })
    credentialForm.api_key = ''
    await loadCredentials()
    notify('تم إرسال بيانات الاعتماد إلى الخادم وحفظها.')
  } catch (error) {
    settingsNotice.value = getErrorMessage(error, 'تعذر حفظ بيانات الاعتماد.')
    settingsNoticeType.value = 'error'
  } finally { credentialsBusy.value = false }
}
async function removeCredential(provider) {
  if (!window.confirm(`هل تريد حذف بيانات اعتماد ${providerLabel(provider)}؟`)) return
  credentialsBusy.value = true
  try {
    await aiControl.deleteCredential(provider)
    await loadCredentials()
    notify('تم حذف بيانات الاعتماد.')
  } catch (error) {
    settingsNotice.value = getErrorMessage(error, 'تعذر حذف بيانات الاعتماد.')
    settingsNoticeType.value = 'error'
  } finally { credentialsBusy.value = false }
}
function resetPromptForm() {
  Object.assign(promptForm, { id: null, name: '', system_prompt: '', context_instructions: '', temperature: null, max_tokens: null, is_default: false })
}
function editPrompt(profile) {
  Object.assign(promptForm, {
    id: profile.id, name: profile.name || '', system_prompt: profile.system_prompt || '',
    context_instructions: profile.context_instructions || '', temperature: profile.temperature ?? null,
    max_tokens: profile.max_tokens ?? null, is_default: Boolean(profile.is_default),
  })
}
async function savePrompt() {
  promptsBusy.value = true
  try {
    const payload = {
      name: promptForm.name.trim(), system_prompt: promptForm.system_prompt,
      context_instructions: promptForm.context_instructions,
      temperature: promptForm.temperature === '' ? null : promptForm.temperature,
      max_tokens: promptForm.max_tokens === '' ? null : promptForm.max_tokens,
      is_default: Boolean(promptForm.is_default),
    }
    const saved = promptForm.id
      ? await aiControl.updatePromptProfile(promptForm.id, payload)
      : await aiControl.createPromptProfile(payload)
    await loadPrompts()
    if (saved?.is_default) {
      settings.default_prompt_profile = saved.id
      await saveSettings()
    }
    resetPromptForm()
    notify('تم حفظ قالب التعليمات.')
  } catch (error) {
    settingsNotice.value = getErrorMessage(error, 'تعذر حفظ القالب.')
    settingsNoticeType.value = 'error'
  } finally { promptsBusy.value = false }
}
async function deletePrompt(id) {
  if (!window.confirm('هل تريد حذف قالب التعليمات هذا؟')) return
  try {
    await aiControl.deletePromptProfile(id)
    if (settings.default_prompt_profile === id) settings.default_prompt_profile = null
    await loadPrompts()
    notify('تم حذف القالب.')
  } catch (error) {
    settingsNotice.value = getErrorMessage(error, 'تعذر حذف القالب.')
    settingsNoticeType.value = 'error'
  }
}
async function startNewConversation() {
  errorMessage.value = ''
  activeConversationId.value = null
  messages.value = []
  draft.value = ''
  try {
    const response = await api.post(endpoints.ai.conversations, {
      title: '', provider: settings.preferred_provider, model: settings.preferred_model || '',
    })
    const conversation = response.data
    conversations.value = [conversation, ...conversations.value.filter((item) => item.id !== conversation.id)]
    activeConversationId.value = conversation.id
    notify('تم إنشاء محادثة جديدة.')
  } catch (error) {
    // The chat endpoint can create a conversation when conversation_id is null,
    // so allow the user to continue even if pre-creation failed.
    errorMessage.value = getErrorMessage(error, 'تعذر إنشاء محادثة جديدة. سيتم المحاولة عند الإرسال.')
  }
}
async function selectConversation(id) {
  if (sending.value) return
  errorMessage.value = ''
  try {
    const response = await api.get(endpoints.ai.conversation(id))
    const conversation = response.data
    activeConversationId.value = conversation.id
    messages.value = (conversation.messages || []).filter((message) => message.role !== 'system')
    await scrollToBottom()
  } catch (error) { errorMessage.value = getErrorMessage(error, 'تعذر فتح المحادثة.') }
}
async function archiveConversation(id) {
  if (!window.confirm('هل تريد أرشفة هذه المحادثة؟')) return
  try {
    await api.delete(endpoints.ai.conversation(id))
    conversations.value = conversations.value.filter((item) => item.id !== id)
    if (activeConversationId.value === id) { activeConversationId.value = null; messages.value = [] }
    notify('تمت أرشفة المحادثة.')
  } catch (error) { errorMessage.value = getErrorMessage(error, 'تعذرت أرشفة المحادثة.') }
}
function useSuggestion(text) { draft.value = text }
function onComposerKeydown(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}
async function sendMessage() {
  const content = draft.value.trim()
  if (!content || sending.value) return
  sending.value = true
  errorMessage.value = ''
  draft.value = ''
  messages.value.push({
    id: `local-${Date.now()}`, role: 'user', content,
    created_at: new Date().toISOString(),
  })
  await scrollToBottom()
  try {
    const response = await api.post(endpoints.ai.chat, {
      message: content,
      conversation_id: activeConversationId.value || null,
      provider: settings.preferred_provider,
      model: settings.preferred_model || '',
    }, { timeout: 150000 })
    const data = response.data || {}
    if (data.success === false) throw new Error(data.error || 'فشل طلب الذكاء الاصطناعي.')
    activeConversationId.value = data.conversation_id || activeConversationId.value
    if (data.message) messages.value.push({
      ...data.message, created_at: new Date().toISOString(),
    })
    await loadConversations()
    if (activeConversationId.value) {
      const selected = conversations.value.find((item) => item.id === activeConversationId.value)
      if (!selected || !selected.messages) await selectConversation(activeConversationId.value)
    }
    await scrollToBottom()
  } catch (error) {
    errorMessage.value = getErrorMessage(error, 'تعذر إرسال الرسالة إلى AI Backend.')
    // Keep the user's draft content visible in the conversation for recovery.
  } finally { sending.value = false }
}
async function refreshAll() {
  settingsNotice.value = ''
  try {
    await Promise.all([loadSettings(), loadConversations(), loadCredentials(), loadPrompts()])
    await loadModels()
    notify('تم تحديث البيانات من الخادم.')
  } catch (error) {
    settingsNotice.value = getErrorMessage(error, 'تعذر تحديث كل البيانات.')
    settingsNoticeType.value = 'error'
  }
}
async function scrollToBottom() {
  await nextTick()
  if (messagesContainer.value) messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
}
onMounted(async () => {
  try { await loadSettings() } catch (error) {
    backendAvailable.value = false
    errorMessage.value = getErrorMessage(error, 'تعذر تحميل إعدادات AI. تحقق من تسجيل الدخول واتصال Backend.')
  }
  await Promise.all([loadConversations(), loadCredentials(), loadPrompts()])
  await loadModels()
})
</script>

<style scoped>
:global(body) { margin: 0; }
.ai-chat-page { --ai-ink:#172033; --ai-muted:#718096; --ai-line:#e5eaf2; --ai-surface:#fff; --ai-soft:#f6f8fc; --ai-accent:#6257e8; display:flex; min-height:calc(100vh - 4rem); background:#f4f6fb; color:var(--ai-ink); font-family:inherit; direction:rtl; }
.ai-sidebar { width:285px; flex:0 0 285px; background:#101827; color:#e8edf7; display:flex; flex-direction:column; padding:18px 14px; gap:18px; transition:width .2s,flex-basis .2s; box-sizing:border-box; }
.ai-sidebar.is-collapsed { width:76px; flex-basis:76px; }
.sidebar-brand { display:flex; align-items:center; gap:11px; min-height:48px; }
.brand-mark { width:40px; height:40px; border-radius:13px; background:linear-gradient(135deg,#8475ff,#4e46c8); display:grid; place-items:center; color:#fff; font-weight:800; }
.sidebar-brand strong,.sidebar-brand small { display:block; }
.sidebar-brand small { color:#98a5bb; font-size:11px; margin-top:3px; }
.icon-btn { border:0; background:transparent; color:inherit; font-size:22px; cursor:pointer; margin-inline-start:auto; padding:5px 8px; border-radius:8px; }
.icon-btn:hover { background:#ffffff15; }
.primary-btn,.secondary-btn,.danger-btn,.text-btn { border:0; border-radius:10px; padding:10px 14px; cursor:pointer; font:inherit; font-size:13px; display:inline-flex; align-items:center; justify-content:center; gap:8px; }
.primary-btn { background:var(--ai-accent); color:white; }
.primary-btn:disabled,.secondary-btn:disabled { opacity:.55; cursor:not-allowed; }
.primary-btn.full { width:100%; }
.secondary-btn { background:#eef0fa; color:#343b58; border:1px solid #e1e4f0; }
.danger-btn { color:#b42336; background:#fff0f1; }
.text-btn { background:transparent; color:#6558d9; padding:7px; }
.conversation-list { flex:1; overflow:auto; min-height:100px; }
.list-heading { display:flex; align-items:center; gap:7px; color:#a7b2c6; font-size:12px; padding:4px 8px 12px; }
.list-heading span { background:#ffffff16; padding:2px 7px; border-radius:20px; }
.conversation-item { display:flex; align-items:center; border-radius:9px; margin:3px 0; padding:4px; gap:3px; }
.conversation-item.active,.conversation-item:hover { background:#ffffff12; }
.conversation-select { flex:1; display:flex; min-width:0; gap:9px; text-align:right; align-items:center; color:#e5eaf5; background:transparent; border:0; padding:8px 5px; cursor:pointer; }
.conversation-name { overflow:hidden; white-space:nowrap; text-overflow:ellipsis; font-size:12px; }
.conversation-icon { color:#9e9af8; }
.mini-danger { border:0; color:#aab3c3; background:transparent; cursor:pointer; font-size:20px; border-radius:6px; padding:2px 7px; }
.mini-danger:hover { color:#ff8b98; background:#ffffff10; }
.sidebar-footer { display:flex; align-items:center; gap:7px; border-top:1px solid #ffffff18; padding-top:14px; color:#aab4c6; font-size:11px; }
.status-dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:#e6a23c; flex-shrink:0; }
.status-dot.online { background:#32c98a; box-shadow:0 0 0 3px #32c98a20; }
.ai-main { min-width:0; flex:1; display:flex; flex-direction:column; min-height:calc(100vh - 4rem); }
.topbar { display:flex; align-items:center; justify-content:space-between; gap:20px; padding:23px clamp(16px,3vw,40px); background:#fff; border-bottom:1px solid var(--ai-line); }
.eyebrow { display:block; color:#766ae7; font-size:11px; font-weight:700; margin-bottom:5px; }
.heading-block h1 { font-size:22px; margin:0; letter-spacing:-.4px; }
.heading-block p { margin:6px 0 0; color:var(--ai-muted); font-size:12px; }
.topbar-actions { display:flex; align-items:center; gap:10px; }
.provider-pill { border:1px solid var(--ai-line); background:#f9faff; border-radius:30px; padding:9px 12px; color:#5b6175; font-size:11px; }
.chat-stage { flex:1; overflow:auto; padding:clamp(18px,4vw,48px); display:flex; flex-direction:column; gap:22px; }
.welcome-panel { margin:auto; max-width:620px; text-align:center; }
.welcome-orb { margin:0 auto 20px; width:64px; height:64px; border-radius:21px; display:grid; place-items:center; color:#fff; font-size:30px; background:linear-gradient(135deg,#9488ff,#574de1); box-shadow:0 12px 30px #6558e52b; }
.welcome-panel h2 { margin:0 0 10px; font-size:26px; }
.welcome-panel p { color:var(--ai-muted); line-height:1.9; font-size:13px; max-width:500px; margin:0 auto; }
.suggestions { display:flex; flex-wrap:wrap; justify-content:center; gap:9px; margin-top:25px; }
.suggestions button { border:1px solid #e1e5f0; border-radius:12px; padding:12px 14px; background:#fff; color:#454d65; cursor:pointer; font:inherit; font-size:12px; }
.suggestions button:hover { border-color:#bcb5ff; color:#6257d8; }
.suggestions span { margin-inline-start:8px; color:#8579ed; }
.message-row { display:flex; gap:12px; align-items:flex-start; max-width:900px; width:100%; margin-inline:auto; }
.message-row.user { flex-direction:row-reverse; }
.message-avatar { flex:0 0 34px; width:34px; height:34px; border-radius:12px; display:grid; place-items:center; background:#e8e6ff; color:#6357dc; font-size:11px; font-weight:700; }
.message-row.user .message-avatar { background:#e2f4ed; color:#237a59; }
.message-body { min-width:0; max-width:calc(100% - 45px); }
.message-meta { display:flex; gap:9px; align-items:center; flex-wrap:wrap; color:#778196; font-size:10px; margin:2px 0 7px; }
.message-meta strong { color:#3a4359; font-size:12px; }
.model-meta { color:#8a82d8; }
.message-bubble { white-space:pre-wrap; overflow-wrap:anywhere; line-height:1.9; padding:13px 16px; background:#fff; border:1px solid #e6eaf2; border-radius:3px 14px 14px 14px; font-size:13px; box-shadow:0 3px 10px #17203305; }
.message-row.user .message-bubble { background:#ecebff; border-color:#e3e1ff; border-radius:14px 3px 14px 14px; }
.typing { display:flex; gap:5px; align-items:center; min-width:70px; }
.typing i { width:6px; height:6px; border-radius:50%; background:#8d82e9; animation:blink 1s infinite ease-in-out; }
.typing i:nth-child(2) { animation-delay:.15s; }.typing i:nth-child(3) { animation-delay:.3s; }
@keyframes blink { 0%,80%,100% { opacity:.3; transform:translateY(0); } 40% { opacity:1; transform:translateY(-3px); } }
.composer-wrap { background:#fff; border-top:1px solid var(--ai-line); padding:13px clamp(16px,3vw,40px) 17px; }
.composer-controls { display:flex; align-items:center; flex-wrap:wrap; gap:9px; margin-bottom:10px; }
.control-chip { display:flex; align-items:center; gap:7px; padding:5px 8px; border:1px solid var(--ai-line); border-radius:9px; color:#70798e; font-size:11px; }
.control-chip select { max-width:180px; border:0; outline:0; background:transparent; color:#30384e; font:inherit; }
.model-chip select { min-width:110px; }
.composer { display:flex; align-items:flex-end; gap:10px; padding:10px; border:1px solid #dfe4ef; border-radius:16px; box-shadow:0 5px 18px #202b4510; }
.composer:focus-within { border-color:#a9a0ff; box-shadow:0 0 0 3px #7265ec13; }
.composer textarea { flex:1; min-width:0; resize:vertical; max-height:180px; border:0; outline:0; padding:9px; font:inherit; font-size:13px; line-height:1.8; background:transparent; color:#252d42; }
.send-btn { border:0; border-radius:11px; background:#6257e8; color:#fff; padding:12px 17px; font:inherit; cursor:pointer; white-space:nowrap; }
.send-btn:disabled { opacity:.5; cursor:not-allowed; }
.composer-foot { display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; color:#98a0b0; font-size:10px; padding-top:8px; }
.muted { color:#9ca5b5; font-size:11px; line-height:1.7; }.center { text-align:center; padding:20px 6px; }
.error-banner { display:flex; justify-content:space-between; align-items:center; gap:10px; max-width:900px; width:100%; box-sizing:border-box; margin:0 auto; padding:12px 14px; background:#fff1f1; color:#a52e3e; border:1px solid #ffd4d8; border-radius:10px; font-size:12px; }
.error-banner button { border:0; background:transparent; color:inherit; cursor:pointer; font-size:18px; }
.help-button { display:inline-grid; place-items:center; width:18px; height:18px; padding:0; border:1px solid #b9b5f3; border-radius:50%; background:#f6f5ff; color:#665bdf; font-size:11px; font-weight:800; cursor:pointer; flex-shrink:0; vertical-align:middle; }
.help-button:hover { background:#665bdf; color:white; }
.modal-backdrop { position:fixed; z-index:1000; inset:0; display:flex; align-items:center; justify-content:center; padding:20px; background:#11182b75; backdrop-filter:blur(4px); }
.settings-modal,.help-modal { width:min(760px,100%); max-height:min(90vh,900px); overflow:auto; background:#fff; border-radius:20px; box-shadow:0 25px 80px #0a10253b; padding:23px; box-sizing:border-box; }
.help-modal { width:min(440px,100%); }
.modal-header { display:flex; justify-content:space-between; align-items:flex-start; gap:15px; padding-bottom:17px; border-bottom:1px solid var(--ai-line); }
.modal-header h2 { margin:0; font-size:21px; }
.modal-header .icon-btn { color:#6c7488; }
.settings-tabs { display:flex; flex-wrap:wrap; gap:7px; padding:15px 0; border-bottom:1px solid var(--ai-line); }
.settings-tabs button { display:flex; align-items:center; gap:7px; border:1px solid transparent; background:#f7f8fc; border-radius:9px; padding:8px 11px; color:#616a7e; font:inherit; font-size:12px; cursor:pointer; }
.settings-tabs button.selected { background:#eeedff; color:#5c51d5; border-color:#d9d5ff; }
.settings-content { padding:17px 0 5px; display:flex; flex-direction:column; gap:14px; }
.settings-section-title { display:flex; align-items:center; gap:8px; }
.settings-section-title h3 { margin:0; font-size:16px; }
.field-label { display:flex; flex-direction:column; align-items:stretch; gap:7px; font-size:12px; color:#4f5870; font-weight:600; }
.field-label .help-button { align-self:flex-start; margin-top:-25px; margin-inline-start:95px; }
.field-label input,.field-label select,.field-label textarea { width:100%; box-sizing:border-box; padding:10px 11px; border:1px solid #dfe4ef; border-radius:9px; outline:0; color:#2f374d; background:#fff; font:inherit; font-weight:400; }
.field-label input:focus,.field-label select:focus,.field-label textarea:focus { border-color:#a8a0f7; box-shadow:0 0 0 3px #6558e513; }
.inline-field { display:flex; gap:8px; }.inline-field select { flex:1; min-width:0; }
.switch-row { display:flex; align-items:center; gap:12px; padding:13px; background:#f8f9fd; border:1px solid #edf0f6; border-radius:11px; }
.switch-row span { flex:1; }.switch-row strong,.switch-row small { display:block; }.switch-row strong { font-size:12px; }.switch-row small { color:#8a93a5; font-size:10px; line-height:1.7; margin-top:3px; }
.switch-row input { accent-color:#665bdf; width:17px; height:17px; }
.info-note { padding:11px 13px; border-radius:10px; background:#f3f5ff; color:#666d8a; font-size:11px; line-height:1.8; }
.credential-list,.prompt-list { display:flex; flex-direction:column; gap:7px; }
.credential-item,.prompt-item { display:flex; align-items:center; justify-content:space-between; gap:12px; border:1px solid var(--ai-line); border-radius:10px; padding:10px 12px; }
.credential-item strong,.credential-item small,.prompt-pick strong,.prompt-pick small { display:block; }.credential-item strong,.prompt-pick strong { font-size:12px; }.credential-item small,.prompt-pick small { color:#929bad; font-size:10px; margin-top:4px; }
.credential-form,.prompt-editor { border-top:1px solid var(--ai-line); padding-top:15px; display:flex; flex-direction:column; gap:13px; }
.prompt-editor h4 { margin:0; font-size:14px; }
.prompt-pick { text-align:right; flex:1; border:0; background:transparent; cursor:pointer; color:#374057; }
.two-fields { display:grid; grid-template-columns:1fr 1fr; gap:12px; }.button-row { display:flex; gap:8px; flex-wrap:wrap; }
.status-card { display:flex; align-items:center; gap:12px; padding:15px; background:#f8f9fc; border:1px solid var(--ai-line); border-radius:12px; }
.status-card strong,.status-card small { display:block; }.status-card strong { font-size:13px; }.status-card small { font-size:11px; color:#8b94a6; margin-top:4px; }
.notice { border-radius:9px; padding:10px 12px; margin-top:12px; background:#e9f9f0; color:#23754d; font-size:12px; }
.notice.error { background:#fff0f1; color:#a52e3e; }
.toast-message { position:fixed; z-index:1200; bottom:22px; left:22px; max-width:min(400px,calc(100vw - 44px)); background:#172033; color:#fff; padding:12px 16px; border-radius:11px; box-shadow:0 8px 30px #0002; font-size:12px; }
@media (max-width:900px) { .ai-sidebar { width:235px; flex-basis:235px; }.topbar { align-items:flex-start; flex-direction:column; }.topbar-actions { flex-wrap:wrap; } }
@media (max-width:650px) { .ai-chat-page { min-height:100vh; }.ai-sidebar { width:68px; flex-basis:68px; padding:12px 8px; }.ai-sidebar:not(.is-collapsed) { width:220px; flex-basis:220px; position:absolute; z-index:5; min-height:100%; box-shadow:10px 0 30px #0002; }.ai-sidebar.is-collapsed .sidebar-brand { flex-direction:column; }.topbar { padding:17px 15px; }.heading-block h1 { font-size:18px; }.provider-pill { max-width:100%; }.chat-stage { padding:18px 12px; }.composer-wrap { padding:12px; }.composer-controls { gap:5px; }.control-chip { max-width:100%; }.control-chip select { max-width:120px; }.settings-modal,.help-modal { padding:16px; border-radius:15px; }.two-fields { grid-template-columns:1fr; }.inline-field { flex-direction:column; }.composer-foot { font-size:9px; } }
</style>
