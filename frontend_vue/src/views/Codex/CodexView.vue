<script setup>
import { computed, onMounted, ref } from 'vue'

import { useCodexStore } from '@/stores/codex'
import codex from '@/services/codex'

import Card from 'primevue/card'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Message from 'primevue/message'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ProgressBar from 'primevue/progressbar'
import InputText from 'primevue/inputtext'
import Dialog from 'primevue/dialog'
import Divider from 'primevue/divider'
import Avatar from 'primevue/avatar'
import Badge from 'primevue/badge'
import ProgressSpinner from 'primevue/progressspinner'
import SelectButton from 'primevue/selectbutton'

const store = useCodexStore()

/* -------------------------------------------------------------------------- */
/* STATE                                                                      */
/* -------------------------------------------------------------------------- */

const activeTab = ref('overview')
const search = ref('')

const scanning = ref(false)
const loadingContext = ref(false)
const loadingPage = ref(false)

const actionError = ref('')

const assistantPrompt = ref('')
const assistantAnswer = ref('')
const assistantOpen = ref(false)

const detailsOpen = ref(false)
const detailsTitle = ref('')
const detailsItem = ref(null)

const planOpen = ref(false)
const snapshotOpen = ref(false)

const savingPlan = ref(false)
const savingSnapshot = ref(false)
const creatingChangeSet = ref(false)

const planForm = ref({
  title: '',
  objective: '',
  paths: '',
})

const snapshotForm = ref({
  label: '',
})

const aiProvider = ref('local')
const aiResult = ref(null)
const aiError = ref('')

const analysisMode = ref('analysis')

const providerOptions = [
  {
    label: 'Local',
    value: 'local',
  },
  {
    label: 'OpenAI',
    value: 'openai',
  },
]

const analysisModes = [
  {
    label: 'Analysis',
    value: 'analysis',
  },
  {
    label: 'Change Planning',
    value: 'planning',
  },
]

/* -------------------------------------------------------------------------- */
/* NAVIGATION                                                                  */
/* -------------------------------------------------------------------------- */

const tabs = [
  {
    key: 'overview',
    label: 'Dashboard',
    icon: 'pi pi-home',
  },
  {
    key: 'features',
    label: 'Features',
    icon: 'pi pi-sitemap',
  },
  {
    key: 'apis',
    label: 'API Registry',
    icon: 'pi pi-code',
  },
  {
    key: 'files',
    label: 'Files',
    icon: 'pi pi-file',
  },
  {
    key: 'protected',
    label: 'Protected',
    icon: 'pi pi-shield',
  },
  {
    key: 'changes',
    label: 'Changes',
    icon: 'pi pi-history',
  },
  {
    key: 'snapshots',
    label: 'Snapshots',
    icon: 'pi pi-camera',
  },
]

const quickActions = [
  {
    label: 'Scan Project',
    icon: 'pi pi-search',
    action: 'scan',
    severity: 'primary',
  },
  {
    label: 'View Features',
    icon: 'pi pi-sitemap',
    action: 'features',
    severity: 'secondary',
  },
  {
    label: 'Check API Registry',
    icon: 'pi pi-code',
    action: 'apis',
    severity: 'contrast',
  },
  {
    label: 'Create Snapshot',
    icon: 'pi pi-camera',
    action: 'snapshot',
    severity: 'warn',
  },
  {
    label: 'Ask Codex',
    icon: 'pi pi-sparkles',
    action: 'assistant',
    severity: 'help',
  },
]

/* -------------------------------------------------------------------------- */
/* FALLBACK DATA                                                              */
/* -------------------------------------------------------------------------- */

const fallbackOverview = {
  project: {
    name: 'SO_IAM_OS',
  },

  counts: {
    features: 0,
    files: 0,
    apis: 0,
    protected: 0,
    changes: 0,
    snapshots: 0,
  },

  guarantee:
    'Every discovered backend API is registered in Codex and mapped to a frontend location through the API Registry.',
}

/* -------------------------------------------------------------------------- */
/* COMPUTED                                                                   */
/* -------------------------------------------------------------------------- */

const overview = computed(() => {
  return store.overview || fallbackOverview
})

const featureCount = computed(() => {
  return Number(overview.value?.counts?.features ?? store.features.length ?? 0)
})

const fileCount = computed(() => {
  return Number(overview.value?.counts?.files ?? store.files.length ?? 0)
})

const apiCount = computed(() => {
  return Number(overview.value?.counts?.apis ?? store.apis.length ?? 0)
})

const protectedCount = computed(() => {
  return Number(overview.value?.counts?.protected ?? store.protected.length ?? 0)
})

const changeCount = computed(() => {
  return Number(overview.value?.counts?.changes ?? store.changes.length ?? 0)
})

const snapshotCount = computed(() => {
  return Number(overview.value?.counts?.snapshots ?? store.snapshots.length ?? 0)
})

const mappedApis = computed(() => {
  return store.apis.filter((api) => {
    const status = String(api?.coverage_status || '').toLowerCase()

    const explicitlyMapped = ['mapped', 'covered', 'complete', 'implemented'].includes(status)

    const hasFrontendLocation = Boolean(
      api?.frontend_route ||
      api?.frontend_section ||
      api?.frontend_component ||
      api?.frontend_service,
    )

    return explicitlyMapped || hasFrontendLocation
  }).length
})

const apiCoverage = computed(() => {
  if (!apiCount.value) {
    return 100
  }

  return Math.min(100, Math.round((mappedApis.value / apiCount.value) * 100))
})

const filteredApis = computed(() => {
  return filterRows(store.apis, [
    'method',
    'path',
    'name',
    'app_label',
    'frontend_route',
    'frontend_section',
    'coverage_status',
  ])
})

