<script setup>
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'

defineProps({
  chatMessages: Array,
  chatInput: String,
  busy: Boolean,
})
defineEmits(['update:chatInput', 'send'])
</script>

<template>
  <div class="flex-1 flex flex-col p-6 space-y-4 overflow-y-auto bg-[#0a0d14]">
    <div class="flex items-center justify-between border-b border-slate-800/60 pb-3">
      <div>
        <h2 class="text-lg font-bold text-slate-100 flex items-center gap-2">
          <i class="pi pi-comments text-indigo-400"></i> Codex AI Chat Panel
        </h2>
        <p class="text-xs text-slate-500">
          Direct interactive AI assistant with full project context awareness
        </p>
      </div>
    </div>

    <div class="flex-1 space-y-3 overflow-y-auto pr-2">
      <div
        v-if="!chatMessages.length"
        class="flex flex-col items-center justify-center h-full text-slate-500 text-xs"
      >
        <i class="pi pi-sparkles text-2xl mb-2 text-indigo-400"></i>
        No messages yet. Ask Codex anything about your models, APIs, or components!
      </div>
      <div
        v-for="(msg, i) in chatMessages"
        :key="i"
        :class="[
          'p-3.5 rounded-xl text-xs max-w-2xl shadow-sm leading-relaxed',
          msg.role === 'user'
            ? 'bg-indigo-600/20 text-indigo-100 ml-auto border border-indigo-500/30'
            : 'bg-[#111622] text-slate-200 mr-auto border border-slate-800/80',
        ]"
      >
        <div class="font-bold mb-1 text-[10px] text-slate-400 flex items-center gap-1.5">
          <i
            :class="
              msg.role === 'user' ? 'pi pi-user text-indigo-400' : 'pi pi-microchip text-sky-400'
            "
          ></i>
          {{ msg.role.toUpperCase() }}
        </div>
        <div class="whitespace-pre-wrap font-sans">{{ msg.content }}</div>
      </div>
    </div>

    <div class="flex gap-2 pt-2 border-t border-slate-800/60">
      <InputText
        :modelValue="chatInput"
        @update:modelValue="$emit('update:chatInput', $event)"
        @keyup.enter="$emit('send')"
        placeholder="Type a message or ask Codex..."
        class="flex-1 bg-[#131926] border-slate-800 text-xs text-slate-200"
      />
      <Button
        icon="pi pi-send"
        label="Send"
        :loading="busy"
        @click="$emit('send')"
        size="small"
        class="bg-indigo-600 hover:bg-indigo-500 border-none"
      />
    </div>
  </div>
</template>
