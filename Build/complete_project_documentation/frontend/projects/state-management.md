# projects state management

State is local to this domain unless a matching Pinia store or shared service is found.


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


Store data persistence and shared auth are described in [shared state](../shared-infrastructure/shared-state.md) and [authentication](../shared-infrastructure/authentication.md).
