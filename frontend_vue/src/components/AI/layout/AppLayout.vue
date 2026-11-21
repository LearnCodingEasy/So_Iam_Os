<template>
  <div
    class="app-layout"
    :class="{ 'sidebar-is-collapsed': sidebarCollapsed, 'mobile-menu-open': mobileMenuOpen }"
  >
    <Sidebar
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @navigate="mobileMenuOpen = false"
    />
    <main class="main-content">
      <Topbar @toggle-sidebar="mobileMenuOpen = !mobileMenuOpen" />
      <section class="page-content">
        <slot />
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from './Sidebar.vue'
import Topbar from './Topbar.vue'

const sidebarCollapsed = ref(false)
const mobileMenuOpen = ref(false)
</script>
