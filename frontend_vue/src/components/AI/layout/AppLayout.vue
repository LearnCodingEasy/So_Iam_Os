<template>
  <div class="layout">
    <Sidebar :collapsed="sidebarCollapsed" @toggle="sidebarCollapsed = !sidebarCollapsed" />

    <main class="main-content" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <Topbar @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed" />

      <section class="page-content">
        <slot />
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Sidebar from "./Sidebar.vue";
import Topbar from "./Topbar.vue";

const sidebarCollapsed = ref(false);
</script>
