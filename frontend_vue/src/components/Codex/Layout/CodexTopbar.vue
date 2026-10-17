<script setup>
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'

defineProps({ query: String, activePanel: String, navItems: Array })
defineEmits(['update:query', 'update:activePanel'])
</script>

<template>
  <header class="border-b border-slate-800/60 bg-[#0d111a] px-4 flex flex-col shrink-0">
    <div class="h-14 flex items-center justify-between">
      <div class="relative w-96">
        <i class="pi pi-search absolute left-3 top-2.5 text-slate-500 text-xs"></i>
        <input
          :value="query"
          @input="$emit('update:query', $event.target.value)"
          type="text"
          placeholder="Search files, features, APIs, or ask Codex..."
          class="w-full bg-[#131926] border border-slate-800 rounded-lg pl-9 pr-12 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-indigo-500/50"
        />
      </div>
      <div class="flex items-center gap-3 text-xs text-emerald-400">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Backend Connected
      </div>
    </div>
    <div class="flex items-center justify-between py-2 border-t border-slate-800/40">
      <Tabs
        :value="activePanel"
        @update:value="$emit('update:activePanel', $event)"
        class="codex-tabs"
      >
        <TabList>
          <Tab v-for="tab in navItems" :key="tab.key" :value="tab.key">
            <span class="flex items-center gap-1.5"><i :class="tab.icon"></i>{{ tab.label }}</span>
          </Tab>
        </TabList>
      </Tabs>
    </div>
  </header>
</template>
