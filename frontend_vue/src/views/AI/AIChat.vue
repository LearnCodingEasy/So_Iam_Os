<template>
  <div class="ai-chat-page" :dir="direction">
    <aside class="ai-sidebar" :class="{ 'is-collapsed': sidebarCollapsed }">
      <div class="sidebar-brand">
        <div class="brand-mark">AI</div>
        <div v-if="!sidebarCollapsed">
          <strong>AI Core</strong>
          <small>So_Iam_OS</small>
        </div>
        <button
          class="icon-btn"
          type="button"
          :aria-label="sidebarCollapsed ? 'فتح القائمة' : 'طي القائمة'"
          @click="sidebarCollapsed = !sidebarCollapsed"
        >
          {{ sidebarCollapsed ? '☰' : '‹' }}
        </button>
      </div>
      <button
        v-if="!sidebarCollapsed"
        class="primary-btn full"
        type="button"
        @click="startNewConversation"
      >
        ＋ محادثة جديدة
        <HelpButton @click="showHelp('newConversation')" />
      </button>
      <div v-if="!sidebarCollapsed" class="conversation-list">
        <div class="list-heading">
          المحادثات <span>{{ conversations.length }}</span>
          <HelpButton @click="showHelp('history')" />
        </div>
        <div v-if="loadingConversations" class="muted center">جارٍ تحميل المحادثات…</div>
        <div v-else-if="!conversations.length" class="muted center">
          لا توجد محادثات محفوظة بعد.
        </div>
        <div
          v-for="conversation in conversations"
          :key="conversation.id"
          class="conversation-item"
          :class="{ active: conversation.id === activeConversationId }"
        >
          <button
            class="conversation-select"
            type="button"
            @click="selectConversation(conversation.id)"
          >
            <span class="conversation-icon">▤</span>
            <span class="conversation-name">{{
              conversation.title || `محادثة #${conversation.id}`
            }}</span>
          </button>
          <div class="conversation-actions">
            <button class="mini-danger" type="button" title="أرشفة المحادثة" aria-label="أرشفة المحادثة"
              @click="archiveConversation(conversation.id)">×</button>
            <button class="mini-danger" type="button" title="حذف المحادثة" aria-label="حذف المحادثة"
              @click="deleteConversation(conversation.id)">⌫</button>
          </div>
        </div>
      </div>
      <div v-if="!sidebarCollapsed" class="sidebar-footer">
        <span class="status-dot" :class="{ online: backendAvailable }"></span>
        {{ backendAvailable ? 'واجهة الخادم متاحة' : 'تعذر الاتصال بالخادم' }}
        <HelpButton @click="showHelp('backendStatus')" />
        <button v-if="lastArchivedConversation" class="text-btn" type="button" @click="restoreLastArchived">استعادة آخر محادثة</button>
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
          <span class="provider-pill"
            >{{ providerLabel(settings.preferred_provider) }} ·
            {{ settings.preferred_model || 'النموذج الافتراضي' }}</span
          >
          <button class="secondary-btn" type="button" :disabled="!activeConversationId" @click="inspectContext">
            سياق المحادثة
          </button>
          <button class="secondary-btn" type="button" @click="settingsOpen = true">
            ⚙ الإعدادات
            <HelpButton @click.stop="showHelp('settings')" />
          </button>
        </div>
      </header>

      <section class="chat-stage" ref="messagesContainer">
        <div v-if="!messages.length && !sending" class="welcome-panel">
          <div class="welcome-orb">✦</div>
          <h2>أهلًا بك في AI Core</h2>
          <p>
            اكتب سؤالك، أو اختر اقتراحًا للبدء. يمكنك تغيير المزود والنموذج وإدارة السياق وقوالب
            التعليمات من الإعدادات.
          </p>
          <div class="suggestions">
            <button type="button" @click="useSuggestion('ساعدني في تطوير مشروع Django وVue')">
              تطوير Django وVue <span>↗</span>
            </button>
            <button type="button" @click="useSuggestion('أنشئ لي خطة تعلم عملية للغة Python')">
              خطة تعلم Python <span>↗</span>
            </button>
            <button type="button" @click="useSuggestion('راجع هذه الفكرة وحدد الخطوات التالية')">
              تخطيط الخطوات التالية <span>↗</span>
            </button>
          </div>
        </div>

        <article
          v-for="message in messages"
          :key="message.id || `${message.role}-${message.created_at || message.content}`"
          class="message-row"
          :class="message.role"
        >
          <div class="message-avatar">{{ message.role === 'assistant' ? '✦' : 'أنت' }}</div>
          <div class="message-body">
            <div class="message-meta">
              <strong>{{
                message.role === 'assistant'
                  ? 'AI Core'
                  : message.role === 'system'
                    ? 'تعليمات'
                    : 'أنت'
              }}</strong>
              <span v-if="message.created_at">{{ formatTime(message.created_at) }}</span>
              <span v-else-if="message.time">{{ message.time }}</span>
              <span v-if="message.provider || message.model" class="model-meta"
                >{{ message.provider || '' }} {{ message.model || '' }}</span
              >
              <HelpButton
                v-if="message.role === 'assistant'"
                @click="showHelp('assistantMessage')"
              />
            </div>
            <div class="message-bubble"><MarkdownRenderer v-if="message.role === 'assistant'" :content="message.content" /><span v-else>{{ message.content }}</span></div>
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
              <option value="gemini">Google Gemini</option>
              <option value="deepseek">DeepSeek</option>
              <option value="openrouter">OpenRouter</option>
            </select>
            <HelpButton @click="showHelp('provider')" />
          </label>
          <label class="control-chip model-chip">
            <span>النموذج</span>
            <select v-model="settings.preferred_model" :disabled="modelsLoading">
              <option value="">استخدم الافتراضي</option>
              <option v-for="model in availableModels" :key="model.value" :value="model.value">
                {{ model.label }}
              </option>
            </select>
            <HelpButton @click="showHelp('model')" />
          </label>
          <button class="text-btn" type="button" @click="saveSettings" :disabled="savingSettings">
            {{ savingSettings ? 'جارٍ الحفظ…' : 'حفظ الإعدادات' }}
          </button>
        </div>
        <div class="composer">
          <textarea
            v-model="draft"
            rows="1"
            :disabled="sending"
            placeholder="اكتب رسالتك هنا… (Enter للإرسال، Shift+Enter لسطر جديد)"
            @keydown="onComposerKeydown"
          ></textarea>
          <button
            class="send-btn"
            type="button"
            :disabled="!sending && !draft.trim()"
            @click="sending ? cancelStream() : sendMessage()"
          >
            {{ sending ? 'إيقاف' : 'إرسال ↑' }}
          </button>
        </div>
        <div class="composer-foot">
          <span>قد تحتاج بعض المزودات إلى بيانات اعتماد محفوظة في إعداداتك.</span>
          <button type="button" class="text-btn" @click="settingsOpen = true">
            إدارة المزودات والقوالب <HelpButton @click.stop="showHelp('providerSettings')" />
          </button>
        </div>
      </footer>
    </main>

    <div v-if="contextDialog" class="modal-backdrop" @click.self="contextDialog = false">
      <section class="settings-modal" role="dialog" aria-modal="true" aria-labelledby="context-title">
        <header class="modal-header">
          <div><span class="eyebrow">CONVERSATION CONTEXT</span><h2 id="context-title">فحص سياق المحادثة</h2></div>
          <button class="icon-btn" type="button" aria-label="إغلاق" @click="contextDialog = false">×</button>
        </header>
        <p v-if="contextLoading" class="muted">جارٍ تحميل السياق...</p>
        <pre v-else class="context-json">{{ JSON.stringify(conversationContext, null, 2) }}</pre>
        <div v-if="contextError" class="error-banner" role="alert">{{ contextError }}</div>
      </section>
    </div>

    <!-- Settings drawer -->
    <div v-if="settingsOpen" class="modal-backdrop" @click.self="settingsOpen = false">
      <section
        class="settings-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="settings-title"
      >
        <header class="modal-header">
          <div>
            <span class="eyebrow">تحكم متصل بالـ Backend</span>
            <h2 id="settings-title">إعدادات AI Core</h2>
          </div>
          <button class="icon-btn" type="button" aria-label="إغلاق" @click="settingsOpen = false">
            ×
          </button>
        </header>
        <div class="settings-tabs">
          <button
            v-for="tab in settingsTabs"
            :key="tab.id"
            type="button"
            :class="{ selected: settingsTab === tab.id }"
            @click="settingsTab = tab.id"
          >
            {{ tab.label }} <HelpButton @click.stop="showHelp(tab.help)" />
          </button>
        </div>

        <div v-if="settingsTab === 'general'" class="settings-content">
          <div class="settings-section-title">
            <h3>إعدادات التشغيل</h3>
            <HelpButton @click="showHelp('generalSettings')" />
          </div>
          <label class="field-label"
            >المزود الافتراضي <HelpButton @click="showHelp('provider')" />
            <select v-model="settings.preferred_provider" @change="onProviderChange">
              <option value="ollama">Ollama (محلي)</option>
              <option value="openai">OpenAI</option>
              <option value="gemini">Google Gemini</option>
              <option value="deepseek">DeepSeek</option>
              <option value="openrouter">OpenRouter</option>
            </select>
          </label>
          <label class="field-label"
            >النموذج الافتراضي <HelpButton @click="showHelp('model')" />
            <div class="inline-field">
              <select v-model="settings.preferred_model">
                <option value="">استخدم الافتراضي</option>
                <option v-for="model in availableModels" :key="model.value" :value="model.value">
                  {{ model.label }}
                </option>
              </select>
              <button
                class="secondary-btn"
                type="button"
                @click="loadModels"
                :disabled="modelsLoading"
              >
                {{ modelsLoading ? 'جارٍ الفحص…' : 'تحديث النماذج' }}</button
              ><button
                class="secondary-btn"
                type="button"
                @click="testProvider"
                :disabled="modelsLoading"
              >
                اختبار الاتصال
              </button>
            </div>
          </label>
          <label class="switch-row"
            ><span
              ><strong>استخدام سياق التطبيق</strong
              ><small>يسمح للخادم بإضافة سياق المستخدم المتاح له وفق الكود الحالي.</small></span
            >
            <input type="checkbox" v-model="settings.context_enabled" /><HelpButton
              @click="showHelp('context')"
            />
          </label>
          <label class="field-label"
            >الحد الأقصى لسياق التوكنز
            <HelpButton @click="showHelp('maxContextTokens')" />
            <input
              v-model.number="settings.max_context_tokens"
              type="number"
              min="256"
              max="100000"
              step="256"
            />
          </label>
          <label class="field-label">قالب التعليمات الافتراضي
            <select v-model="settings.default_prompt_profile">
              <option :value="null">بدون قالب افتراضي</option>
              <option v-for="profile in promptProfiles" :key="profile.id" :value="profile.id">{{ profile.name }}</option>
            </select>
          </label>
          <label class="switch-row"><span><strong>تفعيل البث المباشر</strong><small>تفضيل Streaming عند إرسال رسائل المحادثة.</small></span>
            <input type="checkbox" v-model="settings.streaming_enabled" />
          </label>
          <label class="switch-row"><span><strong>تفعيل Fallback</strong><small>السماح بالانتقال لمزود بديل عند فشل المزود الأساسي وفق سياسة الخادم.</small></span>
            <input type="checkbox" v-model="settings.fallback_enabled" />
          </label>
          <label class="field-label">Temperature
            <input v-model.number="settings.temperature" type="number" min="0" max="2" step="0.1" />
          </label>
          <label class="field-label">مهلة الاتصال بالثواني
            <input v-model.number="settings.timeout_seconds" type="number" min="1" max="300" />
          </label>
          <p class="info-note">
            هذه هي إعدادات AISettings التي يدعمها الـ API الحالي. لا تعرض هذه الشاشة خيارات لا يوجد
            لها endpoint فعلي.
          </p>
          <button
            class="primary-btn"
            type="button"
            @click="saveSettings"
            :disabled="savingSettings"
          >
            {{ savingSettings ? 'جارٍ الحفظ…' : 'حفظ الإعدادات' }}
          </button>
        </div>

        <div v-else-if="settingsTab === 'credentials'" class="settings-content">
          <div class="settings-section-title">
            <h3>بيانات اعتماد المزودين</h3>
            <HelpButton @click="showHelp('credentials')" />
          </div>
          <p class="muted">
            يُرسل المفتاح إلى الخادم فقط. لا تتم قراءة المفتاح المحفوظ أو عرضه مرة أخرى في الواجهة.
          </p>
          <div class="credential-list">
            <div
              v-for="credential in credentials"
              :key="credential.provider"
              class="credential-item"
            >
              <div>
                <strong>{{ providerLabel(credential.provider) }}</strong
                ><small>{{ credential.has_api_key ? 'مفتاح محفوظ' : 'لا يوجد مفتاح' }}</small>
              </div>
              <button
                v-if="credential.has_api_key"
                class="danger-btn"
                type="button"
                @click="removeCredential(credential.provider)"
              >
                حذف المفتاح
              </button>
            </div>
            <div v-if="!credentials.length" class="muted">لم يتم إعداد بيانات اعتماد بعد.</div>
          </div>
          <div class="credential-form">
            <label class="field-label"
              >المزود
              <select v-model="credentialForm.provider">
                <option value="openai">OpenAI</option>
                <option value="gemini">Google Gemini</option>
                <option value="deepseek">DeepSeek</option>
                <option value="openrouter">OpenRouter</option>
                <option value="ollama">Ollama</option>
              </select>
            </label>
            <label class="field-label"
              >مفتاح API (يُترك فارغًا إذا لم ترد تغييره)
              <input
                v-model="credentialForm.api_key"
                type="password"
                autocomplete="new-password"
                placeholder="أدخل المفتاح الجديد"
              />
            </label>
            <button
              class="primary-btn"
              type="button"
              @click="saveCredentialAction"
              :disabled="!credentialForm.api_key.trim() || credentialsBusy"
            >
              {{ credentialsBusy ? 'جارٍ الحفظ…' : 'حفظ بيانات الاعتماد' }}
            </button>
          </div>
        </div>

        <div v-else-if="settingsTab === 'prompts'" class="settings-content">
          <div class="settings-section-title">
            <h3>قوالب التعليمات (Prompt Profiles)</h3>
            <HelpButton @click="showHelp('prompts')" />
          </div>
          <div class="prompt-list">
            <div v-for="profile in promptProfiles" :key="profile.id" class="prompt-item">
              <button class="prompt-pick" type="button" @click="editPrompt(profile)">
                <strong>{{ profile.name }}</strong
                ><small>{{ profile.is_default ? 'القالب الافتراضي' : 'اضغط للتعديل' }}</small>
              </button>
              <button
                class="mini-danger"
                type="button"
                title="حذف القالب"
                @click="deletePrompt(profile.id)"
              >
                ×
              </button>
            </div>
          </div>
          <div class="prompt-editor">
            <h4>{{ promptForm.id ? 'تعديل القالب' : 'إنشاء قالب جديد' }}</h4>
            <label class="field-label"
              >اسم القالب <input v-model="promptForm.name" maxlength="120"
            /></label>
            <label class="field-label"
              >System Prompt <HelpButton @click="showHelp('systemPrompt')" /><textarea
                v-model="promptForm.system_prompt"
                rows="4"
              ></textarea>
            </label>
            <label class="field-label"
              >تعليمات السياق
              <textarea v-model="promptForm.context_instructions" rows="3"></textarea>
            </label>
            <div class="two-fields">
              <label class="field-label"
                >Temperature
                <input
                  v-model.number="promptForm.temperature"
                  type="number"
                  min="0"
                  max="2"
                  step="0.1"
              /></label>
              <label class="field-label"
                >Max tokens <input v-model.number="promptForm.max_tokens" type="number" min="1"
              /></label>
            </div>
            <label class="switch-row"
              ><span
                ><strong>اجعل القالب افتراضيًا</strong
                ><small>سيستخدمه Backend عند بناء سياق المحادثة.</small></span
              ><input type="checkbox" v-model="promptForm.is_default"
            /></label>
            <div class="button-row">
              <button
                class="primary-btn"
                type="button"
                @click="savePrompt"
                :disabled="promptsBusy || !promptForm.name.trim()"
              >
                {{ promptsBusy ? 'جارٍ الحفظ…' : 'حفظ القالب' }}
              </button>
              <button class="secondary-btn" type="button" @click="resetPromptForm">
                قالب جديد
              </button>
            </div>
          </div>
        </div>

        <div v-else class="settings-content">
          <div class="settings-section-title">
            <h3>حول الاتصال والحدود</h3>
            <HelpButton @click="showHelp('backendStatus')" />
          </div>
          <div class="status-card">
            <span class="status-dot" :class="{ online: backendAvailable }"></span>
            <div>
              <strong>{{ backendAvailable ? 'تم الاتصال بنجاح' : 'الاتصال غير مؤكد' }}</strong
              ><small>{{
                backendAvailable
                  ? 'تم تحميل إعدادات AI من API.'
                  : 'افحص تسجيل الدخول وعنوان API والخادم.'
              }}</small>
            </div>
          </div>
          <p class="info-note">
            المحادثات والإعدادات والقوالب وبيانات الاعتماد تتعامل مع نقاط API الموجودة. مراقبة
            التنفيذ، حدود الميزانية، وسجل التدقيق لا يتم تمثيلها هنا كميزات فعالة لأنها تحتاج إلى
            endpoints إضافية في Backend.
          </p>
          <button class="secondary-btn" type="button" @click="refreshAll">
            إعادة تحميل بيانات الخادم
          </button>
        </div>
        <div
          v-if="settingsNotice"
          class="notice"
          :class="{ error: settingsNoticeType === 'error' }"
          role="status"
        >
          {{ settingsNotice }}
        </div>
      </section>
    </div>

    <!-- Contextual help popup -->
    <div
      v-if="helpDialog.open"
      class="modal-backdrop help-backdrop"
      @click.self="helpDialog.open = false"
    >
      <section class="help-modal" role="dialog" aria-modal="true" aria-labelledby="help-title">
        <header class="modal-header">
          <div>
            <span class="eyebrow">مركز المساعدة</span>
            <h2 id="help-title">{{ helpDialog.title }}</h2>
          </div>
          <button
            class="icon-btn"
            type="button"
            aria-label="إغلاق"
            @click="helpDialog.open = false"
          >
            ×
          </button>
        </header>
        <p>{{ helpDialog.body }}</p>
        <div class="info-note">
          التغيير لا يُعتبر محفوظًا إلا بعد نجاح طلب API وظهور رسالة نجاح.
        </div>
        <button class="primary-btn full" type="button" @click="helpDialog.open = false">
          فهمت
        </button>
      </section>
    </div>
    <div v-if="toast" class="toast-message" role="status">{{ toast }}</div>
  </div>
