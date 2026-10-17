<script setup>
import { computed, onMounted, ref } from 'vue'

import Card from 'primevue/card'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Badge from 'primevue/badge'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import ProgressBar from 'primevue/progressbar'
import Message from 'primevue/message'
import Dialog from 'primevue/dialog'
import Divider from 'primevue/divider'
import SelectButton from 'primevue/selectbutton'
import ScrollPanel from 'primevue/scrollpanel'
import Skeleton from 'primevue/skeleton'
import Splitter from 'primevue/splitter'
import SplitterPanel from 'primevue/splitterpanel'

import { useCodexStore } from '@/stores/codex'
import codex from '@/services/codex'

const store = useCodexStore()

const activePanel = ref('workspace')
const registryTab = ref('features')
const query = ref('')
const fileQuery = ref('')
const chatInput = ref('')
const busy = ref(false)
const validating = ref(false)
const analyzing = ref(false)
const loading = ref(true)
const errorMessage = ref('')
const successMessage = ref('')
const selected = ref(null)
const selectedFiles = ref([])
const selectedFile = ref(null)
const fileContent = ref('')
const result = ref(null)
const chatMessages = ref([])
const graph = ref(null)
const security = ref(null)
const policy = ref(null)
const agentRuns = ref([])
const auditRows = ref([])
const overview = ref(null)
const context = ref(null)
const projects = ref([])
const files = ref([])
const apis = ref([])
const protectedRows = ref([])
const changes = ref([])
const snapshots = ref([])
const showResult = ref(false)
const showPrompt = ref(false)
const generatedPrompt = ref('')
const promptType = ref('development')
const command = ref('')
const commandResult = ref(null)
const selectedHealth = ref('overview')

const navItems = [
  { key: 'workspace', label: 'Workspace', icon: 'pi pi-home' },
  { key: 'files', label: 'Project Explorer', icon: 'pi pi-folder-open' },
  { key: 'analysis', label: 'Project Analysis', icon: 'pi pi-chart-line' },
  { key: 'chat', label: 'Codex Chat', icon: 'pi pi-comments' },
  { key: 'pipeline', label: 'Development Pipeline', icon: 'pi pi-sitemap' },
  { key: 'registry', label: 'Capability Registry', icon: 'pi pi-bolt' },
  { key: 'agents', label: 'Agents & Tools', icon: 'pi pi-microchip-ai' },
  { key: 'governance', label: 'Governance', icon: 'pi pi-shield' },
]

const pipeline = [
  ['01', 'Research'],
  ['02', 'Requirements'],
  ['03', 'Idea'],
  ['04', 'Visual Research'],
  ['05', 'Architecture'],
  ['06', 'Initialization'],
  ['07', 'Dependencies'],
  ['08', 'Configuration'],
  ['09', 'Libraries'],
  ['10', 'Backend'],
  ['11', 'Frontend'],
  ['12', 'Database'],
  ['13', 'API'],
  ['14', 'UI'],
  ['15', 'Integration'],
  ['16', 'Testing'],
  ['17', 'Debugging'],
  ['18', 'Review'],
  ['19', 'Approval'],
  ['20', 'Release'],
  ['21', 'Maintenance'],
].map(([id, name]) => ({
  id,
  name,
  status: id === '14' ? 'IN_PROGRESS' : id < '14' ? 'COMPLETED' : 'PLANNED',
}))

const unwrap = (value) => {
  if (value && typeof value === 'object' && 'value' in value) return value.value
  return value
}

const capabilitySummary = computed(() => unwrap(store.capabilitySummary) || {})
const capabilityHealth = computed(() => unwrap(store.capabilityHealth) || {})
const capabilityFeatures = computed(() => unwrap(store.capabilityFeatures) || [])
const capabilityTools = computed(() => unwrap(store.capabilityTools) || [])
const capabilityAgents = computed(() => unwrap(store.capabilityAgents) || [])

function filterRows(rows) {
  const q = query.value.trim().toLowerCase()
  if (!q) return rows || []
  return (rows || []).filter((row) => JSON.stringify(row).toLowerCase().includes(q))
}

const features = computed(() => filterRows(capabilityFeatures.value))
const tools = computed(() => filterRows(capabilityTools.value))
const agents = computed(() => filterRows(capabilityAgents.value))

const filteredFiles = computed(() => {
  const q = fileQuery.value.trim().toLowerCase()
  if (!q) return files.value
  return files.value.filter((row) => JSON.stringify(row).toLowerCase().includes(q))
})

const healthScores = computed(
  () =>
    capabilityHealth.value?.scores || {
      architecture: 0,
      frontend: 0,
      backend: 0,
      testing: 0,
      documentation: 0,
      dependencies: 0,
      security: 0,
    },
)

const totalCapabilities = computed(
  () =>
    Number(capabilitySummary.value.features || 0) +
    Number(capabilitySummary.value.tools || 0) +
    Number(capabilitySummary.value.agents || 0),
)

const projectName = computed(
  () =>
    overview.value?.project?.name ||
    overview.value?.name ||
    context.value?.project?.name ||
    'SO_IAM_OS',
)

