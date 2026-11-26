<script setup>
defineProps({ navItems: Array, activePanel: String, projectName: String })
defineEmits(['update:activePanel'])
</script>

<template>
  <aside
    class="w-64 bg-[#0d111a] border-r border-slate-800/60 flex flex-col justify-between shrink-0"
  >
    <div>
      <div class="p-4 border-b border-slate-800/60 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div
            class="w-7 h-7 rounded-lg bg-indigo-600/30 text-indigo-400 flex items-center justify-center font-bold text-sm"
          >
            <i class="pi pi-code"></i>
          </div>
          <div>
            <h2 class="text-sm font-semibold text-slate-100 leading-tight">Codex</h2>
            <p class="text-[10px] text-slate-500">Project Intelligence</p>
          </div>
        </div>
      </div>
      <nav class="p-2 space-y-1 text-xs">
        <button
          v-for="nav in navItems"
          :key="nav.key"
          @click="$emit('update:activePanel', nav.key)"
          :class="[
            'w-full flex items-center justify-between px-3 py-2 rounded-md transition-colors text-left',
            activePanel === nav.key
              ? 'bg-indigo-600/20 text-indigo-400 font-medium'
              : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200',
          ]"
        >
          <span class="flex items-center gap-2.5"
            ><i :class="[nav.icon, 'text-sm']"></i> {{ nav.label }}</span
          >
        </button>
      </nav>
    </div>
    <div
      class="p-3 m-2 rounded-xl bg-gradient-to-br from-indigo-900/30 to-purple-900/20 border border-indigo-500/20 flex items-center gap-3"
    >
      <div class="text-2xl text-indigo-400">🚀</div>
      <div>
        <div class="text-xs font-semibold text-slate-200">{{ projectName }}</div>
        <div class="text-[10px] text-slate-400">Your AI-Powered Future</div>
      </div>
    </div>
  </aside>
</template>