</template>

<script setup>
import { computed, defineComponent, h, onMounted, reactive, ref, nextTick } from 'vue'
import aiControl from '@/services/AI/aiControl'
import { sendMessage as sendNonStreamingMessage, streamMessage } from '@/services/AI/Ai'
import MarkdownRenderer from '@/components/ai/MarkdownRenderer.vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
const direction = computed(() => locale.value === 'ar' ? 'rtl' : 'ltr')

const HelpButton = defineComponent({
  name: 'HelpButton',
  emits: ['click'],
  setup(_, { emit }) {
    return () =>
      h(
        'button',
        {
          class: 'help-button',
          type: 'button',
          title: 'شرح هذه الخاصية',
          'aria-label': 'شرح هذه الخاصية',
          onClick: (event) => {
            event.preventDefault()
            event.stopPropagation()
            emit('click')
          },
        },
        '?',
      )
  },
})

const helpCopy = {
  newConversation: [
    'محادثة جديدة',
    'ينشئ مساحة محادثة جديدة. عند إرسال أول رسالة، يقوم Backend بإنشاء سجل المحادثة وربط الرسائل بحسابك.',
  ],
  history: [
    'سجل المحادثات',
    'يعرض المحادثات النشطة المحفوظة على الخادم. يمكنك فتح محادثة لاستكمالها أو أرشفتها. بيانات كل مستخدم معزولة بحسب صلاحيات Backend.',
  ],
  backendStatus: [
    'حالة Backend',
    'هذه الحالة تعكس نجاح تحميل إعدادات AI من API، ولا تعني أن كل مزود خارجي يعمل. لاختبار المزود، حدّث قائمة النماذج من إعدادات المزود.',
  ],
  settings: [
    'إعدادات AI Core',
    'تتيح إدارة إعدادات AISettings، وبيانات اعتماد المزود، وقوالب التعليمات من نقاط API الموجودة في المشروع.',
  ],
  providerSettings: [
    'إدارة المزودات والقوالب',
    'من هنا تختار المزود الافتراضي، تحفظ مفتاح API بأمان على الخادم، وتدير Prompt Profiles. توفر الميزات يعتمد على إعدادات Backend والمزود.',
  ],
  provider: [
    'مزود الذكاء الاصطناعي',
    'المزود هو الخدمة التي تنفذ الطلب: Ollama محلي، OpenAI، Gemini، DeepSeek أو OpenRouter. يجب حفظ مفتاح المزود السحابي في إعدادات الاعتماد قبل اختباره أو استخدامه.',
  ],
  model: [
    'النموذج',
    'اسم النموذج الذي سيُطلب من المزود. قائمة النماذج تُحمّل من endpoint المزود، وقد لا تكون متاحة إن كان المزود غير مضبوط أو غير متصل.',
  ],
  generalSettings: [
    'إعدادات التشغيل',
    'هذه الحقول تقابل حقول AISettings في Django. اضغط حفظ الإعدادات لإرسالها عبر PATCH إلى /ai/settings/.',
  ],
  context: [
    'استخدام سياق التطبيق',
    'عند التفعيل، يمكن لخدمة AI الحالية تضمين سياق من بيانات التطبيق التي يسمح Backend باسترجاعها. لا يعني ذلك إرسال كل بيانات النظام بلا قيود.',
  ],
  maxContextTokens: [
    'حد سياق التوكنز',
    'قيمة حد السياق المخزنة في AISettings. التطبيق الفعلي لهذا الحد يعتمد على تنفيذ خدمة بناء السياق في Backend.',
  ],
  credentials: [
    'بيانات اعتماد المزودين',
    'أدخل مفتاح API لحفظه على الخادم. واجهة API تعيد حالة وجود المفتاح فقط ولا تعيد المفتاح نفسه. لا تضع أسرارًا في رسائل المحادثة.',
  ],
  prompts: [
    'قوالب التعليمات',
    'قالب Prompt Profile يتضمن اسمًا وتعليمات نظام وتعليمات سياق وTemperature وMax tokens. يمكن تعيين قالب افتراضي ليستخدمه Backend عند بناء المحادثة.',
  ],
  systemPrompt: [
    'System Prompt',
    'تعليمات تحدد الدور والأسلوب المطلوب من النموذج. استخدمها فقط مع بيانات تملك حق إرسالها، ولا تضع كلمات مرور أو مفاتيح API فيها.',
  ],
  assistantMessage: [
    'رسالة المساعد',
    'هذه هي الاستجابة المحفوظة من Backend، وقد يظهر بجانبها اسم المزود والنموذج اللذان أرجعهما الخادم.',
  ],
}

