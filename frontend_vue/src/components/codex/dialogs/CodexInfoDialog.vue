<script setup>
import Dialog from 'primevue/dialog'

defineProps({
  visible: Boolean,
  title: String,
  content: String,
})
defineEmits(['update:visible'])
</script>

<template>
  <Dialog
    :visible="visible"
    @update:visible="$emit('update:visible', $event)"
    modal
    :header="title"
    :style="{ width: 'min(700px, 90vw)' }"
    class="bg-[#111622] text-slate-200 border border-slate-800"
  >
    <p class="text-xs leading-relaxed whitespace-pre-wrap text-slate-300 pt-2">{{ content }}</p>
  </Dialog>
</template>