const currentStage = computed(
  () =>
    context.value?.development_pipeline?.current_stage ||
    context.value?.current_stage?.name ||
    'Frontend / Integration',
)

function notifySuccess(message) {
  successMessage.value = message
  errorMessage.value = ''
  window.setTimeout(() => {
    successMessage.value = ''
  }, 3500)
}

function notifyError(error, fallback = 'Codex operation failed.') {
  const detail =
    error?.response?.data?.detail || error?.response?.data?.message || error?.message || fallback
  errorMessage.value = detail
  successMessage.value = ''
}

async function runAction(action, success = 'Operation completed successfully.') {
  busy.value = true
  errorMessage.value = ''
  try {
    const response = await action()
    result.value = response
    notifySuccess(success)
    return response
  } catch (error) {
    notifyError(error)
    return null
  } finally {
    busy.value = false
  }
}

async function loadCoreData() {
  loading.value = true
  errorMessage.value = ''
  const jobs = [
    ['overview', () => codex.overview()],
    ['context', () => codex.context()],
    ['projects', () => codex.projects()],
    ['files', () => codex.files()],
    ['apis', () => codex.apis()],
    ['protected', () => codex.protected()],
    ['changes', () => codex.changes()],
    ['snapshots', () => codex.snapshots()],
    ['graph', () => codex.graph()],
    ['security', () => codex.security()],
    ['policy', () => codex.policy()],
    ['agentRuns', () => codex.agentRuns()],
    ['audit', () => codex.audit()],
    ['summary', () => codex.registry.summary()],
    ['health', () => codex.registry.health()],
    ['features', () => codex.registry.features()],
    ['tools', () => codex.registry.tools()],
    ['agents', () => codex.registry.agents()],
  ]

  const settled = await Promise.allSettled(jobs.map(([, fn]) => fn()))
  settled.forEach((item, index) => {
    const key = jobs[index][0]
    if (item.status !== 'fulfilled') return
    if (key === 'overview') overview.value = item.value
    if (key === 'context') context.value = item.value
    if (key === 'projects') projects.value = item.value
    if (key === 'files') files.value = item.value
    if (key === 'apis') apis.value = item.value
    if (key === 'protected') protectedRows.value = item.value
    if (key === 'changes') changes.value = item.value
    if (key === 'snapshots') snapshots.value = item.value
    if (key === 'graph') graph.value = item.value
    if (key === 'security') security.value = item.value
    if (key === 'policy') policy.value = item.value
    if (key === 'agentRuns') agentRuns.value = item.value
    if (key === 'audit') auditRows.value = item.value
  })

  try {
    await store.loadCapabilities()
  } catch (error) {
    notifyError(error, 'Could not load the capability registry.')
  } finally {
    loading.value = false
  }
}

async function bootstrap() {
  await runAction(() => store.bootstrapCapabilities(), '350 Codex capabilities bootstrapped.')
  await loadCoreData()
}

async function validate() {
  validating.value = true
  try {
    result.value = await codex.registry.validate()
    await store.loadCapabilities()
    notifySuccess('Capability validation completed.')
  } catch (error) {
    notifyError(error, 'Capability validation failed.')
  } finally {
    validating.value = false
  }
}

async function analyzeProject() {
  analyzing.value = true
  activePanel.value = 'analysis'
  try {
    const [scan, health, graphData, securityData] = await Promise.allSettled([
      codex.scan(),
      codex.registry.health(),
      codex.graph(),
      codex.security(),
    ])
    result.value = scan.status === 'fulfilled' ? scan.value : null
    if (health.status === 'fulfilled') {
      // The Pinia store remains the source of truth when its loader is available.
      await store.loadCapabilities()
    }
    if (graphData.status === 'fulfilled') graph.value = graphData.value
    if (securityData.status === 'fulfilled') security.value = securityData.value
    notifySuccess('Project analysis completed.')
  } catch (error) {
    notifyError(error, 'Project analysis failed.')
  } finally {
    analyzing.value = false
  }
}

async function openFile(file) {
  selectedFile.value = file
  fileContent.value = ''
  const id = file?.id ?? file?.pk ?? file?.path
  if (!id) return
  await runAction(async () => {
    const response = await codex.fileContent(id)
    fileContent.value = response?.content ?? response?.text ?? response?.data ?? ''
    return response
  }, 'File loaded.')
}

function toggleFile(file) {
  const id = file?.id ?? file?.pk ?? file?.path
  const exists = selectedFiles.value.some((item) => (item.id ?? item.pk ?? item.path) === id)
  selectedFiles.value = exists
    ? selectedFiles.value.filter((item) => (item.id ?? item.pk ?? item.path) !== id)
    : [...selectedFiles.value, file]
}

async function analyzeSelectedFiles() {
  if (!selectedFiles.value.length) {
    notifyError(null, 'Select at least one file first.')
    return
  }
  const paths = selectedFiles.value.map((item) => item.path || item.name || item.id).join('\n')
  activePanel.value = 'chat'
  await sendChat(
    `Analyze these selected project files together:\n${paths}\n\nExplain their responsibilities, relationships, APIs, data flow, dependencies, risks, and whether they can be changed independently. Use the actual project context.`,
  )
}

