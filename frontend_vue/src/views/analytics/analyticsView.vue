<template>
  <div class="analytics-page">
    <Toast />
    <header class="page-head">
      <h1>Analytics</h1>
      <Button icon="pi pi-refresh" label="Refresh" :loading="store.loading" @click="load" />
    </header>

    <Message v-if="store.error" severity="error" :closable="false">
      {{ errorText(store.error) }}
      <Button label="Retry" text size="small" @click="load" />
    </Message>

    <Tabs value="metrics">
      <TabList>
        <Tab value="metrics">Metrics</Tab>
        <Tab value="events">Events</Tab>
        <Tab value="reports">Reports</Tab>
      </TabList>
      <TabPanels>
        <!-- METRICS -->
        <TabPanel value="metrics">
          <div class="toolbar">
            <InputText v-model="metricSearch" placeholder="Search metrics" @keyup.enter="searchMetrics" />
            <Button label="New metric" icon="pi pi-plus" @click="openMetric()" />
          </div>
          <DataTable :value="store.metrics" :loading="store.loading" dataKey="id" stripedRows
                     v-model:selection="selectedMetric" selectionMode="single" @rowSelect="selectMetric">
            <template #empty>No metrics yet. Create one to start recording values.</template>
            <Column field="key" header="Key" />
            <Column field="name" header="Name" />
            <Column field="unit" header="Unit" />
            <Column field="kind" header="Kind" />
            <Column header="Active">
              <template #body="{ data }"><Tag :value="data.is_active ? 'active' : 'inactive'" :severity="data.is_active ? 'success' : 'secondary'" /></template>
            </Column>
            <Column header="Actions">
              <template #body="{ data }">
                <Button icon="pi pi-pencil" text @click.stop="openMetric(data)" aria-label="Edit" />
                <Button icon="pi pi-trash" text severity="danger" @click.stop="removeMetric(data)" aria-label="Delete" />
              </template>
            </Column>
          </DataTable>

          <section v-if="selectedMetric" class="detail">
            <h3>{{ selectedMetric.name }}</h3>
            <div v-if="store.summary" class="stats">
              <div><span>Count</span><strong>{{ store.summary.count }}</strong></div>
              <div><span>Latest</span><strong>{{ fmt(store.summary.latest) }}</strong></div>
              <div><span>Min</span><strong>{{ fmt(store.summary.min) }}</strong></div>
              <div><span>Max</span><strong>{{ fmt(store.summary.max) }}</strong></div>
              <div><span>Average</span><strong>{{ fmt(store.summary.average) }}</strong></div>
              <div><span>Change</span><strong>{{ fmt(store.summary.change) }}<template v-if="store.summary.change_percent !== null"> ({{ store.summary.change_percent }}%)</template></strong></div>
            </div>
            <div class="toolbar">
              <InputNumber v-model="snapshotValue" :minFractionDigits="0" :maxFractionDigits="4" placeholder="Value" />
              <Button label="Record value" icon="pi pi-plus" :disabled="snapshotValue === null" @click="recordSnapshot" />
            </div>
            <div v-if="chartData.labels.length" class="chart"><Line :data="chartData" :options="chartOptions" /></div>
            <p v-else class="muted">No recorded values yet for this metric.</p>
          </section>
        </TabPanel>

        <!-- EVENTS -->
        <TabPanel value="events">
          <div class="toolbar">
            <InputText v-model="eventForm.name" placeholder="Event name" />
            <InputText v-model="eventForm.source_app" placeholder="Source app (optional)" />
            <Button label="Record event" icon="pi pi-plus" :disabled="!eventForm.name.trim()" @click="recordEvent" />
          </div>
          <div class="counts">
            <Tag v-for="row in store.eventCounts.events" :key="row.name" :value="`${row.name}: ${row.count}`" />
            <span v-if="!store.eventCounts.events.length" class="muted">No event counts yet.</span>
          </div>
          <DataTable :value="store.events" :loading="store.loading" dataKey="id" stripedRows paginator :rows="10">
            <template #empty>No events recorded.</template>
            <Column field="name" header="Event" />
            <Column field="source_app" header="Source" />
            <Column header="Occurred">
              <template #body="{ data }">{{ new Date(data.occurred_at).toLocaleString() }}</template>
            </Column>
            <Column header="">
              <template #body="{ data }"><Button icon="pi pi-trash" text severity="danger" @click="removeEvent(data)" aria-label="Delete" /></template>
            </Column>
          </DataTable>
        </TabPanel>

        <!-- REPORTS -->
        <TabPanel value="reports">
          <div class="toolbar"><Button label="New report" icon="pi pi-plus" @click="openReport()" /></div>
          <DataTable :value="store.reports" :loading="store.loading" dataKey="id" stripedRows>
            <template #empty>No reports yet.</template>
            <Column field="title" header="Title" />
            <Column field="report_type" header="Type" />
            <Column header="Generated">
              <template #body="{ data }">{{ data.generated_at ? new Date(data.generated_at).toLocaleString() : 'Not generated' }}</template>
            </Column>
            <Column header="Actions">
              <template #body="{ data }">
                <Button icon="pi pi-play" text @click="generate(data)" aria-label="Generate" />
                <Button icon="pi pi-eye" text :disabled="!data.generated_at" @click="viewReport = data" aria-label="View" />
                <Button icon="pi pi-pencil" text @click="openReport(data)" aria-label="Edit" />
                <Button icon="pi pi-trash" text severity="danger" @click="removeReport(data)" aria-label="Delete" />
              </template>
            </Column>
          </DataTable>
        </TabPanel>
      </TabPanels>
    </Tabs>

    <Dialog v-model:visible="metricDialog" modal :header="metricForm.id ? 'Edit metric' : 'New metric'" :style="{ width: '28rem' }">
      <div class="form">
        <label>Key<InputText v-model="metricForm.key" :invalid="!!fieldErrors.key" /></label><small v-if="fieldErrors.key" class="err">{{ fieldErrors.key }}</small>
        <label>Name<InputText v-model="metricForm.name" :invalid="!!fieldErrors.name" /></label><small v-if="fieldErrors.name" class="err">{{ fieldErrors.name }}</small>
        <label>Unit<InputText v-model="metricForm.unit" /></label>
        <label>Kind<Select v-model="metricForm.kind" :options="['gauge', 'counter']" /></label>
        <label>Description<Textarea v-model="metricForm.description" rows="3" /></label>
        <label class="inline"><Checkbox v-model="metricForm.is_active" binary /> Active</label>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="metricDialog = false" />
        <Button label="Save" icon="pi pi-check" :loading="store.loading" :disabled="!metricForm.key || !metricForm.name" @click="submitMetric" />
      </template>
    </Dialog>

    <Dialog v-model:visible="reportDialog" modal :header="reportForm.id ? 'Edit report' : 'New report'" :style="{ width: '28rem' }">
      <div class="form">
        <label>Title<InputText v-model="reportForm.title" :invalid="!!fieldErrors.title" /></label>
        <label>Type<Select v-model="reportForm.report_type" :options="reportTypes" optionLabel="label" optionValue="value" /></label>
        <label>Period start<InputText v-model="reportForm.period_start" type="date" /></label>
        <label>Period end<InputText v-model="reportForm.period_end" type="date" /></label>
        <small v-if="fieldErrors.period_end" class="err">{{ fieldErrors.period_end }}</small>
        <label v-if="reportForm.report_type === 'metric_trend'">Metric
          <Select v-model="reportForm.metric" :options="store.metrics" optionLabel="name" optionValue="id" placeholder="Select a metric" />
        </label>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="reportDialog = false" />
        <Button label="Save" icon="pi pi-check" :loading="store.loading" :disabled="!reportForm.title" @click="submitReport" />
      </template>
    </Dialog>

    <Dialog :visible="!!viewReport" modal :header="viewReport?.title" :style="{ width: '40rem' }" @update:visible="viewReport = null">
      <pre class="json">{{ JSON.stringify(viewReport?.content, null, 2) }}</pre>
    </Dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import Toast from 'primevue/toast'