const filteredFeatures = computed(() => {
  return filterRows(store.features, ['key', 'name', 'app_label', 'status'])
})

const filteredFiles = computed(() => {
  return filterRows(store.files, ['path', 'kind', 'app_label'])
})

const filteredProtected = computed(() => {
  return filterRows(store.protected, ['key', 'reason'])
})

const filteredChanges = computed(() => {
  return filterRows(store.changes, ['title', 'status', 'snapshot_id'])
})

const filteredSnapshots = computed(() => {
  return filterRows(store.snapshots, ['label', 'id'])
})

const recentFeatures = computed(() => {
  return store.features.slice(0, 6)
})

const recentApis = computed(() => {
  return store.apis.slice(0, 6)
})

const recentChanges = computed(() => {
  return store.changes.slice(0, 5)
})

const recentSnapshots = computed(() => {
  return store.snapshots.slice(0, 5)
})

const projectName = computed(() => {
  return overview.value?.project?.name || overview.value?.metadata?.name || 'SO_IAM_OS'
})

const foundationStatus = computed(() => {
  if (store.error) {
    return 'degraded'
  }

  if (store.loading || loadingPage.value) {
    return 'loading'
  }

  return 'online'
})

const foundationStatusLabel = computed(() => {
  const labels = {
    online: 'Codex Foundation Online',
    loading: 'Codex Foundation Loading',
    degraded: 'Codex Foundation Degraded',
  }

  return labels[foundationStatus.value]
})

const projectBreakdown = computed(() => {
  const files = store.files || []

  const backend = files.filter((item) =>
    /django|python|backend/i.test(`${item?.path || ''} ${item?.kind || ''}`),
  ).length

  const frontend = files.filter((item) =>
    /vue|javascript|typescript|frontend/i.test(`${item?.path || ''} ${item?.kind || ''}`),
  ).length

  const migrations = files.filter((item) => /migration/i.test(item?.path || '')).length

  const config = files.filter((item) =>
    /config|json|yaml|yml|toml|env/i.test(`${item?.path || ''} ${item?.kind || ''}`),
  ).length

  const categorized = backend + frontend + migrations + config

  const other = Math.max(fileCount.value - categorized, 0)

  return [
    {
      label: 'Backend (Django)',
      value: backend,
      icon: 'pi pi-server',
    },
    {
      label: 'Frontend (Vue)',
      value: frontend,
      icon: 'pi pi-desktop',
    },
    {
      label: 'Migrations',
      value: migrations,
      icon: 'pi pi-database',
    },
    {
      label: 'Static / Config',
      value: config,
      icon: 'pi pi-cog',
    },
    {
      label: 'Other',
      value: other,
      icon: 'pi pi-folder',
    },
  ]
})

/* -------------------------------------------------------------------------- */
/* FILTER                                                                     */
/* -------------------------------------------------------------------------- */

function filterRows(rows = [], fields = []) {
  const query = search.value.trim().toLowerCase()

  if (!query) {
    return rows
  }

  return rows.filter((row) => {
    return fields.some((field) => {
      return String(row?.[field] ?? '')
        .toLowerCase()
        .includes(query)
    })
  })
}

/* -------------------------------------------------------------------------- */
/* NAVIGATION ACTIONS                                                         */
/* -------------------------------------------------------------------------- */

function setTab(tab) {
  activeTab.value = tab
  search.value = ''
  actionError.value = ''
}

function showDetails(title, item) {
  detailsTitle.value = title
  detailsItem.value = item
  detailsOpen.value = true
}

/* -------------------------------------------------------------------------- */
/* LOAD / SCAN                                                                */
/* -------------------------------------------------------------------------- */

async function load() {
  loadingPage.value = true
  actionError.value = ''

  try {
    await store.loadAll()
  } catch (error) {
    actionError.value =
      error?.response?.data?.detail || error?.message || 'Unable to load Codex data.'
  } finally {
    loadingPage.value = false
  }
}

async function scanProject() {
  scanning.value = true
  actionError.value = ''

  try {
    await store.scan()
    await load()
  } catch (error) {
    actionError.value = error?.response?.data?.detail || error?.message || 'Project scan failed.'
  } finally {
    scanning.value = false
  }
}

/* -------------------------------------------------------------------------- */
/* CODEX AI ASSISTANT                                                         */
/* -------------------------------------------------------------------------- */

function openAssistant(prompt = '') {
  if (prompt) {
    assistantPrompt.value = prompt
  }

  assistantOpen.value = true
}

function resetAssistantResult() {
  assistantAnswer.value = ''
  aiResult.value = null
  aiError.value = ''
}

async function askCodex() {
  const prompt = assistantPrompt.value.trim()

  if (!prompt || loadingContext.value) {
    return
  }

  assistantOpen.value = true
  loadingContext.value = true

  resetAssistantResult()

  try {
    if (aiProvider.value === 'local') {
      const context = await codex.context()

      const project = context?.project || context?.metadata || {}

      const response = [
        `Project: ${project?.name || projectName.value}`,
        '',
        `Registered features: ${featureCount.value}`,
        `Tracked files: ${fileCount.value}`,
        `Registered APIs: ${apiCount.value}`,
        `API frontend coverage: ${apiCoverage.value}%`,
        `Protected features: ${protectedCount.value}`,
        `Planned changes: ${changeCount.value}`,
        `Snapshots: ${snapshotCount.value}`,
        '',
        `Question: ${prompt}`,
        '',
        'Codex Local Context Analysis',
        '--------------------------------',
        'The current Codex Foundation can inspect the registered project context,',
        'features, APIs, files, protected areas, changes and snapshots.',
        '',
        'Execution is intentionally separated from analysis.',
        'Changes should move through the protected workflow:',
        'Analysis → Plan → Snapshot → ChangeSet → Approval → Apply.',
      ].join('\n')

      assistantAnswer.value = response

      return
    }

    const response = await codex.askOpenAI(prompt)

    aiResult.value = response?.result || response?.data || null

    assistantAnswer.value =
      response?.raw ||
      response?.answer ||
      (response?.result
        ? JSON.stringify(response.result, null, 2)
        : 'OpenAI returned no textual response.')
  } catch (error) {
    aiError.value =
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      error?.message ||
      'Codex request failed.'

    assistantAnswer.value = aiError.value
  } finally {
    loadingContext.value = false
  }
}