async function sendChat(message = chatInput.value) {
  const text = String(message || '').trim()
  if (!text) return
  chatMessages.value.push({ role: 'user', content: text })
  chatInput.value = ''
  busy.value = true
  try {
    const response = await codex.askOpenAI(text)
    chatMessages.value.push({
      role: 'assistant',
      content:
        response?.answer ||
        response?.message ||
        response?.content ||
        JSON.stringify(response, null, 2),
    })
  } catch (error) {
    notifyError(error, 'Codex could not answer this request.')
    chatMessages.value.push({
      role: 'assistant',
      content: `Request failed: ${error?.message || 'Unknown error'}`,
      error: true,
    })
  } finally {
    busy.value = false
  }
}

async function runTool(item) {
  selected.value = item
  await runAction(
    () => codex.registry.executeTool(item.key, {}),
    `Tool ${item.name || item.key} executed.`,
  )
  showResult.value = true
}

async function runAgent(item) {
  selected.value = item
  await runAction(
    () =>
      codex.registry.executeAgent(item.key, {
        request: 'Run a safe capability contract smoke test against the current project context.',
      }),
    `Agent ${item.name || item.key} executed.`,
  )
  showResult.value = true
}

async function rebuildGraph() {
  await runAction(async () => {
    graph.value = await codex.rebuildGraph()
    return graph.value
  }, 'Project graph rebuilt.')
}

async function runSecurityScan() {
  await runAction(async () => {
    security.value = await codex.runSecurityScan()
    return security.value
  }, 'Security scan completed.')
}

async function runDuplicates() {
  await runAction(() => codex.duplicates(), 'Duplicate-code analysis completed.')
}

async function explainProject() {
  activePanel.value = 'chat'
  await sendChat(
    'Explain the current SO_IAM_OS architecture and how the Codex application connects the Vue frontend to the Django backend.',
  )
}

async function generatePrompt() {
  const selectedContext = selectedFiles.value.map((f) => f.path || f.name || f.id).join('\n')
  const prompt = `You are an expert full-stack engineer working on SO_IAM_OS.

CONTEXT
Project: ${projectName.value}
Current Stage: ${currentStage.value}
Selected Files:
${selectedContext || 'Use the relevant project files discovered by Codex.'}

GOAL
${chatInput.value || 'Implement the requested Codex change safely and integrate it with the existing Django backend and Vue 3 frontend.'}

CONSTRAINTS
- Work only on the Codex application.
- Preserve approved/protected/locked functionality.
- Reuse existing APIs, services, stores, and dependencies where possible.
- Do not delete or silently replace existing functionality.
- Keep Vue 3 + Pinia + PrimeVue + Axios compatibility.
- Keep Django/DRF contracts compatible.
- Validate frontend, backend, API, permissions, and regression behavior.

EXPECTED OUTPUT
1. Inspect the real project before changing anything.
2. Produce an impact analysis and change plan.
3. Identify protected elements.
4. Implement the smallest safe change.
5. Test the backend and frontend integration.
6. Report files changed, APIs touched, tests executed, risks, and acceptance criteria.`
  generatedPrompt.value = prompt
  showPrompt.value = true
}

async function planChange() {
  const request = chatInput.value.trim()
  if (!request) {
    notifyError(null, 'Describe the change first.')
    return
  }
  await runAction(
    () =>
      codex.planChange({
        request,
        files: selectedFiles.value.map((f) => f.path || f.name || f.id),
      }),
    'Change plan generated.',
  )
  activePanel.value = 'analysis'
}

async function runTestPlan() {
  await runAction(
    () =>
      codex.testPlan(
        chatInput.value || 'Run a comprehensive Codex integration and regression test plan.',
      ),
    'Test plan generated.',
  )
}

async function runCommand() {
  if (!command.value.trim()) return
  commandResult.value = await runAction(
    () => codex.runCommand(command.value.trim()),
    'Command executed.',
  )
}

onMounted(loadCoreData)
</script>

