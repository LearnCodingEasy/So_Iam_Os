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
import ProgressBar from 'primevue/progressbar'
import Message from 'primevue/message'
import { useChallengesStore } from '@/stores/challenges/challengesStore'

const store = useChallengesStore()
const toast = useToast()

const TYPES = ['learning', 'coding', 'goal', 'project']
const STATUSES = ['draft', 'active', 'completed', 'archived']
const loadError = ref('')
const statusFilter = ref(null)
const search = ref('')

const dialog = reactive({ open: false, id: null, form: {}, saving: false, errors: {} })
const stepDialog = reactive({ open: false, challenge: null, form: {}, saving: false, errors: {} })
const attemptDialog = reactive({ open: false, challenge: null, form: {}, saving: false, errors: {} })

const rows = computed(() =>
  store.challenges.filter(
    (c) =>
      (!statusFilter.value || c.status === statusFilter.value) &&
      (!search.value || c.title.toLowerCase().includes(search.value.toLowerCase())),
  ),
)
const progressFor = (id) => store.progress.find((p) => p.challenge === id)?.progress_percent ?? 0

function message(cause) {
  const data = cause?.response?.data
  if (typeof data === 'string') return data
  if (data && typeof data === 'object') {
    return Object.entries(data).map(([k, v]) => `${k}: ${[].concat(v).join(' ')}`).join(' | ')
  }
  return cause?.message || 'Request failed'
}
const notify = (severity, detail) => toast.add({ severity, summary: 'Challenges', detail, life: 4000 })
const fieldErrors = (cause) =>
  cause?.response?.data && typeof cause.response.data === 'object' ? cause.response.data : {}

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
  dialog.form = {
    title: row?.title ?? '',
    description: row?.description ?? '',
    type: row?.type ?? 'learning',
    status: row?.status ?? 'active',
    difficulty: row?.difficulty ?? 'intermediate',
  }
  dialog.open = true
}

async function submit() {
  dialog.saving = true
  dialog.errors = {}
  try {
    await store.save('challenges', { ...dialog.form }, dialog.id)
    dialog.open = false
    notify('success', dialog.id ? 'Challenge updated' : 'Challenge created')
  } catch (cause) {
    dialog.errors = fieldErrors(cause)
    notify('error', message(cause))
  } finally {
    dialog.saving = false
  }
}

async function destroy(row) {
  if (!window.confirm(`Delete “${row.title}” and its steps/attempts?`)) return
  try {
    await store.remove('challenges', row.id)
    notify('success', 'Challenge deleted')
  } catch (cause) {
    notify('error', message(cause))
  }
}

function openStep(challenge) {
  Object.assign(stepDialog, {
    open: true,
    challenge,
    errors: {},
    form: { title: '', instructions: '', order: (challenge.steps?.length ?? 0) + 1 },
  })
}

async function submitStep() {
  stepDialog.saving = true
  stepDialog.errors = {}
  try {
    await store.save('steps', { ...stepDialog.form, challenge: stepDialog.challenge.id })
    stepDialog.open = false
    notify('success', 'Step added')
  } catch (cause) {
    stepDialog.errors = fieldErrors(cause)
    notify('error', message(cause))
  } finally {
    stepDialog.saving = false
  }
}

async function completeStep(row) {
  try {
    const result = await store.completeStep(row.id)
    notify('success', `Progress ${result.progress_percent}%`)
  } catch (cause) {
    notify('error', message(cause))
  }
}

function openAttempt(challenge) {
  Object.assign(attemptDialog, { open: true, challenge, errors: {}, form: { answer: '', score: 0 } })
}

async function submitAttempt() {
  attemptDialog.saving = true
  attemptDialog.errors = {}
  try {
    await store.save('attempts', { ...attemptDialog.form, challenge: attemptDialog.challenge.id })
    attemptDialog.open = false
    notify('success', 'Attempt recorded')
  } catch (cause) {
    attemptDialog.errors = fieldErrors(cause)
    notify('error', message(cause))
  } finally {
    attemptDialog.saving = false
  }
}

onMounted(load)
</script>

