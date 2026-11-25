<template>
  <main class="projects-page">
    <header class="projects-header">
      <div>
        <span class="eyebrow">WORKSPACE / PORTFOLIO</span>
        <h1>Projects</h1>
        <p>Organize initiatives, track status, and keep project context in one place.</p>
      </div>
      <Button label="New project" icon="pi pi-plus" @click="openCreate" />
    </header>

    <Message v-if="store.error" severity="error" :closable="false">
      {{ errorText }} <Button label="Retry" text size="small" @click="load" />
    </Message>

    <section class="projects-toolbar">
      <IconField>
        <InputIcon class="pi pi-search" />
        <InputText v-model="search" placeholder="Search projects…" aria-label="Search projects" />
      </IconField>
      <Select
        v-model="statusFilter"
        :options="statusOptions"
        option-label="label"
        option-value="value"
        placeholder="All statuses"
        show-clear
      />
      <Select v-model="sortBy" :options="sortOptions" option-label="label" option-value="value" />
      <Button
        icon="pi pi-refresh"
        severity="secondary"
        outlined
        aria-label="Refresh projects"
        :loading="store.loading"
        @click="load"
      />
    </section>

    <section class="projects-summary">
      <div>
        <span>Total projects</span><strong>{{ store.count }}</strong>
      </div>
      <div>
        <span>Active in this view</span
        ><strong>{{ filteredProjects.filter((p) => p.status === 'active').length }}</strong>
      </div>
      <div>
        <span>Completed in this view</span
        ><strong>{{ filteredProjects.filter((p) => p.status === 'completed').length }}</strong>
      </div>
    </section>

    <Card class="projects-card">
      <template #content>
        <DataTable
          :value="filteredProjects"
          :loading="store.loading"
          data-key="id"
          paginator
          :rows="10"
          :rows-per-page-options="[10, 20, 50]"
          striped-rows
          sort-mode="single"
          removable-sort
          responsive-layout="scroll"
        >
          <template #empty>
            <div class="projects-empty">
              <i class="pi pi-folder-open" />
              <strong>No projects found</strong>
              <span>Create a project or adjust your search and filters.</span>
            </div>
          </template>
          <Column field="title" header="Project" sortable>
            <template #body="{ data }">
              <button class="project-title" @click="openDetails(data)">{{ data.title }}</button>
              <small>{{ data.description || 'No description provided' }}</small>
            </template>
          </Column>
          <Column field="status" header="Status" sortable>
            <template #body="{ data }"
              ><Tag :value="statusLabel(data.status)" severity="secondary"
            /></template>
          </Column>
          <Column field="updated_at" header="Last updated" sortable>
            <template #body="{ data }">{{ formatDate(data.updated_at) }}</template>
          </Column>
          <Column header="Actions" :exportable="false">
            <template #body="{ data }">
              <div class="project-actions">
                <Button
                  icon="pi pi-eye"
                  text
                  rounded
                  severity="secondary"
                  aria-label="View project details"
                  v-tooltip.top="'View details'"
                  @click="openDetails(data)"
                />
                <Button
                  icon="pi pi-pencil"
                  text
                  rounded
                  severity="secondary"
                  aria-label="Edit project"
                  v-tooltip.top="'Edit project'"
                  @click="openEdit(data)"
                />
                <Button
                  icon="pi pi-trash"
                  text
                  rounded
                  severity="danger"
                  aria-label="Delete project"
                  v-tooltip.top="'Delete project'"
                  :loading="deletingId === data.id"
                  @click="remove(data)"
                />
              </div>
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>

    <Dialog
      v-model:visible="detailsVisible"
      modal
      header="Project details"
      :style="{ width: 'min(36rem, calc(100vw - 2rem))' }"
    >
      <div v-if="detailsLoading" class="projects-empty">
        <i class="pi pi-spin pi-spinner" /><span>Loading project…</span>
      </div>
      <div v-else-if="selectedProject" class="project-details">
        <h2>{{ selectedProject.title }}</h2>
        <Tag :value="statusLabel(selectedProject.status)" severity="secondary" />
        <p>{{ selectedProject.description || 'No description provided.' }}</p>
        <dl>
          <dt>Created</dt>
          <dd>{{ formatDate(selectedProject.created_at) }}</dd>
          <dt>Last updated</dt>
          <dd>{{ formatDate(selectedProject.updated_at) }}</dd>
          <dt>Repository</dt>
          <dd>
            <a
              v-if="selectedProject.repository_url"
              :href="selectedProject.repository_url"
              target="_blank"
              rel="noopener noreferrer"
              >Open repository</a
            ><span v-else>—</span>
          </dd>
          <dt>Website</dt>
          <dd>
            <a
              v-if="selectedProject.website_url"
              :href="selectedProject.website_url"
              target="_blank"
              rel="noopener noreferrer"
              >Open website</a
            ><span v-else>—</span>
          </dd>
        </dl>
        <h3>Metadata</h3>
        <pre>{{ JSON.stringify(selectedProject.metadata || {}, null, 2) }}</pre>
        <Button
          label="Edit project"
          icon="pi pi-pencil"
          @click="((detailsVisible = false), openEdit(selectedProject))"
        />
      </div>
    </Dialog>

    <Dialog
      v-model:visible="dialogVisible"
      modal
      :header="editing ? 'Edit project' : 'Create project'"
      :style="{ width: 'min(34rem, calc(100vw - 2rem))' }"
      :closable="!store.saving"
    >
      <form class="project-form" @submit.prevent="save">
        <label>Project name <InputText v-model.trim="form.title" required maxlength="255" /></label>
        <label>Description <Textarea v-model="form.description" rows="4" auto-resize /></label>
        <label
          >Status
          <Select
            v-model="form.status"
            :options="statusOptions.filter((x) => x.value)"
            option-label="label"
            option-value="value"
          />
        </label>
        <label>Repository URL <InputText v-model.trim="form.repository_url" type="url" /></label>
        <label>Website URL <InputText v-model.trim="form.website_url" type="url" /></label>
        <label>Metadata (JSON) <Textarea v-model="form.metadataJson" rows="4" auto-resize /></label>
        <Message v-if="formError" severity="error" :closable="false">{{ formError }}</Message>
        <div class="form-actions">
          <Button
            label="Cancel"
            severity="secondary"
            text
            type="button"
            @click="dialogVisible = false"
          />
          <Button
            :label="editing ? 'Save changes' : 'Create project'"
            icon="pi pi-check"
            type="submit"
            :loading="store.saving"
          />
        </div>
      </form>
    </Dialog>
    <Toast />
  </main>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useProjectsStore } from '@/stores/projects/projects'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import Message from 'primevue/message'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'