/* -------------------------------------------------------------------------- */
/* QUICK ACTIONS                                                              */
/* -------------------------------------------------------------------------- */

function runQuickAction(action) {
  switch (action) {
    case 'scan':
      return scanProject()

    case 'features':
      return setTab('features')

    case 'apis':
      return setTab('apis')

    case 'snapshot':
      return openSnapshotDialog()

    case 'assistant':
      return openAssistant()

    default:
      return null
  }
}

/* -------------------------------------------------------------------------- */
/* PLAN                                                                       */
/* -------------------------------------------------------------------------- */

function openPlanDialog() {
  planForm.value = {
    title: '',
    objective: '',
    paths: '',
  }

  planOpen.value = true
}

function openPlanFromAnalysis() {
  const featureName = aiResult.value?.feature?.name || aiResult.value?.feature?.key || ''

  const endpoint = aiResult.value?.backend?.endpoint || ''

  const page = aiResult.value?.frontend?.page || ''

  const paths = [
    aiResult.value?.backend?.model,
    aiResult.value?.backend?.serializer,
    endpoint,
    page,
    aiResult.value?.frontend?.service,
  ].filter(Boolean)

  planForm.value = {
    title: featureName ? `Change: ${featureName}` : 'Codex Planned Change',

    objective: `Implement the requested change while preserving existing project architecture and protected areas.${
      featureName ? ` Feature: ${featureName}.` : ''
    }`,

    paths: [...new Set(paths)].join('\n'),
  }

  planOpen.value = true
}

async function submitPlan() {
  const title = planForm.value.title.trim()

  if (!title || savingPlan.value) {
    return
  }

  savingPlan.value = true
  actionError.value = ''

  try {
    await codex.planChange({
      title,

      objective: planForm.value.objective.trim(),

      paths: planForm.value.paths
        .split('\n')
        .map((path) => path.trim())
        .filter(Boolean),
    })

    planOpen.value = false

    await load()

    setTab('changes')
  } catch (error) {
    actionError.value =
      error?.response?.data?.detail || error?.message || 'Unable to create change plan.'
  } finally {
    savingPlan.value = false
  }
}

/* -------------------------------------------------------------------------- */
/* CHANGESET                                                                  */
/* -------------------------------------------------------------------------- */

function createChangeSetFromAnalysis() {
  if (!aiResult.value) {
    return
  }

  openPlanFromAnalysis()
}

async function submitChangeSetFromAnalysis() {
  if (!aiResult.value) {
    return
  }

  creatingChangeSet.value = true
  actionError.value = ''

  try {
    /*
     * The Foundation intentionally keeps execution behind the safe workflow.
     *
     * If the backend exposes a dedicated ChangeSet endpoint later,
     * this function is the single place where that integration should be added.
     *
     * For now we create a protected change plan from the analysis.
     */
    openPlanFromAnalysis()
  } finally {
    creatingChangeSet.value = false
  }
}

/* -------------------------------------------------------------------------- */
/* SNAPSHOT                                                                   */
/* -------------------------------------------------------------------------- */

function openSnapshotDialog() {
  snapshotForm.value = {
    label: `Codex snapshot ${new Date().toLocaleString()}`,
  }

  snapshotOpen.value = true
}

async function submitSnapshot() {
  const label = snapshotForm.value.label.trim()

  if (!label || savingSnapshot.value) {
    return
  }

  savingSnapshot.value = true
  actionError.value = ''

  try {
    await codex.createSnapshot({
      label,
    })

    snapshotOpen.value = false

    await load()

    setTab('snapshots')
  } catch (error) {
    actionError.value =
      error?.response?.data?.detail || error?.message || 'Unable to create project snapshot.'
  } finally {
    savingSnapshot.value = false
  }
}

/* -------------------------------------------------------------------------- */
/* UI HELPERS                                                                 */
/* -------------------------------------------------------------------------- */

function statusSeverity(status) {
  const map = {
    active: 'success',
    planned: 'warn',
    approved: 'info',
    applied: 'success',
    rejected: 'danger',
    rolled_back: 'warn',
    pending: 'secondary',
    failed: 'danger',
  }

  return map[String(status || '').toLowerCase()] || 'secondary'
}

function methodSeverity(method) {
  const map = {
    GET: 'success',
    POST: 'info',
    PUT: 'warn',
    PATCH: 'warn',
    DELETE: 'danger',
  }

  return map[String(method || '').toUpperCase()] || 'secondary'
}

function coverageSeverity(api) {
  const status = String(api?.coverage_status || '').toLowerCase()

  if (['mapped', 'covered', 'complete', 'implemented'].includes(status)) {
    return 'success'
  }

  if (['partial', 'pending'].includes(status)) {
    return 'warn'
  }

  if (['unmapped', 'missing', 'orphaned'].includes(status)) {
    return 'danger'
  }

  return api?.frontend_route || api?.frontend_section ? 'success' : 'secondary'
}

function coverageLabel(api) {
  const status = String(api?.coverage_status || '').toLowerCase()

  if (['mapped', 'covered', 'complete', 'implemented'].includes(status)) {
    return 'Mapped'
  }

  if (['partial', 'pending'].includes(status)) {
    return 'Partial'
  }

  if (['unmapped', 'missing', 'orphaned'].includes(status)) {
    return 'Unmapped'
  }

  return api?.frontend_route || api?.frontend_section ? 'Mapped' : 'Unknown'
}

