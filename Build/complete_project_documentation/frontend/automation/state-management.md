# automation state management

State is local to this domain unless a matching Pinia store or shared service is found.


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


Store data persistence and shared auth are described in [shared state](../shared-infrastructure/shared-state.md) and [authentication](../shared-infrastructure/authentication.md).
