<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Checkbox from 'primevue/checkbox'
import Column from 'primevue/column'
import ConfirmDialog from 'primevue/confirmdialog'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Select from 'primevue/select'
import Textarea from 'primevue/textarea'
import Toast from 'primevue/toast'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import { useAiToolsLaboratoryStore } from '@/stores/ai_tools_laboratory/aiToolsLaboratoryStore'

const store = useAiToolsLaboratoryStore()
const toast = useToast()
const confirm = useConfirm()

const TOOL_STATUS = ['evaluating', 'adopted', 'rejected', 'archived'].map((v) => ({ label: v, value: v }))
const RUN_STATUS = ['pending', 'succeeded', 'failed'].map((v) => ({ label: v, value: v }))

const toolOptions = computed(() => store.tools.map((t) => ({ label: t.name, value: t.id })))
const categoryOptions = computed(() => store.categories.map((c) => ({ label: c.name, value: c.id })))
const configurationOptions = computed(() =>
  store.configurations.map((c) => ({ label: `${c.name} (tool #${c.tool})`, value: c.id })),
)
const toolName = (id) => store.tools.find((t) => t.id === id)?.name ?? `#${id}`
const categoryName = (id) => store.categories.find((c) => c.id === id)?.name ?? '—'

// Resource definitions: table columns + form fields. Field types: text, url,
// textarea, number, select, checkbox, tags (comma separated list), json (object).
const resources = computed(() => ({
  tools: {
    label: 'Tools',
    columns: [
      { field: 'name', header: 'Name' },
      { field: 'vendor', header: 'Vendor' },
      { field: 'category', header: 'Category', format: categoryName },
      { field: 'status', header: 'Status' },
      { field: 'rating', header: 'Rating' },
      { field: 'tags', header: 'Tags', format: (v) => (v || []).join(', ') },
    ],
    fields: [
      { key: 'name', label: 'Name', type: 'text', required: true },
      { key: 'vendor', label: 'Vendor', type: 'text' },
      { key: 'website_url', label: 'Website', type: 'url' },
      { key: 'category', label: 'Category', type: 'select', options: categoryOptions.value, clearable: true },
      { key: 'status', label: 'Status', type: 'select', options: TOOL_STATUS, default: 'evaluating' },
      { key: 'rating', label: 'Rating (1-5)', type: 'number', min: 1, max: 5 },
      { key: 'pricing_model', label: 'Pricing model', type: 'text' },
      { key: 'tags', label: 'Tags (comma separated)', type: 'tags' },
      { key: 'description', label: 'Description', type: 'textarea' },
      { key: 'notes', label: 'Notes', type: 'textarea' },
    ],
  },
  categories: {
    label: 'Categories',
    columns: [
      { field: 'name', header: 'Name' },
      { field: 'description', header: 'Description' },
    ],
    fields: [
      { key: 'name', label: 'Name', type: 'text', required: true },
      { key: 'description', label: 'Description', type: 'textarea' },
    ],
  },
  configurations: {
    label: 'Configurations',
    columns: [
      { field: 'name', header: 'Name' },
      { field: 'tool', header: 'Tool', format: toolName },
      { field: 'is_default', header: 'Default', format: (v) => (v ? 'Yes' : 'No') },
    ],
    fields: [
      { key: 'tool', label: 'Tool', type: 'select', options: toolOptions.value, required: true },
      { key: 'name', label: 'Name', type: 'text', required: true },
      { key: 'settings', label: 'Settings (JSON, no credentials)', type: 'json' },
      { key: 'is_default', label: 'Default for this tool', type: 'checkbox' },
    ],
  },
  executions: {
    label: 'Trial runs',
    columns: [
      { field: 'tool', header: 'Tool', format: toolName },
      { field: 'status', header: 'Status' },
      { field: 'duration_ms', header: 'Duration (ms)' },
      { field: 'executed_at', header: 'Executed', format: (v) => (v ? new Date(v).toLocaleString() : '') },
      { field: 'notes', header: 'Notes' },
    ],
    fields: [
      { key: 'tool', label: 'Tool', type: 'select', options: toolOptions.value, required: true },
      { key: 'configuration', label: 'Configuration', type: 'select', options: configurationOptions.value, clearable: true },
      { key: 'status', label: 'Outcome', type: 'select', options: RUN_STATUS, default: 'pending' },
      { key: 'input_text', label: 'Input', type: 'textarea' },
      { key: 'output_text', label: 'Output', type: 'textarea' },
      { key: 'duration_ms', label: 'Duration (ms)', type: 'number', min: 0 },
      { key: 'notes', label: 'Notes', type: 'textarea' },
    ],
  },
}))

