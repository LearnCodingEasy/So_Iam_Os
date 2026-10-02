<script setup>
/*
// ===================================================
WorkflowCanvas.vue
src/components/Automation/Workflow/WorkflowCanvas.vue

المسؤولية: عرض الـ VueFlow canvas فقط
❌ لا تحتوي على API calls
❌ لا تحتوي على Pinia stores
✅ تستقبل nodes/edges كـ props
✅ تطلع events للـ AutomationView

الاستخدام في AutomationView:
<WorkflowCanvas
  :nodes="nodes"
  :edges="edges"
  @node-click="onNodeSelect"
  @connect="onConnect"
  @drop="onDrop"
  @node-drag-stop="onNodeDragStop"
/>
===================================================
*/
import { computed } from 'vue'
import { VueFlow, Panel } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import CustomNode from '@/components/Automation/Node/CustomNode.vue'
import CustomEdge from '@/components/Automation/Edge/CustomEdge.vue'

// ─── Props ─────────────────────────────────────────
const props = defineProps({
  nodes: { type: Array, default: () => [] },
  edges: { type: Array, default: () => [] },
  isLoading: { type: Boolean, default: false },
  currentWorkflowId: { type: String, default: null },
})
console.log('props: ', props)

// ─── Emits ─────────────────────────────────────────
// كل حدث بيطلع للـ AutomationView اللي بيتعامل مع الـ logic
const emit = defineEmits([
  'update:nodes',
  'update:edges',
  'node-click', // المستخدم ضغط على node
  'connect', // المستخدم ربط node بـ node
  'drop', // المستخدم drop عنصر على الـ canvas
  'drag-over', // drag فوق الـ canvas
  'node-drag-stop', // المستخدم خلّص تحريك node
  'run-task', // تشغيل node
  'delete-node', // حذف node
  'update-node-action', // تعديل action من داخل الـ CustomNode
])

// ─── Node/Edge Types ───────────────────────────────
const nodeTypes = computed(() => ({ custom: CustomNode }))
const edgeTypes = computed(() => ({ custom: CustomEdge }))

// ─── Handlers ──────────────────────────────────────
const onNodeDragStop = ({ node }) => emit('node-drag-stop', node)
const onNodeClick = (event) => emit('node-click', event)
const onConnect = (params) => emit('connect', params)
const onDrop = (e) => emit('drop', e)
const onDragOver = (e) => {
  e.preventDefault()
  e.dataTransfer.dropEffect = 'move'
  emit('drag-over', e)
}
</script>

<template>
  <!-- Loading Overlay -->
  <div v-if="isLoading" class="canvas-loading-overlay">
    <i class="pi pi-spin pi-spinner text-4xl text-blue-400"></i>
    <span class="text-sm text-slate-400 mt-2">جاري التحميل...</span>
  </div>

  <!-- Empty State -->
  <div v-else-if="!currentWorkflowId" class="canvas-empty-state">
    <i class="pi pi-sitemap text-5xl text-slate-600 mb-3"></i>
    <p class="text-slate-400 text-lg">اختر Workflow من القائمة أو أنشئ واحد جديد</p>
  </div>

  <!-- VueFlow Canvas -->
  <VueFlow
    v-else
    class="workflow-canvas"
    :nodes="nodes"
    :edges="edges"
    :node-types="nodeTypes"
    :edge-types="edgeTypes"
    :pan-on-drag="[1]"
    :pan-on-scroll="true"
    :zoom-on-scroll="false"
    @node-click="onNodeClick"
    @dragover="onDragOver"
    @drop="onDrop"
    @connect="onConnect"
    @nodeDragStop="onNodeDragStop"
    @update:nodes="$emit('update:nodes', $event)"
    @update:edges="$emit('update:edges', $event)"
  >
    <!-- شبكة الخلفية -->
    <Background variant="dots" :gap="20" />

    <!-- أدوات التحكم (zoom in/out/fit) -->
    <Controls />

    <!-- خريطة مصغرة -->
    <MiniMap :pannable="true" :zoomable="true" />

    <!-- Slot للـ Toolbar — بيتحكم فيها AutomationView -->
    <Panel position="top-left">
      <slot name="toolbar" />
    </Panel>

    <!-- Node Template -->
    <template #node-custom="props">
      <CustomNode
        v-bind="props"
        @run-task="emit('run-task', $event)"
        @delete-node="emit('delete-node', $event)"
        @update-node-action="emit('update-node-action', $event)"
      />
    </template>

    <!-- Edge Template -->
    <template #edge-custom="props">
      <CustomEdge v-bind="props" />
    </template>
  </VueFlow>
</template>

<style scoped>
.workflow-canvas {
  width: 100%;
  height: 100%;
  background: #0f172a;
}

.canvas-loading-overlay,
.canvas-empty-state {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #0f172a;
  border-radius: 12px;
}
</style>
