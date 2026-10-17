<template>
  <div class="page">
    <header>
      <div>
        <span>CONTROL CENTER</span>
        <h1>Settings</h1>
        <p>إعدادات AI والتعلم اليومية محفوظة في Django.</p>
      </div>
      <Button label="حفظ AI" icon="pi pi-save" :loading="saving" @click="save" />
    </header>
    <Message v-if="error" severity="error">{{ error }}</Message>
    <div class="grid">
      <Card
        ><template #title>AI Provider</template
        ><template #content
          ><div class="form">
            <label
              >Provider<Select v-model="settings.preferred_provider" :options="providers" /></label
            ><label
              >Model<Select
                v-model="settings.preferred_model"
                :options="models"
                :loading="modelsLoading" /></label
            ><label>Context enabled<Checkbox v-model="settings.context_enabled" binary /></label
            ><label
              >Max context tokens<InputNumber
                v-model="settings.max_context_tokens"
                :min="256"
                :max="32000"
            /></label></div></template
      ></Card>
      <Card
        ><template #title>Credentials</template
        ><template #content
          ><DataTable :value="credentials" size="small"
            ><Column field="provider" header="Provider" /><Column header="Status"
              ><template #body="s"
                ><Tag
                  :value="s.data.has_api_key ? 'Configured' : 'Not configured'"
                  :severity="s.data.has_api_key ? 'success' : 'secondary'" /></template></Column
            ><Column header="Actions"
              ><template #body="s"
                ><Button
                  icon="pi pi-trash"
                  text
                  severity="danger"
                  @click="removeCredential(s.data.provider)" /></template></Column></DataTable
          ><Divider />
          <div class="credential">
            <Select v-model="credential.provider" :options="providers" /><Password
              v-model="credential.api_key"
              toggleMask
              placeholder="API Key"
            /><Button label="Add / Update" @click="addCredential" /></div></template
      ></Card>
      <Card class="wide"
        ><template #title>Learning Automation</template
        ><template #content
          ><div class="learning-settings">
            <label
              >Daily Learning Tasks<InputNumber
                v-model="learning.daily_learning_tasks"
                :min="1"
                :max="50" /></label
            ><label
              >Current Learning Goal<Select
                v-model="learning.current_learning_goal"
                :options="learningGoals"
                optionLabel="title"
                optionValue="id"
                placeholder="Select a goal"
                showClear /></label
            ><label
              >Task Generation Enabled<Checkbox
                v-model="learning.task_generation_enabled"
                binary /></label
            ><label
              >Preferred Learning Time<input v-model="learning.preferred_learning_time" type="time"
            /></label>
          </div>
          <div class="save-row">
            <Button
              label="حفظ إعدادات التعلم"
              icon="pi pi-check"
              :loading="learningSaving"
              @click="saveLearning"
            /></div></template
      ></Card>
      <Card class="wide"
        ><template #title>Prompt Profiles</template
        ><template #content
          ><div class="prompt-list">
            <div v-for="p in prompts" :key="p.id" class="prompt">
              <div>
                <strong>{{ p.name }}</strong>
                <p>{{ p.system_prompt }}</p>
              </div>
              <Tag v-if="p.is_default" value="Default" /><Button
                icon="pi pi-trash"
                text
                severity="danger"
                @click="deletePromptProfile(p.id)"
              />
            </div>
          </div>
          <div class="credential">
            <InputText v-model="newPrompt.name" placeholder="Profile name" /><Textarea
              v-model="newPrompt.system_prompt"
              rows="3"
              placeholder="System prompt"
            /><Button label="Create profile" @click="createPrompt" /></div></template
      ></Card>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import api from '@/services/api'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Select from 'primevue/select'
import Checkbox from 'primevue/checkbox'
import InputNumber from 'primevue/inputnumber'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import Password from 'primevue/password'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Divider from 'primevue/divider'
import Message from 'primevue/message'
import { getLearningSettings, updateLearningSettings } from '@/services/settings'
import {
  getAISettings,
  updateAISettings,
  getCredentials,
  saveCredential,
  deleteCredential,
  getProviderModels,
  listPromptProfiles,
  createPromptProfile,
  deletePromptProfile as removePromptProfile,
} from '@/services/aiControl'
const providers = ['ollama', 'openai', 'openrouter'],
  settings = reactive({
    preferred_provider: 'ollama',
    preferred_model: '',
    temperature: 0.7,
    context_enabled: true,
    max_context_tokens: 4096,
  }),
  models = ref([]),
  credentials = ref([]),
  prompts = ref([]),
  saving = ref(false),
  modelsLoading = ref(false),
  error = ref(''),
  credential = reactive({ provider: 'openai', api_key: '' }),
  newPrompt = reactive({ name: '', system_prompt: '' }),
  learning = reactive({
    daily_learning_tasks: 5,
    current_learning_goal: null,
    task_generation_enabled: true,
    preferred_learning_time: '',
  }),
  learningGoals = ref([]),
  learningSaving = ref(false)
async function load() {
  try {
    Object.assign(settings, await getAISettings())
    Object.assign(learning, await getLearningSettings())
    const g = await api.get('/learning/goals/')
    learningGoals.value = Array.isArray(g.data) ? g.data : g.data?.results || []
    credentials.value = await getCredentials()
    prompts.value = await listPromptProfiles()
    await loadModels()
  } catch {
    error.value = 'تعذر تحميل الإعدادات.'
  }
}
async function loadModels() {
  modelsLoading.value = true
  try {
    const r = await getProviderModels(settings.preferred_provider)
    models.value = r.models || []
  } catch {
    models.value = []
  } finally {
    modelsLoading.value = false
  }
}
watch(() => settings.preferred_provider, loadModels)
async function save() {
  saving.value = true
  try {
    await updateAISettings({ ...settings })
  } catch {
    error.value = 'تعذر حفظ إعدادات AI.'
  } finally {
    saving.value = false
  }
}
async function saveLearning() {
  learningSaving.value = true
  try {
    await updateLearningSettings({ ...learning })
  } catch {
    error.value = 'تعذر حفظ إعدادات التعلم.'
  } finally {
    learningSaving.value = false
  }
}
async function addCredential() {
  if (!credential.api_key) return
  try {
    await saveCredential(credential)
    credential.api_key = ''
    credentials.value = await getCredentials()
  } catch {
    error.value = 'تعذر حفظ المفتاح.'
  }
}
async function removeCredential(p) {
  try {
    await deleteCredential(p)
    credentials.value = await getCredentials()
  } catch {
    error.value = 'تعذر حذف المفتاح.'
  }
}
async function createPrompt() {
  if (!newPrompt.name) return
  try {
    await createPromptProfile({ ...newPrompt })
    newPrompt.name = ''
    newPrompt.system_prompt = ''
    prompts.value = await listPromptProfiles()
  } catch {
    error.value = 'تعذر إنشاء Prompt profile.'
  }
}
async function deletePromptProfile(id) {
  try {
    await removePromptProfile(id)
    prompts.value = await listPromptProfiles()
  } catch {
    error.value = 'تعذر حذف الـ Prompt.'
  }
}
onMounted(load)
</script>
