<template>
  <div
    class="app-layout"
    dir="rtl"
    :class="{ 'sidebar-is-collapsed': sidebarCollapsed, 'mobile-menu-open': mobileMenuOpen }"
  >
    <Sidebar
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @navigate="mobileMenuOpen = false"
    />
    <button
      v-if="mobileMenuOpen"
      class="mobile-backdrop"
      type="button"
      aria-label="إغلاق القائمة"
      @click="mobileMenuOpen = false"
    />
    <main class="main-content">
      <Topbar @toggle-sidebar="mobileMenuOpen = !mobileMenuOpen" />
      <section ref="pageEl" class="page-content">
        <slot />
      </section>
    </main>
  </div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './Sidebar.vue'
import Topbar from './Topbar.vue'
import { revealChildren } from '@/composables/useMotion'

const sidebarCollapsed = ref(false)
const mobileMenuOpen = ref(false)
const pageEl = ref(null)
const route = useRoute()

// Page entrance: after each navigation, softly stagger the top-level blocks of the new page.
// Only direct children of the page root are animated (never inputs), and inline styles are cleared afterwards.
let ctx = null
watch(
  () => route.fullPath,
  async () => {
    ctx?.revert()
    await nextTick()
    // The routed view is the first element child of the page container.
    const view = pageEl.value?.firstElementChild
    if (view)
      ctx = revealChildren(view, { selector: ':scope > *', y: 12, stagger: 0.05, duration: 0.45 })
  },
  { flush: 'post', immediate: true },
)
onBeforeUnmount(() => ctx?.revert())
</script>
