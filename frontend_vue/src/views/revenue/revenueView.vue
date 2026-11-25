<template>
  <div class="revenue-page">
    <PageHeader
      eyebrow="Business"
      title="Revenue"
      description="Revenue streams and income records"
      illustration="finance"
    >
      <template #actions>
        <Button label="Add" icon="pi pi-plus" @click="openCreate" />
      </template>
    </PageHeader>

    <Message v-if="store.error" severity="error" :closable="false">
      {{ errorText(store.error) }}
      <Button label="Retry" text size="small" @click="load" />
    </Message>

    <section class="revenue-tiles">
      <Card v-for="t in tiles" :key="t.label">
        <template #title>{{ t.label }}</template>
        <template #content>
          <div v-if="t.values.length" class="tile-values">
            <div v-for="v in t.values" :key="v.currency">{{ v.amount }} {{ v.currency }}</div>
          </div>
          <span v-else class="muted">No data yet</span>
        </template>
      </Card>
    </section>

    <div class="revenue-tabs" role="tablist">
      <Button
        v-for="t in tabs"
        :key="t.key"
        :label="t.label"
        :severity="tab === t.key ? 'primary' : 'secondary'"
        :outlined="tab !== t.key"
        size="small"
        @click="tab = t.key"
      />
    </div>

    <div v-if="tab === 'records'" class="revenue-fromsale">
      <InputText v-model="saleId" placeholder="Sale ID" inputmode="numeric" />
      <Button
        label="Recognise sale as revenue"
        icon="pi pi-download"
        :disabled="!/^\d+$/.test(saleId)"
        @click="fromSale"
      />
    </div>

    <DataTable :value="rows" :loading="store.loading" stripedRows paginator :rows="10" dataKey="id">
      <template #empty
        >No {{ currentTab.label.toLowerCase() }} yet. Use “Add” to create one.</template
      >
      <Column v-for="c in currentTab.columns" :key="c.field" :field="c.field" :header="c.header">
        <template #body="{ data: row }">{{ display(row, c) }}</template>
      </Column>
      <Column header="" style="width: 8rem">
        <template #body="{ data: row }">
          <Button icon="pi pi-pencil" text rounded aria-label="Edit" @click="openEdit(row)" />
          <Button
            icon="pi pi-trash"
            text
            rounded
            severity="danger"
            aria-label="Delete"
            @click="askDelete(row)"
          />
        </template>
      </Column>
    </DataTable>

    <Dialog
      v-model:visible="dialog"
      modal
      :header="(editingId ? 'Edit ' : 'New ') + currentTab.singular"
      :style="{ width: '28rem' }"
    >
      <form class="revenue-form" @submit.prevent="submit">
        <div v-for="f in currentTab.fields" :key="f.name" class="field">
          <label :for="'rev-' + f.name">{{ f.label }}</label>
          <select v-if="f.type === 'select'" :id="'rev-' + f.name" v-model="form[f.name]">
            <option v-if="!f.required" value="">—</option>
            <option v-for="o in optionsFor(f)" :key="o.value" :value="o.value">
              {{ o.label }}
            </option>
          </select>
          <Textarea
            v-else-if="f.type === 'textarea'"
            :id="'rev-' + f.name"
            v-model="form[f.name]"
            rows="3"
          />
          <input
            v-else-if="f.type === 'checkbox'"
            :id="'rev-' + f.name"
            v-model="form[f.name]"
            type="checkbox"
          />
          <InputText
            v-else
            :id="'rev-' + f.name"
            v-model="form[f.name]"
            :type="f.type || 'text'"
            :inputmode="f.type === 'money' ? 'decimal' : undefined"
          />
          <small v-if="fieldErrors[f.name]" class="err">{{ fieldErrors[f.name] }}</small>
        </div>
        <small v-if="fieldErrors.detail || fieldErrors.non_field_errors" class="err">{{
          fieldErrors.detail || fieldErrors.non_field_errors
        }}</small>
        <footer>
          <Button type="button" label="Cancel" text @click="dialog = false" />
          <Button type="submit" label="Save" :loading="saving" />
        </footer>
      </form>
    </Dialog>

    <Dialog v-model:visible="confirm.visible" modal header="Delete" :style="{ width: '24rem' }">
      <p>Delete this {{ currentTab.singular.toLowerCase() }}? This cannot be undone.</p>
      <template #footer>
        <Button label="Cancel" text @click="confirm.visible = false" />
        <Button label="Delete" severity="danger" @click="doDelete" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import PageHeader from '@/components/ui/PageHeader.vue'
