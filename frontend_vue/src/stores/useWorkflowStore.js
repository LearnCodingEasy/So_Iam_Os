// ============================================================
//  useWorkflowStore.js
//  src/stores/useWorkflowStore.js
//
//  المسؤوليات:
//   - CRUD الـ Workflows
//   - Save / AutoSave
//   - تحميل الـ nodes و edges من الـ backend
//   - Auto Layout (dagre)
// ============================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { debounce } from 'lodash'
import dagre from 'dagre'
import automationService from '@/services/AutomationService'

export const useWorkflowStore = defineStore('workflow', () => {
  // ─────────────────────────────────────────
  // State
  // ─────────────────────────────────────────
  const workflows = ref([])
  const currentWorkflow = ref(null)
  const nodes = ref([])
  const edges = ref([])

  const isLoading = ref(false)
  const isSaving = ref(false)
  const isInitialized = ref(false)

  const formWorkflow = ref({ name: '', description: '', status: 'draft' })

  // ─────────────────────────────────────────
  // Getters
  // ─────────────────────────────────────────
  const currentWorkflowId = computed(() => currentWorkflow.value?.id ?? null)

  const workflowById = (id) => workflows.value.find((w) => w.id === id) ?? null

  // ─────────────────────────────────────────
  // Helpers — Map backend node → VueFlow node
  // ─────────────────────────────────────────
  function mapNode(n) {
    return {
      id: n.id,
      type: 'custom',
      position: n.position || {
        x: n.data?.node?.position_x ?? 0,
        y: n.data?.node?.position_y ?? 0,
      },
      data: {
        label: n.data?.label ?? n.data?.node?.label ?? '',
        node: {
          backend_id: n.id,
          id: n.id,
          program_name: n.data?.node?.program_name ?? '',
          element_name: n.data?.node?.element_name ?? '',
          node_type: n.data?.node?.node_type ?? '',
          label: n.data?.node?.label ?? '',
          config: n.data?.node?.config ?? null,
          program: n.data?.node?.program ?? null,
          element: n.data?.node?.element ?? null,
          status: 'idle',
        },
        actions: n.data?.actions ?? [],
      },
    }
  }

  function mapEdge(e) {
    return {
      id: e.id,
      source: e.source,
      target: e.target,
      type: e.type || 'custom',
      data: e.data || {},
    }
  }

  // ─────────────────────────────────────────
  // Load All Workflows
  // ─────────────────────────────────────────
  async function loadWorkflows() {
    try {
      const { data } = await automationService.listWorkflows()
      workflows.value = data
    } catch (err) {
      console.error('loadWorkflows:', err)
      throw err
    }
  }

  // ─────────────────────────────────────────
  // Load Workflow Events (nodes + edges)
  // ─────────────────────────────────────────
  async function loadWorkflowEvents(workflowId) {
    if (!workflowId) return
    nodes.value = []
    edges.value = []

    // بيانات الـ workflow نفسه
    const { data: wfData } = await automationService.getWorkflow(workflowId)
    currentWorkflow.value = wfData
    formWorkflow.value = {
      name: wfData.name,
      description: wfData.description,
      status: wfData.status,
    }

    // الـ nodes و edges
    try {
      const { data } = await automationService.getWorkflow_full_events(workflowId)
      nodes.value = (data.nodes || []).map(mapNode)
      edges.value = (data.edges || []).map(mapEdge)
    } catch (err) {
      console.error('loadWorkflowEvents:', err)
      throw err
    }
  }

  // ─────────────────────────────────────────
  // Select Workflow
  // ─────────────────────────────────────────
  async function selectWorkflow(id) {
    if (!id) return
    isLoading.value = true
    cancelAutoSave()
    try {
      await loadWorkflowEvents(id)
    } finally {
      isLoading.value = false
    }
  }

  // ─────────────────────────────────────────
  // Create Workflow
  // ─────────────────────────────────────────
  async function createWorkflow(payload) {
    const { data } = await automationService.createWorkflow(payload)
    workflows.value.unshift(data)
    currentWorkflow.value = data
    nodes.value = []
    edges.value = []
    await loadWorkflowEvents(data.id)
    return data
  }

  // ─────────────────────────────────────────
  // Update Workflow (status / name / description)
  // ─────────────────────────────────────────
  async function updateWorkflow(id, payload) {
    const { data } = await automationService.updateWorkflow(id, payload)
    const idx = workflows.value.findIndex((w) => w.id === id)
    if (idx !== -1) workflows.value[idx] = { ...workflows.value[idx], ...data }
    if (currentWorkflow.value?.id === id)
      currentWorkflow.value = { ...currentWorkflow.value, ...data }
    return data
  }

  // ─────────────────────────────────────────
  // Delete Workflow
  // ─────────────────────────────────────────
  async function deleteWorkflow(id) {
    await automationService.deleteWorkflow(id)
    workflows.value = workflows.value.filter((w) => w.id !== id)
    if (currentWorkflow.value?.id === id) {
      currentWorkflow.value = null
      nodes.value = []
      edges.value = []
    }
    // إعادة تحميل القائمة
    await loadWorkflows()
  }

  // ─────────────────────────────────────────
  // Save Workflow (save_all)
  //
  //  القاعدة: لو الـ ActionPanel مفتوح → احفظ label الـ node المختار
  //           وبعد الـ reload رجّعه تاني
  // ─────────────────────────────────────────
  async function saveWorkflow({ selectedNode = null, showActionPanel = false } = {}) {
    if (!currentWorkflowId.value) return
    if (isLoading.value || isSaving.value) return

    const exists = workflows.value.find((w) => w.id === currentWorkflowId.value)
    if (!exists) return

    isSaving.value = true
    isLoading.value = true
    cancelAutoSave()

    // نحتفظ بـ label عشان نرجعه بعد الـ reload
    const openNodeLabel = showActionPanel ? (selectedNode?.data?.node?.label ?? null) : null

    try {
      const payload = {
        nodes: nodes.value.map((n) => ({
          id: n.id,
          position: n.position,
          data: n.data,
          actions: n.data?.actions ?? [],
        })),
        edges: edges.value.map((e) => ({
          id: e.id,
          source: e.source,
          target: e.target,
          data: e.data,
        })),
      }

      await automationService.saveWorkflowAll(currentWorkflowId.value, payload)
      await loadWorkflowEvents(currentWorkflowId.value)

      // أرجع الـ selectedNode بعد الـ reload
      if (openNodeLabel && showActionPanel) {
        const refreshed = nodes.value.find((n) => n.data?.node?.label === openNodeLabel)
        return refreshed ?? null // الـ view بتحدّث selectedNode بنفسها
      }
    } finally {
      isLoading.value = false
      isSaving.value = false
    }
  }

  // ─────────────────────────────────────────
  // AutoSave — debounced 500ms
  // ─────────────────────────────────────────
  const debouncedAutoSave = debounce(function (opts) {
    if (!isInitialized.value) return
    if (!currentWorkflowId.value) return
    if (isLoading.value) return
    saveWorkflow(opts)
  }, 500)

  function triggerAutoSave(opts = {}) {
    debouncedAutoSave(opts)
  }

  function cancelAutoSave() {
    debouncedAutoSave.cancel()
  }

  // ─────────────────────────────────────────
  // Clear Canvas
  // ─────────────────────────────────────────
  function clearCanvas() {
    nodes.value = []
    edges.value = []
  }

  // ─────────────────────────────────────────
  // Auto Layout (dagre)
  // ─────────────────────────────────────────
  function autoLayout(direction = 'TB') {
    const g = new dagre.graphlib.Graph()
    g.setGraph({ rankdir: direction, nodesep: 50, ranksep: 80 })
    g.setDefaultEdgeLabel(() => ({}))

    nodes.value.forEach((n) => g.setNode(n.id, { width: 180, height: 60 }))
    edges.value.forEach((e) => g.setEdge(e.source, e.target))
    dagre.layout(g)

    nodes.value = nodes.value.map((node) => {
      const pos = g.node(node.id)
      return { ...node, position: { x: pos.x - 90, y: pos.y - 30 } }
    })
  }

  // ─────────────────────────────────────────
  // Return
  // ─────────────────────────────────────────
  return {
    // state
    workflows,
    currentWorkflow,
    currentWorkflowId,
    nodes,
    edges,
    isLoading,
    isSaving,
    isInitialized,
    formWorkflow,

    // getters
    workflowById,

    // actions
    loadWorkflows,
    loadWorkflowEvents,
    selectWorkflow,
    createWorkflow,
    updateWorkflow,
    deleteWorkflow,
    saveWorkflow,
    triggerAutoSave,
    cancelAutoSave,
    clearCanvas,
    autoLayout,
  }
})
