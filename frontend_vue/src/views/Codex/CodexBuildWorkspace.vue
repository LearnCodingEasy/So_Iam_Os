<script setup>
import { computed, onMounted, ref } from 'vue'
import { VueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Message from 'primevue/message'
import codex from '@/services/codex'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'

const loading = ref(false)
const error = ref('')
const payload = ref(null)
const selectedNode = ref(null)
const nodes = computed(() => payload.value?.graph?.nodes || [])
const edges = computed(() => payload.value?.graph?.edges || [])

async function refresh() {
  loading.value = true
  error.value = ''
  try {
    payload.value = await codex.buildWorkspace()
  } catch (err) {
    error.value = err?.response?.data?.detail || err?.message || 'Could not load the build graph.'
  } finally {
    loading.value = false
  }
}
function statusSeverity(status) {
  if (status === 'passed' || status === 'approved') return 'success'
  if (status === 'failed' || status === 'blocked') return 'danger'
  if (status === 'running') return 'info'
  return 'secondary'
}
onMounted(refresh)
</script>

<template>
  <section class="codex-build-workspace flex min-w-0 flex-1 flex-col gap-3 p-4">
    <header class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h2 class="text-lg font-semibold">Build & Project Lifecycle</h2>
        <p class="text-xs text-surface-500">Live repository discovery · execution is never inferred from file presence</p>
      </div>
      <Button label="Refresh project graph" icon="pi pi-refresh" size="small" :loading="loading" @click="refresh" />
    </header>
    <Message v-if="error" severity="error" :closable="false">{{ error }}</Message>
    <div class="grid min-h-0 flex-1 gap-3 xl:grid-cols-[minmax(0,1fr)_290px]">
      <div class="codex-build-canvas overflow-hidden rounded-xl border border-surface-200 dark:border-surface-700">
        <VueFlow :nodes="nodes" :edges="edges" fit-view-on-init @node-click="(_, node) => selectedNode = node">
          <Background pattern-color="#64748b" :gap="18" />
          <Controls />
          <MiniMap pannable zoomable />
        </VueFlow>
      </div>
      <aside class="rounded-xl border border-surface-200 p-4 dark:border-surface-700">
        <h3 class="mb-3 font-semibold">Node inspector</h3>
        <template v-if="selectedNode">
          <div class="mb-2 break-words font-medium">{{ selectedNode.data?.label || selectedNode.id }}</div>
          <p class="mb-3 text-sm text-surface-500">{{ selectedNode.data?.description || 'Project graph node' }}</p>
          <Tag :value="selectedNode.data?.status || 'discovered'" :severity="statusSeverity(selectedNode.data?.status)" />
          <p class="mt-3 text-xs text-surface-500">Progress: {{ selectedNode.data?.progress ?? 0 }}%</p>
          <p class="mt-2 text-xs">Execution verified: {{ selectedNode.data?.execution_verified ? 'Yes' : 'No' }}</p>
          <div v-if="selectedNode.data?.checks" class="mt-3 space-y-2">
            <div v-for="item in selectedNode.data.checks" :key="item" class="break-all text-xs">
              <i :class="selectedNode.data.found?.includes(item) ? 'pi pi-check-circle text-emerald-500' : 'pi pi-minus-circle text-surface-400'" /> {{ item }}
            </div>
          </div>
        </template>
        <p v-else class="text-sm text-surface-500">Select a node to inspect its source checks and status.</p>
        <div class="mt-5 border-t border-surface-200 pt-3 text-xs text-surface-500 dark:border-surface-700">
          File discovery is informational. A node can only become passed after a real execution record and verification evidence exist.
        </div>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.codex-build-canvas { min-height: 460px; height: 100%; }
.codex-build-canvas :deep(.vue-flow) { background: var(--p-content-background, #fff); }
.codex-build-canvas :deep(.vue-flow__node) { max-width: 220px; }
</style>
