<script setup>
import { ref } from 'vue'
import Dialog from 'primevue/dialog'
import SelectButton from 'primevue/selectbutton'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'

const props = defineProps({
  visible: Boolean,
  promptType: String,
  generatedPrompt: String,
})
const emit = defineEmits(['update:visible', 'update:promptType'])
console.log('emit: ', emit)

const promptCopyState = ref('')

async function copyPrompt() {
  if (!props.generatedPrompt) return
  await navigator.clipboard.writeText(props.generatedPrompt)
  promptCopyState.value = 'Copied!'
  setTimeout(() => (promptCopyState.value = ''), 1800)
}
</script>

<template>
  <Dialog
    :visible="visible"
    @update:visible="$emit('update:visible', $event)"
    modal
    header="Codex Prompt Generator"
    :style="{ width: 'min(900px, 92vw)' }"
    class="bg-[#111622] text-slate-200 border border-slate-800"
  >
    <div class="space-y-4 pt-2">
      <SelectButton
        :modelValue="promptType"
        @update:modelValue="$emit('update:promptType', $event)"
        :options="['development', 'bug', 'image']"
        class="text-xs"
      />
      <Textarea
        :modelValue="generatedPrompt"
        readonly
        rows="15"
        class="w-full font-mono text-xs bg-[#0a0d14] text-slate-300 border-slate-800"
      />
      <div class="flex justify-end">
        <Button
          icon="pi pi-copy"
          :label="promptCopyState || 'Copy Prompt'"
          @click="copyPrompt"
          size="small"
          class="bg-indigo-600 border-none"
        />
      </div>
    </div>
  </Dialog>
</template>
