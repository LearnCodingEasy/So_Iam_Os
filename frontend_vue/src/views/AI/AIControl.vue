<template>
  <main class="ai-control-page" :dir="direction">
    <header class="ai-control-header">
      <div>
        <span class="eyebrow">AI CONTROL CENTER</span>
        <h1>مركز التحكم بالذكاء الاصطناعي</h1>
        <p>إدارة المزودين والمفاتيح والنماذج، واستخدام نفس إعدادات AI في تطبيقات النظام.</p>
      </div>
      <Tag :value="settings.preferred_provider || 'ollama'" severity="info" />
    </header>

    <section class="provider-grid">
      <Card class="provider-card">
        <template #title>إعدادات المزودين</template>
        <template #content>
          <div class="provider-form">
            <label for="ai-provider">المزود</label>
            <Select id="ai-provider" v-model="selectedProvider" :options="providerOptions"
              optionLabel="label" optionValue="value" placeholder="اختر المزود" class="w-full"
              @change="loadModels" />
            <label for="ai-base-url">Base URL (اختياري)</label>
            <InputText id="ai-base-url" v-model="baseUrl" placeholder="https://..." class="w-full" />
            <small v-if="errors.baseUrl" class="field-error">{{ errors.baseUrl }}</small>
            <label for="ai-model">الموديل</label>
            <Select id="ai-model" v-model="selectedModel" :options="modelOptions"
              optionLabel="label" optionValue="value" placeholder="اختر الموديل أو اكتب اسمه"
              editable class="w-full" />
            <label for="ai-api-key">مفتاح API</label>
            <small v-if="errors.apiKey" class="field-error">{{ errors.apiKey }}</small>
            <Password id="ai-api-key" v-model="apiKey" :feedback="false" toggleMask
              :placeholder="credentialStatus ? 'اتركه فارغًا للاحتفاظ بالمفتاح الحالي' : 'أدخل API Key'"
              class="w-full" inputClass="w-full" />
            <label for="ai-priority">أولوية المزود</label>
            <InputText id="ai-priority" v-model="priority" inputmode="numeric" class="w-full" />
            <small v-if="errors.priority" class="field-error">{{ errors.priority }}</small>
            <div class="provider-actions">
              <Button label="حفظ إعدادات المزود" icon="pi pi-lock" :loading="savingCredential"
                @click="saveProviderCredential" />
              <Button label="اختبار الاتصال" icon="pi pi-bolt" severity="secondary" outlined
                :loading="testingProvider" @click="testProvider" />
            </div>
            <div class="provider-actions">
              <Button label="تعيين كمزود افتراضي" icon="pi pi-check"
                :loading="savingSettings" @click="saveProviderSettings" />
              <Button label="تحميل النماذج" icon="pi pi-refresh" severity="secondary" outlined
                :loading="loadingModels" @click="loadModels" />
            </div>
            <Message v-if="providerMessage" :severity="providerMessage.severity" :closable="true"
              @close="providerMessage = null">{{ providerMessage.text }}</Message>
            <small class="security-note">المفتاح يُرسل إلى Django ويُخزن مشفرًا. لا يتم إرجاع قيمته إلى المتصفح بعد الحفظ.</small>
          </div>
        </template>
      </Card>

      <Card class="provider-card">
        <template #title>حالة المزودين</template>
        <template #content>
          <div v-if="providerRows.length" class="provider-list">
            <div v-for="item in providerRows" :key="item.provider" class="provider-row">
              <div>
                <strong>{{ providerLabel(item.provider) }}</strong>
                <small>{{ item.has_api_key ? 'مفتاح محفوظ' : item.provider === 'ollama' ? 'مزود محلي' : 'لا يوجد مفتاح مستخدم' }}</small>
              </div>
              <div class="provider-tags">
                <Tag v-if="item.is_default" value="افتراضي" severity="success" />
                <Tag :value="item.has_api_key || item.provider === 'ollama' ? 'مهيأ' : 'غير مهيأ'"
                  :severity="item.has_api_key || item.provider === 'ollama' ? 'success' : 'secondary'" />
                <Button v-if="item.has_api_key" icon="pi pi-trash" text rounded severity="danger"
                  aria-label="حذف المفتاح" @click="removeCredential(item.provider)" />
              </div>
            </div>
          </div>
          <Message v-else severity="info">لا توجد بيانات مزودين حتى الآن.</Message>
        </template>
      </Card>
    </section>

    <section class="ai-workspace-grid">
      <Card>
        <template #title>المحادثة</template>
        <template #content>
          <div class="messages">
            <div v-for="m in messages" :key="m.id" :class="['message', m.role]">
              <small>{{ m.role }} <span v-if="m.provider">· {{ m.provider }} / {{ m.model }}</span></small>
              <MarkdownRenderer v-if="m.role === 'assistant'" :content="m.content" />
              <div v-else>{{ m.content }}</div>
            </div>
            <Message v-if="chatError" severity="error">{{ chatError }}</Message>
          </div>
          <div class="composer">
            <Textarea v-model="prompt" rows="4" placeholder="اكتب طلبك..." />
            <Button label="إرسال" icon="pi pi-send" :loading="sending" :disabled="!prompt.trim()" @click="send" />
          </div>
        </template>
      </Card>

      <Card>
        <template #title>إنشاء خطة تعلم</template>
        <template #content>
          <Textarea v-model="planPrompt" rows="5" placeholder="مثال: أريد تعلم Django Advanced خلال 8 أسابيع" />
          <div class="provider-actions">
            <Button label="إنشاء معاينة" icon="pi pi-sparkles" :loading="generating"
              :disabled="!planPrompt.trim()" @click="generate" />
            <Button label="توليد بالخلفية" icon="pi pi-clock" severity="secondary" outlined
              :loading="asyncGenerating" :disabled="!planPrompt.trim()" @click="generateAsync" />
            <Button v-if="plan" label="اعتماد وإنشاء" severity="success" icon="pi pi-check"
              :loading="approving" @click="approve" />
          </div>
          <Message v-if="planError" severity="error">{{ planError }}</Message>
          <Message v-if="taskStatus" severity="info">حالة المهمة: {{ taskStatus.status }}</Message>
          <MarkdownRenderer v-if="plan" :content="planMarkdown" />
        </template>
      </Card>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { gsap } from 'gsap'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'
