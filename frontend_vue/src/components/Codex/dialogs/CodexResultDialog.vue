<script setup>
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'

defineProps({
  visible: Boolean,
  title: { type: String, default: 'Execution Result' },
  resultData: [Object, Array, String]
})
defineEmits(['update:visible'])
</script>

<template>
  <Dialog
    :visible="visible"
    @update:visible="$emit('update:visible', $event)"
    modal
    :header="title"
    :style="{ width: 'min(750px, 90vw)' }"
    class="bg-[#111622] text-slate-200 border border-slate-800"
  >
    <div class="space-y-4 pt-2">
      <div class="p-3 bg-[#080b11] rounded-lg font-mono text-xs text-emerald-400 overflow-y-auto max-h-[400px]">
        <pre>{{ typeof resultData === 'object' ? JSON.stringify(resultData, null, 2) : resultData }}</pre>
      </div>
      <div class="flex justify-end">
        <Button
          label="Close"
          severity="secondary"
          size="small"
          @click="$emit('update:visible', false)"
        />
      </div>
    </div>
  </Dialog>
</template>
