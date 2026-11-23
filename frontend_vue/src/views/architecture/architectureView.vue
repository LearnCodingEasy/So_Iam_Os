<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import Textarea from 'primevue/textarea'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'
import { useArchitectureStore } from '@/stores/architecture/architectureStore'

const store = useArchitectureStore()
const toast = useToast()

const tab = ref('components')
const tabs = [
  { key: 'components', label: 'Components' },
  { key: 'dependencies', label: 'Dependencies' },
  { key: 'decisions', label: 'Decisions' },
  { key: 'graph', label: 'Graph' },
]

const opts = (pairs) => pairs.map(([value, label]) => ({ value, label }))
const statusOptions = opts([['draft', 'Draft'], ['active', 'Active'], ['deprecated', 'Deprecated']])
const typeOptions = opts([['service', 'Service'], ['database', 'Database'], ['queue', 'Queue'], ['frontend', 'Frontend'], ['library', 'Library'], ['external', 'External'], ['other', 'Other']])
const depTypeOptions = opts([['depends_on', 'Depends on'], ['calls', 'Calls'], ['reads', 'Reads from'], ['writes', 'Writes to']])
const decisionStatusOptions = opts([['proposed', 'Proposed'], ['accepted', 'Accepted'], ['rejected', 'Rejected'], ['deprecated', 'Deprecated'], ['superseded', 'Superseded']])

const selected = computed(() => store.architectures.find((a) => a.id === store.selectedId) || null)
const componentOptions = computed(() => store.components.map((c) => ({ value: c.id, label: c.name })))
const decisionOptions = computed(() => store.decisions.map((d) => ({ value: d.id, label: d.title })))
const componentName = (id) => store.components.find((c) => c.id === id)?.name ?? `#${id}`

// ---- dialog state (one generic dialog for all four resources) ----
const dialog = reactive({ visible: false, kind: 'architecture', id: null, form: {}, errors: '', saving: false })
const titles = { architecture: 'Architecture', component: 'Component', dependency: 'Dependency', decision: 'Decision' }
const defaults = () => ({
  architecture: { name: '', description: '', status: 'draft', version: '1.0' },
  component: { name: '', component_type: 'service', technology: '', description: '' },
  dependency: { source: null, target: null, dependency_type: 'depends_on', description: '' },
  decision: { title: '', status: 'proposed', context: '', decision: '', consequences: '', decided_on: null, superseded_by: null },
})

function openDialog(kind, row = null) {
  dialog.kind = kind
  dialog.id = row?.id ?? null
  dialog.form = row ? { ...defaults()[kind], ...row } : defaults()[kind]
  dialog.errors = ''
  dialog.visible = true
}

