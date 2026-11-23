<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Checkbox from 'primevue/checkbox'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import Textarea from 'primevue/textarea'
import { useAgentsStore } from '@/stores/agents/agentsStore'

const store = useAgentsStore()
const toast = useToast()
const confirm = useConfirm()

const tab = ref('agents')
const search = ref('')
const statusFilter = ref(null)
const statusOptions = ['draft', 'active', 'paused', 'archived']

// ---- helpers --------------------------------------------------------------
function describeError(err) {
  const d = err?.response?.data
  if (!d) return err?.message || 'Request failed'
  if (typeof d === 'string') return d
  if (d.detail) return d.detail
  return Object.entries(d)
    .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' ') : v}`)
    .join(' | ')
}
const notify = (severity, summary, detail) =>
  toast.add({ severity, summary, detail, life: 4000 })
async function guarded(fn, okMessage) {
  try {
    const result = await fn()
    if (okMessage) notify('success', okMessage)
    return result
  } catch (err) {
    notify('error', 'Error', describeError(err))
    return undefined
  }
}
const statusSeverity = (s) =>
  ({ active: 'success', succeeded: 'success', failed: 'danger', cancelled: 'secondary',
     running: 'info', awaiting_approval: 'warn', paused: 'warn' })[s] || 'secondary'

const filteredAgents = computed(() => {
  const q = search.value.trim().toLowerCase()
  return store.agents.filter(
    (a) =>
      (!statusFilter.value || a.status === statusFilter.value) &&
      (!q || [a.name, a.role, a.description].some((v) => (v || '').toLowerCase().includes(q))),
  )
})
const agentName = (id) => store.agents.find((a) => a.id === id)?.name || `#${id}`

// ---- agent dialog -----------------------------------------------------------
const agentDialog = ref(false)
const editingId = ref(null)
const agentForm = reactive({})
function openAgent(agent = null) {
  editingId.value = agent?.id ?? null
  Object.assign(agentForm, {
    name: '', role: '', description: '', status: 'draft', model_name: '',
    system_prompt: '', requires_approval: true, ...(agent || {}),
  })
  agentDialog.value = true
}
async function saveAgent() {
  const { name, role, description, status, model_name, system_prompt, requires_approval } = agentForm
  const ok = await guarded(
    () => store.saveAgent({ name, role, description, status, model_name, system_prompt, requires_approval }, editingId.value),
    'Agent saved',
  )
  if (ok) agentDialog.value = false
}
function removeAgent(agent) {
  confirm.require({
    message: `Delete agent "${agent.name}" with all its configurations and runs?`,
    header: 'Delete agent',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: () => guarded(() => store.removeAgent(agent.id), 'Agent deleted'),
  })
}

// ---- configurations dialog --------------------------------------------------
const configDialog = ref(false)
const configAgent = ref(null)
const configForm = reactive({ temperature: 0.2, max_steps: 10, tools: '' })
async function openConfigs(agent) {
  configAgent.value = agent
  Object.assign(configForm, { temperature: 0.2, max_steps: 10, tools: '' })
  configDialog.value = true
  await guarded(() => store.fetchConfigurations({ agent: agent.id }))
}
async function addConfig() {
  const tools = configForm.tools.split(',').map((t) => t.trim()).filter(Boolean)
  await guarded(
    () => store.addConfiguration({
      agent: configAgent.value.id, temperature: configForm.temperature,
      max_steps: configForm.max_steps, tools,
    }),
    'Configuration created',
  )
}
const activateConfig = (c) => guarded(() => store.activateConfiguration(c), `Version ${c.version} activated`)

