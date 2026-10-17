<!--  -->

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useCodexStore } from '@/stores/codex'
import codex from '@/services/codex'

// Layout Components
import CodexSidebar from '@/components/Codex/Layout/CodexSidebar.vue'
import CodexRightSidebar from '@/components/Codex/Layout/CodexRightSidebar.vue'
import CodexTopbar from '@/components/Codex/Layout/CodexTopbar.vue'

// Panels
import CodexChatPanel from '@/components/Codex/panels/CodexChatPanel.vue'
import CodexAnalysisPanel from '@/components/Codex/panels/CodexAnalysisPanel.vue'
import CodexPipelinePanel from '@/components/Codex/panels/CodexPipelinePanel.vue'
import CodexGovernancePanel from '@/components/Codex/panels/CodexGovernancePanel.vue'
import CodexRegistryPanel from '@/components/Codex/panels/CodexRegistryPanel.vue'

// Workspace Components
import CodexFileExplorer from '@/components/Codex/workspace/CodexProjectExplorer.vue'
import CodexCodeEditor from '@/components/Codex/workspace/CodexCodeEditor.vue'
import CodexTerminal from '@/components/Codex/workspace/CodexTerminal.vue'

// Dialogs
import CodexPromptDialog from '@/components/Codex/dialogs/CodexPromptDialog.vue'
import CodexInfoDialog from '@/components/Codex/dialogs/CodexInfoDialog.vue'

// Existing shared components
import CodexBuildWorkspace from '@/components/Codex/Build/WorkspaceView.vue'
import CodexCapabilities from '@/components/Codex/Capabilities/CapabilitiesView.vue'

const store = useCodexStore()

const activePanel = ref('workspace')
const query = ref('')
const fileQuery = ref('')
const chatInput = ref('')
const busy = ref(false)
const loading = ref(true)
const errorMessage = ref('')
const successMessage = ref('')
const selectedFile = ref(null)
const selectedFiles = ref([])
const fileContent = ref('')
const result = ref(null)
const chatMessages = ref([])
const graph = ref(null)
const security = ref(null)
const overview = ref(null)
const context = ref(null)
const files = ref([])
const workflow = ref({ steps: [], completed: 0, total: 0 })
const protectedItems = ref([])
const localAIJobs = ref([])
const infoDialog = ref({ visible: false, title: '', content: '' })
const showPrompt = ref(false)
const generatedPrompt = ref('')
const promptType = ref('development')
const promptCopyState = ref('')
const command = ref('')

const navItems = [
  { key: 'workspace', label: 'Workspace', icon: 'pi pi-home' },
  { key: 'files', label: 'Project Explorer', icon: 'pi pi-folder-open' },
  { key: 'analysis', label: 'Project Analysis', icon: 'pi pi-chart-line' },
  { key: 'chat', label: 'Codex Chat', icon: 'pi pi-comments' },
  { key: 'build', label: 'Build Workspace', icon: 'pi pi-sitemap' },
  { key: 'pipeline', label: 'Development Pipeline', icon: 'pi pi-share-alt' },
  { key: 'registry', label: 'Capability Registry', icon: 'pi pi-bolt' },
  { key: 'governance', label: 'Governance', icon: 'pi pi-shield' },
]

const projectName = computed(() => overview.value?.project?.name || 'SO_IAM_OS')
const healthScores = computed(
  () => store.capabilityHealth?.scores || { architecture: 92, frontend: 90, backend: 95 },
)

function notifySuccess(message) {
  successMessage.value = message
}

function notifyError(error, fallback = 'Codex operation failed.') {
  errorMessage.value = error?.message || fallback
}

async function runAction(action, success = 'Operation completed successfully.') {
  busy.value = true
  try {
    const res = await action()
    result.value = res
    notifySuccess(success)
    return res
  } catch (err) {
    notifyError(err)
    return null
  } finally {
    busy.value = false
  }
}

async function loadCoreData() {
  loading.value = true
  try {
    const [ov, ctx, fl] = await Promise.all([codex.overview(), codex.context(), codex.files()])
    overview.value = ov
    context.value = ctx
    files.value = fl
    await store.loadCapabilities()
  } catch (err) {
    notifyError(err)
  } finally {
    loading.value = false
  }
}

async function openFile(file) {
  selectedFile.value = file
  const id = file?.id ?? file?.pk ?? file?.path
  if (!id) return
  await runAction(async () => {
    const res = await codex.fileContent(id)
    fileContent.value = res?.content ?? res?.text ?? ''
    return res
  }, 'File loaded.')
}

