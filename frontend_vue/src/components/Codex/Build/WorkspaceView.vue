<script setup>
import { ref } from 'vue'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Tag from 'primevue/tag'

const buildSteps = ref([
  {
    id: 1,
    name: 'System Architecture Generation',
    status: 'COMPLETED',
    desc: 'Django backend models and Vue 3 frontend components mapped.',
  },
  {
    id: 2,
    name: 'Dependency & Package Verification',
    status: 'IN_PROGRESS',
    desc: 'Validating PrimeVue, TailwindCSS, and Pinia stores.',
  },
  {
    id: 3,
    name: 'API Contract & Schema Sync',
    status: 'PLANNED',
    desc: 'Ensuring Swagger and JWT security tokens match endpoints.',
  },
])
</script>

<template>
  <div class="flex-1 p-6 overflow-y-auto codex-panel bg-[#0a0d14] text-slate-200 space-y-6">
    <div class="flex items-center justify-between border-b border-slate-800/60 pb-4">
      <div>
        <h2 class="text-lg font-bold text-slate-100 flex items-center gap-2">
          <i class="pi pi-sitemap text-indigo-400"></i> Codex Build Workspace
        </h2>
        <p class="text-xs text-slate-500">
          Autonomous multi-agent code generation and system architecture compilation.
        </p>
      </div>
      <Button
        size="small"
        icon="pi pi-play"
        label="Run Build Pipeline"
        class="bg-indigo-600 border-none hover:bg-indigo-500"
      />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card
        v-for="step in buildSteps"
        :key="step.id"
        class="bg-[#111622] border border-slate-800/80 rounded-xl"
      >
        <template #content>
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs font-mono text-slate-500">Phase 0{{ step.id }}</span>
            <Tag
              :value="step.status"
              :severity="
                step.status === 'COMPLETED'
                  ? 'success'
                  : step.status === 'IN_PROGRESS'
                    ? 'warn'
                    : 'secondary'
              "
              class="text-[10px]"
            />
          </div>
          <h3 class="font-bold text-sm text-slate-200 mb-2">{{ step.name }}</h3>
          <p class="text-xs text-slate-400 leading-relaxed">{{ step.desc }}</p>
        </template>
      </Card>
    </div>
  </div>
</template>
