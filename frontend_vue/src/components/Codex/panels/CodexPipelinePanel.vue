<script setup>
import Card from 'primevue/card'
import Button from 'primevue/button'
import Tag from 'primevue/tag'

defineProps({
  workflow: Object,
})
defineEmits(['refresh'])
</script>

<template>
  <div class="flex-1 p-6 overflow-y-auto codex-panel bg-[#0a0d14] text-slate-200 space-y-4">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-lg font-bold text-slate-100 flex items-center gap-2">
          <i class="pi pi-share-alt text-indigo-400"></i> Workflow & Dependency Progression
        </h2>
        <p class="text-xs text-slate-500">
          Library Setup → Configuration → Core Code → Integration → Testing
        </p>
      </div>
      <Button
        size="small"
        icon="pi pi-refresh"
        label="Verify Pipeline"
        @click="$emit('refresh')"
        class="p-button-outlined"
      />
    </div>

    <div class="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
      <Card
        v-for="step in workflow.steps"
        :key="step.key"
        class="bg-[#111622] border border-slate-800/80 rounded-xl"
      >
        <template #content>
          <div class="flex items-start justify-between gap-2">
            <div>
              <div class="text-[10px] text-slate-500 font-mono">
                {{ String(step.order).padStart(2, '0') }}
              </div>
              <div class="font-semibold text-xs text-slate-200 mt-1">{{ step.name }}</div>
            </div>
            <Tag
              :value="step.status"
              :severity="
                step.status === 'completed'
                  ? 'success'
                  : step.status === 'blocked'
                    ? 'danger'
                    : 'warn'
              "
              class="text-[10px]"
            />
          </div>
          <p class="text-[11px] text-slate-400 mt-3 leading-relaxed">{{ step.description }}</p>
          <div class="mt-3 pt-3 border-t border-slate-800/60 text-[10px] text-slate-500 space-y-1">
            <div v-for="(e, key) in step.evidence" :key="key" class="flex justify-between gap-2">
              <span class="truncate">{{ key }}</span>
              <i
                :class="e.exists ? 'pi pi-check text-emerald-400' : 'pi pi-times text-red-400'"
              ></i>
            </div>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>