<template>
  <div class="os-page">
    <Toast />
    <Card>
      <template #title>Challenges</template>
      <template #content>
        <Message v-if="loadError" severity="error" :closable="false">
          {{ loadError }} <Button label="Retry" size="small" text @click="load" />
        </Message>

        <div class="toolbar">
          <div class="filters">
            <InputText v-model="search" placeholder="Search title" aria-label="Search challenges" />
            <Select v-model="statusFilter" :options="STATUSES" showClear placeholder="All statuses" />
          </div>
          <Button label="New challenge" icon="pi pi-plus" size="small" @click="openForm()" />
        </div>

        <DataTable :value="rows" :loading="store.loading" stripedRows paginator :rows="10" dataKey="id">
          <template #empty>No challenges yet. Use “New challenge” to add one.</template>
          <Column field="title" header="Challenge" sortable />
          <Column field="type" header="Type" />
          <Column field="difficulty" header="Difficulty" />
          <Column header="Status"><template #body="{ data }"><Tag :value="data.status" /></template></Column>
          <Column header="Steps"><template #body="{ data }">{{ data.steps?.length ?? 0 }}</template></Column>
          <Column header="Progress" style="min-width: 9rem">
            <template #body="{ data }"><ProgressBar :value="progressFor(data.id)" :showValue="true" /></template>
          </Column>
          <Column header="" style="width: 18rem">
            <template #body="{ data }">
              <Button label="Complete step" size="small" text :disabled="!data.steps?.length" @click="completeStep(data)" />
              <Button label="Add step" size="small" text @click="openStep(data)" />
              <Button label="Attempt" size="small" text @click="openAttempt(data)" />
              <Button icon="pi pi-pencil" size="small" text aria-label="Edit" @click="openForm(data)" />
              <Button icon="pi pi-trash" size="small" text severity="danger" aria-label="Delete" @click="destroy(data)" />
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>

    <Dialog v-model:visible="dialog.open" modal :header="dialog.id ? 'Edit challenge' : 'New challenge'" :style="{ width: '28rem' }">
      <form class="form" @submit.prevent="submit">
        <label for="c-title">Title</label>
        <InputText id="c-title" v-model="dialog.form.title" />
        <small v-if="dialog.errors.title" class="err">{{ [].concat(dialog.errors.title).join(' ') }}</small>
        <label for="c-desc">Description</label>
        <Textarea id="c-desc" v-model="dialog.form.description" rows="3" />
        <label for="c-type">Type</label>
        <Select inputId="c-type" v-model="dialog.form.type" :options="TYPES" />
        <label for="c-status">Status</label>
        <Select inputId="c-status" v-model="dialog.form.status" :options="STATUSES" />
        <label for="c-diff">Difficulty</label>
        <InputText id="c-diff" v-model="dialog.form.difficulty" />
        <div class="actions">
          <Button type="button" label="Cancel" text @click="dialog.open = false" />
          <Button type="submit" label="Save" :loading="dialog.saving" :disabled="!dialog.form.title?.trim()" />
        </div>
      </form>
    </Dialog>

    <Dialog v-model:visible="stepDialog.open" modal header="Add step" :style="{ width: '28rem' }">
      <form class="form" @submit.prevent="submitStep">
        <label for="s-title">Title</label>
        <InputText id="s-title" v-model="stepDialog.form.title" />
        <small v-if="stepDialog.errors.title" class="err">{{ [].concat(stepDialog.errors.title).join(' ') }}</small>
        <label for="s-ins">Instructions</label>
        <Textarea id="s-ins" v-model="stepDialog.form.instructions" rows="3" />
        <label for="s-order">Order</label>
        <InputNumber inputId="s-order" v-model="stepDialog.form.order" :min="0" />
        <div class="actions">
          <Button type="button" label="Cancel" text @click="stepDialog.open = false" />
          <Button type="submit" label="Save" :loading="stepDialog.saving" :disabled="!stepDialog.form.title?.trim()" />
        </div>
      </form>
    </Dialog>

    <Dialog v-model:visible="attemptDialog.open" modal header="Record attempt" :style="{ width: '28rem' }">
      <form class="form" @submit.prevent="submitAttempt">
        <label for="a-answer">Answer</label>
        <Textarea id="a-answer" v-model="attemptDialog.form.answer" rows="4" />
        <label for="a-score">Score (0–100; 70+ completes the challenge)</label>
        <InputNumber inputId="a-score" v-model="attemptDialog.form.score" :min="0" :max="100" />
        <small v-if="attemptDialog.errors.score" class="err">{{ [].concat(attemptDialog.errors.score).join(' ') }}</small>
        <div class="actions">
          <Button type="button" label="Cancel" text @click="attemptDialog.open = false" />
          <Button type="submit" label="Save" :loading="attemptDialog.saving" />
        </div>
      </form>
    </Dialog>
  </div>
</template>

<style scoped>
.os-page { padding: 1rem; }
.toolbar { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem; }
.filters { display: flex; gap: 0.5rem; }
.form { display: flex; flex-direction: column; gap: 0.4rem; }
.form label { font-weight: 600; }
.actions { display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 0.75rem; }
.err { color: var(--p-red-500, #c00); }
</style>
