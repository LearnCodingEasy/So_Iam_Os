# codex state management

State is local to this domain unless a matching Pinia store or shared service is found.


## stores/codex/codex.js
L1: import { defineStore } from 'pinia'
L4: export const useCodexStore = defineStore('codex', {
L5: state: () => ({
L29: actions: {


Store data persistence and shared auth are described in [shared state](../shared-infrastructure/shared-state.md) and [authentication](../shared-infrastructure/authentication.md).
