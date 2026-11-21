# knowledge state management

State is local to this domain unless a matching Pinia store or shared service is found.


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


Store data persistence and shared auth are described in [shared state](../shared-infrastructure/shared-state.md) and [authentication](../shared-infrastructure/authentication.md).
