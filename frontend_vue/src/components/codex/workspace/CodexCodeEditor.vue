<script setup>
import Button from 'primevue/button'

defineProps({ selectedFile: Object, selectedFiles: Array, fileContent: String })
defineEmits(['close', 'freeze', 'summary', 'openLocal', 'analyzeSelected'])
</script>

<template>
  <div class="flex-1 flex flex-col overflow-hidden bg-[#0a0d14]">
    <div
      class="bg-[#0d111a] border-b border-slate-800/60 flex items-center justify-between px-3 py-1.5"
    >
      <div
        class="flex items-center gap-2 bg-[#0a0d14] px-3 py-1 rounded-t-md border-t-2 border-indigo-500 text-xs text-slate-200 font-mono"
      >
        <i class="pi pi-file text-pink-400"></i> {{ selectedFile?.name || 'No file selected' }}
        <i
          class="pi pi-times text-[10px] text-slate-500 hover:text-slate-300 cursor-pointer ml-1"
          @click="$emit('close')"
        ></i>
      </div>
    </div>
    <div class="flex flex-wrap items-center gap-2 px-3 py-2 border-b border-slate-800/60">
      <Button
        size="small"
        severity="secondary"
        outlined
        icon="pi pi-check-circle"
        label="Freeze"
        @click="$emit('freeze')"
      />
      <Button
        size="small"
        severity="info"
        outlined
        icon="pi pi-sparkles"
        label="Summary"
        @click="$emit('summary')"
      />
      <Button
        size="small"
        severity="secondary"
        outlined
        icon="pi pi-folder-open"
        label="Open Local"
        @click="$emit('openLocal')"
      />
    </div>
    <div class="flex-1 overflow-auto p-4 font-mono text-xs text-slate-300 bg-[#0a0d14]">
      <pre v-if="fileContent" class="whitespace-pre-wrap"><code>{{ fileContent }}</code></pre>
      <div v-else class="text-slate-500 text-center py-10">Select a file to inspect.</div>
    </div>
  </div>
</template>