<template>
  <div class="codex-workbench">
    <div class="codex-shell">
      <!-- SIDEBAR -->
      <aside class="codex-sidebar">
        <div class="codex-brand">
          <div class="codex-brand-mark">
            <i class="pi pi-sparkles" />
          </div>
          <div>
            <strong>CODEX</strong>
            <span>Engineering OS</span>
          </div>
        </div>

        <div class="codex-project-mini">
          <div class="project-dot" />
          <div class="project-mini-copy">
            <strong>{{ projectName }}</strong>
            <span>{{ currentStage }}</span>
          </div>
          <Tag value="LIVE" severity="success" />
        </div>

        <nav class="codex-nav">
          <button
            v-for="item in navItems"
            :key="item.key"
            class="codex-nav-item"
            :class="{ active: activePanel === item.key }"
            type="button"
            @click="activePanel = item.key"
          >
            <i :class="item.icon" />
            <span>{{ item.label }}</span>
          </button>
        </nav>

        <div class="codex-sidebar-section">
          <div class="sidebar-label">SYSTEM STATUS</div>
          <div class="status-row">
            <span><i class="pi pi-circle-fill status-online" /> Django API</span>
            <Tag value="ONLINE" severity="success" />
          </div>
          <div class="status-row">
            <span><i class="pi pi-circle-fill status-online" /> Codex Registry</span>
            <Tag :value="`${totalCapabilities}/350`" severity="info" />
          </div>
          <div class="status-row">
            <span><i class="pi pi-circle-fill status-online" /> Project Brain</span>
            <Tag value="READY" severity="success" />
          </div>
        </div>

        <div class="codex-sidebar-footer">
          <Button
            label="Analyze Project"
            icon="pi pi-bolt"
            class="w-full"
            :loading="analyzing"
            @click="analyzeProject"
          />
        </div>
      </aside>

      <!-- MAIN -->
      <main class="codex-main">
        <header class="codex-topbar">
          <div>
            <div class="breadcrumb">
              <span>SO_IAM_OS</span>
              <i class="pi pi-angle-right" />
              <strong>Codex</strong>
            </div>
            <h1>
              {{ navItems.find((item) => item.key === activePanel)?.label || 'Codex Workbench' }}
            </h1>
          </div>

          <div class="topbar-actions">
            <span class="api-indicator">
              <i class="pi pi-circle-fill" />
              Django API Connected
            </span>
            <Button icon="pi pi-refresh" text rounded :loading="loading" @click="loadCoreData" />
            <Button
              icon="pi pi-sparkles"
              label="Generate Prompt"
              severity="secondary"
              @click="generatePrompt"
            />
          </div>
        </header>

        <div v-if="errorMessage" class="codex-alert">
          <Message severity="error" :closable="true" @close="errorMessage = ''">
            {{ errorMessage }}
          </Message>
        </div>
        <div v-if="successMessage" class="codex-alert">
          <Message severity="success" :closable="true" @close="successMessage = ''">
            {{ successMessage }}
          </Message>
        </div>

        <!-- WORKSPACE -->
        <section v-if="activePanel === 'workspace'" class="codex-content">
          <div class="hero-grid">
            <Card class="hero-card">
              <template #content>
                <div class="hero-eyebrow">
                  <Tag value="PROJECT-AWARE AI" severity="info" />
                  <span>Connected to Django + DRF</span>
                </div>
                <h2>Your Engineering Command Center</h2>
                <p>
                  Understand, analyze, build, debug, test and protect SO_IAM_OS from one
                  project-aware development workspace.
                </p>
                <div class="hero-actions">
                  <Button
                    label="Analyze Project"
                    icon="pi pi-bolt"
                    :loading="analyzing"
                    @click="analyzeProject"
                  />
                  <Button
                    label="Open AI Chat"
                    icon="pi pi-comments"
                    outlined
                    @click="activePanel = 'chat'"
                  />
                  <Button
                    label="Project Explorer"
                    icon="pi pi-folder-open"
                    text
                    @click="activePanel = 'files'"
                  />
                </div>
              </template>
            </Card>

            <Card class="health-card">
              <template #title>Project Health</template>
              <template #content>
                <div class="health-score">
                  <strong>{{ capabilityHealth.overall ?? overview?.health_score ?? '—' }}</strong>
                  <span>overall health</span>
                </div>
                <div v-for="(score, key) in healthScores" :key="key" class="health-line">
                  <span>{{ String(key).replaceAll('_', ' ') }}</span>
                  <strong>{{ score }}%</strong>
                  <ProgressBar :value="Number(score)" :showValue="false" />
                </div>
              </template>
            </Card>
          </div>

          <div class="metric-grid">
            <Card class="metric-card">
              <template #content>
                <span>Features</span>
                <strong>{{ capabilitySummary.features || 0 }}</strong>
                <small>Registered capabilities</small>
              </template>
            </Card>
            <Card class="metric-card">
              <template #content>
                <span>Tools</span>
                <strong>{{ capabilitySummary.tools || 0 }}</strong>
                <small>Reusable execution tools</small>
              </template>
            </Card>
            <Card class="metric-card">
              <template #content>
                <span>Agents</span>
                <strong>{{ capabilitySummary.agents || 0 }}</strong>
                <small>Specialized AI agents</small>
              </template>
            </Card>
            <Card class="metric-card">
              <template #content>
                <span>Protected</span>
                <strong>{{ protectedRows.length }}</strong>
                <small>Governed project elements</small>
              </template>
            </Card>
          </div>

          <div class="workspace-grid">
            <Card>
              <template #title>Quick Actions</template>
              <template #content>
                <div class="quick-actions">
                  <Button
                    label="Scan Project"
                    icon="pi pi-search"
                    outlined
                    @click="runAction(() => codex.scan(), 'Project scan completed.')"
                  />
                  <Button
                    label="Rebuild Graph"
                    icon="pi pi-share-alt"
                    outlined
                    @click="rebuildGraph"
                  />
                  <Button
                    label="Security Scan"
                    icon="pi pi-shield"
                    outlined
                    @click="runSecurityScan"
                  />
                  <Button
                    label="Find Duplicates"
                    icon="pi pi-copy"
                    outlined
                    @click="runDuplicates"
                  />
                  <Button
                    label="Explain Architecture"
                    icon="pi pi-question-circle"
                    outlined
                    @click="explainProject"
                  />
                  <Button
                    label="Test Plan"
                    icon="pi pi-check-square"
                    outlined
                    @click="runTestPlan"
                  />
                </div>
              </template>
            </Card>

            <Card>
              <template #title>Codex Registry</template>
              <template #content>
                <div class="registry-overview">
                  <div>
                    <i class="pi pi-star-fill" /><span>Features</span
                    ><strong>{{ capabilitySummary.features || 0 }}</strong>
                  </div>
                  <div>
                    <i class="pi pi-wrench" /><span>Tools</span
                    ><strong>{{ capabilitySummary.tools || 0 }}</strong>
                  </div>
                  <div>
                    <i class="pi pi-microchip-ai" /><span>Agents</span
                    ><strong>{{ capabilitySummary.agents || 0 }}</strong>
                  </div>
                </div>
                <Button
                  label="Open Registry"
                  icon="pi pi-arrow-right"
                  text
                  @click="activePanel = 'registry'"
                />
              </template>
            </Card>
          </div>
        </section>

        <!-- FILE EXPLORER -->
        <section v-else-if="activePanel === 'files'" class="codex-content">
          <div class="section-toolbar">
            <div>
              <h2>Project Explorer</h2>
              <span>{{ files.length }} indexed project files</span>
            </div>
            <div class="toolbar-actions">
              <InputText v-model="fileQuery" placeholder="Search files, paths, symbols..." />
              <Button
                label="Analyze Selected"
                icon="pi pi-sparkles"
                :disabled="!selectedFiles.length"
                @click="analyzeSelectedFiles"
              />
            </div>
          </div>

          <div class="selection-strip" v-if="selectedFiles.length">
            <i class="pi pi-check-circle" />
            {{ selectedFiles.length }} files selected
            <Button
              label="Ask AI About Selected Files"
              size="small"
              text
              @click="analyzeSelectedFiles"
            />
          </div>

          <Splitter class="file-workbench" style="height: 680px">
            <SplitterPanel :size="38" :minSize="25">
              <div class="file-list">
                <div v-if="loading" class="file-skeleton">
                  <Skeleton v-for="i in 8" :key="i" height="42px" />
                </div>
                <div v-else-if="!filteredFiles.length" class="empty-state">
                  <i class="pi pi-folder-open" />
                  <strong>No files found</strong>
                  <span>Run a project scan to build the file index.</span>
                </div>
                <div
                  v-for="file in filteredFiles"
                  v-else
                  :key="file.id || file.path || file.name"
                  class="file-row"
                  :class="{ selected: selectedFile === file }"
                >
                  <button type="button" class="file-select" @click.stop="toggleFile(file)">
                    <i
                      :class="
                        selectedFiles.some(
                          (x) => (x.id ?? x.pk ?? x.path) === (file.id ?? file.pk ?? file.path),
                        )
                          ? 'pi pi-check-square'
                          : 'pi pi-stop'
                      "
                    />
                  </button>
                  <button type="button" class="file-main" @click="openFile(file)">
                    <i class="pi pi-file-code" />
                    <span>
                      <strong>{{ file.name || file.path }}</strong>
                      <small>{{ file.path || file.type || 'Project file' }}</small>
                    </span>
                  </button>
                </div>
              </div>
            </SplitterPanel>

            <SplitterPanel :size="62" :minSize="40">
              <div class="file-viewer">
                <div v-if="selectedFile" class="viewer-header">
                  <div>
                    <i class="pi pi-file-code" />
                    <strong>{{ selectedFile.name || selectedFile.path }}</strong>
                    <span>{{ selectedFile.path }}</span>
                  </div>
                  <div>
                    <Tag :value="selectedFile.language || selectedFile.type || 'source'" />
                    <Button
                      icon="pi pi-copy"
                      text
                      rounded
                      title="Copy file content"
                      @click="navigator.clipboard?.writeText(fileContent)"
                    />
                  </div>
                </div>
                <ScrollPanel v-if="selectedFile" class="code-scroll">
                  <pre
                    class="code-viewer"
                  ><code>{{ fileContent || 'Loading file content…' }}</code></pre>
                </ScrollPanel>
                <div v-else class="empty-viewer">
                  <i class="pi pi-file" />
                  <h3>Select a file</h3>
                  <p>Open a file to inspect its source, metadata and project relationships.</p>
                </div>
              </div>
            </SplitterPanel>
          </Splitter>
        </section>

        <!-- ANALYSIS -->
        <section v-else-if="activePanel === 'analysis'" class="codex-content">
          <div class="section-toolbar">
            <div>
              <h2>Project Intelligence</h2>
              <span>Actual project data from Django Codex services</span>
            </div>
            <div class="toolbar-actions">
              <Button
                label="Full Analysis"
                icon="pi pi-bolt"
                :loading="analyzing"
                @click="analyzeProject"
              />
              <Button
                label="Rebuild Graph"
                icon="pi pi-share-alt"
                outlined
                :loading="busy"
                @click="rebuildGraph"
              />
            </div>
          </div>

          <div class="analysis-grid">
            <Card>
              <template #title>Architecture</template>
              <template #content>
                <div class="analysis-stat">
                  <strong>{{ healthScores.architecture }}%</strong>
                  <ProgressBar :value="Number(healthScores.architecture)" :showValue="false" />
                </div>
                <div class="analysis-list">
                  <span
                    >Applications <b>{{ overview?.apps_count ?? projects.length }}</b></span
                  >
                  <span
                    >Files <b>{{ files.length }}</b></span
                  >
                  <span
                    >APIs <b>{{ apis.length }}</b></span
                  >
                  <span
                    >Protected <b>{{ protectedRows.length }}</b></span
                  >
                </div>
              </template>
            </Card>

            <Card>
              <template #title>Security</template>
              <template #content>
                <div v-if="security" class="analysis-list">
                  <span
                    >Score <b>{{ security.score ?? '—' }}</b></span
                  >
                  <span
                    >Findings
                    <b>{{ security.findings?.length ?? security.issues?.length ?? 0 }}</b></span
                  >
                  <span>Prompt Injection <Tag value="Protected" severity="success" /></span>
                </div>
                <Button
                  label="Run Security Scan"
                  icon="pi pi-shield"
                  text
                  @click="runSecurityScan"
                />
              </template>
            </Card>

            <Card class="analysis-wide">
              <template #title>Project Knowledge Graph</template>
              <template #content>
                <div class="graph-preview">
                  <div class="graph-node">Frontend</div>
                  <i class="pi pi-arrow-right" />
                  <div class="graph-node">API</div>
                  <i class="pi pi-arrow-right" />
                  <div class="graph-node">Django</div>
                  <i class="pi pi-arrow-right" />
                  <div class="graph-node">Database</div>
                </div>
                <pre v-if="graph" class="compact-json">{{ JSON.stringify(graph, null, 2) }}</pre>
              </template>
            </Card>
          </div>

          <Card class="data-card">
            <template #title>Recent Changes</template>
            <template #content>
              <DataTable :value="changes" paginator :rows="8" stripedRows responsiveLayout="scroll">
                <Column field="id" header="#" />
                <Column field="title" header="Change" />
                <Column field="status" header="Status">
                  <template #body="slotProps">
                    <Tag :value="slotProps.data.status || 'RECORDED'" severity="info" />
                  </template>
                </Column>
                <Column field="created_at" header="Created" />
              </DataTable>
            </template>
          </Card>
        </section>

        <!-- CHAT -->
        <section v-else-if="activePanel === 'chat'" class="codex-content chat-page">
          <div class="section-toolbar">
            <div>
              <h2>Codex Chat</h2>
              <span>Project-aware AI connected to the Codex backend</span>
            </div>
            <Tag value="PROJECT CONTEXT ACTIVE" severity="success" />
          </div>

          <Card class="chat-card">
            <template #content>
              <ScrollPanel class="chat-scroll">
                <div v-if="!chatMessages.length" class="chat-empty">
                  <div class="chat-orb"><i class="pi pi-sparkles" /></div>
                  <h2>Ask Codex about your project</h2>
                  <p>
                    Codex can inspect architecture, files, APIs, errors, dependencies and protected
                    elements.
                  </p>
                  <div class="chat-suggestions">
                    <Button
                      label="Explain the architecture"
                      outlined
                      @click="
                        sendChat(
                          'Explain the current SO_IAM_OS architecture and Codex integration.',
                        )
                      "
                    />
                    <Button
                      label="Find risky dependencies"
                      outlined
                      @click="
                        sendChat(
                          'Analyze dependencies and identify risky or unnecessary dependencies.',
                        )
                      "
                    />
                    <Button
                      label="What should I do next?"
                      outlined
                      @click="
                        sendChat(
                          'Determine the best next action for the project based on current state, errors, dependencies and incomplete work.',
                        )
                      "
                    />
                  </div>
                </div>

                <div
                  v-for="(message, index) in chatMessages"
                  :key="index"
                  class="chat-message"
                  :class="message.role"
                >
                  <div class="message-avatar">
                    <i :class="message.role === 'user' ? 'pi pi-user' : 'pi pi-sparkles'" />
                  </div>
                  <div class="message-body">
                    <small>{{ message.role === 'user' ? 'You' : 'Codex AI' }}</small>
                    <pre>{{ message.content }}</pre>
                  </div>
                </div>
              </ScrollPanel>

              <div class="chat-composer">
                <Textarea
                  v-model="chatInput"
                  autoResize
                  rows="3"
                  placeholder="Ask Codex to understand, plan, debug, modify or test the project…"
                  @keydown.ctrl.enter="sendChat()"
                />
                <div class="composer-actions">
                  <Button label="Plan Change" icon="pi pi-list-check" text @click="planChange" />
                  <Button label="Generate Prompt" icon="pi pi-copy" text @click="generatePrompt" />
                  <Button
                    label="Send"
                    icon="pi pi-send"
                    :loading="busy"
                    :disabled="!chatInput.trim()"
                    @click="sendChat()"
                  />
                </div>
              </div>
            </template>
          </Card>
        </section>

        <!-- PIPELINE -->
        <section v-else-if="activePanel === 'pipeline'" class="codex-content">
          <div class="section-toolbar">
            <div>
              <h2>Development Pipeline</h2>
              <span>Configurable project lifecycle with dependency-aware stages</span>
            </div>
            <Tag :value="currentStage" severity="info" />
          </div>

          <Card class="pipeline-card">
            <template #content>
              <div class="pipeline-track">
                <div
                  v-for="step in pipeline"
                  :key="step.id"
                  class="pipeline-step"
                  :class="step.status.toLowerCase()"
                >
                  <div class="pipeline-number">{{ step.id }}</div>
                  <div class="pipeline-copy">
                    <strong>{{ step.name }}</strong>
                    <span>{{ step.status }}</span>
                  </div>
                  <i
                    :class="
                      step.status === 'COMPLETED'
                        ? 'pi pi-check-circle'
                        : step.status === 'IN_PROGRESS'
                          ? 'pi pi-play-circle'
                          : 'pi pi-circle'
                    "
                  />
                </div>
              </div>
            </template>
          </Card>

          <div class="workspace-grid">
            <Card>
              <template #title>Next Best Action</template>
              <template #content>
                <div class="next-action">
                  <i class="pi pi-arrow-right" />
                  <div>
                    <strong>Connect, validate and protect the current Codex workbench</strong>
                    <span
                      >Run integration tests, review the registry, then approve/protect stable
                      functionality.</span
                    >
                  </div>
                </div>
                <Button label="Generate Test Plan" icon="pi pi-check-square" @click="runTestPlan" />
              </template>
            </Card>
            <Card>
              <template #title>Project Context</template>
              <template #content>
                <pre class="compact-json">{{
                  JSON.stringify(
                    context?.development_pipeline || context?.current_stage || {},
                    null,
                    2,
                  )
                }}</pre>
              </template>
            </Card>
          </div>
        </section>

        <!-- REGISTRY -->
        <section v-else-if="activePanel === 'registry'" class="codex-content">
          <Card class="registry-hero">
            <template #content>
              <div class="registry-heading">
                <div>
                  <div class="eyebrow">CODEX CAPABILITY SYSTEM</div>
                  <h2>350 Integrated Capabilities</h2>
                  <p>150 Features · 100 Tools · 100 Agents</p>
                </div>
                <div class="registry-actions">
                  <Button
                    label="Bootstrap"
                    icon="pi pi-refresh"
                    outlined
                    :loading="busy"
                    @click="bootstrap"
                  />
                  <Button
                    label="Validate All"
                    icon="pi pi-check-circle"
                    :loading="validating"
                    @click="validate"
                  />
                </div>
              </div>
            </template>
          </Card>

          <div class="registry-tabs">
            <Button
              :label="`150 Features`"
              :severity="registryTab === 'features' ? 'primary' : 'secondary'"
              :outlined="registryTab !== 'features'"
              @click="registryTab = 'features'"
            />
            <Button
              :label="`100 Tools`"
              :severity="registryTab === 'tools' ? 'primary' : 'secondary'"
              :outlined="registryTab !== 'tools'"
              @click="registryTab = 'tools'"
            />
            <Button
              :label="`100 Agents`"
              :severity="registryTab === 'agents' ? 'primary' : 'secondary'"
              :outlined="registryTab !== 'agents'"
              @click="registryTab = 'agents'"
            />
            <InputText v-model="query" placeholder="Search capability…" class="registry-search" />
          </div>

          <DataTable
            v-if="registryTab === 'features'"
            :value="features"
            paginator
            :rows="15"
            stripedRows
            responsiveLayout="scroll"
            class="data-card"
          >
            <Column field="id" header="#" style="width: 80px" />
            <Column field="name" header="Feature" sortable />
            <Column field="category" header="Category" sortable />
            <Column field="status" header="Status">
              <template #body="slotProps">
                <Tag :value="slotProps.data.status || 'IMPLEMENTED'" severity="success" />
              </template>
            </Column>
            <Column field="protection_level" header="Protection">
              <template #body="slotProps">
                <Tag
                  :value="slotProps.data.protection_level || 'NORMAL'"
                  :severity="slotProps.data.protection_level === 'LOCKED' ? 'danger' : 'info'"
                />
              </template>
            </Column>
          </DataTable>

          <DataTable
            v-else-if="registryTab === 'tools'"
            :value="tools"
            paginator
            :rows="15"
            stripedRows
            responsiveLayout="scroll"
            class="data-card"
          >
            <Column field="key" header="Key" sortable />
            <Column field="name" header="Tool" sortable />
            <Column field="category" header="Category" sortable />
            <Column field="risk" header="Risk" />
            <Column header="Execution" style="width: 140px">
              <template #body="slotProps">
                <Button
                  label="Run"
                  icon="pi pi-play"
                  size="small"
                  text
                  :loading="busy && selected === slotProps.data"
                  @click="runTool(slotProps.data)"
                />
              </template>
            </Column>
          </DataTable>

          <DataTable
            v-else
            :value="agents"
            paginator
            :rows="15"
            stripedRows
            responsiveLayout="scroll"
            class="data-card"
          >
            <Column field="key" header="Key" sortable />
            <Column field="name" header="Agent" sortable />
            <Column field="category" header="Category" sortable />
            <Column field="risk" header="Risk" />
            <Column header="Tools">
              <template #body="slotProps">{{ slotProps.data.tools?.length || 0 }}</template>
            </Column>
            <Column header="Execution" style="width: 140px">
              <template #body="slotProps">
                <Button
                  label="Run"
                  icon="pi pi-play"
                  size="small"
                  text
                  :loading="busy && selected === slotProps.data"
                  @click="runAgent(slotProps.data)"
                />
              </template>
            </Column>
          </DataTable>
        </section>

        <!-- AGENTS & TOOLS -->
        <section v-else-if="activePanel === 'agents'" class="codex-content">
          <div class="section-toolbar">
            <div>
              <h2>Agents & Tools</h2>
              <span>Specialized execution layer governed by Codex permissions</span>
            </div>
            <Button
              label="Open Full Registry"
              icon="pi pi-list"
              outlined
              @click="activePanel = 'registry'"
            />
          </div>

          <div class="agent-grid">
            <Card v-for="agent in agents.slice(0, 12)" :key="agent.key" class="agent-card">
              <template #content>
                <div class="agent-icon"><i class="pi pi-microchip-ai" /></div>
                <Tag :value="agent.category || 'GENERAL'" severity="info" />
                <h3>{{ agent.name }}</h3>
                <p>
                  {{ agent.purpose || agent.description || 'Specialized Codex project agent.' }}
                </p>
                <div class="agent-meta">
                  <span
                    >Risk <b>{{ agent.risk || 'LOW' }}</b></span
                  >
                  <span
                    >Tools <b>{{ agent.tools?.length || 0 }}</b></span
                  >
                </div>
                <Button label="Run Smoke Test" icon="pi pi-play" text @click="runAgent(agent)" />
              </template>
            </Card>
          </div>
        </section>

        <!-- GOVERNANCE -->
        <section v-else-if="activePanel === 'governance'" class="codex-content">
          <div class="section-toolbar">
            <div>
              <h2>Governance & Protection</h2>
              <span>Protected project elements and execution permissions</span>
            </div>
          </div>

          <div class="workspace-grid">
            <Card>
              <template #title>Permissions</template>
              <template #content>
                <div class="permission-list">
                  <div v-for="(value, key) in policy?.permissions || {}" :key="key">
                    <span>{{ key }}</span>
                    <Tag
                      :value="String(value).toUpperCase()"
                      :severity="
                        value === 'ALLOW' ? 'success' : value === 'DENY' ? 'danger' : 'warning'
                      "
                    />
                  </div>
                </div>
              </template>
            </Card>

            <Card>
              <template #title>Protected Elements</template>
              <template #content>
                <div class="protected-summary">
                  <strong>{{ protectedRows.length }}</strong>
                  <span>registered protected elements</span>
                </div>
                <DataTable :value="protectedRows.slice(0, 10)" stripedRows>
                  <Column field="name" header="Element" />
                  <Column field="type" header="Type" />
                  <Column field="protection_level" header="Protection" />
                </DataTable>
              </template>
            </Card>
          </div>

          <Card class="data-card">
            <template #title>Audit Trail</template>
            <template #content>
              <DataTable
                :value="auditRows"
                paginator
                :rows="10"
                stripedRows
                responsiveLayout="scroll"
              >
                <Column field="action" header="Action" />
                <Column field="actor" header="Actor" />
                <Column field="status" header="Status" />
                <Column field="created_at" header="Created" />
              </DataTable>
            </template>
          </Card>

          <Card class="command-card">
            <template #title>Command Gateway</template>
            <template #content>
              <div class="command-row">
                <InputText v-model="command" placeholder="Command key…" />
                <Button
                  label="Run Command"
                  icon="pi pi-terminal"
                  :disabled="!command.trim()"
                  @click="runCommand"
                />
              </div>
              <pre v-if="commandResult" class="compact-json">{{
                JSON.stringify(commandResult, null, 2)
              }}</pre>
            </template>
          </Card>
        </section>
      </main>
    </div>

    <!-- EXECUTION RESULT -->
    <Dialog
      v-model:visible="showResult"
      modal
      header="Codex Execution Result"
      :style="{ width: '70rem', maxWidth: '92vw' }"
    >
      <pre class="dialog-json">{{ JSON.stringify(result, null, 2) }}</pre>
    </Dialog>

    <!-- PROMPT GENERATOR -->
    <Dialog
      v-model:visible="showPrompt"
      modal
      header="Generated Codex Prompt"
      :style="{ width: '70rem', maxWidth: '92vw' }"
    >
      <div class="prompt-dialog">
        <div class="prompt-toolbar">
          <SelectButton
            v-model="promptType"
            :options="['development', 'debugging', 'architecture']"
          />
          <Button
            label="Copy Prompt"
            icon="pi pi-copy"
            @click="
              navigator.clipboard?.writeText(generatedPrompt)
              notifySuccess('Prompt copied.')
            "
          />
        </div>
        <Textarea v-model="generatedPrompt" rows="24" autoResize class="prompt-editor" />
      </div>
    </Dialog>
  </div>
</template>

<style src="@/assets/scss/Codex/_Codex.scss"></style>
