<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import Textarea from 'primevue/textarea'
import { useMarketingStore } from '@/stores/marketing/marketingStore'

const store = useMarketingStore()
const toast = useToast()

const tab = ref('campaigns')
const search = ref('')
const dialogOpen = ref(false)
const saving = ref(false)
const editingId = ref(null)
const form = reactive({})
const fieldErrors = ref({})
const perfOpen = ref(false)

const opts = (pairs) => pairs.map(([value, label]) => ({ value, label }))
const campaignStatus = opts([['draft', 'Draft'], ['scheduled', 'Scheduled'], ['running', 'Running'], ['completed', 'Completed'], ['cancelled', 'Cancelled']])
const contentStatus = opts([['draft', 'Draft'], ['scheduled', 'Scheduled']])
const contentType = opts([['post', 'Post'], ['article', 'Article'], ['email', 'Email'], ['video', 'Video'], ['landing_page', 'Landing page'], ['other', 'Other']])
const channelType = opts([['social', 'Social'], ['email', 'Email'], ['content', 'Content'], ['ads', 'Ads'], ['event', 'Event'], ['referral', 'Referral'], ['other', 'Other']])

const channelOptions = computed(() => store.channels.map((c) => ({ value: c.id, label: c.name })))
const campaignOptions = computed(() => store.campaigns.map((c) => ({ value: c.id, label: c.name })))

// kind -> store collection, labels, form fields
const schema = computed(() => ({
  campaigns: {
    label: 'Campaign', rows: store.campaigns, search: ['name', 'objective'],
    fields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'objective', label: 'Objective', type: 'area' },
      { key: 'status', label: 'Status', type: 'select', options: campaignStatus },
      { key: 'channel', label: 'Channel', type: 'select', options: channelOptions.value, clearable: true },
      { key: 'budget', label: 'Budget', type: 'text' },
      { key: 'spent', label: 'Spent', type: 'text' },
      { key: 'start_date', label: 'Start (YYYY-MM-DD)', type: 'text' },
      { key: 'end_date', label: 'End (YYYY-MM-DD)', type: 'text' },
    ],
    defaults: { name: '', objective: '', status: 'draft', channel: null, budget: '0', spent: '0', start_date: '', end_date: '' },
  },
  content: {
    label: 'Content', rows: store.content, search: ['title', 'body'],
    fields: [
      { key: 'title', label: 'Title', type: 'text' },
      { key: 'body', label: 'Body', type: 'area' },
      { key: 'content_type', label: 'Type', type: 'select', options: contentType },
      { key: 'status', label: 'Status', type: 'select', options: contentStatus },
      { key: 'campaign', label: 'Campaign', type: 'select', options: campaignOptions.value, clearable: true },
      { key: 'publish_at', label: 'Publish at (ISO, required if scheduled)', type: 'text' },
      { key: 'url', label: 'URL', type: 'text' },
    ],
    defaults: { title: '', body: '', content_type: 'post', status: 'draft', campaign: null, publish_at: '', url: '' },
  },
  leadSources: {
    label: 'Lead source', rows: store.leadSources, search: ['name', 'description'],
    fields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'description', label: 'Description', type: 'area' },
      { key: 'channel', label: 'Channel', type: 'select', options: channelOptions.value, clearable: true },
      { key: 'campaign', label: 'Campaign', type: 'select', options: campaignOptions.value, clearable: true },
    ],
    defaults: { name: '', description: '', channel: null, campaign: null },
  },
  channels: {
    label: 'Channel', rows: store.channels, search: ['name', 'url'],
    fields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'channel_type', label: 'Type', type: 'select', options: channelType },
      { key: 'url', label: 'URL', type: 'text' },
    ],
    defaults: { name: '', channel_type: 'social', url: '' },
  },
}))

const current = computed(() => schema.value[tab.value])
const filteredRows = computed(() => {
  const q = search.value.trim().toLowerCase()
  const rows = current.value.rows
  if (!q) return rows
  return rows.filter((r) => current.value.search.some((k) => String(r[k] ?? '').toLowerCase().includes(q)))
})

const tabs = [
  { key: 'campaigns', label: 'Campaigns' },
  { key: 'content', label: 'Content' },
  { key: 'leadSources', label: 'Lead sources' },
  { key: 'channels', label: 'Channels' },
]

function notifyError(cause, fallback) {
  const d = cause?.response?.data
  const detail = typeof d === 'string' ? fallback : d?.detail
  toast.add({ severity: 'error', summary: fallback, detail: detail || cause?.message, life: 5000 })
}

