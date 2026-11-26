<script setup>
import Card from 'primevue/card'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'

defineProps({
  protectedItems: Array,
  localAIJobs: Array,
})
defineEmits(['manifest'])
</script>

<template>
  <div class="flex-1 p-6 overflow-y-auto codex-panel space-y-6 bg-[#0a0d14] text-slate-200">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-lg font-bold text-slate-100 flex items-center gap-2">
          <i class="pi pi-shield text-indigo-400"></i> Protected Registry & Local AI Governance
        </h2>
        <p class="text-xs text-slate-500">
          Approved paths are frozen and exported to external-AI governance manifests.
        </p>
      </div>
      <div class="flex gap-2">
        <Button
          size="small"
          icon="pi pi-file-export"
          label="Generate Manifests"
          @click="$emit('manifest')"
          class="bg-indigo-600 border-none"
        />
      </div>
    </div>

    <Card class="bg-[#111622] border border-slate-800/80">
      <template #title
        ><span class="text-xs font-bold text-slate-200"
          >Protected Items ({{ protectedItems.length }})</span
        ></template
      >
      <template #content>
        <DataTable
          :value="protectedItems"
          size="small"
          paginator
          :rows="5"
          responsiveLayout="scroll"
          class="text-xs"
        >
          <Column field="key" header="Key" />
          <Column field="item_type" header="Type" />
          <Column field="path" header="Path" />
          <Column field="reason" header="Reason" />
          <Column header="Frozen">
            <template #body="{ data }"
              ><Tag
                :value="data.frozen ? 'FROZEN' : 'OPEN'"
                :severity="data.frozen ? 'success' : 'warn'"
                class="text-[10px]"
            /></template>
          </Column>
        </DataTable>
      </template>
    </Card>

    <Card class="bg-[#111622] border border-slate-800/80">
      <template #title
        ><span class="text-xs font-bold text-slate-200">Background Local AI Jobs</span></template
      >
      <template #content>
        <DataTable :value="localAIJobs" size="small" responsiveLayout="scroll" class="text-xs">
          <Column field="id" header="ID" />
          <Column field="task_type" header="Task" />
          <Column field="status" header="Status" />
          <Column field="provider" header="Provider" />
          <Column field="created_at" header="Created" />
        </DataTable>
      </template>
    </Card>
  </div>
</template>
