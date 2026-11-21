<script setup>
import { RouterView } from 'vue-router'
import { useUserStore } from '@/stores/accounts/user'
import AppLayout from '@/components/ai/layout/AppLayout.vue'
import LiveDebugConsole from '@/components/shared/LiveDebugConsole.vue'

const userStore = useUserStore()
</script>

<template>
  <div class="wrapper_page_app">
    <AppLayout v-if="userStore.isLoggedIn">
      <RouterView />
    </AppLayout>
    <RouterView v-else />

    <prime_toast />
    <prime_confirm_dialog />
    <LiveDebugConsole />
    <SystemToaster position="top-right" rich-colors close-button />
  </div>
</template>

<style lang="scss">
.wrapper_page_app {
  min-height: 100vh;
}
</style>
