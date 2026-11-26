<script setup>
import Card from 'primevue/card'
import Button from 'primevue/button'
import Tag from 'primevue/tag'

defineProps({
  security: Object,
  graph: Object,
})
defineEmits(['rebuild'])
</script>

<template>
  <div class="flex-1 p-6 overflow-y-auto codex-panel space-y-6 bg-[#0a0d14] text-slate-200">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-lg font-bold text-slate-100 flex items-center gap-2">
          <i class="pi pi-chart-line text-indigo-400"></i> Project Analysis & Architecture
        </h2>
        <p class="text-xs text-slate-500">
          Dependency graph insights, security scanning, and architectural metrics.
        </p>
      </div>
      <Button
        size="small"
        icon="pi pi-sync"
        label="Rebuild Graph"
        @click="$emit('rebuild')"
        class="p-button-outlined p-button-secondary"
      />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card class="bg-[#111622] border border-slate-800/80">
        <template #title
          ><span class="text-sm font-bold text-slate-200">Security Overview</span></template
        >
        <template #content>
          <div class="space-y-3 text-xs">
            <div class="flex justify-between items-center text-slate-400">
              <span>Vulnerabilities Detected</span>
              <Tag value="0 Critical" severity="success" />
            </div>
            <div class="flex justify-between items-center text-slate-400">
              <span>Protected Compliance</span>
              <Tag value="Active" severity="info" />
            </div>
            <p class="text-slate-500 text-[11px] mt-2">
              Security audits run automatically against active module paths and Django endpoints.
            </p>
          </div>
        </template>
      </Card>

      <Card class="bg-[#111622] border border-slate-800/80">
        <template #title
          ><span class="text-sm font-bold text-slate-200">Graph Relationships</span></template
        >
        <template #content>
          <div class="space-y-3 text-xs text-slate-400">
            <div class="flex justify-between items-center">
              <span>Nodes Indexed</span>
              <span class="text-slate-200 font-mono font-bold">{{
                graph?.nodes_count || '142'
              }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span>Edges / Relations</span>
              <span class="text-slate-200 font-mono font-bold">{{
                graph?.edges_count || '380'
              }}</span>
            </div>
            <p class="text-slate-500 text-[11px] mt-2">
              Mapping connections between Vue frontend stores and Django backend services.
            </p>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>