const active = ref('tools')
const search = ref('')
const statusFilter = ref(null)
const dialogOpen = ref(false)
const editingId = ref(null)
const form = reactive({})
const saving = ref(false)
const formError = ref('')
const loadError = ref('')

const current = computed(() => resources.value[active.value])
const rows = computed(() => {
  let list = store[active.value] || []
  if (active.value === 'tools' && statusFilter.value) list = list.filter((t) => t.status === statusFilter.value)
  const q = search.value.trim().toLowerCase()
  if (q) list = list.filter((row) => JSON.stringify(row).toLowerCase().includes(q))
  return list
})

function describeError(cause) {
  const body = cause?.response?.data
  if (!body) return cause?.message || 'Request failed.'
  if (typeof body === 'string') return body
  return Object.entries(body)
    .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(' ') : value}`)
    .join(' | ')
}

function openDialog(row = null) {
  formError.value = ''
  editingId.value = row?.id ?? null
  Object.keys(form).forEach((key) => delete form[key])
  for (const field of current.value.fields) {
    const raw = row ? row[field.key] : field.default
    if (field.type === 'tags') form[field.key] = (raw || []).join(', ')
    else if (field.type === 'json') form[field.key] = JSON.stringify(raw ?? {}, null, 2)
    else if (field.type === 'checkbox') form[field.key] = Boolean(raw)
    else form[field.key] = raw ?? (field.type === 'number' || field.type === 'select' ? null : '')
  }
  dialogOpen.value = true
}

function buildPayload() {
  const payload = {}
  for (const field of current.value.fields) {
    const value = form[field.key]
    if (field.type === 'tags') {
      payload[field.key] = String(value || '').split(',').map((t) => t.trim()).filter(Boolean)
    } else if (field.type === 'json') {
      try {
        payload[field.key] = value && value.trim() ? JSON.parse(value) : {}
      } catch {
        throw new Error(`${field.label}: invalid JSON.`)
      }
    } else if (field.type === 'number' || field.type === 'select') {
      payload[field.key] = value === '' ? null : value
    } else {
      payload[field.key] = value
    }
  }
  return payload
}

async function submit() {
  formError.value = ''
  saving.value = true
  try {
    await store.save(active.value, buildPayload(), editingId.value)
    dialogOpen.value = false
    toast.add({ severity: 'success', summary: 'Saved', life: 2500 })
  } catch (cause) {
    formError.value = describeError(cause)
  } finally {
    saving.value = false
  }
}

function askRemove(row) {
  confirm.require({
    message: 'Delete this item? This cannot be undone.',
    header: 'Confirm delete',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await store.remove(active.value, row.id)
        toast.add({ severity: 'success', summary: 'Deleted', life: 2500 })
      } catch (cause) {
        toast.add({ severity: 'error', summary: 'Delete failed', detail: describeError(cause), life: 5000 })
      }
    },
  })
}

function switchTab(name) {
  active.value = name
  search.value = ''
  statusFilter.value = null
}

async function load() {
  loadError.value = ''
  try {
    await store.refresh()
  } catch (cause) {
    loadError.value = describeError(cause)
  }
}

onMounted(load)
</script>

<template>
  <div class="lab-page">
    <Toast />
    <ConfirmDialog />

    <Card>
      <template #title>AI Tools Laboratory</template>
      <template #content>
        <Message v-if="loadError" severity="error" :closable="false">
          {{ loadError }}
          <Button label="Retry" size="small" text @click="load" />
        </Message>

        <div v-if="store.summary" class="lab-summary">
          <span>Tools: <strong>{{ store.summary.tools_total }}</strong></span>
          <span>
            Avg rating:
            <strong>{{ store.summary.average_rating ?? '—' }}</strong>
          </span>
          <span>Trial runs: <strong>{{ store.summary.executions_total }}</strong></span>
          <span>
            Success rate:
            <strong>
              {{ store.summary.success_rate == null ? '—' : Math.round(store.summary.success_rate * 100) + '%' }}
            </strong>
          </span>
          <span v-for="(n, status) in store.summary.tools_by_status" :key="status">
            {{ status }}: <strong>{{ n }}</strong>
          </span>
        </div>

        <div class="lab-tabs">
          <Button
            v-for="(def, name) in resources"
            :key="name"
            :label="def.label"
            :severity="active === name ? 'primary' : 'secondary'"
            :outlined="active !== name"
            size="small"
            @click="switchTab(name)"
          />
        </div>

        <div class="lab-toolbar">
          <InputText v-model="search" placeholder="Search…" />
          <Select
            v-if="active === 'tools'"
            v-model="statusFilter"
            :options="TOOL_STATUS"
            option-label="label"
            option-value="value"
            placeholder="All statuses"
            show-clear
          />
          <Button label="New" icon="pi pi-plus" @click="openDialog()" />
        </div>

        <DataTable :value="rows" :loading="store.loading" striped-rows data-key="id" paginator :rows="10">
          <template #empty>No {{ current.label.toLowerCase() }} yet.</template>
          <Column v-for="col in current.columns" :key="col.field" :field="col.field" :header="col.header">
            <template #body="{ data }">
              {{ col.format ? col.format(data[col.field]) : data[col.field] }}
            </template>
          </Column>
          <Column header="Actions">
            <template #body="{ data }">
              <Button icon="pi pi-pencil" text size="small" aria-label="Edit" @click="openDialog(data)" />
              <Button icon="pi pi-trash" text size="small" severity="danger" aria-label="Delete" @click="askRemove(data)" />
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>

    <Dialog v-model:visible="dialogOpen" modal :header="editingId ? 'Edit' : 'New'" :style="{ width: '34rem' }">
      <Message v-if="formError" severity="error" :closable="false">{{ formError }}</Message>
      <form class="lab-form" @submit.prevent="submit">
        <label v-for="field in current.fields" :key="field.key" class="lab-field">
          <span>{{ field.label }}<em v-if="field.required"> *</em></span>
          <Textarea v-if="field.type === 'textarea' || field.type === 'json'" v-model="form[field.key]" rows="3" auto-resize />
          <InputNumber
            v-else-if="field.type === 'number'"
            v-model="form[field.key]"
            :min="field.min"
            :max="field.max"
            :use-grouping="false"
          />
          <Select
            v-else-if="field.type === 'select'"
            v-model="form[field.key]"
            :options="field.options"
            option-label="label"
            option-value="value"
            :show-clear="field.clearable"
          />
          <Checkbox v-else-if="field.type === 'checkbox'" v-model="form[field.key]" binary />
          <InputText v-else v-model="form[field.key]" :type="field.type === 'url' ? 'url' : 'text'" :required="field.required" />
        </label>
        <div class="lab-actions">
          <Button type="button" label="Cancel" severity="secondary" text @click="dialogOpen = false" />
          <Button type="submit" label="Save" :loading="saving" />
        </div>
      </form>
    </Dialog>
  </div>
</template>

<style scoped>
.lab-page { padding: 1rem; }
.lab-summary { display: flex; flex-wrap: wrap; gap: 1.25rem; margin-bottom: 1rem; }
.lab-tabs, .lab-toolbar { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
.lab-form { display: grid; gap: 0.75rem; }
.lab-field { display: grid; gap: 0.25rem; }
.lab-actions { display: flex; justify-content: flex-end; gap: 0.5rem; }
</style>