import NProgress from 'nprogress'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Message from 'primevue/message'
import Password from 'primevue/password'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import Textarea from 'primevue/textarea'
import InputText from 'primevue/inputtext'
import MarkdownRenderer from '@/components/ai/MarkdownRenderer.vue'
import { sendMessage } from '@/services/AI/Ai'
import {
  approveLearningPlan, deleteCredential, getAISettings, getCredentials,
  getProviderModels, listAIProviders, previewLearningPlan, saveCredential,
  testProviderConnection, updateAISettings,
  getTaskStatus, startLearningPlanAsync,
} from '@/services/AI/aiControl'

const { locale } = useI18n()
const direction = computed(() => locale.value === 'ar' ? 'rtl' : 'ltr')

const providerOptions = [
  { label: 'Ollama', value: 'ollama' },
  { label: 'OpenAI', value: 'openai' },
  { label: 'OpenRouter', value: 'openrouter' },
  { label: 'Google Gemini', value: 'gemini' },
  { label: 'DeepSeek', value: 'deepseek' },
]
const settings = ref({ preferred_provider: 'ollama', preferred_model: '' })
const selectedProvider = ref('ollama')
const selectedModel = ref('')

const credentials = ref([])
const providerRows = ref([])
const modelOptions = ref([])
const providerMessage = ref(null)
const chatError = ref('')
const planError = ref('')
const messages = ref([])
const prompt = ref('')
const planPrompt = ref('')
const plan = ref(null)
const taskStatus = ref(null)
const sending = ref(false)
const generating = ref(false)
const asyncGenerating = ref(false)
const approving = ref(false)
const savingCredential = ref(false)
const savingSettings = ref(false)
const testingProvider = ref(false)
const loadingModels = ref(false)

