<script setup>
import Button from 'primevue/button'

defineProps({ chatInput: String, healthScores: Object })
defineEmits(['update:chatInput', 'analyze', 'prompt', 'send', 'navigate'])
</script>

<template>
  <aside
    class="w-80 bg-[#0d111a] border-l border-slate-800/60 flex flex-col shrink-0 p-3 overflow-y-auto space-y-4"
  >
    <div class="bg-[#111622] border border-slate-800/80 rounded-xl p-3 space-y-3">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold text-slate-200 flex items-center gap-1.5">
          <i class="pi pi-cog text-indigo-400"></i> Codex AI Assistant
        </span>
        <span
          class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.5 rounded font-medium"
          >Project Aware</span
        >
      </div>
      <div class="bg-[#171d2c] border border-slate-800 p-2.5 rounded-lg text-xs text-slate-300">
        Hello! I'm Codex. Ask me anything about your project components.
      </div>
      <div class="grid grid-cols-2 gap-1.5 text-[11px]">
        <Button
          size="small"
          severity="secondary"
          outlined
          icon="pi pi-chart-line"
          label="Analyze"
          @click="$emit('analyze')"
        />
        <Button
          size="small"
          severity="secondary"
          outlined
          icon="pi pi-code"
          label="Prompt"
          @click="$emit('prompt')"
        />
      </div>
      <div class="relative">
        <input
          :value="chatInput"
          @input="$emit('update:chatInput', $event.target.value)"
          @keyup.enter="$emit('send')"
          type="text"
          placeholder="Ask a question..."
          class="w-full bg-[#0a0d14] border border-slate-800 rounded-lg pr-8 pl-2.5 py-1.5 text-xs text-slate-300 focus:outline-none"
        />
        <button @click="$emit('send')" class="absolute right-2 top-1.5 text-indigo-400">
          <i class="pi pi-send text-xs"></i>
        </button>
      </div>
    </div>
  </aside>
</template>