function toggleFile(file) {
  const id = file?.id ?? file?.pk ?? file?.path
  const exists = selectedFiles.value.some((item) => (item.id ?? item.pk ?? item.path) === id)
  selectedFiles.value = exists
    ? selectedFiles.value.filter((item) => (item.id ?? item.pk ?? item.path) !== id)
    : [...selectedFiles.value, file]
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
      content: response?.answer || response?.message || 'Done',
    })
  } catch (error) {
    notifyError(error)
  } finally {
    busy.value = false
  }
}

async function generatePrompt() {
  try {
    const selectedContext = selectedFiles.value.map((f) => f.path || f.name)
    const response = await codex.generatePrompt(
      promptType.value,
      chatInput.value || 'Implement change.',
      selectedContext,
    )
    generatedPrompt.value = response?.prompt || ''
    showPrompt.value = true
  } catch (error) {
    notifyError(error)
  }
}

onMounted(async () => {
  await loadCoreData()
})
</script>

<template>
  <div
    class="codex-view flex h-screen w-full bg-[#0a0d14] text-slate-200 font-sans overflow-hidden"
  >
    <!-- Left Navigation Sidebar -->
    <CodexSidebar
      :navItems="navItems"
      :activePanel="activePanel"
      :projectName="projectName"
      @update:activePanel="activePanel = $event"
    />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <CodexTopbar
        v-model:query="query"
        :activePanel="activePanel"
        :navItems="navItems"
        @update:activePanel="activePanel = $event"
      />

      <div class="flex-1 flex overflow-hidden">
        <!-- Workspace / Explorer & Code Editor -->
        <template v-if="activePanel === 'files' || activePanel === 'workspace'">
          <CodexFileExplorer
            :files="files"
            :loading="loading"
            :selectedFile="selectedFile"
            :selectedFiles="selectedFiles"
            v-model:fileQuery="fileQuery"
            @openFile="openFile"
            @toggleFile="toggleFile"
          />
          <div class="flex-1 flex flex-col overflow-hidden bg-[#0a0d14]">
            <CodexCodeEditor
              :selectedFile="selectedFile"
              :selectedFiles="selectedFiles"
              :fileContent="fileContent"
              @close="selectedFile = null"
              @freeze="
                runAction(() => codex.freezeProtectedItem({ path: selectedFile?.path }), 'Frozen.')
              "
              @summary="
                runAction(
                  () => codex.createLocalAIJob('summarize', { path: selectedFile?.path }),
                  'Job queued.',
                )
              "
              @openLocal="codex.openLocalFile(selectedFile?.path)"
              @analyzeSelected="activePanel = 'chat'"
            />
            <CodexTerminal
              v-model:command="command"
              :result="result"
              @run="runAction(() => codex.runCommand(command), 'Command executed.')"
            />
          </div>
        </template>

        <!-- Dynamic Panels -->
        <template v-else-if="activePanel === 'chat'">
          <CodexChatPanel
            :chatMessages="chatMessages"
            v-model:chatInput="chatInput"
            :busy="busy"
            @send="sendChat"
          />
        </template>

        <template v-else-if="activePanel === 'analysis'">
          <CodexAnalysisPanel
            :security="security"
            :graph="graph"
            @rebuild="runAction(() => codex.rebuildGraph(), 'Rebuilt.')"
          />
        </template>

        <template v-else-if="activePanel === 'build'">
          <CodexBuildWorkspace class="flex-1 min-w-0" />
        </template>

        <template v-else-if="activePanel === 'pipeline'">
          <CodexPipelinePanel :workflow="workflow" @refresh="loadCoreData" />
        </template>

        <template v-else-if="activePanel === 'registry'">
          <CodexRegistryPanel>
            <CodexCapabilities />
          </CodexRegistryPanel>
        </template>

        <template v-else-if="activePanel === 'governance'">
          <CodexGovernancePanel
            :protectedItems="protectedItems"
            :localAIJobs="localAIJobs"
            @manifest="runAction(() => codex.generateManifest(), 'Manifest generated.')"
          />
        </template>

        <!-- Right Assistant Sidebar -->
        <CodexRightSidebar
          v-model:chatInput="chatInput"
          :healthScores="healthScores"
          @analyze="activePanel = 'analysis'"
          @prompt="generatePrompt"
          @send="sendChat"
          @navigate="activePanel = $event"
        />
      </div>
    </div>
    <CodexPromptDialog
      v-model:visible="showPrompt"
      v-model:promptType="promptType"
      :generatedPrompt="generatedPrompt"
    />
    <CodexInfoDialog
      v-model:visible="infoDialog.visible"
      :title="infoDialog.title"
      :content="infoDialog.content"
    />
  </div>
</template>

<style src="@/assets/scss/Codex/_CodexView.scss" lang="scss"></style>
