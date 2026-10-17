<script setup>
import { ref } from 'vue'
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import Tag from 'primevue/tag'

const activeTab = ref('features')

const mockFeatures = ref([
  { key: 'auth_jwt', name: 'JWT Authentication', category: 'Security', status: 'Approved' },
  { key: 'rag_search', name: 'RAG Vector Search', category: 'AI Engine', status: 'Active' },
  { key: 'django_orm', name: 'Django ORM Models', category: 'Backend', status: 'Approved' },
])

const mockTools = ref([
  { key: 'file_compiler', name: 'File Compiler Tool', type: 'System', state: 'Ready' },
  { key: 'schema_validator', name: 'Schema Validator', type: 'API', state: 'Active' },
])
</script>

<template>
  <div class="flex-1 p-6 overflow-y-auto codex-panel bg-[#0a0d14] text-slate-200 space-y-6">
    <div class="flex items-center justify-between border-b border-slate-800/60 pb-4">
      <div>
        <h2 class="text-lg font-bold text-slate-100 flex items-center gap-2">
          <i class="pi pi-bolt text-indigo-400"></i> Capability Registry & Management
        </h2>
        <p class="text-xs text-slate-500">
          Manage registered system features, tools, and autonomous AI agents.
        </p>
      </div>
    </div>

    <Tabs :value="activeTab" @update:value="activeTab = $event" class="codex-tabs">
      <TabList>
        <Tab value="features"><i class="pi pi-star mr-1.5"></i>Features</Tab>
        <Tab value="tools"><i class="pi pi-cog mr-1.5"></i>Tools</Tab>
      </TabList>
    </Tabs>

    <Card class="bg-[#111622] border border-slate-800/80">
      <template #content>
        <div v-if="activeTab === 'features'">
          <DataTable :value="mockFeatures" size="small" responsiveLayout="scroll" class="text-xs">
            <Column field="key" header="Key" />
            <Column field="name" header="Feature Name" />
            <Column field="category" header="Category" />
            <Column header="Status">
              <template #body="{ data }">
                <Tag :value="data.status" severity="success" class="text-[10px]" />
              </template>
            </Column>
          </DataTable>
        </div>

        <div v-else-if="activeTab === 'tools'">
          <DataTable :value="mockTools" size="small" responsiveLayout="scroll" class="text-xs">
            <Column field="key" header="Tool Key" />
            <Column field="name" header="Tool Name" />
            <Column field="type" header="Type" />
            <Column header="State">
              <template #body="{ data }">
                <Tag :value="data.state" severity="info" class="text-[10px]" />
              </template>
            </Column>
          </DataTable>
        </div>
      </template>
    </Card>
  </div>
</template>