const store = useProjectsStore()
const toast = useToast()
const search = ref('')
const statusFilter = ref(null)
const sortBy = ref('-updated_at')
const dialogVisible = ref(false)
const detailsVisible = ref(false)
const detailsLoading = ref(false)
const selectedProject = ref(null)
const editing = ref(null)
const deletingId = ref(null)
const formError = ref('')
const form = reactive({
  title: '',
  description: '',
  status: 'planning',
  repository_url: '',
  website_url: '',
  metadataJson: '{}',
})
const statusOptions = [
  { label: 'All statuses', value: null },
  { label: 'Planning', value: 'planning' },
  { label: 'Active', value: 'active' },
  { label: 'Paused', value: 'paused' },
  { label: 'Completed', value: 'completed' },
  { label: 'Archived', value: 'archived' },
]
const sortOptions = [
  { label: 'Recently updated', value: '-updated_at' },
  { label: 'Name A–Z', value: 'title' },
  { label: 'Name Z–A', value: '-title' },
  { label: 'Oldest updated', value: 'updated_at' },
]
const errorText = computed(
  () => store.error?.response?.data?.detail || store.error?.message || 'Unable to load projects.',
)
const filteredProjects = computed(() => {
  const query = search.value.trim().toLowerCase()
  return store.items
    .filter(
      (p) =>
        (!statusFilter.value || p.status === statusFilter.value) &&
        (!query || `${p.title || ''} ${p.description || ''}`.toLowerCase().includes(query)),
    )
    .slice()
    .sort((a, b) => {
      const key = sortBy.value.replace(/^-/, '')
      const direction = sortBy.value.startsWith('-') ? -1 : 1
      return String(a[key] || '').localeCompare(String(b[key] || '')) * direction
    })
})
const load = () =>
  store.fetchProjects({
    ordering: sortBy.value,
    search: search.value || undefined,
    status: statusFilter.value || undefined,
  })
watch([search, statusFilter, sortBy], () => load())
const resetForm = () =>
  Object.assign(form, {
    title: '',
    description: '',
    status: 'planning',
    repository_url: '',
    website_url: '',
    metadataJson: '{}',
  })
const openDetails = async (project) => {
  detailsVisible.value = true
  detailsLoading.value = true
  selectedProject.value = project
  try {
    selectedProject.value = await store.getProject(project.id)
  } catch (error) {
    selectedProject.value = null
    toast.add({
      severity: 'error',
      summary: 'Unable to load details',
      detail: error?.response?.data?.detail || 'Project details could not be loaded.',
      life: 4000,
    })
  } finally {
    detailsLoading.value = false
  }
}
const openCreate = () => {
  editing.value = null
  formError.value = ''
  resetForm()
  dialogVisible.value = true
}
const openEdit = (project) => {
  editing.value = project.id
  formError.value = ''
  Object.assign(form, {
    title: project.title || '',
    description: project.description || '',
    status: project.status || 'planning',
    repository_url: project.repository_url || '',
    website_url: project.website_url || '',
    metadataJson: JSON.stringify(project.metadata || {}, null, 2),
  })
  dialogVisible.value = true
}
const save = async () => {
  formError.value = ''
  try {
    let metadata
    try {
      metadata = JSON.parse(form.metadataJson || '{}')
    } catch {
      throw new Error('Metadata must be valid JSON.')
    }
    if (!metadata || typeof metadata !== 'object' || Array.isArray(metadata))
      throw new Error('Metadata must be a JSON object.')
    const { metadataJson, ...fields } = form
    const payload = { ...fields, metadata }
    if (editing.value) await store.updateProject(editing.value, payload)
    else await store.createProject(payload)
    dialogVisible.value = false
    toast.add({
      severity: 'success',
      summary: 'Saved',
      detail: 'Project saved successfully.',
      life: 3000,
    })
    await load()
  } catch (error) {
    formError.value =
      error?.response?.data?.detail ||
      Object.values(error?.response?.data || {})
        .flat()
        .join(' ') ||
      error?.message ||
      'Unable to save project.'
  }
}
const remove = async (project) => {
  if (!window.confirm(`Delete project “${project.title}”? This cannot be undone.`)) return
  deletingId.value = project.id
  try {
    await store.deleteProject(project.id)
    toast.add({ severity: 'success', summary: 'Deleted', detail: 'Project deleted.', life: 2500 })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Delete failed',
      detail: error?.response?.data?.detail || 'Unable to delete project.',
      life: 4000,
    })
  } finally {
    deletingId.value = null
  }
}
const statusLabel = (value) =>
  statusOptions.find((x) => x.value === value)?.label || value || 'Unknown'
const formatDate = (value) => (value ? new Date(value).toLocaleDateString() : '—')
onMounted(load)
</script>