function describeError(err) {
  const data = err?.response?.data
  if (!data) return err?.message || 'Request failed.'
  if (typeof data === 'string') return data
  return Object.entries(data)
    .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' ') : typeof v === 'object' ? JSON.stringify(v) : v}`)
    .join('\n')
}

async function save() {
  dialog.saving = true
  dialog.errors = ''
  try {
    const f = { ...dialog.form }
    if (dialog.kind === 'architecture') {
      const saved = await store.saveArchitecture(f, dialog.id)
      if (!dialog.id) await select(saved.id)
      else if (dialog.id === store.selectedId) await store.selectArchitecture(dialog.id)
    } else {
      f.architecture = store.selectedId
      if (dialog.kind === 'dependency') delete f.architecture
      await store.saveChild(dialog.kind, f, dialog.id)
    }
    dialog.visible = false
    toast.add({ severity: 'success', summary: `${titles[dialog.kind]} saved`, life: 2500 })
  } catch (err) {
    dialog.errors = describeError(err)
  } finally {
    dialog.saving = false
  }
}

async function remove(kind, row) {
  if (!window.confirm(`Delete this ${titles[kind].toLowerCase()}?`)) return
  try {
    if (kind === 'architecture') await store.removeArchitecture(row.id)
    else await store.removeChild(kind, row.id)
    toast.add({ severity: 'success', summary: `${titles[kind]} deleted`, life: 2500 })
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Delete failed', detail: describeError(err), life: 5000 })
  }
}

async function select(id) {
  try {
    await store.selectArchitecture(id)
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Could not load architecture', detail: describeError(err), life: 5000 })
  }
}

onMounted(() => store.fetchArchitectures().catch(() => {}))
</script>

<template>
  <div class="arch-page">
    <Toast />
    <header class="arch-head">
      <h1>Architecture</h1>
      <Button label="New architecture" icon="pi pi-plus" @click="openDialog('architecture')" />
    </header>

    <Message v-if="store.error && !store.architectures.length" severity="error" :closable="false">
      {{ describeError(store.error) }}
      <Button label="Retry" text size="small" @click="store.fetchArchitectures()" />
    </Message>

    <div class="arch-layout">
      <aside class="arch-list">
        <p v-if="store.loading">Loading…</p>
        <p v-else-if="!store.architectures.length" class="muted">No architectures yet. Create your first one.</p>
        <ul v-else>
          <li v-for="a in store.architectures" :key="a.id" :class="{ active: a.id === store.selectedId }">
            <button type="button" class="arch-item" @click="select(a.id)">
              <strong>{{ a.name }}</strong>
              <span class="muted">v{{ a.version }}</span>
              <Tag :value="a.status" />
            </button>
            <Button icon="pi pi-pencil" text size="small" aria-label="Edit" @click="openDialog('architecture', a)" />
            <Button icon="pi pi-trash" text severity="danger" size="small" aria-label="Delete" @click="remove('architecture', a)" />
          </li>
        </ul>
      </aside>

      <section class="arch-detail">
        <p v-if="!selected" class="muted">Select an architecture to manage its components, dependencies and decisions.</p>
        <template v-else>
          <p v-if="selected.description">{{ selected.description }}</p>
          <nav class="arch-tabs">
            <Button v-for="t in tabs" :key="t.key" :label="t.label" size="small" :outlined="tab !== t.key" @click="tab = t.key" />
          </nav>

          <!-- Components -->
          <div v-if="tab === 'components'">
            <Button label="Add component" icon="pi pi-plus" size="small" @click="openDialog('component')" />
            <DataTable :value="store.components" :loading="store.detailLoading" size="small">
              <template #empty>No components yet.</template>
              <Column field="name" header="Name" />
              <Column field="component_type" header="Type" />
              <Column field="technology" header="Technology" />
              <Column header="" style="width: 7rem">
                <template #body="{ data }">
                  <Button icon="pi pi-pencil" text size="small" aria-label="Edit" @click="openDialog('component', data)" />
                  <Button icon="pi pi-trash" text severity="danger" size="small" aria-label="Delete" @click="remove('component', data)" />
                </template>
              </Column>
            </DataTable>
          </div>

          <!-- Dependencies -->
          <div v-else-if="tab === 'dependencies'">
            <Button label="Add dependency" icon="pi pi-plus" size="small" :disabled="store.components.length < 2" @click="openDialog('dependency')" />
            <small v-if="store.components.length < 2" class="muted"> Add at least two components first.</small>
            <DataTable :value="store.dependencies" :loading="store.detailLoading" size="small">
              <template #empty>No dependencies yet.</template>
              <Column header="Source"><template #body="{ data }">{{ componentName(data.source) }}</template></Column>
              <Column field="dependency_type" header="Relation" />
              <Column header="Target"><template #body="{ data }">{{ componentName(data.target) }}</template></Column>
              <Column header="" style="width: 7rem">
                <template #body="{ data }">
                  <Button icon="pi pi-pencil" text size="small" aria-label="Edit" @click="openDialog('dependency', data)" />
                  <Button icon="pi pi-trash" text severity="danger" size="small" aria-label="Delete" @click="remove('dependency', data)" />
                </template>
              </Column>
            </DataTable>
          </div>

          <!-- Decisions -->
          <div v-else-if="tab === 'decisions'">
            <Button label="Add decision" icon="pi pi-plus" size="small" @click="openDialog('decision')" />
            <DataTable :value="store.decisions" :loading="store.detailLoading" size="small">
              <template #empty>No decisions recorded yet.</template>
              <Column field="title" header="Title" />
              <Column field="status" header="Status" />
              <Column field="decided_on" header="Decided on" />
              <Column header="" style="width: 7rem">
                <template #body="{ data }">
                  <Button icon="pi pi-pencil" text size="small" aria-label="Edit" @click="openDialog('decision', data)" />
                  <Button icon="pi pi-trash" text severity="danger" size="small" aria-label="Delete" @click="remove('decision', data)" />
                </template>
              </Column>
            </DataTable>
          </div>

          <!-- Graph (read-only list view of GET /architectures/{id}/graph/) -->
          <div v-else>
            <p v-if="!store.graph || !store.graph.nodes.length" class="muted">No components to display.</p>
            <template v-else>
              <p class="muted">
                {{ store.graph.metrics.components }} components · {{ store.graph.metrics.dependencies }} dependencies ·
                {{ store.graph.metrics.isolated.length }} isolated
              </p>
              <ul class="graph-tree">
                <li v-for="n in store.graph.nodes" :key="n.id">
                  <strong>{{ n.name }}</strong> <span class="muted">({{ n.type }})</span>
                  <span v-if="n.id === store.graph.metrics.most_depended_on"> ★ most depended on</span>
                  <ul>
                    <li v-for="e in store.graph.edges.filter((x) => x.source === n.id)" :key="e.id">
                      {{ e.type }} → {{ componentName(e.target) }}
                    </li>
                  </ul>
                </li>
              </ul>
            </template>
          </div>
        </template>
      </section>
    </div>

    <Dialog v-model:visible="dialog.visible" modal :header="`${dialog.id ? 'Edit' : 'New'} ${titles[dialog.kind].toLowerCase()}`" :style="{ width: '32rem' }">
      <form class="arch-form" @submit.prevent="save">
        <Message v-if="dialog.errors" severity="error" :closable="false"><pre>{{ dialog.errors }}</pre></Message>

        <template v-if="dialog.kind === 'architecture'">
          <label>Name<InputText v-model="dialog.form.name" required /></label>
          <label>Version<InputText v-model="dialog.form.version" required /></label>
          <label>Status<Select v-model="dialog.form.status" :options="statusOptions" option-label="label" option-value="value" /></label>
          <label>Description<Textarea v-model="dialog.form.description" rows="3" /></label>
        </template>

        <template v-else-if="dialog.kind === 'component'">
          <label>Name<InputText v-model="dialog.form.name" required /></label>
          <label>Type<Select v-model="dialog.form.component_type" :options="typeOptions" option-label="label" option-value="value" /></label>
          <label>Technology<InputText v-model="dialog.form.technology" /></label>
          <label>Description<Textarea v-model="dialog.form.description" rows="3" /></label>
        </template>

        <template v-else-if="dialog.kind === 'dependency'">
          <label>Source<Select v-model="dialog.form.source" :options="componentOptions" option-label="label" option-value="value" /></label>
          <label>Relation<Select v-model="dialog.form.dependency_type" :options="depTypeOptions" option-label="label" option-value="value" /></label>
          <label>Target<Select v-model="dialog.form.target" :options="componentOptions" option-label="label" option-value="value" /></label>
          <label>Description<Textarea v-model="dialog.form.description" rows="2" /></label>
        </template>

        <template v-else>
          <label>Title<InputText v-model="dialog.form.title" required /></label>
          <label>Status<Select v-model="dialog.form.status" :options="decisionStatusOptions" option-label="label" option-value="value" /></label>
          <label>Superseded by<Select v-model="dialog.form.superseded_by" :options="decisionOptions" option-label="label" option-value="value" show-clear /></label>
          <label>Decided on<InputText v-model="dialog.form.decided_on" type="date" /></label>
          <label>Context<Textarea v-model="dialog.form.context" rows="2" /></label>
          <label>Decision<Textarea v-model="dialog.form.decision" rows="2" /></label>
          <label>Consequences<Textarea v-model="dialog.form.consequences" rows="2" /></label>
        </template>

        <div class="arch-actions">
          <Button type="button" label="Cancel" text @click="dialog.visible = false" />
          <Button type="submit" label="Save" icon="pi pi-check" :loading="dialog.saving" />
        </div>
      </form>
    </Dialog>
  </div>
</template>

<style scoped>
.arch-page { padding: 1rem; }
.arch-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.arch-layout { display: grid; grid-template-columns: 18rem 1fr; gap: 1rem; }
.arch-list ul { list-style: none; margin: 0; padding: 0; }
.arch-list li { display: flex; align-items: center; gap: 0.25rem; padding: 0.25rem; border-radius: 6px; }
.arch-list li.active { background: var(--p-highlight-background, rgba(100, 100, 255, 0.12)); }
.arch-item { flex: 1; display: flex; flex-wrap: wrap; gap: 0.4rem; align-items: center; background: none; border: 0; text-align: start; cursor: pointer; color: inherit; }
.arch-tabs { display: flex; gap: 0.5rem; margin: 0.75rem 0; }
.arch-form { display: flex; flex-direction: column; gap: 0.75rem; }
.arch-form label { display: flex; flex-direction: column; gap: 0.25rem; }
.arch-form pre { margin: 0; white-space: pre-wrap; font: inherit; }
.arch-actions { display: flex; justify-content: flex-end; gap: 0.5rem; }
.muted { opacity: 0.7; }
.graph-tree ul { margin: 0.25rem 0 0.5rem 1.25rem; }
@media (max-width: 768px) { .arch-layout { grid-template-columns: 1fr; } }
</style>
