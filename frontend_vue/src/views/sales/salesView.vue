<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import Toast from 'primevue/toast'
import Card from 'primevue/card'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import Message from 'primevue/message'
import { useSalesStore } from '@/stores/sales/salesStore'

const store = useSalesStore()
const toast = useToast()

const STAGES = ['prospecting', 'qualified', 'proposal', 'negotiation', 'won', 'lost']
const OPEN = ['prospecting', 'qualified', 'proposal', 'negotiation']
const ACTIVITY_TYPES = ['call', 'email', 'meeting', 'demo', 'proposal', 'note']
const OFFER_STATUSES = ['draft', 'active', 'retired']
const TABS = [
  { key: 'deals', label: 'Deals' },
  { key: 'offers', label: 'Offers' },
  { key: 'sales', label: 'Sales' },
  { key: 'activities', label: 'Activities' },
]

// Editable fields per resource (read-only fields such as stage/status are never sent).
const FIELDS = {
  deals: ['title', 'value', 'currency', 'offer', 'expected_close_date'],
  offers: ['name', 'description', 'price', 'currency', 'status'],
  sales: ['amount', 'currency', 'deal', 'offer', 'reference'],
  activities: ['deal', 'activity_type', 'notes'],
}
const BLANK = {
  deals: () => ({ title: '', value: 0, currency: 'USD', offer: null, expected_close_date: '' }),
  offers: () => ({ name: '', description: '', price: 0, currency: 'USD', status: 'draft' }),
  sales: () => ({ amount: 0, currency: 'USD', deal: null, offer: null, reference: '' }),
  activities: () => ({ deal: null, activity_type: 'note', notes: '' }),
}
const MONEY = ['value', 'price', 'amount']

const tab = ref('deals')
const dialog = reactive({ open: false, id: null, form: {}, saving: false, errors: {} })
const lost = reactive({ open: false, deal: null, reason: '', saving: false })
const loadError = ref('')

const rows = computed(() => store[tab.value])
const dealOptions = computed(() => store.deals.map((d) => ({ label: d.title, value: d.id })))
const offerOptions = computed(() => store.offers.map((o) => ({ label: o.name, value: o.id })))
const title = computed(() => TABS.find((t) => t.key === tab.value).label)
const dealTitle = (id) => store.deals.find((d) => d.id === id)?.title || (id ? `#${id}` : '—')
const offerName = (id) => store.offers.find((o) => o.id === id)?.name || (id ? `#${id}` : '—')
const closed = (d) => !OPEN.includes(d.stage)

function message(cause) {
  const data = cause?.response?.data
  if (typeof data === 'string') return data
  if (data && typeof data === 'object') {
    return Object.entries(data).map(([k, v]) => `${k}: ${[].concat(v).join(' ')}`).join(' | ')
  }
  return cause?.message || 'Request failed'
}
const notify = (severity, detail) => toast.add({ severity, summary: title.value, detail, life: 4000 })

async function load() {
  loadError.value = ''
  try {
    await store.fetchAll()
  } catch (cause) {
    loadError.value = message(cause)
  }
}

function openForm(row = null) {
  dialog.id = row?.id ?? null
  dialog.errors = {}
  const form = BLANK[tab.value]()
  if (row) {
    for (const f of FIELDS[tab.value]) form[f] = MONEY.includes(f) ? Number(row[f]) : (row[f] ?? form[f])
  }
  dialog.form = form
  dialog.open = true
}

async function submit() {
  const payload = {}
  for (const f of FIELDS[tab.value]) {
    const v = dialog.form[f]
    if (MONEY.includes(f)) payload[f] = Number(v ?? 0).toFixed(2)
    else if (v === '' && ['expected_close_date', 'offer', 'deal'].includes(f)) payload[f] = null
    else payload[f] = v
  }
  dialog.saving = true
  dialog.errors = {}
  try {
    await store.save(tab.value, payload, dialog.id)
    dialog.open = false
    notify('success', dialog.id ? 'Updated' : 'Created')
  } catch (cause) {
    dialog.errors = cause?.response?.data && typeof cause.response.data === 'object' ? cause.response.data : {}
    notify('error', message(cause))
  } finally {
    dialog.saving = false
  }
}

async function destroy(row) {
  if (!window.confirm('Delete this record?')) return
  try {
    await store.remove(tab.value, row.id)
    notify('success', 'Deleted')
  } catch (cause) {
    notify('error', message(cause))
  }
}

