<script setup>
import { computed, onMounted, ref } from 'vue'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import ProgressBar from 'primevue/progressbar'
import Message from 'primevue/message'
import Dialog from 'primevue/dialog'
import { useCodexStore } from '@/stores/codex'
import codex from '@/services/codex'

const store = useCodexStore()
const query = ref('')
const busy = ref(false)
const validating = ref(false)
const selected = ref(null)
const result = ref(null)
const registryTab = ref('features')
const infoVisible = ref(false)
const infoItem = ref(null)

function showInfo(item) {
  infoItem.value = item
  infoVisible.value = true
}

const features = computed(() => filter(store.capabilityFeatures.value || store.capabilityFeatures))
const tools = computed(() => filter(store.capabilityTools.value || store.capabilityTools))
const agents = computed(() => filter(store.capabilityAgents.value || store.capabilityAgents))

function filter(rows) {
  const q = query.value.trim().toLowerCase()
  if (!q) return rows
  return rows.filter((row) => JSON.stringify(row).toLowerCase().includes(q))
}

async function validate() {
  validating.value = true
  try {
    result.value = await codex.registry.validate()
    await store.loadCapabilities()
  } finally {
    validating.value = false
  }
}

async function bootstrap() {
  busy.value = true
  try {
    result.value = await store.bootstrapCapabilities()
  } finally {
    busy.value = false
  }
}

async function runTool(item) {
  selected.value = item
  busy.value = true
  try { result.value = await codex.registry.executeTool(item.key, {}) } finally { busy.value = false }
}

async function runAgent(item) {
  selected.value = item
  busy.value = true
  try { result.value = await codex.registry.executeAgent(item.key, { request: 'Run a safe capability contract smoke test.' }) } finally { busy.value = false }
}

onMounted(async () => {
  if (!store.capabilitySummary) await store.loadCapabilities()
})
</script>

<template>
  <div class="codex-capabilities">
    <Card class="capability-hero">
      <template #title>
        <div class="capability-heading">
          <div><i class="pi pi-sparkles" /> Codex Capability Registry</div>
          <div class="capability-actions">
            <Tag :value="`${store.capabilitySummary?.features || 0} Features`" severity="info" />
            <Tag :value="`${store.capabilitySummary?.tools || 0} Tools`" severity="success" />
            <Tag :value="`${store.capabilitySummary?.agents || 0} Agents`" severity="warning" />
          </div>
        </div>
      </template>
      <template #content>
        <div class="capability-toolbar">
          <InputText v-model="query" placeholder="Search 900 Codex registry entries..." class="capability-search" />
          <Button label="Bootstrap" icon="pi pi-refresh" :loading="busy" outlined @click="bootstrap" />
          <Button label="Validate All" icon="pi pi-check-circle" :loading="validating" @click="validate" />
        </div>
        <div v-if="store.capabilityHealth" class="capability-health">
          <div v-for="(score, key) in store.capabilityHealth.scores" :key="key" class="health-item">
            <span>{{ key }}</span><strong>{{ score }}%</strong><ProgressBar :value="score" :showValue="false" />
          </div>
        </div>
        <Message v-if="result" :severity="result.passed === false ? 'warn' : 'success'" :closable="false">
          {{ result.passed === false ? 'Capability validation reported issues.' : 'Registry operation completed. Check the output to distinguish a catalog contract from a fully implemented action.' }}
        </Message>
      </template>
    </Card>

    <div class="registry-tabs">
      <Button label="300 Features" :severity="registryTab === 'features' ? 'primary' : 'secondary'" :outlined="registryTab !== 'features'" @click="registryTab = 'features'" />
      <Button label="300 Tools" :severity="registryTab === 'tools' ? 'primary' : 'secondary'" :outlined="registryTab !== 'tools'" @click="registryTab = 'tools'" />
      <Button label="300 Agents" :severity="registryTab === 'agents' ? 'primary' : 'secondary'" :outlined="registryTab !== 'agents'" @click="registryTab = 'agents'" />
    </div>

    <DataTable v-if="registryTab === 'features'" :value="features" paginator :rows="15" stripedRows responsiveLayout="scroll">
      <Column field="id" header="#" style="width: 80px" />
      <Column field="name" header="Feature" sortable />
      <Column field="category" header="Category" sortable />
      <Column field="status" header="Status"><template #body="slotProps"><Tag :value="slotProps.data.status" severity="success" /></template></Column>
      <Column field="protection_level" header="Protection" />
      <Column header="Info" style="width: 80px"><template #body="slotProps"><Button icon="pi pi-question-circle" text rounded size="small" @click="showInfo(slotProps.data)" /></template></Column>
    </DataTable>

    <DataTable v-else-if="registryTab === 'tools'" :value="tools" paginator :rows="15" stripedRows responsiveLayout="scroll">
      <Column field="key" header="Key" sortable />
      <Column field="name" header="Tool" sortable />
      <Column field="category" header="Category" sortable />
      <Column field="risk" header="Risk" />
      <Column header="Info" style="width: 70px"><template #body="slotProps"><Button icon="pi pi-question-circle" text rounded size="small" @click="showInfo(slotProps.data)" /></template></Column>
      <Column header="Execution" style="width: 140px"><template #body="slotProps"><Button label="Run" icon="pi pi-play" size="small" text @click="runTool(slotProps.data)" /></template></Column>
    </DataTable>

    <DataTable v-else :value="agents" paginator :rows="15" stripedRows responsiveLayout="scroll">
      <Column field="key" header="Key" sortable />
      <Column field="name" header="Agent" sortable />
      <Column field="category" header="Category" sortable />
      <Column field="risk" header="Risk" />
      <Column field="tools" header="Tools"><template #body="slotProps">{{ slotProps.data.tools?.length || 0 }}</template></Column>
      <Column header="Info" style="width: 70px"><template #body="slotProps"><Button icon="pi pi-question-circle" text rounded size="small" @click="showInfo(slotProps.data)" /></template></Column>
      <Column header="Execution" style="width: 140px"><template #body="slotProps"><Button label="Run" icon="pi pi-play" size="small" text @click="runAgent(slotProps.data)" /></template></Column>
    </DataTable>

    <Card v-if="selected" class="capability-result">
      <template #title>Last Execution</template>
      <template #content><pre>{{ JSON.stringify(result, null, 2) }}</pre></template>
    </Card>

    <Dialog v-model:visible="infoVisible" modal header="Capability Information" :style="{ width: 'min(760px, 92vw)' }">
      <div v-if="infoItem" class="space-y-3 text-sm">
        <div><strong>{{ infoItem.name }}</strong> <Tag :value="infoItem.key" severity="info" /></div>
        <p class="text-slate-500">{{ infoItem.purpose || 'No purpose description supplied.' }}</p>
        <div class="grid gap-2 md:grid-cols-2">
          <pre class="p-3 bg-slate-950 rounded text-xs overflow-auto">{{ JSON.stringify(infoItem.input_schema || infoItem.permissions || {}, null, 2) }}</pre>
          <pre class="p-3 bg-slate-950 rounded text-xs overflow-auto">{{ JSON.stringify(infoItem.output_schema || infoItem.validation || {}, null, 2) }}</pre>
        </div>
      </div>
    </Dialog>
  </div>
</template>

<style src="@/assets/scss/Codex/_CodexCapabilities.scss"></style>