import { computed, onMounted, reactive, ref } from 'vue'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Textarea from 'primevue/textarea'
import { useToast } from 'primevue/usetoast'
import { useRevenueStore } from '@/stores/revenue/revenueStore'

const store = useRevenueStore()
const toast = useToast()

const SOURCE_TYPES = ['service', 'product', 'subscription', 'affiliate', 'other']
const STREAM_STATUS = ['active', 'paused', 'ended']
const INTERVALS = ['monthly', 'quarterly', 'yearly']
const RECURRING_STATUS = ['active', 'paused', 'cancelled']
const enumOptions = (values) => values.map((v) => ({ value: v, label: v }))

const tabs = [
  {
    key: 'records',
    label: 'Records',
    singular: 'Record',
    columns: [
      { field: 'received_on', header: 'Received' },
      { field: 'amount', header: 'Amount' },
      { field: 'currency', header: 'Currency' },
      { field: 'stream', header: 'Stream', ref: 'streams' },
      { field: 'description', header: 'Description' },
    ],
    fields: [
      { name: 'amount', label: 'Amount', type: 'money', required: true },
      { name: 'currency', label: 'Currency (3 letters)', default: 'USD' },
      { name: 'received_on', label: 'Received on', type: 'date', required: true },
      { name: 'stream', label: 'Stream', type: 'select', ref: 'streams' },
      { name: 'description', label: 'Description' },
      { name: 'reference', label: 'Reference' },
    ],
  },
  {
    key: 'streams',
    label: 'Streams',
    singular: 'Stream',
    columns: [
      { field: 'name', header: 'Name' },
      { field: 'source', header: 'Source', ref: 'sources' },
      { field: 'status', header: 'Status' },
    ],
    fields: [
      { name: 'name', label: 'Name', required: true },
      { name: 'source', label: 'Source', type: 'select', ref: 'sources', required: true },
      {
        name: 'status',
        label: 'Status',
        type: 'select',
        options: enumOptions(STREAM_STATUS),
        required: true,
        default: 'active',
      },
      { name: 'description', label: 'Description', type: 'textarea' },
    ],
  },
  {
    key: 'sources',
    label: 'Sources',
    singular: 'Source',
    columns: [
      { field: 'name', header: 'Name' },
      { field: 'source_type', header: 'Type' },
      { field: 'is_active', header: 'Active' },
    ],
    fields: [
      { name: 'name', label: 'Name', required: true },
      {
        name: 'source_type',
        label: 'Type',
        type: 'select',
        options: enumOptions(SOURCE_TYPES),
        required: true,
        default: 'service',
      },
      { name: 'description', label: 'Description', type: 'textarea' },
      { name: 'is_active', label: 'Active', type: 'checkbox', default: true },
    ],
  },
  {
    key: 'recurring',
    label: 'Recurring',
    singular: 'Recurring item',
    columns: [
      { field: 'name', header: 'Name' },
      { field: 'amount', header: 'Amount' },
      { field: 'currency', header: 'Currency' },
      { field: 'interval', header: 'Interval' },
      { field: 'status', header: 'Status' },
      { field: 'start_date', header: 'Start' },
    ],
    fields: [
      { name: 'stream', label: 'Stream', type: 'select', ref: 'streams', required: true },
      { name: 'name', label: 'Name' },
      { name: 'amount', label: 'Amount', type: 'money', required: true },
      { name: 'currency', label: 'Currency (3 letters)', default: 'USD' },
      {
        name: 'interval',
        label: 'Interval',
        type: 'select',
        options: enumOptions(INTERVALS),
        required: true,
        default: 'monthly',
      },
      {
        name: 'status',
        label: 'Status',
        type: 'select',
        options: enumOptions(RECURRING_STATUS),
        required: true,
        default: 'active',
      },
      { name: 'start_date', label: 'Start date', type: 'date', required: true },
      { name: 'end_date', label: 'End date', type: 'date' },
    ],
  },
]

const tab = ref('records')
const currentTab = computed(() => tabs.find((t) => t.key === tab.value))
const rows = computed(() => store[tab.value])