async function load() {
  try {
    await store.fetchAll()
  } catch (cause) {
    notifyError(cause, 'Could not load marketing data')
  }
}

function openCreate() {
  editingId.value = null
  fieldErrors.value = {}
  Object.keys(form).forEach((k) => delete form[k])
  Object.assign(form, current.value.defaults)
  dialogOpen.value = true
}

function openEdit(row) {
  editingId.value = row.id
  fieldErrors.value = {}
  Object.keys(form).forEach((k) => delete form[k])
  const values = {}
  for (const f of current.value.fields) values[f.key] = row[f.key] ?? current.value.defaults[f.key]
  Object.assign(form, values)
  dialogOpen.value = true
}

function buildPayload() {
  const payload = { ...form }
  // Optional date/time fields must be null, not '', for the API.
  for (const k of ['start_date', 'end_date', 'publish_at']) if (k in payload && !payload[k]) payload[k] = null
  return payload
}

async function submit() {
  saving.value = true
  fieldErrors.value = {}
  try {
    await store.save(tab.value, buildPayload(), editingId.value)
    dialogOpen.value = false
    toast.add({ severity: 'success', summary: `${current.value.label} saved`, life: 2500 })
  } catch (cause) {
    const d = cause?.response?.data
    if (d && typeof d === 'object') fieldErrors.value = d
    notifyError(cause, `Could not save ${current.value.label.toLowerCase()}`)
  } finally {
    saving.value = false
  }
}

async function destroy(row) {
  if (!window.confirm(`Delete "${row.name || row.title}"?`)) return
  try {
    await store.remove(tab.value, row.id)
    toast.add({ severity: 'success', summary: 'Deleted', life: 2500 })
  } catch (cause) {
    notifyError(cause, 'Could not delete')
  }
}

async function publish(row) {
  try {
    await store.publish(row.id)
    toast.add({ severity: 'success', summary: 'Marked as published', life: 2500 })
  } catch (cause) {
    notifyError(cause, 'Could not publish')
  }
}

async function showPerformance(row) {
  store.performance = null
  perfOpen.value = true
  try {
    await store.loadPerformance(row.id)
  } catch (cause) {
    perfOpen.value = false
    notifyError(cause, 'Could not load performance')
  }
}

const fieldError = (k) => {
  const e = fieldErrors.value[k]
  return Array.isArray(e) ? e.join(' ') : e
}
const nameOf = (list, id) => list.find((x) => x.id === id)?.name ?? '—'

onMounted(load)
</script>