async function moveStage(deal, stage) {
  if (stage === 'lost') {
    Object.assign(lost, { open: true, deal, reason: '' })
    return
  }
  try {
    await store.setStage(deal.id, stage)
    notify('success', `Deal moved to ${stage}`)
  } catch (cause) {
    notify('error', message(cause))
  }
}

async function confirmLost() {
  lost.saving = true
  try {
    await store.setStage(lost.deal.id, 'lost', lost.reason)
    lost.open = false
    notify('success', 'Deal marked lost')
  } catch (cause) {
    notify('error', message(cause))
  } finally {
    lost.saving = false
  }
}

async function refund(sale) {
  try {
    await store.refund(sale.id)
    notify('success', 'Sale refunded')
  } catch (cause) {
    notify('error', message(cause))
  }
}

const fmtMoney = (amount, currency) => `${Number(amount).toLocaleString(undefined, { minimumFractionDigits: 2 })} ${currency}`
const fmtDate = (v) => (v ? new Date(v).toLocaleString() : '—')
const winRate = computed(() => (store.pipeline?.win_rate == null ? '—' : `${Math.round(store.pipeline.win_rate * 100)}%`))
const stageTotal = (s) => Object.entries(store.pipeline?.stages?.[s]?.value || {}).map(([c, v]) => fmtMoney(v, c)).join(', ') || '—'

onMounted(load)
</script>