import Button from 'primevue/button'
import Message from 'primevue/message'
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import Checkbox from 'primevue/checkbox'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend,
} from 'chart.js'
import { useAnalyticsStore } from '@/stores/analytics/analyticsStore'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend)

const store = useAnalyticsStore()
const toast = useToast()
const confirm = useConfirm()

const reportTypes = [
  { label: 'Metric summary', value: 'summary' },
  { label: 'Metric trend', value: 'metric_trend' },
  { label: 'Event counts', value: 'events' },
]

const metricSearch = ref('')
const selectedMetric = ref(null)
const snapshotValue = ref(null)
const metricDialog = ref(false)
const reportDialog = ref(false)
const viewReport = ref(null)
const fieldErrors = ref({})
const eventForm = reactive({ name: '', source_app: '' })
const blankMetric = () => ({ id: null, key: '', name: '', unit: '', kind: 'gauge', description: '', is_active: true })
const blankReport = () => ({ id: null, title: '', report_type: 'summary', period_start: '', period_end: '', metric: null })
const metricForm = reactive(blankMetric())
const reportForm = reactive(blankReport())

const chartOptions = { responsive: true, maintainAspectRatio: false }
const chartData = computed(() => {
  const rows = [...store.snapshots].sort((a, b) => new Date(a.recorded_at) - new Date(b.recorded_at))
  return {
    labels: rows.map((r) => new Date(r.recorded_at).toLocaleString()),
    datasets: [{ label: selectedMetric.value?.name || 'Value', data: rows.map((r) => Number(r.value)), borderColor: '#6366f1', tension: 0.2 }],
  }
})

const fmt = (v) => (v === null || v === undefined ? '—' : v)