const nameOf = (collection, id) => store[collection].find((x) => x.id === id)?.name ?? id ?? '—'
function display(row, col) {
  const v = row[col.field]
  if (col.ref) return v == null ? '—' : nameOf(col.ref, v)
  if (typeof v === 'boolean') return v ? 'Yes' : 'No'
  return v === '' || v == null ? '—' : v
}
const optionsFor = (f) => f.options || store[f.ref].map((x) => ({ value: x.id, label: x.name }))

const tileValues = (obj) =>
  Object.entries(obj || {}).map(([currency, amount]) => ({ currency, amount }))
const tiles = computed(() => [
  { label: 'Total received', values: tileValues(store.summary?.totals) },
  { label: 'MRR', values: tileValues(store.mrr?.mrr) },
  { label: 'ARR', values: tileValues(store.mrr?.arr) },
])

function errorText(e) {
  const d = e?.response?.data
  if (d?.detail) return d.detail
  if (d && typeof d === 'object')
    return Object.entries(d)
      .map(([k, v]) => `${k}: ${[].concat(v).join(' ')}`)
      .join(' · ')
  return e?.message || 'Request failed.'
}

const dialog = ref(false)
const saving = ref(false)
const editingId = ref(null)
const form = reactive({})
const fieldErrors = reactive({})

function resetForm(row) {
  Object.keys(form).forEach((k) => delete form[k])
  Object.keys(fieldErrors).forEach((k) => delete fieldErrors[k])
  for (const f of currentTab.value.fields) {
    const v = row ? row[f.name] : f.default
    form[f.name] = v ?? (f.type === 'checkbox' ? false : '')
  }
}
function openCreate() {
  editingId.value = null
  resetForm(null)
  dialog.value = true
}
function openEdit(row) {
  editingId.value = row.id
  resetForm(row)
  dialog.value = true
}

function payload() {
  const out = {}
  for (const f of currentTab.value.fields) {
    let v = form[f.name]
    if (f.type === 'checkbox') v = !!v
    else if (v === '' || v == null) {
      if (f.required) continue
      v = f.type === 'select' || f.type === 'date' ? null : ''
    } else if (f.type === 'select' && f.ref) v = Number(v)
    else if (f.name === 'currency') v = String(v).trim().toUpperCase()
    out[f.name] = v
  }
  return out
}

async function submit() {
  Object.keys(fieldErrors).forEach((k) => delete fieldErrors[k])
  saving.value = true
  try {
    await store.save(tab.value, payload(), editingId.value)
    dialog.value = false
    toast.add({ severity: 'success', summary: 'Saved', life: 2500 })
  } catch (e) {
    const d = e?.response?.data
    if (d && typeof d === 'object') {
      for (const [k, v] of Object.entries(d)) fieldErrors[k] = [].concat(v).join(' ')
    } else fieldErrors.detail = e?.message || 'Request failed.'
  } finally {
    saving.value = false
  }
}

const confirm = reactive({ visible: false, id: null })
const askDelete = (row) => {
  confirm.id = row.id
  confirm.visible = true
}
async function doDelete() {
  try {
    await store.remove(tab.value, confirm.id)
    toast.add({ severity: 'success', summary: 'Deleted', life: 2500 })
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Delete failed', detail: errorText(e), life: 5000 })
  } finally {
    confirm.visible = false
  }
}

const saleId = ref('')
async function fromSale() {
  try {
    await store.recordFromSale(Number(saleId.value))
    saleId.value = ''
    toast.add({ severity: 'success', summary: 'Sale recognised as revenue', life: 2500 })
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Could not record sale',
      detail: errorText(e),
      life: 5000,
    })
  }
}

const load = () => store.fetchAll().catch(() => {})
onMounted(load)
</script>

<style scoped>
.revenue-page {
  padding: 1rem;
  display: grid;
  gap: 1rem;
}
.revenue-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.revenue-tiles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
  gap: 1rem;
}
.revenue-tabs,
.revenue-fromsale {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.revenue-form {
  display: grid;
  gap: 0.75rem;
}
.revenue-form .field {
  display: grid;
  gap: 0.25rem;
}
.revenue-form footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
.err {
  color: var(--p-red-500, #dc2626);
}
.muted {
  opacity: 0.6;
}
</style>
