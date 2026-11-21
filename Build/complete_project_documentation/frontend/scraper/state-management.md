# scraper state management

State is local to this domain unless a matching Pinia store or shared service is found.


## stores/accounts/user.js
L1: import { defineStore } from 'pinia'
L48: export const useUserStore = defineStore('user', {
L53: state: () => ({
L67: getters: {
L113: actions: {

## stores/ai/useAIStore.js
L1: import { defineStore } from 'pinia'
L7: export const useAIStore = defineStore('ai-management', () => {
L8: const providers = ref([])
L9: const credentials = ref([])
L10: const settings = ref(null)
L11: const conversations = ref([])
L12: const executions = ref([])
L13: const usage = ref({})
L14: const budgets = ref([])
L15: const audit = ref([])
L16: const workflows = ref([])
L17: const health = ref(null)
L18: const capabilities = ref([])
L19: const loading = ref(false)
L20: const error = ref(null)

## stores/automation/useProgramElementStore.js
L11: import { defineStore } from 'pinia'
L15: export const useProgramElementStore = defineStore('programElement', () => {
L19: const elements = ref([])
L20: const currentElement = ref(null)
L21: const isLoading = ref(false)
L23: const form = ref({
L52: const currentElementId = computed(() => currentElement.value?.id ?? null)

## stores/automation/useProgramStore.js
L11: import { defineStore } from 'pinia'
L15: export const useProgramStore = defineStore('program', () => {
L19: const programs = ref([])
L20: const currentProgram = ref(null)
L21: const isLoading = ref(false)
L22: const isScanning = ref(false)
L24: const form = ref({
L37: const currentProgramId = computed(() => currentProgram.value?.id ?? null)
L185: const openWindows = ref([])

## stores/automation/useTaskStore.js
L12: import { defineStore } from 'pinia'
L16: export const useTaskStore = defineStore('task', () => {
L20: const tasks = ref([])
L21: const currentTask = ref(null)
L23: const currentTaskRunId = ref(null)
L24: const isLoading = ref(false)
L26: const form = ref({
L35: const currentTaskId = computed(() => currentTask.value?.id ?? null)

## stores/automation/useWorkflowStore.js
L12: import { defineStore } from 'pinia'
L18: export const useWorkflowStore = defineStore('workflow', () => {
L22: const workflows = ref([])
L23: const currentWorkflow = ref(null)
L24: const nodes = ref([])
L25: const edges = ref([])
L27: const isLoading = ref(false)
L28: const isSaving = ref(false)
L29: const isInitialized = ref(false)
L31: const formWorkflow = ref({ name: '', description: '', status: 'draft' })
L36: const currentWorkflowId = computed(() => currentWorkflow.value?.id ?? null)
L65: actions: n.data?.actions ?? [],
L201: actions: n.data?.actions ?? [],

## stores/codex/codex.js
L1: import { defineStore } from 'pinia'
L4: export const useCodexStore = defineStore('codex', {
L5: state: () => ({
L29: actions: {

## stores/goals/goalsStore.js
L1: import { defineStore } from 'pinia'
L5: export const useGoalsStore = defineStore('goals', () => {
L6: const items = ref([])
L7: const analytics = ref(null)
L8: const count = ref(0)
L9: const next = ref(null)
L10: const previous = ref(null)
L11: const loading = ref(false)
L12: const analyticsLoading = ref(false)
L13: const error = ref(null)

## stores/knowledge/knowledgeStore.js
L1: import { defineStore } from 'pinia'
L19: export const useKnowledgeStore = defineStore('knowledge', () => {
L20: const items = ref([])
L21: const count = ref(0)
L22: const next = ref(null)
L23: const previous = ref(null)
L24: const filesByKnowledgeId = ref({})
L25: const loading = ref(false)
L26: const saving = ref(false)
L27: const error = ref(null)
L29: const lastUploadReport = ref({ uploaded: [], failed: [] })

## stores/projects/projects.js
L1: import { defineStore } from 'pinia'
L5: export const useProjectsStore = defineStore('projects', () => {
L6: const items = ref([])
L7: const count = ref(0)
L8: const next = ref(null)
L9: const previous = ref(null)
L10: const loading = ref(false)
L11: const saving = ref(false)
L12: const error = ref(null)

## stores/shared/counter.js
L2: import { defineStore } from 'pinia'
L4: export const useCounterStore = defineStore('counter', () => {
L5: const count = ref(0)
L6: const doubleCount = computed(() => count.value * 2)

## stores/shared/primeTheme.js
L4: const _appState = reactive({ theme: 'Aura', darkTheme: false })
L5: app.config.globalProperties.$appState = _appState


Store data persistence and shared auth are described in [shared state](../shared-infrastructure/shared-state.md) and [authentication](../shared-infrastructure/authentication.md).
