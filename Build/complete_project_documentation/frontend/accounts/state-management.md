# accounts state management

State is local to this domain unless a matching Pinia store or shared service is found.


## stores/accounts/user.js
L1: import { defineStore } from 'pinia'
L48: export const useUserStore = defineStore('user', {
L53: state: () => ({
L67: getters: {
L113: actions: {


Store data persistence and shared auth are described in [shared state](../shared-infrastructure/shared-state.md) and [authentication](../shared-infrastructure/authentication.md).
