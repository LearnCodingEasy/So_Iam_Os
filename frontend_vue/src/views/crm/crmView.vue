<script setup>
import PageHeader from '@/components/ui/PageHeader.vue'
import { computed, onMounted, reactive, ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import DatePicker from 'primevue/datepicker'
import Dialog from 'primevue/dialog'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Select from 'primevue/select'
import Tab from 'primevue/tab'
import TabList from 'primevue/tablist'
import TabPanel from 'primevue/tabpanel'
import TabPanels from 'primevue/tabpanels'
import Tabs from 'primevue/tabs'
import Tag from 'primevue/tag'
import Textarea from 'primevue/textarea'
import { useCrmStore } from '@/stores/crm/crmStore'

const store = useCrmStore()
const toast = useToast()
const confirm = useConfirm()

const search = ref('')
const tab = ref('contacts')
const dialog = reactive({
  open: false,
  resource: 'contacts',
  id: null,
  form: {},
  errors: {},
  saving: false,
})

const STATUS = ['active', 'inactive', 'archived'].map((v) => ({ label: v, value: v }))
const TYPES = ['call', 'email', 'meeting', 'message', 'note'].map((v) => ({ label: v, value: v }))
const STAGES = ['lead', 'prospect', 'customer', 'partner', 'churned'].map((v) => ({
  label: v,
  value: v,
}))

// field specs drive the single create/edit dialog for every resource
const SPECS = {
  companies: {
    title: 'Company',
    fields: [
      { key: 'name', label: 'Name', type: 'text', required: true },
      { key: 'industry', label: 'Industry', type: 'text' },
      { key: 'website', label: 'Website', type: 'text' },
      { key: 'size', label: 'Size', type: 'text' },
      { key: 'notes', label: 'Notes', type: 'area' },
    ],
    defaults: () => ({ name: '', industry: '', website: '', size: '', notes: '' }),
  },
  contacts: {
    title: 'Contact',
    fields: [
      { key: 'first_name', label: 'First name', type: 'text', required: true },
      { key: 'last_name', label: 'Last name', type: 'text' },
      { key: 'email', label: 'Email', type: 'text' },
      { key: 'phone', label: 'Phone', type: 'text' },
      { key: 'job_title', label: 'Job title', type: 'text' },
      { key: 'company', label: 'Company', type: 'select', options: () => companyOptions.value },
      { key: 'source', label: 'Source', type: 'text' },
      { key: 'status', label: 'Status', type: 'select', options: () => STATUS },
      { key: 'notes', label: 'Notes', type: 'area' },
    ],
    defaults: () => ({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      job_title: '',
      company: null,
      source: '',
      status: 'active',
      notes: '',
    }),
  },
  interactions: {
    title: 'Interaction',
    fields: [
      {
        key: 'contact',
        label: 'Contact',
        type: 'select',
        required: true,
        options: () => contactOptions.value,
      },
      { key: 'interaction_type', label: 'Type', type: 'select', options: () => TYPES },
      { key: 'subject', label: 'Subject', type: 'text', required: true },
      { key: 'occurred_at', label: 'Occurred at', type: 'date' },
      { key: 'follow_up_at', label: 'Follow up at', type: 'date' },
      { key: 'notes', label: 'Notes', type: 'area' },
    ],
    defaults: () => ({
      contact: null,
      interaction_type: 'note',
      subject: '',
      occurred_at: new Date(),
      follow_up_at: null,
      notes: '',
    }),
  },
  relationships: {
    title: 'Relationship',
    fields: [
      {
        key: 'contact',
        label: 'Contact',
        type: 'select',
        required: true,
        options: () => contactOptions.value,
        lockOnEdit: true,
      },
      { key: 'stage', label: 'Stage', type: 'select', options: () => STAGES },
      { key: 'health_score', label: 'Health score (0-100)', type: 'number' },
      { key: 'next_step', label: 'Next step', type: 'area' },
    ],
    defaults: () => ({ contact: null, stage: 'lead', health_score: 50, next_step: '' }),
  },
}
const DATE_KEYS = ['occurred_at', 'follow_up_at']

const companyOptions = computed(() => store.companies.map((c) => ({ label: c.name, value: c.id })))
const contactOptions = computed(() =>
  store.contacts.map((c) => ({ label: c.full_name || c.first_name, value: c.id })),
)
const contactName = (id) => contactOptions.value.find((o) => o.value === id)?.label || `#${id}`
const companyName = (id) =>
  id ? companyOptions.value.find((o) => o.value === id)?.label || `#${id}` : '—'
const fmt = (v) => (v ? new Date(v).toLocaleString() : '—')
const stageEntries = computed(() => Object.entries(store.pipeline?.stages || {}))
const spec = computed(() => SPECS[dialog.resource])

function describe(cause) {
  const d = cause?.response?.data
  if (d && typeof d === 'object') {
    return Object.entries(d)
      .map(([k, v]) => `${k}: ${[].concat(v).join(' ')}`)
      .join(' | ')
  }
  return cause?.message || 'Request failed'
}

async function load() {
  try {
    await store.refresh()
  } catch (cause) {
    toast.add({
      severity: 'error',
      summary: 'Could not load CRM data',
      detail: describe(cause),
      life: 5000,
    })
  }
}

let searchTimer
function onSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => store.fetchContacts({ search: search.value }).catch(() => {}), 300)
}