<template>
  <div class="sales-page">
    <Toast />
    <Card>
      <template #title>Sales</template>
      <template #content>
        <Message v-if="loadError" severity="error" :closable="false">
          {{ loadError }} <Button label="Retry" size="small" text @click="load" />
        </Message>

        <div v-if="store.pipeline" class="pipeline" data-testid="pipeline">
          <div v-for="s in STAGES" :key="s" class="stage">
            <strong>{{ s }}</strong>
            <span>{{ store.pipeline.stages?.[s]?.count ?? 0 }} deals</span>
            <small>{{ stageTotal(s) }}</small>
          </div>
          <div class="stage"><strong>Win rate</strong><span>{{ winRate }}</span></div>
        </div>

        <div class="toolbar">
          <div class="tabs">
            <Button v-for="t in TABS" :key="t.key" :label="t.label" size="small"
              :severity="tab === t.key ? 'primary' : 'secondary'" :outlined="tab !== t.key" @click="tab = t.key" />
          </div>
          <Button label="New" icon="pi pi-plus" size="small" @click="openForm()" />
        </div>

        <DataTable :value="rows" :loading="store.loading" stripedRows paginator :rows="10" dataKey="id">
          <template #empty>No {{ title.toLowerCase() }} yet. Use “New” to add one.</template>

          <template v-if="tab === 'deals'">
            <Column field="title" header="Deal" sortable />
            <Column header="Value" sortable sortField="value"><template #body="{ data }">{{ fmtMoney(data.value, data.currency) }}</template></Column>
            <Column header="Stage">
              <template #body="{ data }">
                <Select v-if="!closed(data)" :modelValue="data.stage" :options="OPEN.concat(['won', 'lost'])"
                  size="small" @update:modelValue="(s) => moveStage(data, s)" />
                <Tag v-else :value="data.stage" :severity="data.stage === 'won' ? 'success' : 'danger'" />
              </template>
            </Column>
            <Column header="Offer"><template #body="{ data }">{{ offerName(data.offer) }}</template></Column>
            <Column field="expected_close_date" header="Expected close" />
          </template>

          <template v-else-if="tab === 'offers'">
            <Column field="name" header="Offer" sortable />
            <Column header="Price" sortable sortField="price"><template #body="{ data }">{{ fmtMoney(data.price, data.currency) }}</template></Column>
            <Column header="Status"><template #body="{ data }"><Tag :value="data.status" /></template></Column>
          </template>

          <template v-else-if="tab === 'sales'">
            <Column header="Amount" sortable sortField="amount"><template #body="{ data }">{{ fmtMoney(data.amount, data.currency) }}</template></Column>
            <Column header="Status"><template #body="{ data }"><Tag :value="data.status" :severity="data.status === 'refunded' ? 'warn' : 'success'" /></template></Column>
            <Column header="Deal"><template #body="{ data }">{{ dealTitle(data.deal) }}</template></Column>
            <Column header="Sold"><template #body="{ data }">{{ fmtDate(data.sold_at) }}</template></Column>
            <Column field="reference" header="Reference" />
          </template>

          <template v-else>
            <Column field="activity_type" header="Type" />
            <Column header="Deal"><template #body="{ data }">{{ dealTitle(data.deal) }}</template></Column>
            <Column field="notes" header="Notes" />
            <Column header="When"><template #body="{ data }">{{ fmtDate(data.occurred_at) }}</template></Column>
          </template>

          <Column header="" style="width: 12rem">
            <template #body="{ data }">
              <Button v-if="tab === 'sales' && data.status === 'completed'" label="Refund" size="small" text severity="warn" @click="refund(data)" />
              <Button v-if="!(tab === 'deals' && closed(data))" icon="pi pi-pencil" size="small" text aria-label="Edit" @click="openForm(data)" />
              <Button icon="pi pi-trash" size="small" text severity="danger" aria-label="Delete" @click="destroy(data)" />
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>

    <Dialog v-model:visible="dialog.open" modal :header="(dialog.id ? 'Edit ' : 'New ') + title" :style="{ width: '28rem' }">
      <form class="form" @submit.prevent="submit">
        <template v-for="f in FIELDS[tab]" :key="f">
          <label :for="`f-${f}`">{{ f.replace('_', ' ') }}</label>
          <InputNumber v-if="MONEY.includes(f)" :inputId="`f-${f}`" v-model="dialog.form[f]" mode="decimal" :minFractionDigits="2" :maxFractionDigits="2" :min="0" />
          <Select v-else-if="f === 'deal'" :inputId="`f-${f}`" v-model="dialog.form[f]" :options="dealOptions" optionLabel="label" optionValue="value" showClear placeholder="Select deal" />
          <Select v-else-if="f === 'offer'" :inputId="`f-${f}`" v-model="dialog.form[f]" :options="offerOptions" optionLabel="label" optionValue="value" showClear placeholder="Select offer" />
          <Select v-else-if="f === 'activity_type'" :inputId="`f-${f}`" v-model="dialog.form[f]" :options="ACTIVITY_TYPES" />
          <Select v-else-if="f === 'status'" :inputId="`f-${f}`" v-model="dialog.form[f]" :options="OFFER_STATUSES" />
          <Textarea v-else-if="f === 'description' || f === 'notes'" :id="`f-${f}`" v-model="dialog.form[f]" rows="3" />
          <InputText v-else :id="`f-${f}`" v-model="dialog.form[f]" :type="f === 'expected_close_date' ? 'date' : 'text'" :maxlength="f === 'currency' ? 3 : undefined" />
          <small v-if="dialog.errors[f]" class="err">{{ [].concat(dialog.errors[f]).join(' ') }}</small>
        </template>
        <small v-if="dialog.errors.detail" class="err">{{ [].concat(dialog.errors.detail).join(' ') }}</small>
        <div class="actions">
          <Button type="button" label="Cancel" text @click="dialog.open = false" />
          <Button type="submit" label="Save" :loading="dialog.saving" />
        </div>
      </form>
    </Dialog>

    <Dialog v-model:visible="lost.open" modal header="Mark deal lost" :style="{ width: '24rem' }">
      <div class="form">
        <label for="lost-reason">Reason (required)</label>
        <Textarea id="lost-reason" v-model="lost.reason" rows="3" />
        <div class="actions">
          <Button label="Cancel" text @click="lost.open = false" />
          <Button label="Mark lost" severity="danger" :disabled="!lost.reason.trim()" :loading="lost.saving" @click="confirmLost" />
        </div>
      </div>
    </Dialog>
  </div>
</template>

<style scoped>
.sales-page { padding: 1rem; }
.pipeline { display: grid; grid-template-columns: repeat(auto-fit, minmax(8rem, 1fr)); gap: 0.5rem; margin-bottom: 1rem; }
.stage { display: flex; flex-direction: column; padding: 0.5rem; border: 1px solid var(--p-content-border-color, #ddd); border-radius: 6px; text-transform: capitalize; }
.toolbar { display: flex; justify-content: space-between; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem; }
.tabs { display: flex; gap: 0.25rem; }
.form { display: flex; flex-direction: column; gap: 0.4rem; }
.form label { text-transform: capitalize; font-weight: 600; }
.actions { display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 0.75rem; }
.err { color: var(--p-red-500, #c00); }
</style>
