# codex source-file catalog

Files associated with this domain's view/service/store/component directories are listed. Imports and declaration names are static excerpts; global callers are not exhaustive.


## views/codex/CodexBuildWorkspace.vue
- Type: .vue
- Declarations: L14: const loading = ref(false); L15: const error = ref(''); L16: const payload = ref(null); L17: const selectedNode = ref(null); L18: const nodes = computed(() => payload.value?.graph?.nodes || []); L19: const edges = computed(() => payload.value?.graph?.edges || []); L21: async function refresh() {; L32: function statusSeverity(status) {
- Imports (first five): import { computed, onMounted, ref } from 'vue'; import { VueFlow } from '@vue-flow/core'; import { Background } from '@vue-flow/background'; import { Controls } from '@vue-flow/controls'; import { MiniMap } from '@vue-flow/minimap'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/codex/CodexCapabilities.spec.js
- Type: .js
- Declarations: L8: const store = useCodexStore()
- Imports (first five): import { beforeEach, describe, expect, it } from 'vitest'; import { createPinia, setActivePinia } from 'pinia'; import { useCodexStore } from '@/stores/codex/codex'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/codex/CodexCapabilities.vue
- Type: .vue
- Declarations: L15: const store = useCodexStore(); L16: const query = ref(''); L17: const busy = ref(false); L18: const validating = ref(false); L19: const selected = ref(null); L20: const result = ref(null); L21: const registryTab = ref('features'); L22: const infoVisible = ref(false); L23: const infoItem = ref(null); L25: function showInfo(item) {; L30: const features = computed(() => filter(store.capabilityFeatures.value || store.capabilityFeatures)); L31: const tools = computed(() => filter(store.capabilityTools.value || store.capabilityTools)); L32: const agents = computed(() => filter(store.capabilityAgents.value || store.capabilityAgents)); L34: function filter(rows) {; L35: const q = query.value.trim().toLowerCase(); L40: async function validate() {; L50: async function bootstrap() {; L59: async function runTool(item) {; L65: async function runAgent(item) {
- Imports (first five): import { computed, onMounted, ref } from 'vue'; import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'; import DataTable from 'primevue/datatable'
- Consumers: direct route/import references are listed where identified; no full call graph.


## views/codex/CodexView.vue
- Type: .vue
- Declarations: L35: const store = useCodexStore(); L36: const router = useRouter(); L38: const activePanel = ref('workspace'); L39: const query = ref(''); L40: const fileQuery = ref(''); L41: const chatInput = ref(''); L42: const busy = ref(false); L43: const loading = ref(true); L44: const errorMessage = ref(''); L45: const successMessage = ref(''); L46: const selectedFile = ref(null); L47: const selectedFiles = ref([]); L48: const fileContent = ref(''); L49: const result = ref(null); L50: const chatMessages = ref([]); L51: const graph = ref(null); L52: const security = ref(null); L53: const overview = ref(null); L54: const context = ref(null); L55: const files = ref([]); L56: const features = ref([]); L57: const apis = ref([]); L58: const discoveredRoutes = computed(() => router.getRoutes(); L62: const workflow = ref({ steps: [], completed: 0, total: 0 }); L63: const protectedItems = ref([]); L64: const localAIJobs = ref([]); L65: const infoDialog = ref({ visible: false, title: '', content: '' }); L66: const showPrompt = ref(false); L67: const generatedPrompt = ref(''); L68: const promptType = ref('development')
- Imports (first five): import { computed, onMounted, ref } from 'vue'; import { useRouter } from 'vue-router'; import { useCodexStore } from '@/stores/codex/codex'; import codex from '@/services/Codex/codex'; import CodexSidebar from '@/components/codex/Layout/CodexSidebar.vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## services/Codex/codex.js
- Type: .js
- Declarations: L4: const list = (data) =>; L7: const data = async (request) => (await request).data
- Imports (first five): import api from '@/services/Shared/api'; import { endpoints } from '@/services/Shared/endpoints'
- Consumers: direct route/import references are listed where identified; no full call graph.


## stores/codex/codex.js
- Type: .js
- Declarations: L4: export const useCodexStore = defineStore('codex', {; L83: const result = await codex.bootstrap(); L106: const result = await codex.registry.bootstrap(); L111: const result = await codex.scan()
- Imports (first five): import { defineStore } from 'pinia'; import codex from '@/services/Codex/codex'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/Build/WorkspaceView.vue
- Type: .vue
- Declarations: L7: const buildSteps = ref([
- Imports (first five): import { ref } from 'vue'; import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/Capabilities/CapabilitiesView.vue
- Type: .vue
- Declarations: L11: const activeTab = ref('features'); L13: const mockFeatures = ref([; L19: const mockTools = ref([
- Imports (first five): import { ref } from 'vue'; import Card from 'primevue/card'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tabs from 'primevue/tabs'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/dialogs/CodexInfoDialog.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Dialog from 'primevue/dialog'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/dialogs/CodexPromptDialog.vue
- Type: .vue
- Declarations: L8: const props = defineProps({; L13: const emit = defineEmits(['update:visible', 'update:promptType']); L16: const promptCopyState = ref(''); L18: async function copyPrompt() {
- Imports (first five): import { ref } from 'vue'; import Dialog from 'primevue/dialog'; import SelectButton from 'primevue/selectbutton'; import Textarea from 'primevue/textarea'; import Button from 'primevue/button'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/dialogs/CodexResultDialog.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Dialog from 'primevue/dialog'; import Button from 'primevue/button'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/Layout/CodexRightSidebar.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Button from 'primevue/button'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/Layout/CodexSidebar.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/Layout/CodexTopbar.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Tabs from 'primevue/tabs'; import TabList from 'primevue/tablist'; import Tab from 'primevue/tab'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/panels/CodexAnalysisPanel.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/panels/CodexChatPanel.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Button from 'primevue/button'; import InputText from 'primevue/inputtext'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/panels/CodexGovernancePanel.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import DataTable from 'primevue/datatable'; import Column from 'primevue/column'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/panels/CodexPipelinePanel.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Card from 'primevue/card'; import Button from 'primevue/button'; import Tag from 'primevue/tag'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/panels/CodexRegistryPanel.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/workspace/CodexCodeEditor.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): import Button from 'primevue/button'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/workspace/CodexFileActions.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/workspace/CodexInspectorWorkspace.vue
- Type: .vue
- Declarations: L4: const props = defineProps({; L11: const emit = defineEmits(['openFile', 'askAI', 'scan']); L13: const activeApp = ref(null); L14: const activeRoute = ref(''); L15: const inspectEnabled = ref(false); L16: const viewport = ref('desktop'); L17: const selectedElement = ref(null); L18: const resourcePaths = ref([]); L19: const previewError = ref(''); L20: const frame = ref(null); L23: const appFeatures = computed(() => [...props.features].sort((a, b) => (a.name || '').localeCompare(b.name || ''))); L24: const activeRoutes = computed(() => {; L26: const slug = String(activeApp.value.app_label || activeApp.value.name || '').toLowerCase().replace(/[^a-z0-9]+/g, ''); L28: const routeText = `${route.name || ''} ${route.path || ''}`.toLowerCase().replace(/[^a-z0-9]+/g, ''); L32: const currentRoute = computed(() => props.routes.find((route) => route.path === activeRoute.value) || null); L33: const matchedFile = computed(() => {; L34: const path = selectedElement.value?.sourcePath; L36: const normalized = path.replaceAll('\\', '/').replace(/^.*?frontend_vue\//, 'frontend_vue/'); L39: const relatedApis = computed(() => {; L40: const observed = resourcePaths.value; L42: const path = url.split('?')[0].replace(/\/$/, ''); L43: const endpoint = String(api.path || '').replace(/\/$/, ''); L48: function chooseApp(app) {; L53: const candidates = props.routes.filter((route) => {; L54: const slug = String(app.app_label || app.name || '').toLowerCase().replace(/[^a-z0-9]+/g, ''); L55: const routeText = `${route.name || ''} ${route.path || ''}`.toLowerCase().replace(/[^a-z0-9]+/g, ''); L61: function readElement(element, doc) {; L62: const chain = []; L67: const tag = node.tagName?.toLowerCase(); L76: const instance = node.__vueParentComponent
- Imports (first five): import { computed, onBeforeUnmount, ref, watch } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/workspace/CodexProjectExplorer.vue
- Type: .vue
- Declarations: L4: const props = defineProps({; L13: const filteredFiles = computed(() => {; L14: const q = (props.fileQuery || '').trim().toLowerCase()
- Imports (first five): import { computed } from 'vue'
- Consumers: direct route/import references are listed where identified; no full call graph.


## components/codex/workspace/CodexTerminal.vue
- Type: .vue
- Declarations: none matched
- Imports (first five): none matched
- Consumers: direct route/import references are listed where identified; no full call graph.

