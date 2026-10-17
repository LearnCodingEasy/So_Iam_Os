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
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'

import { useCodexStore } from '@/stores/codex'
import CodexCapabilities from './CodexCapabilities.vue'
import codex from '@/services/codex'
import CodexBuildWorkspace from './CodexBuildWorkspace.vue'

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
const workflow = ref({ steps: [], completed: 0, total: 0 })
const protectedItems = ref([])
const localAIJobs = ref([])
const infoDialog = ref({ visible: false, title: '', content: '' })
const localPath = ref('')
const promptCopyState = ref('')

const navItems = [
  { key: 'workspace', label: 'Workspace', icon: 'pi pi-home' },
  { key: 'files', label: 'Project Explorer', icon: 'pi pi-folder-open' },
  { key: 'analysis', label: 'Project Analysis', icon: 'pi pi-chart-line' },
  { key: 'chat', label: 'Codex Chat', icon: 'pi pi-comments' },
  { key: 'build', label: 'Build Workspace', icon: 'pi pi-sitemap' },
  { key: 'pipeline', label: 'Development Pipeline', icon: 'pi pi-share-alt' },
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

const highlightedCode = computed(() => {
  const source = String(fileContent.value || '')
  const escaped = source
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
  const language = String(selectedFile.value?.kind || selectedFile.value?.path || '').toLowerCase()
  if (!source) return ''
  let html = escaped
  html = html.replace(/(&quot;.*?&quot;|".*?"|'.*?')/g, '<span class="codex-token-string">$1</span>')
  if (/python|\.py/.test(language)) {
    html = html.replace(/\b(def|class|from|import|return|if|elif|else|for|while|try|except|with|as|in|is|None|True|False|async|await)\b/g, '<span class="codex-token-keyword">$1</span>')
  } else if (/vue|javascript|\.js|typescript|\.ts/.test(language)) {
    html = html.replace(/\b(const|let|var|function|return|if|else|for|while|import|from|export|default|async|await|new|class|extends|true|false|null|undefined)\b/g, '<span class="codex-token-keyword">$1</span>')
  } else if (/scss|css/.test(language)) {
    html = html.replace(/([\w-]+)(?=\s*:)/g, '<span class="codex-token-property">$1</span>')
  } else if (/json/.test(language)) {
    html = html.replace(/(&quot;[^&]+?&quot;)(?=\s*:)/g, '<span class="codex-token-property">$1</span>')
  } else if (/markdown|\.md/.test(language)) {
    html = html.replace(/^(#{1,6}\s.*)$/gm, '<span class="codex-token-heading">$1</span>')
  }
  return html.replace(/\b(\d+(?:\.\d+)?)\b/g, '<span class="codex-token-number">$1</span>')
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
  const paths = selectedFiles.value.map((item) => item.path || item.name || item.id)
  activePanel.value = 'chat'
  await sendChat(
    `Analyze these selected project files together. Explain their responsibilities, relationships, APIs, data flow, dependencies, risks, and whether they can be changed independently. Use the actual source contents and project context.`,
    paths,
  )
}

async function sendChat(message = chatInput.value, paths = []) {
  const text = String(message || '').trim()
  if (!text) return
  chatMessages.value.push({ role: 'user', content: text })
  chatInput.value = ''
  busy.value = true
  try {
    const response = await codex.askOpenAI(text, paths)
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
  try {
    const selectedContext = selectedFiles.value.map((f) => f.path || f.name || f.id)
    const response = await codex.generatePrompt(
      promptType.value,
      chatInput.value || 'Implement the requested Codex change safely.',
      selectedContext,
    )
    generatedPrompt.value = response?.prompt || ''
    showPrompt.value = true
  } catch (error) {
    notifyError(error, 'Could not generate the Codex prompt.')
  }
}

async function copyPrompt() {
  if (!generatedPrompt.value) return
  await navigator.clipboard.writeText(generatedPrompt.value)
  promptCopyState.value = 'Copied'
  window.setTimeout(() => (promptCopyState.value = ''), 1800)
}

function showInfo(title, content) {
  infoDialog.value = { visible: true, title, content }
}

async function loadGovernance() {
  try {
    const [flow, protectedRows, jobs] = await Promise.all([
      codex.workflow(),
      codex.protectedItems(),
      codex.localAIJobs(),
    ])
    workflow.value = flow
    protectedItems.value = protectedRows
    localAIJobs.value = jobs
  } catch (error) {
    notifyError(error, 'Could not load Codex governance state.')
  }
}

async function generateManifest() {
  await runAction(() => codex.generateManifest(), 'PROJECT_CONTEXT.json and project_manifest.json generated.')
  await loadGovernance()
}

async function freezeSelectedFile() {
  if (!selectedFile.value?.path) {
    notifyError(null, 'Open a file first.')
    return
  }
  await runAction(
    () => codex.freezeProtectedItem({
      key: `file:${selectedFile.value.path}`,
      item_type: 'file',
      path: selectedFile.value.path,
      reason: 'Approved and frozen from Codex UI.',
    }),
    'File frozen in the Protected Registry.',
  )
  await loadGovernance()
}

async function requestLocalSummary() {
  if (!selectedFile.value?.path) {
    notifyError(null, 'Open a file first.')
    return
  }
  await runAction(
    () => codex.createLocalAIJob('summarize', { path: selectedFile.value.path }),
    'Local AI summary job queued in the background.',
  )
  await loadGovernance()
}

async function openLocalFile() {
  if (!selectedFile.value?.path) return
  const response = await runAction(() => codex.openLocalFile(selectedFile.value.path), 'Local file path resolved.')
  if (response?.file_url) {
    localPath.value = response.absolute_path || ''
    window.open(response.file_url, '_blank', 'noopener,noreferrer')
  }
}

async function analyzeModule() {
  const path = selectedFile.value?.path || 'backend_django/codex'
  await runAction(() => codex.architectureAnalyze(path), 'Architecture module analysis completed.')
  activePanel.value = 'analysis'
}

async function indexMarkdown() {
  const path = selectedFile.value?.kind === 'markdown' ? selectedFile.value.path : ''
  await runAction(() => codex.markdownNavigation(path), 'Markdown deep-navigation index generated.')
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

onMounted(async () => { await loadCoreData(); await loadGovernance() })
</script>

<template>
  <div
    class="codex-view flex h-screen w-full bg-[#0a0d14] text-slate-200 font-sans overflow-hidden"
  >

    <aside
      class="w-64 bg-[#0d111a] border-r border-slate-800/60 flex flex-col justify-between shrink-0"
    >
      <div>

        <div class="p-4 border-b border-slate-800/60 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <div
              class="w-7 h-7 rounded-lg bg-indigo-600/30 text-indigo-400 flex items-center justify-center font-bold text-sm"
            >
              <i class="pi pi-code"></i>
            </div>
            <div>
              <h2 class="text-sm font-semibold text-slate-100 leading-tight">Codex</h2>
              <p class="text-[10px] text-slate-500">Project Intelligence</p>
            </div>
          </div>
        </div>


        <nav class="p-2 space-y-1 text-xs">
          <button
            v-for="nav in navItems"
            :key="nav.key"
            @click="activePanel = nav.key"
            :class="[
              'w-full flex items-center justify-between px-3 py-2 rounded-md transition-colors text-left',
              activePanel === nav.key
                ? 'bg-indigo-600/20 text-indigo-400 font-medium'
                : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200',
            ]"
          >
            <span class="flex items-center gap-2.5">
              <i :class="[nav.icon, 'text-sm']"></i> {{ nav.label }}
            </span>
            <span
              v-if="nav.badge"
              class="bg-indigo-500/20 text-indigo-400 text-[9px] font-bold px-1.5 py-0.5 rounded"
            >
              {{ nav.badge }}
            </span>
          </button>
        </nav>
      </div>


      <div
        class="p-3 m-2 rounded-xl bg-gradient-to-br from-indigo-900/30 to-purple-900/20 border border-indigo-500/20 flex items-center gap-3"
      >
        <div class="text-2xl text-indigo-400">🚀</div>
        <div>
          <div class="text-xs font-semibold text-slate-200">{{ projectName }}</div>
          <div class="text-[10px] text-slate-400">Your AI-Powered Future</div>
          <div class="text-[9px] text-slate-500 mt-0.5">v1.0.0</div>
        </div>
      </div>
    </aside>


    <div class="flex-1 flex flex-col overflow-hidden">

      <header
        class="h-14 border-b border-slate-800/60 bg-[#0d111a] px-4 flex items-center justify-between shrink-0"
      >

        <div class="relative w-96">
          <i class="pi pi-search absolute left-3 top-2.5 text-slate-500 text-xs"></i>
          <input
            v-model="query"
            type="text"
            placeholder="Search files, features, APIs, or ask Codex..."
            class="w-full bg-[#131926] border border-slate-800 rounded-lg pl-9 pr-12 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-indigo-500/50"
          />
          <span
            class="absolute right-2.5 top-2 text-[10px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded border border-slate-700"
            >Ctrl + K</span
          >
        </div>


        <div class="flex items-center gap-4 text-xs">
          <div class="flex items-center gap-1.5 text-emerald-400 text-[11px]">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Backend
            Connected
          </div>
          <div class="flex items-center gap-1.5 text-sky-400 text-[11px]">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span> Frontend Connected
          </div>
          <div class="flex items-center gap-1.5 text-indigo-400 text-[11px]">
            <span class="w-2 h-2 rounded-full bg-indigo-400"></span> Database Connected
          </div>

          <div class="h-4 w-[1px] bg-slate-800"></div>

          <button class="text-slate-400 hover:text-slate-200"><i class="pi pi-bell"></i></button>
          <button class="text-slate-400 hover:text-slate-200"><i class="pi pi-cog"></i></button>

          <div class="flex items-center gap-2 pl-2">
            <div
              class="w-7 h-7 rounded-full bg-indigo-600 text-white font-bold flex items-center justify-center text-xs"
            >
              SA
            </div>
            <span class="text-xs font-medium text-slate-300">So_Iam</span>
          </div>
        </div>
      </header>


      <div
        class="px-6 py-3 border-b border-slate-800/60 bg-[#0a0d14] flex items-center justify-between shrink-0"
      >
        <div>
          <h1 class="text-base font-bold text-slate-100 flex items-center gap-2">
            Codex - Project Intelligence
          </h1>
          <p class="text-[11px] text-slate-500">Understand · Analyze · Plan · Build · Protect</p>
        </div>


        <Tabs v-model:value="activePanel" class="codex-tabs">
          <TabList>
            <Tab v-for="tab in navItems" :key="tab.key" :value="tab.key">
              <span class="flex items-center gap-1.5"><i :class="tab.icon"></i>{{ tab.label }}</span>
            </Tab>
          </TabList>
        </Tabs>
      </div>


      <div class="flex-1 flex overflow-hidden">

        <template v-if="activePanel === 'files' || activePanel === 'workspace'">

          <div class="w-64 bg-[#0d111a] border-r border-slate-800/60 flex flex-col shrink-0">
            <div class="p-3 border-b border-slate-800/60 flex items-center justify-between">
              <span class="text-xs font-semibold text-slate-300">Project Explorer</span>
              <i
                class="pi pi-filter text-xs text-slate-500 cursor-pointer hover:text-slate-300"
              ></i>
            </div>

            <div class="p-2">
              <input
                v-model="fileQuery"
                type="text"
                placeholder="Search files..."
                class="w-full bg-[#131926] border border-slate-800 rounded px-2.5 py-1 text-[11px] text-slate-300 focus:outline-none"
              />
            </div>


            <div class="flex-1 overflow-y-auto px-2 py-1 text-xs text-slate-400 space-y-1">
              <div v-if="loading" class="p-2 text-slate-500 text-center">Loading files...</div>
              <div v-else-if="!filteredFiles.length" class="p-2 text-slate-500 text-center">
                No files found
              </div>
              <div v-else>
                <div
                  v-for="file in filteredFiles"
                  :key="file.id || file.path"
                  @click="openFile(file)"
                  :class="[
                    'flex items-center justify-between py-1.5 px-2 rounded cursor-pointer text-xs font-mono transition-colors',
                    selectedFile?.path === file.path
                      ? 'bg-indigo-600/20 text-indigo-300 font-semibold'
                      : 'hover:bg-slate-800/40 text-slate-300',
                  ]"
                >
                  <span class="flex items-center gap-2 truncate">
                    <i class="pi pi-file text-pink-400"></i>
                    {{ file.name || file.path }}
                  </span>
                  <i
                    @click.stop="toggleFile(file)"
                    :class="[
                      'pi text-[10px]',
                      selectedFiles.some((f) => f.path === file.path)
                        ? 'pi-check-circle text-indigo-400'
                        : 'pi-circle text-slate-600',
                    ]"
                  ></i>
                </div>
              </div>
            </div>
          </div>


          <div class="flex-1 flex flex-col overflow-hidden bg-[#0a0d14]">
            <div
              class="bg-[#0d111a] border-b border-slate-800/60 flex items-center justify-between px-3 py-1.5"
            >
              <div
                class="flex items-center gap-2 bg-[#0a0d14] px-3 py-1 rounded-t-md border-t-2 border-indigo-500 text-xs text-slate-200 font-mono"
              >
                <i class="pi pi-file text-pink-400"></i>
                {{ selectedFile?.name || 'CodexView.scss' }}
                <i
                  class="pi pi-times text-[10px] text-slate-500 hover:text-slate-300 cursor-pointer ml-1"
                  @click="selectedFile = null"
                ></i>
              </div>
            </div>

            <div class="codex-file-actions flex flex-wrap items-center gap-2 px-3 py-2 border-b border-slate-800/60">
              <Button size="small" severity="secondary" outlined icon="pi pi-check-circle" label="Freeze File" @click="freezeSelectedFile" />
              <Button size="small" severity="info" outlined icon="pi pi-sparkles" label="Local Summary" @click="requestLocalSummary" />
              <Button size="small" severity="secondary" outlined icon="pi pi-folder-open" label="Open Local" @click="openLocalFile" />
              <Button size="small" severity="secondary" outlined icon="pi pi-sitemap" label="Analyze Module" @click="analyzeModule" />
              <Button size="small" severity="secondary" outlined icon="pi pi-book" label="Index Markdown" @click="indexMarkdown" />
              <Button size="small" severity="secondary" outlined icon="pi pi-question-circle" label="Help" @click="showInfo('File Inspector', 'Select a file to inspect its real source, select multiple files to send their bounded source context to Codex, freeze approved paths, queue a Local AI summary, or inspect the owning architecture module.')" />
              <Button v-if="selectedFiles.length" size="small" severity="primary" :label="`Analyze ${selectedFiles.length} Selected`" icon="pi pi-comments" @click="analyzeSelectedFiles" />
            </div>


            <div
              class="flex-1 overflow-auto p-4 font-mono text-xs text-slate-300 leading-relaxed bg-[#0a0d14]"
            >
              <div class="text-slate-600 mb-2">
                // {{ selectedFile?.path || 'frontend_vue/src/assets/scss/codex/CodexView.scss' }}
              </div>
              <pre v-if="fileContent" class="codex-code whitespace-pre-wrap" :data-language="selectedFile?.kind"><code v-html="highlightedCode"></code></pre>
              <div v-else class="space-y-1">
                <p class="text-pink-400">.codex-view <span class="text-slate-300">{</span></p>
                <p class="pl-4 text-sky-300">display: <span class="text-amber-300">flex</span>;</p>
                <p class="pl-4 text-sky-300">height: <span class="text-amber-300">100vh</span>;</p>
                <p class="pl-4 text-sky-300">
                  background: <span class="text-indigo-400">$surface-ground</span>;
                </p>
                <p class="text-slate-300">}</p>
              </div>
            </div>


            <div class="h-48 border-t border-slate-800/60 bg-[#0d111a] flex flex-col shrink-0">
              <div
                class="flex items-center justify-between border-b border-slate-800/60 px-3 text-xs bg-[#0a0d14]"
              >
                <div class="flex items-center gap-2">
                  <button
                    class="px-3 py-1.5 border-b-2 border-indigo-500 text-indigo-400 font-medium"
                  >
                    API Response
                  </button>
                  <button class="px-3 py-1.5 text-slate-400 hover:text-slate-200">Terminal</button>
                  <button class="px-3 py-1.5 text-slate-400 hover:text-slate-200">Logs</button>
                </div>
              </div>


              <div class="p-2 border-b border-slate-800/60 flex items-center gap-2 bg-[#0d111a]">
                <select
                  class="bg-[#131926] border border-slate-800 text-sky-400 text-xs rounded px-2 py-1 font-semibold focus:outline-none"
                >
                  <option>GET</option>
                  <option>POST</option>
                </select>
                <input
                  type="text"
                  v-model="command"
                  placeholder="/api/codex/registry/health/"
                  class="flex-1 bg-[#131926] border border-slate-800 text-xs font-mono text-slate-300 px-3 py-1 rounded focus:outline-none"
                />
                <button
                  @click="runCommand"
                  class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-3 py-1 rounded font-medium"
                >
                  Send
                </button>
                <span
                  class="bg-emerald-500/20 text-emerald-400 text-[11px] font-bold px-2 py-0.5 rounded"
                  >200 OK</span
                >
              </div>


              <div
                class="flex-1 p-3 font-mono text-xs text-emerald-400 overflow-y-auto bg-[#080b11]"
              >
                <pre>{{
                  result
                    ? JSON.stringify(result, null, 2)
                    : '{\n  "status": "healthy",\n  "features": { "total": 150, "approved": 120 }\n}'
                }}</pre>
              </div>
            </div>
          </div>
        </template>


        <template v-else-if="activePanel === 'chat'">
          <div class="flex-1 flex flex-col p-6 space-y-4 overflow-y-auto bg-[#0a0d14]">
            <h2 class="text-lg font-bold text-slate-100">Codex AI Chat Panel</h2>
            <div class="flex-1 space-y-3 overflow-y-auto">
              <div
                v-for="(msg, i) in chatMessages"
                :key="i"
                :class="[
                  'p-3 rounded-lg text-xs max-w-xl',
                  msg.role === 'user'
                    ? 'bg-indigo-600/20 text-indigo-200 ml-auto'
                    : 'bg-slate-800 text-slate-200',
                ]"
              >
                {{ msg.content }}
              </div>
            </div>
            <div class="flex gap-2">
              <input
                v-model="chatInput"
                @keyup.enter="sendChat()"
                placeholder="Type a message..."
                class="flex-1 bg-[#131926] border border-slate-800 rounded px-3 py-2 text-xs text-slate-200"
              />
              <button
                @click="sendChat()"
                class="bg-indigo-600 px-4 py-2 text-xs rounded text-white font-medium"
              >
                Send
              </button>
            </div>
          </div>
        </template>

        <template v-else-if="activePanel === 'build'">
          <CodexBuildWorkspace class="flex-1 min-w-0" />
        </template>

        <template v-else-if="activePanel === 'pipeline'">
          <div class="flex-1 p-6 overflow-y-auto codex-panel">
            <div class="flex items-center justify-between mb-4">
              <div>
                <h2 class="text-lg font-bold">Workflow & Dependency Progression</h2>
                <p class="text-xs text-slate-500">Library Setup → Configuration → Core Code → Integration → Testing</p>
              </div>
              <Button size="small" icon="pi pi-refresh" label="Verify" @click="loadGovernance" />
            </div>
            <div class="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
              <Card v-for="step in workflow.steps" :key="step.key" class="codex-workflow-card">
                <template #content>
                  <div class="flex items-start justify-between gap-2">
                    <div>
                      <div class="text-xs text-slate-500">{{ String(step.order).padStart(2, '0') }}</div>
                      <div class="font-semibold text-sm mt-1">{{ step.name }}</div>
                    </div>
                    <Tag :value="step.status" :severity="step.status === 'completed' ? 'success' : step.status === 'blocked' ? 'danger' : 'warn'" />
                  </div>
                  <p class="text-xs text-slate-400 mt-3">{{ step.description }}</p>
                  <div class="mt-3 text-[11px] text-slate-500">
                    <div v-for="(e, key) in step.evidence" :key="key" class="flex justify-between gap-2">
                      <span class="truncate">{{ key }}</span><i :class="e.exists ? 'pi pi-check text-emerald-400' : 'pi pi-times text-red-400'"></i>
                    </div>
                  </div>
                </template>
              </Card>
            </div>
          </div>
        </template>

        <template v-else-if="activePanel === 'governance'">
          <div class="flex-1 p-6 overflow-y-auto codex-panel space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-lg font-bold">Protected Registry & Local AI</h2>
                <p class="text-xs text-slate-500">Approved paths are frozen and exported to external-AI governance manifests.</p>
              </div>
              <div class="flex gap-2">
                <Button size="small" icon="pi pi-file-export" label="Generate Manifests" @click="generateManifest" />
                <Button size="small" severity="secondary" icon="pi pi-question-circle" @click="showInfo('Governance', 'Protected items are persisted in Django. Frozen paths are checked before Codex applies changes and are exported to PROJECT_CONTEXT.json and project_manifest.json.')" />
              </div>
            </div>
            <Card>
              <template #title>Protected Items ({{ protectedItems.length }})</template>
              <template #content>
                <DataTable :value="protectedItems" size="small" paginator :rows="8" responsiveLayout="scroll">
                  <Column field="key" header="Key" />
                  <Column field="item_type" header="Type" />
                  <Column field="path" header="Path" />
                  <Column field="reason" header="Reason" />
                  <Column header="Frozen">
                    <template #body="{ data }"><Tag :value="data.frozen ? 'FROZEN' : 'OPEN'" :severity="data.frozen ? 'success' : 'warn'" /></template>
                  </Column>
                </DataTable>
              </template>
            </Card>
            <Card>
              <template #title>Background Local AI Jobs</template>
              <template #content>
                <DataTable :value="localAIJobs" size="small" responsiveLayout="scroll">
                  <Column field="id" header="ID" />
                  <Column field="task_type" header="Task" />
                  <Column field="status" header="Status" />
                  <Column field="provider" header="Provider" />
                  <Column field="created_at" header="Created" />
                </DataTable>
              </template>
            </Card>
          </div>
        </template>

        <template v-else-if="activePanel === 'registry'">
          <div class="flex-1 p-6 overflow-y-auto codex-panel">
            <CodexCapabilities />
          </div>
        </template>

        <template v-else>
          <div class="flex-1 p-6 text-slate-300 bg-[#0a0d14]">
            <h2 class="text-base font-bold capitalize">{{ activePanel }} View</h2>
            <p class="text-xs text-slate-500 mt-1">Data loaded live from backend services.</p>
            <pre class="mt-4 p-4 bg-[#0d111a] rounded text-xs text-emerald-400 font-mono">{{
              JSON.stringify({ overview, healthScores, totalCapabilities }, null, 2)
            }}</pre>
          </div>
        </template>


        <aside
          class="w-80 bg-[#0d111a] border-l border-slate-800/60 flex flex-col shrink-0 p-3 overflow-y-auto space-y-4"
        >

          <div class="bg-[#111622] border border-slate-800/80 rounded-xl p-3 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-200 flex items-center gap-1.5">
                <i class="pi pi-cog text-indigo-400"></i> Codex AI Assistant
              </span>
              <span
                class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.5 rounded font-medium"
                >Project Aware</span
              >
            </div>

            <div
              class="bg-[#171d2c] border border-slate-800 p-2.5 rounded-lg text-xs text-slate-300 leading-relaxed"
            >
              Hello! I'm Codex. Ask me anything about your backend models, APIs, or Vue components.
            </div>

            <div class="grid grid-cols-2 gap-1.5 text-[11px]">
              <button
                @click="analyzeProject"
                class="bg-[#171d2c] hover:bg-slate-800 border border-slate-800 text-slate-300 p-1.5 rounded flex items-center gap-1"
              >
                <i class="pi pi-chart-line text-indigo-400"></i> Analyze
              </button>
              <button
                @click="generatePrompt"
                class="bg-[#171d2c] hover:bg-slate-800 border border-slate-800 text-slate-300 p-1.5 rounded flex items-center gap-1"
              >
                <i class="pi pi-code text-sky-400"></i> Prompt
              </button>
            </div>

            <div class="relative">
              <input
                v-model="chatInput"
                @keyup.enter="sendChat()"
                type="text"
                placeholder="Ask a question..."
                class="w-full bg-[#0a0d14] border border-slate-800 rounded-lg pr-8 pl-2.5 py-1.5 text-xs text-slate-300 focus:outline-none"
              />
              <button @click="sendChat()" class="absolute right-2 top-1.5 text-indigo-400">
                <i class="pi pi-send text-xs"></i>
              </button>
            </div>
          </div>


          <div class="bg-[#111622] border border-slate-800/80 rounded-xl p-3 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-200">Project Analysis</span>
              <a
                href="#"
                @click.prevent="activePanel = 'analysis'"
                class="text-[10px] text-indigo-400 hover:underline"
                >View Details</a
              >
            </div>

            <div class="flex items-center gap-4">
              <div
                class="w-16 h-16 rounded-full border-4 border-emerald-500 flex flex-col items-center justify-center shrink-0"
              >
                <span class="text-sm font-bold text-slate-100">92%</span>
                <span class="text-[8px] text-emerald-400">Excellent</span>
              </div>

              <div class="flex-1 space-y-1.5 text-[10px]">
                <div v-for="(score, key) in healthScores" :key="key">
                  <div class="flex justify-between text-slate-400 capitalize">
                    <span>{{ key }}</span
                    ><span>{{ score }}%</span>
                  </div>
                  <div class="w-full bg-slate-800 h-1 rounded-full overflow-hidden">
                    <div class="bg-indigo-500 h-full" :style="{ width: score + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>

  <Dialog v-model:visible="showPrompt" modal header="Codex Prompt Generator" :style="{ width: 'min(900px, 92vw)' }">
    <div class="space-y-3">
      <SelectButton v-model="promptType" :options="['development', 'bug', 'image']" />
      <Textarea v-model="generatedPrompt" rows="18" class="w-full font-mono text-xs" />
      <div class="flex justify-end">
        <Button icon="pi pi-copy" :label="promptCopyState || 'Copy Prompt'" @click="copyPrompt" />
      </div>
    </div>
  </Dialog>

  <Dialog v-model:visible="infoDialog.visible" modal :header="infoDialog.title" :style="{ width: 'min(700px, 90vw)' }">
    <p class="text-sm leading-6 whitespace-pre-wrap text-slate-300">{{ infoDialog.content }}</p>
  </Dialog>
</template>

<style src="@/assets/scss/Codex/_CodexView.scss" lang="scss"></style>