const credentialSchema = toTypedSchema(z.object({
  apiKey: z.string().trim().optional().or(z.literal('')),
  baseUrl: z.string().trim().url('Base URL غير صالح').or(z.literal('')),
  model: z.string().trim().max(255).optional(),
  priority: z.coerce.number().int().min(1).max(999),
}))
const { handleSubmit, errors, defineField } = useForm({
  validationSchema: credentialSchema,
  initialValues: { apiKey: '', baseUrl: '', model: '', priority: 100 },
})
const [apiKey] = defineField('apiKey')
const [baseUrl] = defineField('baseUrl')
const [model] = defineField('model')
const [priority] = defineField('priority')

const planMarkdown = computed(() => plan.value ? `\`\`\`json\n${JSON.stringify(plan.value, null, 2)}\n\`\`\`` : '')

const credentialStatus = computed(() =>
  credentials.value.some((item) => item.provider === selectedProvider.value && item.has_api_key),
)

function providerLabel(provider) {
  return providerOptions.find((item) => item.value === provider)?.label || provider
}

async function refreshProviderData() {
  const [savedCredentials, providers] = await Promise.all([
    getCredentials(),
    listAIProviders(),
  ])
  credentials.value = savedCredentials
  providerRows.value = providers.providers || []
}

async function load() {
  try {
    settings.value = await getAISettings()
    selectedProvider.value = settings.value.preferred_provider || 'ollama'
    selectedModel.value = settings.value.preferred_model || ''
    gsap.fromTo('.ai-control-header', { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.35, ease: 'power2.out' })
    await refreshProviderData()
    await loadModels()
  } catch (error) {
    providerMessage.value = { severity: 'error', text: error?.response?.data?.detail || 'تعذر تحميل إعدادات الذكاء الاصطناعي.' }
  }
}

const saveProviderCredential = handleSubmit(async (values) => {
  savingCredential.value = true
  providerMessage.value = null
  try {
    NProgress.start()
    const credentialPayload = { provider: selectedProvider.value, base_url: values.baseUrl, model: values.model || selectedModel.value, priority: values.priority }
    if (values.apiKey.trim()) credentialPayload.api_key = values.apiKey.trim()
    await saveCredential(credentialPayload)
    apiKey.value = ''
    await refreshProviderData()
    providerMessage.value = { severity: 'success', text: `تم حفظ إعدادات ${providerLabel(selectedProvider.value)} بشكل آمن.` }
  } catch (error) {
    providerMessage.value = { severity: 'error', text: error?.response?.data?.detail || 'تعذر حفظ المفتاح.' }
  } finally {
    savingCredential.value = false
    NProgress.done()
  }
})

async function removeCredential(provider) {
  try {
    await deleteCredential(provider)
    await refreshProviderData()
    providerMessage.value = { severity: 'success', text: `تم حذف بيانات ${providerLabel(provider)}.` }
  } catch {
    providerMessage.value = { severity: 'error', text: 'تعذر حذف بيانات المزود.' }
  }
}

async function saveProviderSettings() {
  savingSettings.value = true
  try {
    settings.value = await updateAISettings({
      preferred_provider: selectedProvider.value,
      preferred_model: selectedModel.value,
    })
    providerMessage.value = { severity: 'success', text: 'تم تحديث المزود الافتراضي.' }
    await refreshProviderData()
  } catch (error) {
    providerMessage.value = { severity: 'error', text: error?.response?.data?.detail || 'تعذر تحديث الإعدادات.' }
  } finally {
    savingSettings.value = false
  }
}