// ---- runs -------------------------------------------------------------------
const runDialog = ref(false)
const runForm = reactive({ agent: null, goal: '' })
const activeAgents = computed(() => store.agents.filter((a) => a.status === 'active'))
function openRun(agent = null) {
  Object.assign(runForm, { agent: agent?.id ?? null, goal: '' })
  runDialog.value = true
}
async function startRun() {
  const ok = await guarded(() => store.startRun({ agent: runForm.agent, goal: runForm.goal }), 'Run created')
  if (ok) {
    runDialog.value = false
    tab.value = 'runs'
  }
}
const runAction = (action, run) =>
  guarded(() => store.runAction(action, run.id), `Run ${action} done`)

const stepsDialog = ref(false)
const stepsRun = ref(null)
async function showSteps(run) {
  stepsRun.value = run
  stepsDialog.value = true
  await guarded(() => store.fetchExecutions(run.id))
}

onMounted(() => guarded(() => store.refresh()))
</script>

<template>
  <div class="agents-page">
    <Card>
      <template #title>AI Agents</template>
      <template #content>
        <Message v-if="store.error" severity="error" :closable="false">
          {{ describeError(store.error) }}
          <Button label="Retry" text size="small" @click="guarded(() => store.refresh())" />
        </Message>

        <div class="tabs">
          <Button label="Agents" :outlined="tab !== 'agents'" size="small" @click="tab = 'agents'" />
          <Button label="Runs" :outlined="tab !== 'runs'" size="small" @click="tab = 'runs'" />
        </div>

        <!-- Agents -->
        <div v-if="tab === 'agents'">
          <div class="toolbar">
            <InputText v-model="search" placeholder="Search agents…" />
            <Select v-model="statusFilter" :options="statusOptions" showClear placeholder="Status" />
            <Button label="New agent" icon="pi pi-plus" @click="openAgent()" />
          </div>
          <DataTable :value="filteredAgents" :loading="store.loading" dataKey="id" stripedRows paginator :rows="10">
            <template #empty>No agents yet. Create your first agent.</template>
            <Column field="name" header="Name" sortable />
            <Column field="role" header="Role" />
            <Column header="Status" sortable field="status">
              <template #body="{ data }"><Tag :value="data.status" :severity="statusSeverity(data.status)" /></template>
            </Column>
            <Column header="Approval">
              <template #body="{ data }">{{ data.requires_approval ? 'Required' : 'Automatic' }}</template>
            </Column>
            <Column header="Actions">
              <template #body="{ data }">
                <Button icon="pi pi-pencil" text rounded aria-label="Edit" @click="openAgent(data)" />
                <Button icon="pi pi-sliders-h" text rounded aria-label="Configurations" @click="openConfigs(data)" />
                <Button icon="pi pi-play" text rounded aria-label="Start run" :disabled="data.status !== 'active'" @click="openRun(data)" />
                <Button icon="pi pi-trash" text rounded severity="danger" aria-label="Delete" @click="removeAgent(data)" />
              </template>
            </Column>
          </DataTable>
        </div>

        <!-- Runs -->
        <div v-else>
          <div class="toolbar">
            <Button label="New run" icon="pi pi-plus" :disabled="!activeAgents.length" @click="openRun()" />
            <Button label="Reload" icon="pi pi-refresh" text @click="guarded(() => store.fetchRuns())" />
          </div>
          <DataTable :value="store.runs" :loading="store.loading" dataKey="id" stripedRows paginator :rows="10">
            <template #empty>No runs yet.</template>
            <Column header="Agent"><template #body="{ data }">{{ agentName(data.agent) }}</template></Column>
            <Column field="goal" header="Goal" />
            <Column field="status" header="Status" sortable>
              <template #body="{ data }"><Tag :value="data.status" :severity="statusSeverity(data.status)" /></template>
            </Column>
            <Column header="Actions">
              <template #body="{ data }">
                <Button label="Approve" size="small" text v-if="data.status === 'awaiting_approval'" @click="runAction('approve', data)" />
                <Button label="Execute" size="small" text v-if="data.status === 'pending'" @click="runAction('execute', data)" />
                <Button label="Cancel" size="small" text severity="danger"
                  v-if="['awaiting_approval', 'pending', 'running'].includes(data.status)" @click="runAction('cancel', data)" />
                <Button label="Steps" size="small" text @click="showSteps(data)" />
              </template>
            </Column>
          </DataTable>
        </div>
      </template>
    </Card>

    <Dialog v-model:visible="agentDialog" modal :header="editingId ? 'Edit agent' : 'New agent'" :style="{ width: '34rem' }">
      <div class="form">
        <label>Name<InputText v-model="agentForm.name" /></label>
        <label>Role<InputText v-model="agentForm.role" /></label>
        <label>Description<Textarea v-model="agentForm.description" rows="2" /></label>
        <label>Status<Select v-model="agentForm.status" :options="statusOptions" /></label>
        <label>Model<InputText v-model="agentForm.model_name" placeholder="Optional model name" /></label>
        <label>System prompt<Textarea v-model="agentForm.system_prompt" rows="4" /></label>
        <label class="check"><Checkbox v-model="agentForm.requires_approval" binary /> Runs require approval</label>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="agentDialog = false" />
        <Button label="Save" :loading="store.loading" :disabled="!agentForm.name?.trim()" @click="saveAgent" />
      </template>
    </Dialog>

    <Dialog v-model:visible="configDialog" modal :header="`Configurations — ${configAgent?.name || ''}`" :style="{ width: '40rem' }">
      <DataTable :value="store.configurations" dataKey="id" size="small">
        <template #empty>No configurations. Add one below.</template>
        <Column field="version" header="Version" />
        <Column field="temperature" header="Temp." />
        <Column field="max_steps" header="Max steps" />
        <Column header="Active">
          <template #body="{ data }">
            <Tag v-if="data.is_active" value="active" severity="success" />
            <Button v-else label="Activate" size="small" text @click="activateConfig(data)" />
          </template>
        </Column>
      </DataTable>
      <div class="form inline">
        <label>Temperature (0–2)<InputNumber v-model="configForm.temperature" :min="0" :max="2" :minFractionDigits="1" :maxFractionDigits="2" /></label>
        <label>Max steps (1–100)<InputNumber v-model="configForm.max_steps" :min="1" :max="100" /></label>
        <label>Tools (comma separated)<InputText v-model="configForm.tools" /></label>
        <Button label="Add version" icon="pi pi-plus" @click="addConfig" />
      </div>
    </Dialog>

    <Dialog v-model:visible="runDialog" modal header="Start run" :style="{ width: '32rem' }">
      <div class="form">
        <label>Agent
          <Select v-model="runForm.agent" :options="activeAgents" optionLabel="name" optionValue="id" placeholder="Active agent" />
        </label>
        <label>Goal<Textarea v-model="runForm.goal" rows="4" /></label>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="runDialog = false" />
        <Button label="Start" :loading="store.loading" :disabled="!runForm.agent || !runForm.goal.trim()" @click="startRun" />
      </template>
    </Dialog>

    <Dialog v-model:visible="stepsDialog" modal :header="`Run #${stepsRun?.id} steps`" :style="{ width: '44rem' }">
      <Message v-if="stepsRun?.error" severity="error" :closable="false">{{ stepsRun.error }}</Message>
      <DataTable :value="store.executions" dataKey="id" size="small">
        <template #empty>No steps recorded yet.</template>
        <Column field="step_index" header="#" />
        <Column field="action" header="Action" />
        <Column field="status" header="Status" />
        <Column field="duration_ms" header="ms" />
        <Column header="Output">
          <template #body="{ data }">{{ data.error || data.output_data?.content || '' }}</template>
        </Column>
      </DataTable>
    </Dialog>
  </div>
</template>

<style scoped>
.agents-page { padding: 1rem; }
.tabs, .toolbar { display: flex; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap; align-items: center; }
.form { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1rem; }
.form.inline { flex-direction: row; flex-wrap: wrap; align-items: end; }
.form label { display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.875rem; }
.form label.check { flex-direction: row; align-items: center; }
</style>