function relativeDate(value) {
  if (!value) {
    return '—'
  }

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleString()
}

function jsonValue(value) {
  try {
    return JSON.stringify(value, null, 2)
  } catch {
    return String(value ?? '')
  }
}

/* -------------------------------------------------------------------------- */
/* LIFECYCLE                                                                  */
/* -------------------------------------------------------------------------- */

onMounted(load)
</script>

<template>
  <div class="codex-page">
    <div class="codex-shell">
      <!-- ================================================================ -->
      <!-- SIDEBAR                                                         -->
      <!-- ================================================================ -->

      <aside class="codex-sidebar">
        <div class="codex-brand">
          <div class="brand-mark">
            <i class="pi pi-sparkles" />
          </div>

          <div>
            <strong>Codex</strong>
            <small>AI Project Intelligence</small>
          </div>
        </div>

        <div class="sidebar-caption">CODEX</div>

        <button
          v-for="item in tabs"
          :key="item.key"
          type="button"
          class="codex-nav-item"
          :class="{
            active: activeTab === item.key,
          }"
          @click="setTab(item.key)"
        >
          <i :class="item.icon" />

          <span>
            {{ item.label }}
          </span>

          <Badge v-if="item.key === 'apis'" :value="apiCount" severity="info" />
        </button>

        <Divider />

        <div class="sidebar-caption">SAFE WORKFLOW</div>

        <button class="codex-nav-item" type="button" @click="openPlanDialog">
          <i class="pi pi-file-edit" />
          <span>Plan Change</span>
        </button>

        <button class="codex-nav-item" type="button" @click="openSnapshotDialog">
          <i class="pi pi-camera" />
          <span>Create Snapshot</span>
        </button>

        <button
          class="codex-nav-item"
          type="button"
          :disabled="!aiResult"
          @click="createChangeSetFromAnalysis"
        >
          <i class="pi pi-list-check" />
          <span>Create ChangeSet</span>
        </button>

        <div class="codex-online">
          <span class="online-dot" :class="foundationStatus" />

          <span>
            {{ foundationStatusLabel }}
          </span>
        </div>
      </aside>

      <!-- ================================================================ -->
      <!-- MAIN                                                             -->
      <!-- ================================================================ -->

      <main class="codex-main">
        <!-- TOPBAR -->

        <header class="codex-topbar">
          <div class="codex-search">
            <i class="pi pi-search" />

            <InputText v-model="search" placeholder="Search Codex — files, features, APIs..." />

            <span class="shortcut"> Ctrl + K </span>
          </div>

          <div class="topbar-actions">
            <Button icon="pi pi-bell" text rounded aria-label="Notifications" />

            <Button icon="pi pi-sun" text rounded aria-label="Theme" />

            <Avatar label="HS" shape="circle" />
          </div>
        </header>

        <!-- CONTENT -->

        <div class="codex-content">
          <!-- ============================================================ -->
          <!-- HEADING                                                     -->
          <!-- ============================================================ -->

          <div class="page-heading">
            <div>
              <div class="breadcrumb">
                Home
                <i class="pi pi-angle-right" />
                Codex
              </div>

              <div class="heading-row">
                <div class="heading-icon">
                  <i class="pi pi-sparkles" />
                </div>

                <div>
                  <h1>Codex</h1>

                  <p>
                    AI-powered project intelligence, architecture awareness and safe change
                    planning.
                  </p>
                </div>
              </div>
            </div>

            <div class="heading-actions">
              <Button label="Plan Change" icon="pi pi-file-edit" outlined @click="openPlanDialog" />

              <Button
                label="Scan Project"
                icon="pi pi-refresh"
                :loading="scanning"
                @click="scanProject"
              />
            </div>
          </div>

          <!-- ============================================================ -->
          <!-- SYSTEM MESSAGES                                             -->
          <!-- ============================================================ -->

          <Message severity="info" :closable="false" class="codex-rule">
            <div>
              <strong>API coverage rule:</strong>

              every discovered backend API must be registered in Codex and mapped to a frontend
              location through the API Registry. This prevents backend endpoints from becoming
              invisible or orphaned from the frontend architecture.
            </div>
          </Message>

          <Message v-if="store.error" severity="warn" :closable="false">
            {{
              typeof store.error === 'string'
                ? store.error
                : 'Codex API is unavailable. Showing the local foundation shell.'
            }}
          </Message>

          <Message v-if="actionError" severity="error" :closable="true" @close="actionError = ''">
            {{ actionError }}
          </Message>

          <!-- ============================================================ -->
          <!-- METRICS                                                     -->
          <!-- ============================================================ -->

          <div class="metric-grid">
            <Card class="metric-card" @click="setTab('features')">
              <template #content>
                <div class="metric-icon feature">
                  <i class="pi pi-sitemap" />
                </div>

                <div class="metric-label">Features</div>

                <div class="metric-value">
                  {{ featureCount }}
                </div>

                <div class="metric-sub">
                  Registered project capabilities
                  <i class="pi pi-arrow-right" />
                </div>
              </template>
            </Card>

            <Card class="metric-card" @click="setTab('files')">
              <template #content>
                <div class="metric-icon files">
                  <i class="pi pi-file" />
                </div>

                <div class="metric-label">Files</div>

                <div class="metric-value">
                  {{ fileCount }}
                </div>

                <div class="metric-sub">
                  Tracked project files
                  <i class="pi pi-arrow-right" />
                </div>
              </template>
            </Card>

            <Card class="metric-card" @click="setTab('apis')">
              <template #content>
                <div class="metric-icon api">
                  <i class="pi pi-code" />
                </div>

                <div class="metric-label">APIs</div>

                <div class="metric-value">
                  {{ apiCount }}
                </div>

                <div class="metric-sub">
                  Registered endpoints
                  <i class="pi pi-arrow-right" />
                </div>
              </template>
            </Card>

            <Card class="metric-card" @click="setTab('protected')">
              <template #content>
                <div class="metric-icon protected">
                  <i class="pi pi-shield" />
                </div>

                <div class="metric-label">Protected Features</div>

                <div class="metric-value">
                  {{ protectedCount }}
                </div>

                <div class="metric-sub">
                  Active protection rules
                  <i class="pi pi-arrow-right" />
                </div>
              </template>
            </Card>

            <Card class="metric-card" @click="setTab('snapshots')">
              <template #content>
                <div class="metric-icon snapshot">
                  <i class="pi pi-camera" />
                </div>

                <div class="metric-label">Snapshots</div>

                <div class="metric-value">
                  {{ snapshotCount }}
                </div>

                <div class="metric-sub">
                  Available project states
                  <i class="pi pi-arrow-right" />
                </div>
              </template>
            </Card>
          </div>

          <!-- ============================================================ -->
          <!-- OVERVIEW                                                     -->
          <!-- ============================================================ -->

          <template v-if="activeTab === 'overview'">
            <div class="overview-grid">
              <!-- PROJECT OVERVIEW -->

              <Card class="panel project-overview">
                <template #title>
                  <div class="panel-title">
                    <span>
                      <i class="pi pi-folder-open" />
                      Project Overview
                    </span>

                    <Tag value="Project Scanned" severity="success" />
                  </div>
                </template>

                <template #subtitle> {{ projectName }} — full project intelligence </template>

                <template #content>
                  <div class="overview-body">
                    <div class="donut">
                      <div class="donut-inner">
                        <strong>
                          {{ fileCount }}
                        </strong>

                        <span> Total Files </span>
                      </div>
                    </div>

                    <div class="breakdown">
                      <div v-for="item in projectBreakdown" :key="item.label" class="breakdown-row">
                        <div class="breakdown-label">
                          <i :class="item.icon" />

                          {{ item.label }}
                        </div>

                        <strong>
                          {{ item.value }}
                        </strong>
                      </div>
                    </div>
                  </div>
                </template>
              </Card>

              <!-- ARCHITECTURE -->

              <Card class="panel architecture">
                <template #title>
                  <div class="panel-title">
                    <span>
                      <i class="pi pi-share-alt" />
                      System Architecture
                    </span>

                    <Tag value="Live analysis" severity="info" />
                  </div>
                </template>

                <template #subtitle> Current project structure </template>

                <template #content>
                  <div class="architecture-map">
                    <div class="arch-node root">
                      <i class="pi pi-desktop" />
                      Frontend — Vue 3
                    </div>

                    <div class="arch-line" />

                    <div class="arch-node api-layer">
                      <i class="pi pi-server" />
                      API Layer — DRF
                    </div>

                    <div class="arch-line" />

                    <div class="arch-domains">
                      <span>Users</span>
                      <span>AI</span>
                      <span>Learning</span>
                      <span>Knowledge</span>
                      <span>Goals</span>
                      <span>Tasks</span>
                      <span>Jobs</span>
                      <span>Social</span>
                      <span>Notifications</span>
                      <span>Codex</span>
                    </div>
                  </div>
                </template>
              </Card>

              <!-- ASSISTANT -->

              <Card class="panel assistant-panel">
                <template #title>
                  <div class="panel-title">
                    <span>
                      <i class="pi pi-sparkles" />
                      Codex AI Assistant
                    </span>

                    <Tag
                      :value="aiProvider === 'openai' ? 'OpenAI' : 'Local'"
                      :severity="aiProvider === 'openai' ? 'success' : 'secondary'"
                    />
                  </div>
                </template>

                <template #subtitle>
                  Ask about your project and get context-aware insights
                </template>

                <template #content>
                  <div class="assistant-message">
                    What would you like to know about your project?
                  </div>

                  <div class="assistant-actions">
                    <Button label="Show all APIs" size="small" outlined @click="setTab('apis')" />

                    <Button
                      label="List protected features"
                      size="small"
                      outlined
                      @click="setTab('protected')"
                    />

                    <Button
                      label="Analyze structure"
                      size="small"
                      outlined
                      @click="
                        openAssistant(
                          'Analyze the current project architecture and identify important relationships.',
                        )
                      "
                    />

                    <Button
                      label="Find tracked files"
                      size="small"
                      outlined
                      @click="setTab('files')"
                    />
                  </div>

                  <div class="assistant-input">
                    <InputText
                      v-model="assistantPrompt"
                      placeholder="Ask anything about your project..."
                      @keyup.enter="askCodex"
                    />

                    <Button
                      icon="pi pi-send"
                      :loading="loadingContext"
                      aria-label="Ask Codex"
                      @click="askCodex"
                    />
                  </div>

                  <div class="codex-provider-selector">
                    <SelectButton
                      v-model="aiProvider"
                      :options="providerOptions"
                      optionLabel="label"
                      optionValue="value"
                      aria-label="Codex provider"
                    />
                  </div>
                </template>
              </Card>
            </div>

            <!-- ========================================================== -->
            <!-- LOWER GRID                                                 -->
            <!-- ========================================================== -->

            <div class="lower-grid">
              <!-- ACTIVITY -->

              <Card class="panel activity-panel">
                <template #title>
                  <div class="panel-title">
                    <span>
                      <i class="pi pi-bolt" />
                      Recent Activity
                    </span>

                    <Button label="View Changes" text size="small" @click="setTab('changes')" />
                  </div>
                </template>

                <template #content>
                  <div v-if="recentChanges.length" class="activity-list">
                    <div v-for="change in recentChanges" :key="change.id" class="activity-item">
                      <div class="activity-icon">
                        <i class="pi pi-history" />
                      </div>

                      <div class="activity-copy">
                        <strong>
                          {{ change.title }}
                        </strong>

                        <span>
                          {{ change.status }}
                          ·
                          {{ relativeDate(change.created_at) }}
                        </span>
                      </div>

                      <Tag :value="change.status" :severity="statusSeverity(change.status)" />
                    </div>
                  </div>

                  <div v-else class="empty-state">
                    <i class="pi pi-inbox" />
                    <span> No changes planned yet. </span>
                  </div>
                </template>
              </Card>

              <!-- FEATURES -->

              <Card class="panel feature-panel">
                <template #title>
                  <div class="panel-title">
                    <span>
                      <i class="pi pi-sitemap" />
                      Recent Features
                    </span>

                    <Button label="View All" text size="small" @click="setTab('features')" />
                  </div>
                </template>

                <template #content>
                  <div class="feature-list">
                    <button
                      v-for="feature in recentFeatures"
                      :key="feature.id || feature.key"
                      type="button"
                      class="feature-row"
                      @click="showDetails('Feature Details', feature)"
                    >
                      <div class="feature-bullet">
                        <i class="pi pi-box" />
                      </div>

                      <div class="feature-copy">
                        <strong>
                          {{ feature.name || feature.key }}
                        </strong>

                        <span>
                          {{ feature.app_label || 'Project' }}
                        </span>
                      </div>

                      <Tag v-if="feature.protected" value="Protected" severity="success" />

                      <i class="pi pi-angle-right" />
                    </button>
                  </div>
                </template>
              </Card>

              <!-- API -->

              <Card class="panel api-panel">
                <template #title>
                  <div class="panel-title">
                    <span>
                      <i class="pi pi-code" />
                      API Registry
                    </span>

                    <Button label="View All" text size="small" @click="setTab('apis')" />
                  </div>
                </template>

                <template #content>
                  <div class="coverage-head">
                    <span> Frontend coverage </span>

                    <strong> {{ apiCoverage }}% </strong>
                  </div>

                  <ProgressBar :value="apiCoverage" :showValue="false" />

                  <div class="api-list">
                    <button
                      v-for="api in recentApis"
                      :key="api.id || `${api.method}-${api.path}`"
                      type="button"
                      class="api-row"
                      @click="showDetails('API Endpoint', api)"
                    >
                      <Tag :value="api.method" :severity="methodSeverity(api.method)" />

                      <div>
                        <strong>
                          {{ api.path }}
                        </strong>

                        <span>
                          {{ api.frontend_route || 'No frontend route' }}

                          ·

                          {{ api.frontend_section || 'API Registry' }}
                        </span>
                      </div>

                      <Tag :value="coverageLabel(api)" :severity="coverageSeverity(api)" />
                    </button>
                  </div>
                </template>
              </Card>
            </div>

            <!-- ========================================================== -->
            <!-- QUICK ACTIONS                                              -->
            <!-- ========================================================== -->

            <Card class="panel quick-panel">
              <template #title> Quick Actions </template>

              <template #content>
                <div class="quick-grid">
                  <Button
                    v-for="item in quickActions"
                    :key="item.action"
                    :label="item.label"
                    :icon="item.icon"
                    :severity="item.severity"
                    outlined
                    @click="runQuickAction(item.action)"
                  />
                </div>
              </template>
            </Card>

            <!-- ========================================================== -->
            <!-- FOUNDATION                                                 -->
            <!-- ========================================================== -->

            <Card class="foundation-banner">
              <template #content>
                <div class="foundation-icon">
                  <i class="pi pi-shield" />
                </div>

                <div class="foundation-copy">
                  <strong> Codex Foundation </strong>

                  <span> Project intelligence · Safe changes · Full traceability </span>
                </div>

                <div class="foundation-progress">
                  <ProgressBar :value="100" :showValue="false" />

                  <small> Foundation initialized successfully </small>
                </div>
              </template>
            </Card>
          </template>

          <!-- ============================================================ -->
          <!-- REGISTRIES                                                   -->
          <!-- ============================================================ -->

          <template v-else>
            <Card class="table-panel">
              <template #title>
                <div class="table-header">
                  <div>
                    <strong>
                      {{ tabs.find((item) => item.key === activeTab)?.label }}
                    </strong>

                    <span> Codex registry </span>
                  </div>

                  <div class="table-tools">
                    <InputText v-model="search" placeholder="Filter current registry..." />

                    <Button
                      icon="pi pi-refresh"
                      text
                      rounded
                      :loading="store.loading || loadingPage"
                      @click="load"
                    />
                  </div>
                </div>
              </template>

              <template #content>
                <!-- FEATURES -->

                <DataTable
                  v-if="activeTab === 'features'"
                  :value="filteredFeatures"
                  paginator
                  :rows="15"
                  stripedRows
                  responsiveLayout="scroll"
                  class="codex-table"
                >
                  <Column field="key" header="Key" sortable />

                  <Column field="name" header="Feature" sortable />

                  <Column field="app_label" header="App" sortable />

                  <Column field="status" header="Status">
                    <template #body="slotProps">
                      <Tag
                        :value="slotProps.data.status"
                        :severity="statusSeverity(slotProps.data.status)"
                      />
                    </template>
                  </Column>

                  <Column field="protected" header="Protection">
                    <template #body="slotProps">
                      <Tag
                        :value="slotProps.data.protected ? 'Protected' : 'Standard'"
                        :severity="slotProps.data.protected ? 'success' : 'secondary'"
                      />
                    </template>
                  </Column>

                  <Column header="">
                    <template #body="slotProps">
                      <Button
                        icon="pi pi-eye"
                        text
                        rounded
                        @click="showDetails('Feature Details', slotProps.data)"
                      />
                    </template>
                  </Column>
                </DataTable>

                <!-- APIs -->

                <DataTable
                  v-else-if="activeTab === 'apis'"
                  :value="filteredApis"
                  paginator
                  :rows="20"
                  stripedRows
                  responsiveLayout="scroll"
                  class="codex-table"
                >
                  <Column field="method" header="Method" sortable>
                    <template #body="slotProps">
                      <Tag
                        :value="slotProps.data.method"
                        :severity="methodSeverity(slotProps.data.method)"
                      />
                    </template>
                  </Column>

                  <Column field="path" header="Backend API" sortable />

                  <Column field="app_label" header="App" sortable />

                  <Column field="frontend_route" header="Frontend Route">
                    <template #body="slotProps">
                      <code>
                        {{ slotProps.data.frontend_route || '—' }}
                      </code>
                    </template>
                  </Column>

                  <Column field="frontend_section" header="Frontend Section" />

                  <Column field="coverage_status" header="Coverage">
                    <template #body="slotProps">
                      <Tag
                        :value="coverageLabel(slotProps.data)"
                        :severity="coverageSeverity(slotProps.data)"
                      />
                    </template>
                  </Column>

                  <Column header="">
                    <template #body="slotProps">
                      <Button
                        icon="pi pi-eye"
                        text
                        rounded
                        @click="showDetails('API Endpoint', slotProps.data)"
                      />
                    </template>
                  </Column>
                </DataTable>

                <!-- FILES -->

                <DataTable
                  v-else-if="activeTab === 'files'"
                  :value="filteredFiles"
                  paginator
                  :rows="20"
                  stripedRows
                  responsiveLayout="scroll"
                  class="codex-table"
                >
                  <Column field="path" header="Path" sortable />

                  <Column field="kind" header="Kind" sortable />

                  <Column field="app_label" header="App" sortable />

                  <Column field="size" header="Bytes" sortable />

                  <Column field="protected" header="Protected">
                    <template #body="slotProps">
                      <Tag
                        :value="slotProps.data.protected ? 'Yes' : 'No'"
                        :severity="slotProps.data.protected ? 'danger' : 'secondary'"
                      />
                    </template>
                  </Column>
                </DataTable>

                <!-- PROTECTED -->

                <DataTable
                  v-else-if="activeTab === 'protected'"
                  :value="filteredProtected"
                  paginator
                  :rows="15"
                  stripedRows
                  responsiveLayout="scroll"
                  class="codex-table"
                >
                  <Column field="key" header="Key" sortable />

                  <Column field="reason" header="Reason" />

                  <Column field="enabled" header="Enabled">
                    <template #body="slotProps">
                      <Tag
                        :value="slotProps.data.enabled ? 'Enabled' : 'Disabled'"
                        :severity="slotProps.data.enabled ? 'success' : 'secondary'"
                      />
                    </template>
                  </Column>
                </DataTable>

                <!-- CHANGES -->

                <DataTable
                  v-else-if="activeTab === 'changes'"
                  :value="filteredChanges"
                  paginator
                  :rows="15"
                  stripedRows
                  responsiveLayout="scroll"
                  class="codex-table"
                >
                  <Column field="title" header="Title" sortable />

                  <Column field="status" header="Status">
                    <template #body="slotProps">
                      <Tag
                        :value="slotProps.data.status"
                        :severity="statusSeverity(slotProps.data.status)"
                      />
                    </template>
                  </Column>

                  <Column field="snapshot_id" header="Snapshot" />

                  <Column field="created_at" header="Created">
                    <template #body="slotProps">
                      {{ relativeDate(slotProps.data.created_at) }}
                    </template>
                  </Column>
                </DataTable>

                <!-- SNAPSHOTS -->

                <DataTable
                  v-else-if="activeTab === 'snapshots'"
                  :value="filteredSnapshots"
                  paginator
                  :rows="15"
                  stripedRows
                  responsiveLayout="scroll"
                  class="codex-table"
                >
                  <Column field="label" header="Label" sortable />

                  <Column field="created_at" header="Created">
                    <template #body="slotProps">
                      {{ relativeDate(slotProps.data.created_at) }}
                    </template>
                  </Column>

                  <Column field="id" header="ID" sortable />
                </DataTable>
              </template>
            </Card>
          </template>
        </div>
      </main>
    </div>

    <!-- ======================================== -->
    <!-- DETAILS DIALOG -->
    <!-- ============================================= -->

    <Dialog
      v-model:visible="detailsOpen"
      modal
      :header="detailsTitle"
      :style="{
        width: 'min(760px, 94vw)',
      }"
    >
      <pre class="details-json">{{ jsonValue(detailsItem) }}</pre>
    </Dialog>

    <!-- ================================================================== -->
    <!-- AI ASSISTANT                                                      -->
    <!-- ================================================================== -->

    <Dialog
      v-model:visible="assistantOpen"
      modal
      header="Codex Project Assistant"
      :style="{
        width: 'min(760px, 94vw)',
      }"
    >
      <div class="assistant-dialog">
        <div class="assistant-dialog-head">
          <Avatar icon="pi pi-sparkles" shape="circle" />

          <div>
            <strong> Project Intelligence </strong>

            <span> Context-aware project analysis. </span>
          </div>
        </div>

        <Divider />

        <div class="assistant-provider">
          <SelectButton
            v-model="aiProvider"
            :options="providerOptions"
            optionLabel="label"
            optionValue="value"
          />

          <Tag
            :value="aiProvider === 'openai' ? 'Backend → OpenAI' : 'Local Context'"
            :severity="aiProvider === 'openai' ? 'success' : 'secondary'"
          />
        </div>

        <div class="analysis-mode">
          <SelectButton
            v-model="analysisMode"
            :options="analysisModes"
            optionLabel="label"
            optionValue="value"
          />
        </div>

        <div v-if="loadingContext" class="assistant-loading">
          <ProgressSpinner style="width: 32px; height: 32px" strokeWidth="5" />

          <span> Reading project context... </span>
        </div>

        <Message v-else-if="aiError" severity="error" :closable="false">
          {{ aiError }}
        </Message>

        <pre v-else class="assistant-answer">{{
          assistantAnswer || 'Ask Codex a question about your project.'
        }}</pre>

        <div class="assistant-dialog-input">
          <InputText
            v-model="assistantPrompt"
            placeholder="Ask about APIs, features, files, architecture..."
            @keyup.enter="askCodex"
          />

          <Button
            icon="pi pi-send"
            :label="aiProvider === 'openai' ? 'Ask OpenAI' : 'Ask Codex'"
            :loading="loadingContext"
            @click="askCodex"
          />
        </div>
      </div>
    </Dialog>

    <!-- ================================================================== -->
    <!-- AI RESULT                                                         -->
    <!-- ================================================================== -->

    <Card v-if="aiResult" class="change-analysis-card">
      <template #title>
        <div class="analysis-title">
          <i class="pi pi-sparkles" />

          <span> Codex Analysis </span>

          <Tag
            :value="aiProvider === 'openai' ? 'OpenAI' : 'Local'"
            :severity="aiProvider === 'openai' ? 'success' : 'secondary'"
          />
        </div>
      </template>

      <template #content>
        <Message v-if="aiResult.feature" severity="info" :closable="false">
          Feature:
          {{ aiResult.feature.name || aiResult.feature.key || 'Unknown' }}
        </Message>

        <Divider />

        <h4>Backend</h4>

        <ul>
          <li>
            Model:
            {{ aiResult.backend?.model || 'Not found' }}
          </li>

          <li>
            Serializer:
            {{ aiResult.backend?.serializer || 'Not found' }}
          </li>

          <li>
            Endpoint:
            {{ aiResult.backend?.endpoint || 'Not found' }}
          </li>

          <li>
            Storage:
            {{ aiResult.backend?.storage || 'Not found' }}
          </li>
        </ul>

        <Divider />

        <h4>Frontend</h4>

        <ul>
          <li>
            Page:
            {{ aiResult.frontend?.page || 'Not found' }}
          </li>

          <li>
            Service:
            {{ aiResult.frontend?.service || 'Not found' }}
          </li>

          <li>
            Route:
            {{ aiResult.frontend?.route || 'Not found' }}
          </li>
        </ul>

        <Divider />

        <h4>Database</h4>

        <Message
          :severity="aiResult.database?.migration_required ? 'warn' : 'success'"
          :closable="false"
        >
          {{
            aiResult.database?.migration_required ? 'Migration required' : 'No migration required'
          }}
        </Message>

        <Divider />

        <div class="analysis-actions">
          <Button
            label="Create ChangeSet"
            icon="pi pi-list-check"
            severity="warn"
            :loading="creatingChangeSet"
            @click="submitChangeSetFromAnalysis"
          />

          <Button
            label="Plan Safe Change"
            icon="pi pi-file-edit"
            outlined
            @click="openPlanFromAnalysis"
          />
        </div>
      </template>
    </Card>

    <!-- ================================================================== -->
    <!-- PLAN DIALOG                                                       -->
    <!-- ================================================================== -->

    <Dialog
      v-model:visible="planOpen"
      modal
      header="Plan a Safe Change"
      :style="{
        width: 'min(680px, 94vw)',
      }"
    >
      <div class="form-stack">
        <label>
          Change title

          <InputText
            v-model="planForm.title"
            class="w-full"
            placeholder="Example: Improve API registry mapping"
          />
        </label>

        <label>
          Objective

          <textarea
            v-model="planForm.objective"
            class="p-inputtextarea p-inputtext w-full"
            rows="4"
            placeholder="What should change and why?"
          />
        </label>

        <label>
          Paths

          <small> one path per line </small>

          <textarea
            v-model="planForm.paths"
            class="p-inputtextarea p-inputtext w-full"
            rows="5"
            placeholder="frontend_vue/src/views/Codex/CodexView.vue&#10;backend_django/codex/views.py"
          />
        </label>

        <Message severity="warn" :closable="false">
          Planning only. The Codex Foundation does not directly apply source-code changes at this
          stage.
        </Message>

        <div class="dialog-actions">
          <Button label="Cancel" text @click="planOpen = false" />

          <Button
            label="Create Plan"
            icon="pi pi-check"
            :loading="savingPlan"
            :disabled="!planForm.title.trim()"
            @click="submitPlan"
          />
        </div>
      </div>
    </Dialog>

    <!-- ================================================================== -->
    <!-- SNAPSHOT DIALOG                                                   -->
    <!-- ================================================================== -->

    <Dialog
      v-model:visible="snapshotOpen"
      modal
      header="Create Project Snapshot"
      :style="{
        width: 'min(560px, 94vw)',
      }"
    >
      <div class="form-stack">
        <label>
          Snapshot label

          <InputText
            v-model="snapshotForm.label"
            class="w-full"
            placeholder="Before Codex change"
          />
        </label>

        <Message severity="info" :closable="false">
          A snapshot records the current project manifest for future rollback workflows.
        </Message>

        <div class="dialog-actions">
          <Button label="Cancel" text @click="snapshotOpen = false" />

          <Button
            label="Create Snapshot"
            icon="pi pi-camera"
            :loading="savingSnapshot"
            :disabled="!snapshotForm.label.trim()"
            @click="submitSnapshot"
          />
        </div>
      </div>
    </Dialog>
  </div>
</template>