function openDialog(resource, row = null) {
  const form = { ...SPECS[resource].defaults() }
  if (row) {
    for (const key of Object.keys(form)) {
      form[key] = DATE_KEYS.includes(key) && row[key] ? new Date(row[key]) : (row[key] ?? form[key])
    }
  }
  Object.assign(dialog, {
    open: true,
    resource,
    id: row?.id ?? null,
    form,
    errors: {},
    saving: false,
  })
}

async function submit() {
  dialog.saving = true
  dialog.errors = {}
  const payload = { ...dialog.form }
  for (const key of DATE_KEYS) {
    if (key in payload) payload[key] = payload[key] ? new Date(payload[key]).toISOString() : null
  }
  if (dialog.resource === 'relationships' && dialog.id) delete payload.contact
  if (dialog.resource === 'contacts' && !payload.company) payload.company = null
  try {
    await store.save(dialog.resource, payload, dialog.id)
    toast.add({ severity: 'success', summary: `${spec.value.title} saved`, life: 2500 })
    dialog.open = false
  } catch (cause) {
    const d = cause?.response?.data
    dialog.errors = d && typeof d === 'object' ? d : { detail: describe(cause) }
  } finally {
    dialog.saving = false
  }
}

function askRemove(resource, row, label) {
  confirm.require({
    message: `Delete ${label}?`,
    header: 'Confirm delete',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await store.remove(resource, row.id)
        toast.add({ severity: 'success', summary: 'Deleted', life: 2000 })
      } catch (cause) {
        toast.add({
          severity: 'error',
          summary: 'Delete failed',
          detail: describe(cause),
          life: 5000,
        })
      }
    },
  })
}

const errorText = (key) => [].concat(dialog.errors[key] || []).join(' ')

onMounted(load)
</script>