const sidebarCollapsed = ref(false)
const settingsOpen = ref(false)
const contextDialog = ref(false)
const contextLoading = ref(false)
const conversationContext = ref(null)
const contextError = ref('')
const settingsTab = ref('general')
const settingsTabs = [
  { id: 'general', label: 'عام', help: 'generalSettings' },
  { id: 'credentials', label: 'المزودات', help: 'credentials' },
  { id: 'prompts', label: 'قوالب Prompts', help: 'prompts' },
  { id: 'status', label: 'الاتصال والحدود', help: 'backendStatus' },
]
const conversations = ref([])
const activeConversationId = ref(null)
const lastArchivedConversation = ref(null)
const messages = ref([])
const draft = ref('')
const sending = ref(false)
const streamController = ref(null)
const retryDraft = ref('')
const retryIdempotencyKey = ref('')
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
  streaming_enabled: true,
  fallback_enabled: true,
  temperature: 0.7,
  timeout_seconds: 35,
})
const credentialForm = reactive({ provider: 'openai', api_key: '' })
const promptForm = reactive({
  id: null,
  name: '',
  system_prompt: '',
  context_instructions: '',
  temperature: null,
  max_tokens: null,
  is_default: false,
})
const helpDialog = reactive({ open: false, title: '', body: '' })