async function testProvider() {
  testingProvider.value = true
  try {
    const result = await testProviderConnection(selectedProvider.value, selectedModel.value)
    providerMessage.value = {
      severity: result.connected ? 'success' : 'error',
      text: result.connected
        ? `نجح اختبار التوليد الفعلي باستخدام ${result.model || selectedModel.value || selectedProvider.value}.`
        : result.error || 'فشل الاتصال بالمزود.',
    }
    if (result.connected) modelOptions.value = (result.models || []).map((item) => ({ label: item.name || item.id, value: item.id }))
  } catch (error) {
    providerMessage.value = { severity: 'error', text: error?.response?.data?.error || 'فشل اختبار الاتصال.' }
  } finally {
    testingProvider.value = false
  }
}

async function loadModels() {
  loadingModels.value = true
  modelOptions.value = []
  try {
    const result = await getProviderModels(selectedProvider.value)
    modelOptions.value = (result.models || []).map((item) => ({ label: item.name || item.id, value: item.id }))
  } catch (error) {
    providerMessage.value = { severity: 'warn', text: error?.response?.data?.error || 'تعذر تحميل قائمة النماذج؛ يمكنك كتابة اسم الموديل يدويًا.' }
  } finally {
    loadingModels.value = false
  }
}

async function send() {
  if (!prompt.value.trim()) return
  sending.value = true
  chatError.value = ''
  const question = prompt.value.trim()
  try {
    const result = await sendMessage({
      message: question,
      provider: settings.value.preferred_provider,
      model: settings.value.preferred_model,
    })
    messages.value.push(
      { id: `${Date.now()}-user`, role: 'user', content: question },
      { id: `${Date.now()}-assistant`, role: 'assistant', content: result.message?.content || 'لم يصل رد.', provider: result.message?.provider, model: result.message?.model },
    )
    prompt.value = ''
  } catch (error) {
    chatError.value = error?.response?.data?.error || 'تعذر الاتصال بمزود الذكاء الاصطناعي. راجع إعدادات المزودين.'
  } finally {
    sending.value = false
  }
}

async function generate() {
  if (!planPrompt.value.trim()) return
  generating.value = true
  planError.value = ''
  plan.value = null
  try {
    const result = await previewLearningPlan({
      message: planPrompt.value,
      provider: settings.value.preferred_provider,
      model: settings.value.preferred_model,
    })
    plan.value = result.plan
  } catch (error) {
    planError.value = error?.response?.data?.error || 'تعذر إنشاء المعاينة.'
  } finally {
    generating.value = false
  }
}

async function poll(taskId) {
  for (let index = 0; index < 30; index += 1) {
    await new Promise((resolve) => setTimeout(resolve, 2000))
    taskStatus.value = await getTaskStatus(taskId)
    if (['completed', 'success', 'failed', 'failure'].includes(taskStatus.value.status)) {
      if (taskStatus.value.status === 'success' && taskStatus.value.result) plan.value = taskStatus.value.result.plan || taskStatus.value.result
      if (['failed', 'failure'].includes(taskStatus.value.status)) planError.value = taskStatus.value.error || 'فشلت مهمة توليد خطة التعلم.'
      break
    }
  }
}

async function generateAsync() {
  if (!planPrompt.value.trim()) return
  asyncGenerating.value = true
  planError.value = ''
  taskStatus.value = null
  try {
    const task = await startLearningPlanAsync({
      message: planPrompt.value,
      provider: settings.value.preferred_provider,
      model: settings.value.preferred_model,
    })
    taskStatus.value = task
    await poll(task.task_id)
  } catch (error) {
    planError.value = error?.response?.data?.detail || error?.response?.data?.error || error?.message || 'تعذر بدء مهمة التعلم.'
  } finally {
    asyncGenerating.value = false
  }
}

async function approve() {
  if (!plan.value) return
  approving.value = true
  try {
    await approveLearningPlan(plan.value)
    planError.value = ''
  } catch (error) {
    planError.value = error?.response?.data?.error || 'تعذر اعتماد خطة التعلم.'
  } finally {
    approving.value = false
  }
}

onMounted(load)
</script>

<style lang="scss">
@use '@/assets/scss/views/AIControl.scss';
</style>

<style lang="scss" src="@/assets/scss/AI/AI.scss"></style>
