<script setup>
defineProps({ command: String, result: [Object, Array, String] })
defineEmits(['update:command', 'run'])
</script>

<template>
  <div class="h-48 border-t border-slate-800/60 bg-[#0d111a] flex flex-col shrink-0">
    <div class="p-2 border-b border-slate-800/60 flex items-center gap-2 bg-[#0d111a]">
      <input
        :value="command"
        @input="$emit('update:command', $event.target.value)"
        type="text"
        placeholder="/api/codex/..."
        class="flex-1 bg-[#131926] border border-slate-800 text-xs font-mono text-slate-300 px-3 py-1 rounded focus:outline-none"
      />
      <button
        @click="$emit('run')"
        class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-3 py-1 rounded"
      >
        Send
      </button>
    </div>
    <div class="flex-1 p-3 font-mono text-xs text-emerald-400 overflow-y-auto bg-[#080b11]">
      <pre>{{ result ? JSON.stringify(result, null, 2) : '// Ready...' }}</pre>
    </div>
  </div>
</template>
