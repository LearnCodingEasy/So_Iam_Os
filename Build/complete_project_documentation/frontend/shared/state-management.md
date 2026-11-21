# shared state management

State is local to this domain unless a matching Pinia store or shared service is found.


## stores/shared/counter.js
L2: import { defineStore } from 'pinia'
L4: export const useCounterStore = defineStore('counter', () => {
L5: const count = ref(0)
L6: const doubleCount = computed(() => count.value * 2)

## stores/shared/primeTheme.js
L4: const _appState = reactive({ theme: 'Aura', darkTheme: false })
L5: app.config.globalProperties.$appState = _appState


Store data persistence and shared auth are described in [shared state](../shared-infrastructure/shared-state.md) and [authentication](../shared-infrastructure/authentication.md).
