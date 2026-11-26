<script setup>
import { computed } from 'vue'

const props = defineProps({
  files: Array,
  loading: Boolean,
  selectedFile: Object,
  selectedFiles: Array,
  fileQuery: String,
})
defineEmits(['update:fileQuery', 'openFile', 'toggleFile'])

const filteredFiles = computed(() => {
  const q = (props.fileQuery || '').trim().toLowerCase()
  if (!q) return props.files
  return props.files.filter((row) => JSON.stringify(row).toLowerCase().includes(q))
})
</script>

<template>
  <div class="w-64 bg-[#0d111a] border-r border-slate-800/60 flex flex-col shrink-0">
    <div class="p-3 border-b border-slate-800/60 flex items-center justify-between">
      <span class="text-xs font-semibold text-slate-300">Project Explorer</span>
    </div>
    <div class="p-2">
      <input
        :value="fileQuery"
        @input="$emit('update:fileQuery', $event.target.value)"
        type="text"
        placeholder="Search files..."
        class="w-full bg-[#131926] border border-slate-800 rounded px-2.5 py-1 text-[11px] text-slate-300 focus:outline-none"
      />
    </div>
    <div class="flex-1 overflow-y-auto px-2 py-1 text-xs text-slate-400 space-y-1">
      <div v-if="loading" class="p-2 text-slate-500 text-center">Loading files...</div>
      <div v-else-if="!filteredFiles.length" class="p-2 text-slate-500 text-center">
        No files found
      </div>
      <div v-else>
        <div
          v-for="file in filteredFiles"
          :key="file.id || file.path"
          @click="$emit('openFile', file)"
          :class="[
            'flex items-center justify-between py-1.5 px-2 rounded cursor-pointer text-xs font-mono transition-colors',
            selectedFile?.path === file.path
              ? 'bg-indigo-600/20 text-indigo-300 font-semibold'
              : 'hover:bg-slate-800/40 text-slate-300',
          ]"
        >
          <span class="flex items-center gap-2 truncate"
            ><i class="pi pi-file text-pink-400"></i> {{ file.name || file.path }}</span
          >
          <i
            @click.stop="$emit('toggleFile', file)"
            :class="[
              'pi text-[10px]',
              selectedFiles.some((f) => f.path === file.path)
                ? 'pi-check-circle text-indigo-400'
                : 'pi-circle text-slate-600',
            ]"
          ></i>
        </div>
      </div>
    </div>
  </div>
</template>
