# ai state management

State is local to this domain unless a matching Pinia store or shared service is found.


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


Store data persistence and shared auth are described in [shared state](../shared-infrastructure/shared-state.md) and [authentication](../shared-infrastructure/authentication.md).