const activeConversationTitle = computed(() => {
  const active = conversations.value.find((item) => item.id === activeConversationId.value)
  return active?.title || 'محادثة جديدة'
})

function showHelp(key) {
  const copy = helpCopy[key] || [
    'شرح الخاصية',
    'هذه الخاصية مرتبطة بعناصر واجهة AI Core. راجع حالة الخادم ورسالة الاستجابة لمعرفة ما إذا تم حفظ التغيير.',
  ]
  helpDialog.title = copy[0]
  helpDialog.body = copy[1]
  helpDialog.open = true
}
function providerLabel(provider) {
  return (
    {
      ollama: 'Ollama',
      openai: 'OpenAI',
      openrouter: 'OpenRouter',
      gemini: 'Google Gemini',
      deepseek: 'DeepSeek',
    }[provider] ||
    provider ||
    'غير محدد'
  )
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
  window.setTimeout(() => {
    if (toast.value === message) toast.value = ''
  }, 3200)
}
function formatTime(value) {
  const date = new Date(value)
  return Number.isNaN(date.getTime())
    ? ''
    : date.toLocaleString('ar-EG', { dateStyle: 'short', timeStyle: 'short' })
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
    conversations.value = await aiControl.listAIConversations()
    backendAvailable.value = true
  } catch (error) {
    errorMessage.value = getErrorMessage(error, 'تعذر تحميل المحادثات.')
    backendAvailable.value = false
  } finally {
    loadingConversations.value = false
  }
}
async function loadCredentials() {
  try {
    credentials.value = await aiControl.getCredentials()
  } catch (error) {
    settingsNotice.value = getErrorMessage(error, 'تعذر تحميل بيانات الاعتماد.')
    settingsNoticeType.value = 'error'
  }
}
async function loadPrompts() {
  try {
    promptProfiles.value = await aiControl.listPromptProfiles()
  } catch (error) {
    settingsNotice.value = getErrorMessage(error, 'تعذر تحميل القوالب.')
    settingsNoticeType.value = 'error'
  }
}
async function loadModels() {
  modelsLoading.value = true
  try {
    const data = await aiControl.getProviderModels(settings.preferred_provider)
    availableModels.value = normalizeList(data).map(normalizeModel).filter(Boolean)
    if (data?.success === false) throw new Error(data.error || 'فشل جلب النماذج.')
    if (!availableModels.value.length)
      notify(
        'لم يرجع المزود قائمة نماذج. يمكنك كتابة اسم النموذج الافتراضي في إعدادات Backend.',
        'error',
      )
  } catch (error) {
    availableModels.value = []
    settingsNotice.value = getErrorMessage(error, 'تعذر تحميل النماذج لهذا المزود.')
    settingsNoticeType.value = 'error'
  } finally {
    modelsLoading.value = false
  }
}
async function testProvider() {
  modelsLoading.value = true
  try {
    const result = await aiControl.testProviderConnection(settings.preferred_provider)
    if (result?.connected) {
      availableModels.value = normalizeList({ models: result.models })
        .map(normalizeModel)
        .filter(Boolean)
      notify(`الاتصال ناجح مع ${providerLabel(settings.preferred_provider)}.`, 'success')
    } else {
      throw new Error(result?.error || 'فشل الاتصال بالمزود.')
    }
  } catch (error) {
    settingsNotice.value = getErrorMessage(error, 'فشل اختبار الاتصال بالمزود.')
    settingsNoticeType.value = 'error'
  } finally {
    modelsLoading.value = false
  }
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
      streaming_enabled: Boolean(settings.streaming_enabled),
      fallback_enabled: Boolean(settings.fallback_enabled),
      temperature: Number(settings.temperature),
      timeout_seconds: Number(settings.timeout_seconds),
    }
    const saved = await aiControl.updateAISettings(payload)
    Object.assign(settings, saved)
    notify('تم حفظ إعدادات AI على الخادم.')
  } catch (error) {
    const message = getErrorMessage(error, 'تعذر حفظ الإعدادات.')
    settingsNotice.value = message
    settingsNoticeType.value = 'error'
    errorMessage.value = message
  } finally {
    savingSettings.value = false
  }
}
async function saveCredentialAction() {
  if (!credentialForm.api_key.trim()) return
  credentialsBusy.value = true
  try {
    await aiControl.saveCredential({
      provider: credentialForm.provider,
      api_key: credentialForm.api_key,
    })
    credentialForm.api_key = ''
    await loadCredentials()
    notify('تم إرسال بيانات الاعتماد إلى الخادم وحفظها.')
  } catch (error) {
    settingsNotice.value = getErrorMessage(error, 'تعذر حفظ بيانات الاعتماد.')
    settingsNoticeType.value = 'error'
  } finally {
    credentialsBusy.value = false
  }
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
  } finally {
    credentialsBusy.value = false
  }
}
function resetPromptForm() {
  Object.assign(promptForm, {
    id: null,
    name: '',
    system_prompt: '',
    context_instructions: '',
    temperature: null,
    max_tokens: null,
    is_default: false,
  })
}
function editPrompt(profile) {
  Object.assign(promptForm, {
    id: profile.id,
    name: profile.name || '',
    system_prompt: profile.system_prompt || '',
    context_instructions: profile.context_instructions || '',
    temperature: profile.temperature ?? null,
    max_tokens: profile.max_tokens ?? null,
    is_default: Boolean(profile.is_default),
  })
}
async function savePrompt() {
  promptsBusy.value = true
  try {
    const payload = {
      name: promptForm.name.trim(),
      system_prompt: promptForm.system_prompt,
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
  } finally {
    promptsBusy.value = false
  }
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
    const conversation = await aiControl.createAIConversation({
      title: '',
      provider: settings.preferred_provider,
      model: settings.preferred_model || '',
    })
    conversations.value = [
      conversation,
      ...conversations.value.filter((item) => item.id !== conversation.id),
    ]
    activeConversationId.value = conversation.id
    notify('تم إنشاء محادثة جديدة.')
  } catch (error) {
    // The chat endpoint can create a conversation when conversation_id is null,
    // so allow the user to continue even if pre-creation failed.
    errorMessage.value = getErrorMessage(
      error,
      'تعذر إنشاء محادثة جديدة. سيتم المحاولة عند الإرسال.',
    )
  }
}
async function selectConversation(id) {
  if (sending.value) return
  errorMessage.value = ''
  try {
    const conversation = await aiControl.getAIConversation(id)
    activeConversationId.value = conversation.id
    messages.value = (conversation.messages || []).filter((message) => message.role !== 'system')
    await scrollToBottom()
  } catch (error) {
    errorMessage.value = getErrorMessage(error, 'تعذر فتح المحادثة.')
  }
}
async function archiveConversation(id) {
  if (!window.confirm('هل تريد أرشفة هذه المحادثة؟')) return
  try {
    const archived = conversations.value.find((item) => item.id === id)
    await aiControl.setAIConversationAction(id, 'archive')
    lastArchivedConversation.value = archived || { id, title: `محادثة #${id}` }
    conversations.value = conversations.value.filter((item) => item.id !== id)
    if (activeConversationId.value === id) {
      activeConversationId.value = null
      messages.value = []
    }
    notify('تمت أرشفة المحادثة.')
  } catch (error) {
    errorMessage.value = getErrorMessage(error, 'تعذرت أرشفة المحادثة.')
  }
}
async function restoreLastArchived() {
  if (!lastArchivedConversation.value?.id) return
  try {
    const restored = await aiControl.setAIConversationAction(lastArchivedConversation.value.id, 'restore')
    conversations.value = [restored, ...conversations.value.filter((item) => item.id !== restored.id)]
    lastArchivedConversation.value = null
    notify('تمت استعادة المحادثة.')
  } catch (error) {
    errorMessage.value = getErrorMessage(error, 'تعذرت استعادة المحادثة.')
  }
}
async function deleteConversation(id) {
  if (!window.confirm('سيتم حذف المحادثة وإخفاؤها من السجل. هل تريد المتابعة؟')) return
  try {
    await aiControl.setAIConversationAction(id, 'delete')
    conversations.value = conversations.value.filter((item) => item.id !== id)
    if (activeConversationId.value === id) {
      activeConversationId.value = null
      messages.value = []
    }
    if (lastArchivedConversation.value?.id === id) lastArchivedConversation.value = null
    notify('تم حذف المحادثة.')
  } catch (error) {
    errorMessage.value = getErrorMessage(error, 'تعذر حذف المحادثة.')
  }
}
async function inspectContext() {
  if (!activeConversationId.value) return
  contextDialog.value = true
  contextLoading.value = true
  contextError.value = ''
  conversationContext.value = null
  try {
    conversationContext.value = await aiControl.getAIConversationContext(activeConversationId.value)
  } catch (error) {
    contextError.value = getErrorMessage(error, 'تعذر فحص سياق المحادثة.')
  } finally {
    contextLoading.value = false
  }
}
function useSuggestion(text) {
  draft.value = text
}
function onComposerKeydown(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}
function cancelStream() {
  streamController.value?.abort()
}

