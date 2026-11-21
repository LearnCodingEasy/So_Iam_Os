# goals state management

State is local to this domain unless a matching Pinia store or shared service is found.


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


Store data persistence and shared auth are described in [shared state](../shared-infrastructure/shared-state.md) and [authentication](../shared-infrastructure/authentication.md).