<template>
  <div class="mk-page">
    <header class="mk-head">
      <h1>Marketing</h1>
      <Button label="Refresh" icon="pi pi-refresh" severity="secondary" :loading="store.loading" @click="load" />
    </header>

    <Message v-if="store.error && !store.loading" severity="error" :closable="false">
      Marketing data could not be loaded. <Button label="Retry" link @click="load" />
    </Message>

    <div v-if="store.overview" class="mk-stats">
      <Card><template #title>Campaigns</template><template #content>{{ store.overview.campaigns }}</template></Card>
      <Card><template #title>Budget</template><template #content>{{ store.overview.budget }}</template></Card>
      <Card><template #title>Spent</template><template #content>{{ store.overview.spent }}</template></Card>
      <Card><template #title>Leads</template><template #content>{{ store.overview.leads }}</template></Card>
      <Card><template #title>Cost per lead</template><template #content>{{ store.overview.cost_per_lead ?? '—' }}</template></Card>
      <Card><template #title>Published</template><template #content>{{ store.overview.published_content }}</template></Card>
    </div>

    <nav class="mk-tabs" role="tablist">
      <Button
        v-for="t in tabs" :key="t.key" :label="t.label" role="tab"
        :severity="tab === t.key ? 'primary' : 'secondary'" :text="tab !== t.key"
        @click="tab = t.key; search = ''"
      />
    </nav>

    <div class="mk-toolbar">
      <InputText v-model="search" placeholder="Search…" aria-label="Search" />
      <Button :label="`New ${current.label.toLowerCase()}`" icon="pi pi-plus" @click="openCreate" />
    </div>

    <DataTable :value="filteredRows" :loading="store.loading" stripedRows dataKey="id" paginator :rows="10">
      <template #empty>No {{ current.label.toLowerCase() }} records yet.</template>

      <template v-if="tab === 'campaigns'">
        <Column field="name" header="Name" sortable />
        <Column field="status" header="Status"><template #body="{ data }"><Tag :value="data.status" /></template></Column>
        <Column header="Channel"><template #body="{ data }">{{ nameOf(store.channels, data.channel) }}</template></Column>
        <Column field="budget" header="Budget" />
        <Column field="spent" header="Spent" />
      </template>
      <template v-else-if="tab === 'content'">
        <Column field="title" header="Title" sortable />
        <Column field="content_type" header="Type" />
        <Column field="status" header="Status"><template #body="{ data }"><Tag :value="data.status" /></template></Column>
        <Column header="Campaign"><template #body="{ data }">{{ nameOf(store.campaigns, data.campaign) }}</template></Column>
      </template>
      <template v-else-if="tab === 'leadSources'">
        <Column field="name" header="Name" sortable />
        <Column header="Campaign"><template #body="{ data }">{{ nameOf(store.campaigns, data.campaign) }}</template></Column>
        <Column field="leads_count" header="Leads" />
        <Column field="is_active" header="Active"><template #body="{ data }">{{ data.is_active ? 'Yes' : 'No' }}</template></Column>
      </template>
      <template v-else>
        <Column field="name" header="Name" sortable />
        <Column field="channel_type" header="Type" />
        <Column field="url" header="URL" />
      </template>

      <Column header="Actions">
        <template #body="{ data }">
          <div class="mk-actions">
            <Button v-if="tab === 'campaigns'" icon="pi pi-chart-bar" text aria-label="Performance" @click="showPerformance(data)" />
            <Button v-if="tab === 'content' && data.status !== 'published'" icon="pi pi-check" text aria-label="Mark published" @click="publish(data)" />
            <Button icon="pi pi-pencil" text aria-label="Edit" @click="openEdit(data)" />
            <Button icon="pi pi-trash" text severity="danger" aria-label="Delete" @click="destroy(data)" />
          </div>
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="dialogOpen" modal :header="`${editingId ? 'Edit' : 'New'} ${current.label.toLowerCase()}`" :style="{ width: '32rem' }">
      <form class="mk-form" @submit.prevent="submit">
        <div v-for="f in current.fields" :key="f.key" class="mk-field">
          <label :for="`mk-${f.key}`">{{ f.label }}</label>
          <Textarea v-if="f.type === 'area'" :id="`mk-${f.key}`" v-model="form[f.key]" rows="3" />
          <Select
            v-else-if="f.type === 'select'" :inputId="`mk-${f.key}`" v-model="form[f.key]"
            :options="f.options" optionLabel="label" optionValue="value" :showClear="f.clearable" />
          <InputText v-else :id="`mk-${f.key}`" v-model="form[f.key]" />
          <small v-if="fieldError(f.key)" class="mk-error">{{ fieldError(f.key) }}</small>
        </div>
        <small v-if="fieldError('detail')" class="mk-error">{{ fieldError('detail') }}</small>
        <div class="mk-form-actions">
          <Button type="button" label="Cancel" severity="secondary" @click="dialogOpen = false" />
          <Button type="submit" label="Save" :loading="saving" />
        </div>
      </form>
    </Dialog>

    <Dialog v-model:visible="perfOpen" modal header="Campaign performance" :style="{ width: '28rem' }">
      <p v-if="!store.performance">Loading…</p>
      <dl v-else class="mk-perf">
        <dt>Status</dt><dd>{{ store.performance.status }}</dd>
        <dt>Budget</dt><dd>{{ store.performance.budget }}</dd>
        <dt>Spent</dt><dd>{{ store.performance.spent }}</dd>
        <dt>Remaining</dt><dd>{{ store.performance.remaining }}<template v-if="store.performance.over_budget"> (over budget)</template></dd>
        <dt>Leads</dt><dd>{{ store.performance.leads }}</dd>
        <dt>Cost per lead</dt><dd>{{ store.performance.cost_per_lead ?? '—' }}</dd>
        <dt>Content pieces</dt><dd>{{ store.performance.content.total }}</dd>
      </dl>
    </Dialog>
  </div>
</template>

<style scoped>
.mk-page { padding: 1rem; display: grid; gap: 1rem; }
.mk-head, .mk-toolbar { display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
.mk-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr)); gap: 0.75rem; }
.mk-tabs, .mk-actions { display: flex; gap: 0.25rem; flex-wrap: wrap; }
.mk-form { display: grid; gap: 0.75rem; }
.mk-field { display: grid; gap: 0.25rem; }
.mk-form-actions { display: flex; justify-content: flex-end; gap: 0.5rem; }
.mk-error { color: var(--p-red-500, #ef4444); }
.mk-perf { display: grid; grid-template-columns: auto 1fr; gap: 0.25rem 1rem; }
.mk-perf dt { font-weight: 600; }
</style>