function errorText(cause) {
  const d = cause?.response?.data
  if (d?.detail) return d.detail
  if (d && typeof d === 'object') return Object.entries(d).map(([k, v]) => `${k}: ${[].concat(v).join(' ')}`).join(' | ')
  return cause?.message || 'Request failed.'
}
function setFieldErrors(cause) {
  const d = cause?.response?.data
  fieldErrors.value = {}
  if (d && typeof d === 'object') for (const [k, v] of Object.entries(d)) fieldErrors.value[k] = [].concat(v).join(' ')
}
const notify = (severity, summary, detail) => toast.add({ severity, summary, detail, life: 4000 })
const fail = (cause) => notify('error', 'Error', errorText(cause))

async function load() {
  try { await store.refresh() } catch { /* shown via store.error */ }
}
async function searchMetrics() {
  try { await store.fetchMetrics(metricSearch.value ? { search: metricSearch.value } : {}) } catch { /* store.error */ }
}
async function selectMetric() {
  if (!selectedMetric.value) return
  try {
    await Promise.all([store.fetchSummary(selectedMetric.value.id), store.fetchSnapshots(selectedMetric.value.id)])
  } catch (cause) { fail(cause) }
}

function openMetric(row) {
  fieldErrors.value = {}
  Object.assign(metricForm, row ? { ...blankMetric(), ...row } : blankMetric())
  metricDialog.value = true
}
async function submitMetric() {
  const { id, ...payload } = metricForm
  try {
    await store.saveMetric(payload, id)
    metricDialog.value = false
    notify('success', 'Saved', 'Metric saved.')
  } catch (cause) { setFieldErrors(cause); fail(cause) }
}
function removeMetric(row) {
  confirm.require({
    message: `Delete metric "${row.name}" and all its values?`, header: 'Confirm', icon: 'pi pi-exclamation-triangle',
    accept: async () => {
      try {
        await store.removeMetric(row.id)
        if (selectedMetric.value?.id === row.id) selectedMetric.value = null
        notify('success', 'Deleted', 'Metric deleted.')
      } catch (cause) { fail(cause) }
    },
  })
}
async function recordSnapshot() {
  try {
    await store.addSnapshot({ metric: selectedMetric.value.id, value: String(snapshotValue.value) })
    snapshotValue.value = null
    await store.fetchSummary(selectedMetric.value.id)
    notify('success', 'Recorded', 'Value recorded.')
  } catch (cause) { fail(cause) }
}

async function recordEvent() {
  try {
    await store.addEvent({ name: eventForm.name.trim(), source_app: eventForm.source_app.trim() })
    eventForm.name = ''
    eventForm.source_app = ''
    notify('success', 'Recorded', 'Event recorded.')
  } catch (cause) { fail(cause) }
}
async function removeEvent(row) {
  try {
    const { deleteEvent } = await import('@/services/Analytics/Analytics')
    await deleteEvent(row.id)
    await Promise.all([store.fetchEvents(), store.fetchEventCounts()])
  } catch (cause) { fail(cause) }
}

function openReport(row) {
  fieldErrors.value = {}
  Object.assign(reportForm, blankReport(), row ? {
    id: row.id, title: row.title, report_type: row.report_type,
    period_start: row.period_start || '', period_end: row.period_end || '', metric: row.parameters?.metric ?? null,
  } : {})
  reportDialog.value = true
}
async function submitReport() {
  const payload = {
    title: reportForm.title, report_type: reportForm.report_type,
    period_start: reportForm.period_start || null, period_end: reportForm.period_end || null,
    parameters: reportForm.report_type === 'metric_trend' && reportForm.metric ? { metric: reportForm.metric } : {},
  }
  try {
    await store.saveReport(payload, reportForm.id)
    reportDialog.value = false
    notify('success', 'Saved', 'Report saved.')
  } catch (cause) { setFieldErrors(cause); fail(cause) }
}
async function generate(row) {
  try {
    await store.generateReport(row.id)
    notify('success', 'Generated', 'Report generated.')
  } catch (cause) { fail(cause) }
}
function removeReport(row) {
  confirm.require({
    message: `Delete report "${row.title}"?`, header: 'Confirm', icon: 'pi pi-exclamation-triangle',
    accept: async () => {
      try { await store.removeReport(row.id); notify('success', 'Deleted', 'Report deleted.') } catch (cause) { fail(cause) }
    },
  })
}

onMounted(load)
</script>

<style scoped>
.analytics-page { padding: 1rem; }
.page-head, .toolbar { display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; margin-bottom: 1rem; flex-wrap: wrap; }
.toolbar { justify-content: flex-start; }
.detail { margin-top: 1.5rem; }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(7rem, 1fr)); gap: 0.75rem; margin-bottom: 1rem; }
.stats span { display: block; font-size: 0.75rem; opacity: 0.7; }
.chart { height: 18rem; }
.counts { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
.form { display: flex; flex-direction: column; gap: 0.75rem; }
.form label { display: flex; flex-direction: column; gap: 0.25rem; }
.form label.inline { flex-direction: row; align-items: center; }
.err { color: var(--p-red-500, #ef4444); }
.muted { opacity: 0.65; }
.json { max-height: 24rem; overflow: auto; font-size: 0.8rem; }
</style>