async function sendMessage() {
  const content = draft.value.trim()
  if (!content || sending.value) return
  sending.value = true
  errorMessage.value = ''
  draft.value = ''
  const localUserId = `local-user-${Date.now()}`
  const localAssistantId = `local-assistant-${Date.now()}`
  const idempotencyKey = retryDraft.value === content && retryIdempotencyKey.value
    ? retryIdempotencyKey.value
    : (globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random().toString(36).slice(2)}`)
  messages.value.push({
    id: localUserId,
    role: 'user',
    content,
    created_at: new Date().toISOString(),
  })
  messages.value.push({
    id: localAssistantId,
    role: 'assistant',
    content: '',
    provider: settings.preferred_provider,
    model: settings.preferred_model,
    streaming: true,
  })
  streamController.value = new AbortController()
  await scrollToBottom()
  try {
    const requestPayload = {
      message: content,
      conversation_id: activeConversationId.value || null,
      provider: settings.preferred_provider,
      model: settings.preferred_model || '',
      idempotencyKey,
      signal: streamController.value.signal,
    }
    const response = settings.streaming_enabled
      ? await streamMessage({
          ...requestPayload,
          onChunk: (chunk) => {
            const assistantMessage = messages.value.find((item) => item.id === localAssistantId)
            if (assistantMessage) assistantMessage.content += chunk
            scrollToBottom()
          },
        })
      : await sendNonStreamingMessage(requestPayload)
    activeConversationId.value = response.conversation_id || activeConversationId.value
    retryDraft.value = ''
    retryIdempotencyKey.value = ''
    const assistant = messages.value.find((item) => item.id === localAssistantId)
    if (assistant) {
      assistant.id = response.message?.id || localAssistantId
      assistant.content = response.message?.content || assistant.content
      assistant.provider = response.provider || response.message?.provider || assistant.provider
      assistant.model = response.model || response.message?.model || assistant.model
      assistant.streaming = false
      assistant.created_at = new Date().toISOString()
    }
    await loadConversations()
    if (activeConversationId.value) {
      const conversation = await aiControl.getAIConversation(activeConversationId.value)
      messages.value = (conversation.messages || []).filter((item) => item.role !== 'system')
    }
    await scrollToBottom()
  } catch (error) {
    messages.value = messages.value.filter((item) => item.id !== localAssistantId)
    if (error?.name === 'AbortError') {
      errorMessage.value = 'تم إيقاف البث. لم يتم تأكيد اكتمال الرسالة أو حفظها.'
    } else {
      errorMessage.value = getErrorMessage(error, 'تعذر إرسال الرسالة إلى AI Backend.')
    }
    draft.value = content
    retryDraft.value = content
    retryIdempotencyKey.value = error?.code === 'previous_attempt_failed' ? '' : idempotencyKey
  } finally {
    sending.value = false
    streamController.value = null
  }
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
  if (messagesContainer.value)
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
}
onMounted(async () => {
  try {
    await loadSettings()
  } catch (error) {
    backendAvailable.value = false
    errorMessage.value = getErrorMessage(
      error,
      'تعذر تحميل إعدادات AI. تحقق من تسجيل الدخول واتصال Backend.',
    )
  }
  await Promise.all([loadConversations(), loadCredentials(), loadPrompts()])
  await loadModels()
})
</script>
