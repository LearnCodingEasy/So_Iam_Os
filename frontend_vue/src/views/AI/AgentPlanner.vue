<template>
  <main class="agent-planner-page" :dir="direction">
    <header><span class="eyebrow">AI AGENTS</span><h1>مخطط الوكلاء ومقترحات المهام</h1><p>خطط مقترحة واختيار مزود مناسب ومراجعة مقترحات المهام دون تنفيذ تلقائي.</p></header>
    <div class="planner-grid">
      <Card>
        <template #title>تخطيط Workflow</template>
        <template #content>
          <Textarea v-model="request" rows="5" class="w-full" placeholder="صف الهدف أو العملية المطلوبة..." />
          <div class="actions"><Button label="إنشاء خطة" icon="pi pi-sparkles" :loading="planning" :disabled="!request.trim()" @click="plan" /><Button label="اختيار Agent / Provider" severity="secondary" outlined icon="pi pi-compass" :loading="selecting" :disabled="!request.trim()" @click="selectAgent" /></div>
          <Message v-if="error" severity="error" class="mt-3">{{ error }}</Message>
          <Message v-if="selection" severity="info" class="mt-3">المزود: {{ selection.provider }} · النموذج: {{ selection.model }} — {{ selection.reason }}</Message>
          <div v-if="result" class="mt-4">
            <Message severity="success">{{ result.explanation }} هذا مخطط مقترح وليس تنفيذاً.</Message>
            <DataTable :value="result.nodes || []" class="mt-3"><Column field="id" header="ID" /><Column field="type" header="Node" /><Column field="label" header="Label" /></DataTable>
            <pre class="json-view">{{ JSON.stringify(result.edges || [], null, 2) }}</pre>
          </div>
        </template>
      </Card>
      <Card>
        <template #title>مقترح مهمة</template>
        <template #content>
          <div class="form-stack">
            <label>عنوان المهمة<InputText v-model="task.title" maxlength="255" /></label>
            <label>الوصف<Textarea v-model="task.description" rows="3" autoResize /></label>
            <label>الخطوات (كل خطوة في سطر)<Textarea v-model="stepsText" rows="4" /></label>
            <label>الأولوية<Select v-model="task.priority" :options="priorityOptions" optionLabel="label" optionValue="value" /></label>
            <Button label="إنشاء مقترح" icon="pi pi-list-check" :loading="proposing" :disabled="!task.title.trim()" @click="createProposal" />
          </div>
          <Message v-if="proposalError" severity="error" class="mt-3">{{ proposalError }}</Message>
          <div v-if="proposal" class="proposal-result mt-3"><Tag value="مقترح فقط — لم يتم إنشاء مهمة" severity="warn" /><pre class="json-view">{{ JSON.stringify(proposal, null, 2) }}</pre></div>
        </template>
      </Card>
    </div>
  </main>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Textarea from 'primevue/textarea'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Message from 'primevue/message'
import Tag from 'primevue/tag'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import aiControl from '@/services/AI/aiControl'

const { locale } = useI18n()
const direction = computed(() => locale.value === 'ar' ? 'rtl' : 'ltr')
const request = ref('')
const planning = ref(false), selecting = ref(false), proposing = ref(false)
const error = ref(''), proposalError = ref('')
const result = ref(null), selection = ref(null), proposal = ref(null)
const task = reactive({ title: '', description: '', priority: 'medium' })
const stepsText = ref('')
const priorityOptions = [{ label: 'منخفضة', value: 'low' }, { label: 'متوسطة', value: 'medium' }, { label: 'عالية', value: 'high' }, { label: 'عاجلة', value: 'urgent' }]

async function plan() {
  if (!request.value.trim()) return
  planning.value = true; error.value = ''; result.value = null
  try { result.value = await aiControl.createAgentPlan({ request: request.value.trim() }) }
  catch (cause) { error.value = cause?.response?.data?.detail || cause?.response?.data?.error || cause?.message || 'تعذر إنشاء الخطة.' }
  finally { planning.value = false }
}
async function selectAgent() {
  if (!request.value.trim()) return
  selecting.value = true; error.value = ''; selection.value = null
  try { selection.value = await aiControl.selectAIAgent({ message: request.value.trim(), task_type: 'chat' }) }
  catch (cause) { error.value = cause?.response?.data?.detail || cause?.message || 'تعذر اختيار Agent.' }
  finally { selecting.value = false }
}
async function createProposal() {
  proposing.value = true; proposalError.value = ''; proposal.value = null
  try {
    proposal.value = await aiControl.proposeAITask({
      title: task.title.trim(), description: task.description,
      steps: stepsText.value.split('\n').map((line) => line.trim()).filter(Boolean),
      priority: task.priority,
    })
  } catch (cause) { proposalError.value = cause?.response?.data?.detail || cause?.message || 'تعذر إنشاء مقترح المهمة.' }
  finally { proposing.value = false }
}
</script>

<style scoped>
.agent-planner-page{padding:clamp(1rem,2vw,2rem);display:grid;gap:1.2rem}.agent-planner-page h1{margin:.3rem 0}.agent-planner-page header p{color:var(--p-text-muted-color)}.eyebrow{color:var(--p-primary-color);font-size:.75rem;letter-spacing:.12em;font-weight:700}.planner-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}.w-full{width:100%}.actions{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.8rem}.form-stack{display:grid;gap:.8rem}.form-stack label{display:grid;gap:.35rem}.form-stack :deep(.p-inputtext),.form-stack :deep(.p-select){width:100%}.mt-3{margin-top:1rem}.json-view{background:var(--p-surface-100);border-radius:8px;padding:1rem;overflow:auto;max-height:320px;direction:ltr;text-align:left;font-size:.8rem}.proposal-result{display:grid;gap:.7rem}@media(max-width:800px){.planner-grid{grid-template-columns:1fr}}
</style>