<template>
  <div class="crm-page">
    <PageHeader
      eyebrow="Business"
      title="CRM"
      description="Customer relationships, deals and activities"
      illustration="jobs"
    >
      <template #actions>
        <Button
          label="Refresh"
          icon="pi pi-refresh"
          severity="secondary"
          :loading="store.loading"
          @click="load"
        />
      </template>
    </PageHeader>

    <Message v-if="store.error" severity="error" :closable="false">
      {{ describe(store.error) }}
    </Message>

    <Tabs v-model:value="tab">
      <TabList>
        <Tab value="contacts">Contacts</Tab>
        <Tab value="companies">Companies</Tab>
        <Tab value="interactions">Interactions</Tab>
        <Tab value="relationships">Relationships</Tab>
        <Tab value="pipeline">Pipeline &amp; follow-ups</Tab>
      </TabList>
      <TabPanels>
        <TabPanel value="contacts">
          <div class="toolbar">
            <InputText v-model="search" placeholder="Search contacts" @input="onSearch" />
            <Button label="New contact" icon="pi pi-plus" @click="openDialog('contacts')" />
          </div>
          <DataTable :value="store.contacts" :loading="store.loading" stripedRows data-key="id">
            <template #empty>No contacts found.</template>
            <Column field="full_name" header="Name" />
            <Column field="email" header="Email" />
            <Column field="job_title" header="Title" />
            <Column header="Company"
              ><template #body="{ data }">{{ companyName(data.company) }}</template></Column
            >
            <Column header="Status"
              ><template #body="{ data }"><Tag :value="data.status" /></template
            ></Column>
            <Column header="">
              <template #body="{ data }">
                <Button
                  icon="pi pi-pencil"
                  text
                  aria-label="Edit"
                  @click="openDialog('contacts', data)"
                />
                <Button
                  icon="pi pi-trash"
                  text
                  severity="danger"
                  aria-label="Delete"
                  @click="askRemove('contacts', data, data.full_name)"
                />
              </template>
            </Column>
          </DataTable>
        </TabPanel>

        <TabPanel value="companies">
          <div class="toolbar">
            <Button label="New company" icon="pi pi-plus" @click="openDialog('companies')" />
          </div>
          <DataTable :value="store.companies" :loading="store.loading" stripedRows data-key="id">
            <template #empty>No companies yet.</template>
            <Column field="name" header="Name" />
            <Column field="industry" header="Industry" />
            <Column field="size" header="Size" />
            <Column header="">
              <template #body="{ data }">
                <Button
                  icon="pi pi-pencil"
                  text
                  aria-label="Edit"
                  @click="openDialog('companies', data)"
                />
                <Button
                  icon="pi pi-trash"
                  text
                  severity="danger"
                  aria-label="Delete"
                  @click="askRemove('companies', data, data.name)"
                />
              </template>
            </Column>
          </DataTable>
        </TabPanel>

        <TabPanel value="interactions">
          <div class="toolbar">
            <Button label="Log interaction" icon="pi pi-plus" @click="openDialog('interactions')" />
          </div>
          <DataTable :value="store.interactions" :loading="store.loading" stripedRows data-key="id">
            <template #empty>No interactions logged.</template>
            <Column field="subject" header="Subject" />
            <Column header="Contact"
              ><template #body="{ data }">{{ contactName(data.contact) }}</template></Column
            >
            <Column field="interaction_type" header="Type" />
            <Column header="When"
              ><template #body="{ data }">{{ fmt(data.occurred_at) }}</template></Column
            >
            <Column header="Follow up"
              ><template #body="{ data }">{{ fmt(data.follow_up_at) }}</template></Column
            >
            <Column header="">
              <template #body="{ data }">
                <Button
                  icon="pi pi-pencil"
                  text
                  aria-label="Edit"
                  @click="openDialog('interactions', data)"
                />
                <Button
                  icon="pi pi-trash"
                  text
                  severity="danger"
                  aria-label="Delete"
                  @click="askRemove('interactions', data, data.subject)"
                />
              </template>
            </Column>
          </DataTable>
        </TabPanel>

        <TabPanel value="relationships">
          <div class="toolbar">
            <Button
              label="New relationship"
              icon="pi pi-plus"
              @click="openDialog('relationships')"
            />
          </div>
          <DataTable
            :value="store.relationships"
            :loading="store.loading"
            stripedRows
            data-key="id"
          >
            <template #empty>No relationships tracked.</template>
            <Column header="Contact"
              ><template #body="{ data }">{{ contactName(data.contact) }}</template></Column
            >
            <Column header="Stage"
              ><template #body="{ data }"><Tag :value="data.stage" /></template
            ></Column>
            <Column field="health_score" header="Health" />
            <Column field="next_step" header="Next step" />
            <Column header="">
              <template #body="{ data }">
                <Button
                  icon="pi pi-pencil"
                  text
                  aria-label="Edit"
                  @click="openDialog('relationships', data)"
                />
                <Button
                  icon="pi pi-trash"
                  text
                  severity="danger"
                  aria-label="Delete"
                  @click="askRemove('relationships', data, 'this relationship')"
                />
              </template>
            </Column>
          </DataTable>
        </TabPanel>

        <TabPanel value="pipeline">
          <div class="grid">
            <Card v-for="[stage, n] in stageEntries" :key="stage">
              <template #title>{{ stage }}</template>
              <template #content
                ><strong>{{ n }}</strong></template
              >
            </Card>
            <p v-if="!stageEntries.length">No pipeline data.</p>
          </div>
          <h3>Follow-ups due (next 7 days, overdue first)</h3>
          <DataTable :value="store.followUps" :loading="store.loading" stripedRows data-key="id">
            <template #empty>Nothing to follow up.</template>
            <Column field="subject" header="Subject" />
            <Column header="Contact"
              ><template #body="{ data }">{{ contactName(data.contact) }}</template></Column
            >
            <Column header="Due"
              ><template #body="{ data }">{{ fmt(data.follow_up_at) }}</template></Column
            >
          </DataTable>
        </TabPanel>
      </TabPanels>
    </Tabs>

    <Dialog
      v-model:visible="dialog.open"
      modal
      :header="`${dialog.id ? 'Edit' : 'New'} ${spec.title}`"
      :style="{ width: '32rem' }"
    >
      <form class="form" @submit.prevent="submit">
        <Message
          v-if="errorText('detail') || errorText('non_field_errors')"
          severity="error"
          :closable="false"
        >
          {{ errorText('detail') }} {{ errorText('non_field_errors') }}
        </Message>
        <div v-for="f in spec.fields" :key="f.key" class="field">
          <label :for="`crm-${f.key}`">{{ f.label }}<span v-if="f.required"> *</span></label>
          <InputText v-if="f.type === 'text'" :id="`crm-${f.key}`" v-model="dialog.form[f.key]" />
          <Textarea
            v-else-if="f.type === 'area'"
            :id="`crm-${f.key}`"
            v-model="dialog.form[f.key]"
            rows="3"
          />
          <InputNumber
            v-else-if="f.type === 'number'"
            :input-id="`crm-${f.key}`"
            v-model="dialog.form[f.key]"
            :min="0"
            :max="100"
          />
          <DatePicker
            v-else-if="f.type === 'date'"
            :input-id="`crm-${f.key}`"
            v-model="dialog.form[f.key]"
            show-time
            show-button-bar
          />
          <Select
            v-else
            :input-id="`crm-${f.key}`"
            v-model="dialog.form[f.key]"
            :options="f.options()"
            option-label="label"
            option-value="value"
            :show-clear="!f.required"
            :disabled="f.lockOnEdit && !!dialog.id"
          />
          <small v-if="errorText(f.key)" class="err">{{ errorText(f.key) }}</small>
        </div>
        <div class="actions">
          <Button type="button" label="Cancel" severity="secondary" @click="dialog.open = false" />
          <Button type="submit" label="Save" :loading="dialog.saving" />
        </div>
      </form>
    </Dialog>
  </div>
</template>

<style scoped>
.crm-page {
  padding: 1rem;
}
.crm-head,
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}
.form {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}
.field {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}
.actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
.err {
  color: var(--p-red-500, #ef4444);
}
</style>
