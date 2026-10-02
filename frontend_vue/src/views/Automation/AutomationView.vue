<script setup>
// ==================================================
//  AutomationView.vue
//  src/views/AutomationView.vue
//
//  المسؤولية: المتحكم الرئيسي — يربط كل الـ components ببعض
//
//  ❌ مش المسؤولية:
//    - API calls مباشرة (ده في الـ stores + services)
//    - HTML ضخم للـ Programs/Elements/Tasks (ده في NodeMarketplace)
//    - VueFlow setup (ده في WorkflowCanvas)
//    - Toolbar buttons (ده في WorkflowToolbar)
//
//  ✅ المسؤولية:
//    - Dialog visibility (createProgramVisible, ...)
//    - selectedNode + showActionPanel
//    - ربط الـ events من الـ components بالـ stores
//    - onMounted data loading
// ==================================================

// ─── Vue ─────────────────────────────────────────-
import { ref, reactive, watch, onMounted, onUnmounted } from 'vue'
import { useVueFlow } from '@vue-flow/core'
import { debounce } from 'lodash'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
// ─── Stores ───────────────────────────────────────
import { useProgramStore } from '@/stores/useProgramStore'
import { useProgramElementStore } from '@/stores/useProgramElementStore'
import { useWorkflowStore } from '@/stores/useWorkflowStore'
import { useTaskStore } from '@/stores/useTaskStore'
// ─── Services ─────────────────────────────────────
import automationService from '@/services/AutomationService'
// ─── Composables ──────────────────────────────────
import { useApiTracker } from '@/composables/useApiTracker'
// ─── Extracted Components ─────────────────────────
import NodeMarketplace from '@/components/Automation/Node/NodeMarketplace.vue'
import NodeVisualBuilder from '@/components/Automation/Node/NodeVisualBuilder.vue'
import WorkflowCanvas from '@/components/Automation/Workflow/WorkflowCanvas.vue'
import WorkflowToolbar from '@/components/Automation/Workflow/WorkflowToolbar.vue'
import WorkflowVersions from '@/components/Automation/Workflow/WorkflowVersions.vue'
import ActionPanel from '@/components/Automation/Action/ActionPanel.vue'
import CreateProgram from '@/components/Automation/Program/CreateProgram.vue'
import EditProgram from '@/components/Automation/Program/EditProgram.vue'
import LiveConsole from '@/components/Automation/Execution/LiveConsole.vue'
import RealtimeGraph from '@/components/Automation/Execution/RealtimeGraph.vue'
import ApiFlowPanel from '@/components/Automation/ApiFlowPanel.vue'
import AIPrompt from '@/components/Automation/AIPrompt.vue'
import AIAsk from '@/components/AI/AIChat.vue'
// ─── Plugin Registry ──────────────────────────────
// بيستخدمه buildPayloadFromUI بدل الـ switch القديم
import registry from '@/plugins/PluginRegistry'
// ==================================================
// 🔌 Init
// ==================================================
const toast = useToast()
const confirm = useConfirm()
const { project } = useVueFlow()
const tracker = useApiTracker()
const programStore = useProgramStore()
const elementStore = useProgramElementStore()
const workflowStore = useWorkflowStore()
const taskStore = useTaskStore()
// ==================================================
// 🛠️ useAsyncAction — UX Engine
// ==================================================
// كل API call بيمر عبر tracker.execute → يظهر في ApiFlowPanel
// ==================================================
function useAsyncAction() {
  const loading = ref(false)

  const run = async (apiFn, options = {}) => {
    if (loading.value) return // guard ضد double-click

    const {
      validate = null,
      successSummary = null,
      successDetail = null,
      errorSummary = 'حصل خطأ',
      onSuccess = null,
      onError = null,
    } = options

    if (validate) {
      const validErr = validate()
      if (validErr) {
        toast.add({
          severity: 'warn',
          summary: '⚠️ تحقق من البيانات',
          detail: validErr,
          life: 4000,
        })
        return
      }
    }

    loading.value = true
    try {
      const result = await tracker.execute({ serviceFn: apiFn })
      if (successSummary)
        toast.add({
          severity: 'success',
          summary: `✅ ${successSummary}`,
          detail: successDetail,
          life: 4000,
        })
      if (onSuccess) await onSuccess(result)
      return result
    } catch (err) {
      const status = err?.response?.status
      const body = err?.response?.data
      let detail = err?.message || 'خطأ غير متوقع'

      if (status === 400 && body && typeof body === 'object')
        detail = Object.entries(body)
          .map(([f, m]) => `${f}: ${Array.isArray(m) ? m[0] : m}`)
          .slice(0, 3)
          .join(' | ')
      else if (status === 401) detail = 'انتهت جلستك — سجّل دخول من جديد'
      else if (status === 403) detail = 'مش عندك صلاحية لهذه العملية'
      else if (status === 404) detail = 'العنصر المطلوب غير موجود'
      else if (status === 413) detail = 'الملف كبير جداً — الحد الأقصى 5MB'
      else if (status === 500) detail = 'خطأ في السيرفر — حاول مرة أخرى'

      toast.add({ severity: 'error', summary: `❌ ${errorSummary}`, detail, life: 6000 })
      if (onError) onError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return { run, loading }
}
// instance مستقلة لكل domain — loading states منفصلة
const programAction = useAsyncAction()
const elementAction = useAsyncAction()
const workflowAction = useAsyncAction()
const taskAction = useAsyncAction()
const nodeAction = useAsyncAction()

// ==================================================
// 🎨 UI State (خاص بالـ View فقط — مش في الـ store)
// ==================================================

// ─── Dialog Visibility ────────────────────────────
const createProgramVisible = ref(false)
const editProgramVisible = ref(false)
const createProgramElementVisible = ref(false)
const editProgramElementVisible = ref(false)
const createTaskVisible = ref(false)
const editTaskVisible = ref(false)
const showVersions = ref(false)
const showRealtimeGraph = ref(false)

// ─── Canvas State ─────────────────────────────────
const showActionPanel = ref(false)
const newActionTypeForPanel = ref('open_program')
const selectedNode = ref(null)
const draggedItem = ref(null)
const isLayouting = ref(false)

// ─── NodeVisualBuilder ────────────────────────────
const showBuilder = ref(false)
const builderPlugin = ref(null)

// ─── Delays (simple — no store needed) ────────────
const delays = ref([])

// ─── Position Sync Queue (bypass tracker) ─────────
const syncState = reactive({ updateQueue: [], isSyncing: false })

// ─── ApiFlowPanel state ───────────────────────────
const { stages, result, error: trackerError, meta } = tracker
console.log('result: ', result)

// ==================================================
// 🍞 Toast shorthand
// ==================================================
const showToast = (severity, summary, detail, life = 4000) => {
  const icon = { success: '✅', error: '❌', warn: '⚠️', info: 'ℹ️' }[severity] ?? ''
  toast.add({ severity, summary: `${icon} ${summary}`, detail, life })
}

// ==================================================
// ══════════════════════════════════════════════════
// 1️⃣ PROGRAMS
// ══════════════════════════════════════════════════
// programStore: programs[], form, CRUD, open/close/focus/maximize
// View:         dialog visibility + useAsyncAction
// ==================================================
const createProgram = () =>
  programAction.run(() => programStore.createProgram(), {
    validate: () => programStore.validateForm(),
    successSummary: 'تم إنشاء البرنامج',
    successDetail: `"${programStore.form.name}" أُنشئ بنجاح`,
    errorSummary: 'فشل إنشاء البرنامج',
    onSuccess: () => {
      createProgramVisible.value = false
    },
  })

const openEditProgram = async (id) => {
  try {
    await programStore.loadProgram(id)
    editProgramVisible.value = true
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
  }
}

const editProgram = () =>
  programAction.run(() => programStore.updateProgram(programStore.currentProgramId), {
    validate: () => programStore.validateForm(),
    successSummary: 'تم تحديث البرنامج',
    errorSummary: 'فشل تحديث البرنامج',
    onSuccess: () => {
      editProgramVisible.value = false
    },
  })

const confirmDeleteProgram = (program) => {
  confirm.require({
    message: `هل أنت متأكد من حذف "${program.name}"؟`,
    header: '⚠️ تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'نعم، احذف',
    rejectLabel: 'إلغاء',
    accept: () =>
      programAction.run(() => programStore.deleteProgram(program.id), {
        successSummary: 'تم الحذف',
        errorSummary: 'فشل الحذف',
      }),
  })
}

// ==================================================
// 2️⃣ PROGRAM ELEMENTS
// ==================================================
const createProgramElement = () =>
  elementAction.run(() => elementStore.createElement(), {
    validate: () => elementStore.validateForm(),
    successSummary: 'تم إنشاء العنصر',
    errorSummary: 'فشل إنشاء العنصر',
    onSuccess: () => {
      createProgramElementVisible.value = false
    },
  })

const openEditProgramElement = async (id) => {
  try {
    await elementStore.loadElement(id)
    editProgramElementVisible.value = true
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
  }
}

const editProgramElement = () =>
  elementAction.run(() => elementStore.updateElement(elementStore.currentElementId), {
    validate: () => elementStore.validateForm(),
    successSummary: 'تم تحديث العنصر',
    errorSummary: 'فشل تحديث العنصر',
    onSuccess: () => {
      editProgramElementVisible.value = false
    },
  })

const confirmDeleteProgramElement = (el) => {
  confirm.require({
    message: `هل تريد حذف "${el.name}"؟`,
    header: '⚠️ تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'نعم، احذف',
    rejectLabel: 'إلغاء',
    accept: () =>
      elementAction.run(() => elementStore.deleteElement(el.id), {
        successSummary: 'تم الحذف',
        errorSummary: 'فشل الحذف',
      }),
  })
}

const selectedWindow = ref(null)

const handleSmartScan = () =>
  elementAction.run(
    async () => {
      const pattern = selectedWindow.value?.suggested_pattern
      const programId = elementStore.form.program
      console.log('🔍 pattern:', pattern)
      console.log('🔍 programId:', programId)

      // ✅ tracker.execute → يظهر في ApiFlowPanel
      const result = await tracker.execute({
        serviceFn: () => automationService.scanProgramElements(programId, pattern),
      })

      // ✅ حدّث قائمة العناصر بعد الحفظ
      await elementStore.loadElements()
      return result
    },
    {
      validate: () =>
        !elementStore.form.program
          ? 'اختر برنامج أولاً'
          : !selectedWindow.value
            ? 'اختر النافذة'
            : null,
      successSummary: 'تم المسح بنجاح',
      successDetail: `تم حفظ العناصر في قاعدة البيانات`,
      errorSummary: 'فشل المسح - تأكد أن البرنامج مفتوح',
      onSuccess: (result) => {
        const count = result?.data?.count ?? 0
        showToast('success', 'تم المسح', `تم حفظ ${count} عنصر جديد ✅`)
      },
    },
  )
// ==================================================
// 3️⃣ WORKFLOWS
// ==================================================
const selectWorkflow = async (id) => {
  workflowStore.cancelAutoSave()
  await workflowStore.selectWorkflow(id)
}

const createWorkflow = () =>
  workflowAction.run(
    () =>
      workflowStore.createWorkflow({
        name: workflowStore.formWorkflow.name,
        description: workflowStore.formWorkflow.description,
        status: workflowStore.formWorkflow.status,
      }),
    {
      validate: () => (!workflowStore.formWorkflow.name?.trim() ? 'الاسم مطلوب' : null),
      successSummary: 'تم إنشاء الـ Workflow',
      errorSummary: 'فشل إنشاء الـ Workflow',
    },
  )

const saveWorkflow = async () => {
  const refreshedNode = await workflowStore.saveWorkflow({
    selectedNode: selectedNode.value,
    showActionPanel: showActionPanel.value,
  })
  if (refreshedNode) selectedNode.value = refreshedNode
  showToast('success', 'تم الحفظ', 'Workflow saved', 12000)
}

const updateStatusWorkflow = (status) =>
  workflowAction.run(
    () => workflowStore.updateWorkflow(workflowStore.currentWorkflowId, { status }),
    {
      successSummary: 'تم تحديث الحالة',
      successDetail: `Status: ${status}`,
      errorSummary: 'فشل تحديث الحالة',
    },
  )

const deleteWorkflow = (id) =>
  workflowAction.run(() => workflowStore.deleteWorkflow(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
  })

const clearWorkflow = () => workflowStore.clearCanvas()

const autoLayout = (dir = 'TB') => {
  isLayouting.value = true
  workflowStore.autoLayout(dir)
  setTimeout(() => {
    isLayouting.value = false
  }, 400)
}

// ==================================================
// 4️⃣ NODES
// ==================================================

// Helper — دايماً اجيب الـ fresh node من الـ store
const getFreshNode = (nodeId) =>
  workflowStore.nodes.find((n) => n.id === nodeId || n.data?.node?.backend_id === nodeId) ??
  selectedNode.value

// Node Click
const onNodeSelect = async ({ node }) => {
  const fresh = getFreshNode(node.id)
  selectedNode.value = fresh ?? node
  showActionPanel.value = true

  // ✅ استخدم backend_id مش node.id (ممكن يكون stale بعد save_all)
  const backendId = fresh?.data?.node?.backend_id ?? fresh?.id ?? node.id
  if (backendId) {
    try {
      await automationService.getWorkflowNode(backendId)
    } catch (_) {
      console.log('_: ', _)
    }
  }
}

// Create Node (Drag & Drop)
const createNode = async (item, dropEvent) => {
  if (!workflowStore.currentWorkflowId) {
    showToast('warn', 'لا يوجد Workflow', 'اختر Workflow الأول', 9000)
    return
  }
  workflowStore.isLoading = true
  workflowStore.cancelAutoSave()

  try {
    const position = project({ x: dropEvent.clientX, y: dropEvent.clientY })
    const actionMap = {
      program: 'open_program',
      'program-element': 'press',
      delay: 'wait',
      plugin: item.id,
    }
    const actionType = actionMap[item.type] ?? 'custom'

    const programData = programStore.programById?.(item.id)
    const nodeLabel = programData?.name ?? item.label ?? item.name ?? actionType

    const uiConfig = {
      ui: {
        theme: { background: '#0f172a', border: '#334155', shadow: '#334155' },
        layout: { width: 260, height: 240, rounded: true },
      },
      inputs: [
        { key: 'text', label: 'Text', type: 'string', value: '' },
        { key: 'delay', label: 'Delay (ms)', type: 'number', value: 0 },
      ],
      ai: { enabled: false, context: {}, memory: [], suggestions: [] },
    }

    // ✅ Step 1 — Create Node
    const nodeResult = await tracker.execute({
      serviceFn: () =>
        automationService.createWorkflowNode({
          workflow: workflowStore.currentWorkflowId,
          node_type: item.type === 'plugin' ? 'custom' : item.type,
          label: nodeLabel,
          program: item.type === 'program' ? item.id : null,
          element: item.type === 'program-element' ? item.id : null,
          position_x: position.x,
          position_y: position.y,
          config: uiConfig,
        }),
    })
    const nodeData = nodeResult?.data ?? nodeResult

    // ✅ Step 2 — Create Action (بنستخدم Plugin Registry بدل switch)
    const payload = item.type === 'plugin' ? registry.buildPayload(item.id, {}) : {}

    const actionResult = await tracker.execute({
      serviceFn: () =>
        automationService.createAction({
          node: nodeData.id,
          action_type: actionType,
          payload,
        }),
    })
    const actionResponse = actionResult.data

    // ✅ Push للـ Canvas (نفس structure بتاعة loadWorkflowEvents)
    workflowStore.nodes.push({
      id: nodeData.id,
      type: 'custom',
      position: { x: nodeData.position_x, y: nodeData.position_y },
      data: {
        label: nodeData.label,
        node: {
          backend_id: nodeData.id,
          id: nodeData.id,
          program_name: nodeData.program_name,
          element_name: nodeData.element_name,
          node_type: nodeData.node_type,
          label: nodeData.label,
          config: nodeData.config,
          program: nodeData.program,
          element: nodeData.element,
          status: 'idle',
        },
        actions: actionResponse ? [actionResponse] : [],
      },
    })

    showToast('success', 'Node Created', nodeData.label, 9000)
  } catch (err) {
    showToast('error', 'فشل إنشاء الـ Node', err?.message, 9000)
  } finally {
    workflowStore.isLoading = false
  }
}

// Delete Node
const deleteNodeOnWorkflow = (id) =>
  nodeAction.run(() => automationService.deleteWorkflowNode(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      workflowStore.nodes = workflowStore.nodes.filter((n) => n.id !== id)
      workflowStore.edges = workflowStore.edges.filter((e) => e.source !== id && e.target !== id)
    },
  })

// Run Node (test)
const runTaskFromNode = (nodeData) => {
  const backendId = nodeData?.backend_id
  if (!backendId) {
    showToast('error', 'Node Error', 'Backend ID not found')
    return
  }
  nodeAction.run(() => automationService.runWorkflowNode(backendId), {
    successSummary: 'Node Running',
    errorSummary: 'Execution Failed',
  })
}

// ─── Node Actions ────────────────────────────────

// ✅ buildPayloadFromUI — الآن بيستخدم Plugin Registry بدل switch
const buildPayloadFromUI = (type, extraData = {}) => registry.buildPayload(type, extraData) ?? {}

// CREATE ACTION
const createNodeAction = async ({ nodeId, action_type }) => {
  // ✅ دايماً استخدم backend_id للـ API — مطلقاً مش VueFlow UUID
  const fresh = getFreshNode(nodeId)
  const realId = fresh?.data?.node?.backend_id ?? fresh?.id

  if (!realId) {
    showToast('error', 'Node ID missing', 'تأكد إن الـ node محفوظ في الباك اند')
    return
  }

  const payload = buildPayloadFromUI(action_type, {})

  await nodeAction.run(
    () => automationService.createAction({ node: realId, action_type, payload }),
    {
      successSummary: 'تم إنشاء الـ Action',
      successDetail: action_type,
      errorSummary: 'فشل إنشاء الـ Action',
      onSuccess: (result) => {
        // ✅ tracker.execute بيرجع axios response { data, status } — مش بس data
        const actionResponse = result?.data ?? result
        if (!actionResponse) return

        const idx = workflowStore.nodes.findIndex(
          (n) => n.id === realId || n.data?.node?.backend_id === realId,
        )
        if (idx !== -1) {
          workflowStore.nodes[idx] = {
            ...workflowStore.nodes[idx],
            data: {
              ...workflowStore.nodes[idx].data,
              actions: [...(workflowStore.nodes[idx].data.actions ?? []), actionResponse],
            },
          }
          selectedNode.value = workflowStore.nodes[idx]
        }
      },
    },
  )
}

// UPDATE ACTION — Optimistic + Rollback
const updateNodeAction = async ({ nodeId, actionId, newActionType }) => {
  const payload = buildPayloadFromUI(newActionType, {})
  const idx = workflowStore.nodes.findIndex((n) => n.id === nodeId)
  const oldActions = idx !== -1 ? [...workflowStore.nodes[idx].data.actions] : []

  // Optimistic Update
  if (idx !== -1) {
    workflowStore.nodes[idx] = {
      ...workflowStore.nodes[idx],
      data: {
        ...workflowStore.nodes[idx].data,
        actions: workflowStore.nodes[idx].data.actions.map((a) =>
          a.id === actionId ? { ...a, action_type: newActionType, payload } : a,
        ),
      },
    }
    selectedNode.value = workflowStore.nodes[idx]
  }

  await nodeAction.run(
    () => automationService.updateAction(actionId, { action_type: newActionType, payload }),
    {
      successSummary: 'تم تحديث الـ Action',
      successDetail: newActionType,
      errorSummary: 'فشل تحديث الـ Action',
      onError: () => {
        // Rollback لو الـ API fail
        if (idx !== -1) {
          workflowStore.nodes[idx] = {
            ...workflowStore.nodes[idx],
            data: { ...workflowStore.nodes[idx].data, actions: oldActions },
          }
          selectedNode.value = workflowStore.nodes[idx]
        }
      },
    },
  )
}

// DELETE ACTION
const deleteNodeAction = ({ nodeId, actionId }) =>
  nodeAction.run(() => automationService.deleteAction(actionId), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      const idx = workflowStore.nodes.findIndex((n) => n.id === nodeId)
      if (idx !== -1) {
        workflowStore.nodes[idx] = {
          ...workflowStore.nodes[idx],
          data: {
            ...workflowStore.nodes[idx].data,
            actions: workflowStore.nodes[idx].data.actions.filter((a) => a.id !== actionId),
          },
        }
        selectedNode.value = workflowStore.nodes[idx]
      }
    },
  })

// ==================================================
// 5️⃣ EDGES
// ==================================================
const onConnect = async (params) => {
  if (!workflowStore.currentWorkflowId) return
  await nodeAction.run(
    () =>
      automationService.createWorkflowEdge({
        workflow: workflowStore.currentWorkflowId,
        source_node: params.source,
        target_node: params.target,
        condition: 'success',
      }),
    {
      successSummary: 'تم ربط الـ Nodes',
      errorSummary: 'فشل إنشاء الـ Edge',
      onSuccess: (result) => {
        const data = result?.data ?? result
        if (!data?.id) {
          console.error('❌ Edge response missing id:', data)
          return
        }
        workflowStore.edges.push({
          id: data.id,
          source: data.source_node,
          target: data.target_node,
          type: 'default',
          data: { label: data.condition },
          animated: true,
          style: { stroke: '#4CAF50', strokeWidth: 2 },
        })
      },
    },
  )
}

// ==================================================
// 6️⃣ DRAG & DROP
// ==================================================
const startDrag = (item) => {
  draggedItem.value = item
}
const onDragOver = (e) => {
  e.preventDefault()
  e.dataTransfer.dropEffect = 'move'
}
const onDrop = async (e) => {
  e.preventDefault()
  if (!draggedItem.value) return
  await createNode(draggedItem.value, e)
  draggedItem.value = null
}

// Position Sync (bypass tracker — لا يظهر في ApiFlowPanel)
const onNodeDragStop = (node) => {
  const backendId = node.data?.node?.backend_id ?? node.id
  if (!backendId) return
  syncState.updateQueue.push({
    type: 'node-position',
    id: backendId,
    position_x: node.position.x,
    position_y: node.position.y,
  })
  debouncedSync()
}

const processQueue = async () => {
  if (syncState.isSyncing) return
  syncState.isSyncing = true
  while (syncState.updateQueue.length > 0) {
    const job = syncState.updateQueue.shift()
    try {
      if (job.type === 'node-position')
        await automationService.updateWorkflowNode(job.id, {
          position_x: job.position_x,
          position_y: job.position_y,
        })
    } catch (err) {
      console.error('Sync error:', err)
    }
  }
  syncState.isSyncing = false
}
const debouncedSync = debounce(processQueue, 300)

// ==================================================
// 7️⃣ NodeVisualBuilder (Configure Plugin before Drop)
// ==================================================
// لما المستخدم يجر plugin من الـ Marketplace →
// لو محتاج config (مش open_program / close_program) → يفتح الـ Builder
// ==================================================
/*
const openBuilder = (plugin) => {
  builderPlugin.value = plugin
  showBuilder.value = true
}
*/
const onBuilderConfirm = async ({ plugin_id, label, color, payload }) => {
  if (!workflowStore.currentWorkflowId) {
    showToast('warn', 'لا يوجد Workflow', 'اختر Workflow الأول', 9000)
    return
  }
  // Drop في المنتصف لو مفيش event
  const position = project({ x: window.innerWidth / 2, y: window.innerHeight / 2 })
  workflowStore.isLoading = true
  workflowStore.cancelAutoSave()

  try {
    const nodeResult = await tracker.execute({
      serviceFn: () =>
        automationService.createWorkflowNode({
          workflow: workflowStore.currentWorkflowId,
          node_type: 'custom',
          label,
          position_x: position.x,
          position_y: position.y,
          config: {
            ui: {
              theme: { background: '#0f172a', border: color, shadow: color },
              layout: { width: 260, height: 240, rounded: true },
            },
          },
        }),
    })
    const nodeData = nodeResult?.data ?? nodeResult

    const actionResult = await tracker.execute({
      serviceFn: () =>
        automationService.createAction({ node: nodeData.id, action_type: plugin_id, payload }),
    })
    const actionResponse = actionResult.data

    workflowStore.nodes.push({
      id: nodeData.id,
      type: 'custom',
      position: { x: nodeData.position_x, y: nodeData.position_y },
      data: {
        label,
        node: {
          backend_id: nodeData.id,
          id: nodeData.id,
          label,
          status: 'idle',
          config: nodeData.config,
        },
        actions: actionResponse ? [actionResponse] : [],
      },
    })
    showToast('success', 'Node Created', label, 9000)
  } catch (err) {
    showToast('error', 'فشل إنشاء الـ Node', err?.message)
  } finally {
    workflowStore.isLoading = false
  }
}

// ==================================================
// 8️⃣ WORKFLOW EXECUTION
// ==================================================
const startWorkflow = () =>
  workflowAction.run(() => automationService.runWorkflow(workflowStore.currentWorkflowId), {
    validate: () => (!workflowStore.currentWorkflowId ? 'اختر Workflow الأول' : null),
    successSummary: '🚀 Workflow Started',
    successDetail: 'Workflow Started successfully',
    errorSummary: 'فشل تشغيل الـ Workflow',
    onSuccess: (result) => {
      const payload = result?.data ?? result
      taskStore.setTaskRunId(payload.task_run_id)
    },
  })

// ==================================================
// 9️⃣ TASKS
// ==================================================
const createTask = () =>
  taskAction.run(() => taskStore.createTask(), {
    validate: () => taskStore.validateForm(),
    successSummary: 'تم إنشاء الـ Task',
    errorSummary: 'فشل إنشاء الـ Task',
    onSuccess: () => {
      createTaskVisible.value = false
    },
  })

const openEditTask = async (id) => {
  try {
    await taskStore.loadTask(id)
    editTaskVisible.value = true
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
  }
}

const editTask = () =>
  taskAction.run(() => taskStore.updateTask(taskStore.currentTaskId), {
    validate: () => taskStore.validateForm(),
    successSummary: 'تم تحديث الـ Task',
    errorSummary: 'فشل تحديث الـ Task',
    onSuccess: () => {
      editTaskVisible.value = false
    },
  })

const confirmDeleteTask = (task) => {
  confirm.require({
    message: `هل تريد حذف "${task.name}"؟`,
    header: '⚠️ تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'نعم، احذف',
    rejectLabel: 'إلغاء',
    accept: () =>
      taskAction.run(() => taskStore.deleteTask(task.id), {
        successSummary: 'تم الحذف',
        errorSummary: 'فشل الحذف',
      }),
  })
}
//
const handleUpdateNodeAction = (data) => {
  updateNodeAction(data)
}
// ==================================================
// 💾 Watches
// ==================================================
// لما الـ dialog يفتح
watch(createProgramElementVisible, async (val) => {
  if (val) await programStore.loadOpenWindows()
  console.log('programStore.loadOpenWindows(): ', programStore.loadOpenWindows())
})
// AutoSave — لما الـ nodes أو الـ edges تتغير
watch(
  [() => workflowStore.nodes, () => workflowStore.edges],
  () => {
    workflowStore.triggerAutoSave({
      selectedNode: selectedNode.value,
      showActionPanel: showActionPanel.value,
    })
  },
  { deep: true },
)

// مزامنة program مع element form
watch(
  () => programStore.currentProgramId,
  (id) => {
    if (id) elementStore.form.program = id
  },
)

// ==================================================
// 🚀 onMounted — تحميل كل البيانات في نفس الوقت
// ==================================================

let pollInterval = null

onMounted(async () => {
  // ... الكود الحالي لتحميل البيانات الأولية ...
  await Promise.all([
    programStore.loadPrograms(),
    elementStore.loadElements(),
    workflowStore.loadWorkflows(),
    taskStore.loadTasks(),
    automationService
      .listDelays()
      .then((r) => {
        delays.value = r.data
      })
      .catch(() => {}),
  ])

  // تفعيل السحب (Polling) كل 500ms لتحديث الحالات اللحظية
  pollInterval = setInterval(async () => {
    // 1. تحديث حالة الـ Workflow إذا كان قيد التشغيل
    if (workflowStore.currentWorkflowId && workflowAction.loading.value) {
      await workflowStore.loadWorkflowEvents(workflowStore.currentWorkflowId)
      console.log('🟢 APP READY')
    }
    // 2. تحديث قائمة المهام (Tasks) لرؤية التقدم
    // await taskStore.loadTasks()
  }, 500)
})

// تنظيف الـ Interval عند إغلاق الصفحة لمنع تسريب الذاكرة
onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>

<template>
  <main class="automation-view">
    <div style="background-color: #aaa">
      <AIPrompt />
      <AIAsk />
    </div>

    <div class="automation-layout grid grid-cols-12 gap-4 h-full">
      <!-- ══════════════════════════════════════════════════
      SIDEBAR — NodeMarketplace
      بيحل محل الـ aside القديمة (programs/elements/tasks)
      ══════════════════════════════════════════════════ -->
      <aside class="automation-sidebar">
        <NodeMarketplace
          :programs="programStore.programs"
          :elements="elementStore.elements"
          :delays="delays"
          :tasks="taskStore.tasks"
          :workflows="workflowStore.workflows"
          :loading-programs="programStore.loading"
          :loading-elements="elementStore.loading"
          :loading-tasks="taskStore.loading"
          @drag-start="startDrag"
          @item-click="({ type, id }) => type === 'program' && programStore.loadProgram(id)"
          @select-workflow="selectWorkflow"
          @create-program="createProgramVisible = true"
          @create-element="createProgramElementVisible = true"
          @create-task="createTaskVisible = true"
          @edit-program="openEditProgram"
          @delete-program="confirmDeleteProgram"
          @edit-element="openEditProgramElement"
          @delete-element="confirmDeleteProgramElement"
          @edit-task="openEditTask"
          @delete-task="confirmDeleteTask"
        />
      </aside>
      <!-- ═══════ MAIN — WorkflowCanvas ═══ -->
      <section class="automation-canvas">
        <!-- Workflow Header Bar -->
        <div class="workflow-header">
          <div class="workflow-header__fields">
            <prime_input_text
              v-model="workflowStore.formWorkflow.name"
              placeholder="اسم الـ Workflow"
              size="small"
              class="w-48"
            />
            <prime_input_text
              v-model="workflowStore.formWorkflow.description"
              placeholder="وصف اختياري"
              size="small"
              class="w-64"
            />
          </div>

          <div class="workflow-header__actions">
            <!-- Versions -->
            <prime_button
              icon="pi pi-history"
              size="small"
              outlined
              :disabled="!workflowStore.currentWorkflowId"
              @click="showVersions = true"
              v-tooltip="'سجل الـ Versions'"
            />
            <!-- Realtime Graph -->
            <prime_button
              icon="pi pi-chart-bar"
              size="small"
              outlined
              :disabled="!taskStore.taskRunId"
              @click="showRealtimeGraph = true"
              v-tooltip="'Realtime Graph'"
            />
            <!-- Delete Workflow -->
            <prime_button
              icon="pi pi-trash"
              size="small"
              severity="danger"
              outlined
              :disabled="!workflowStore.currentWorkflowId"
              @click="deleteWorkflow(workflowStore.currentWorkflowId)"
            />
          </div>
        </div>

        <!-- ─── WorkflowCanvas ──────────────────────────── -->
        <WorkflowCanvas
          :nodes="workflowStore.nodes"
          :edges="workflowStore.edges"
          :is-loading="workflowStore.isLoading"
          :current-workflow-id="workflowStore.currentWorkflowId"
          @update:nodes="workflowStore.nodes = $event"
          @update:edges="workflowStore.edges = $event"
          @node-click="onNodeSelect"
          @connect="onConnect"
          @drop="onDrop"
          @drag-over="onDragOver"
          @node-drag-stop="onNodeDragStop"
          @run-task="runTaskFromNode"
          @delete-node="deleteNodeOnWorkflow"
          @update-node-action="handleUpdateNodeAction"
        >
          <!-- ─── Toolbar (slot inside Canvas Panel) ───── -->
          <template #toolbar>
            <WorkflowToolbar
              :has-workflow="!!workflowStore.currentWorkflowId"
              :is-saving="workflowStore.isSaving"
              :is-running="workflowAction.loading.value"
              :is-loading="workflowStore.isLoading"
              :workflow-status="workflowStore.currentWorkflow?.status"
              @save="saveWorkflow"
              @run="startWorkflow"
              @create="createWorkflow"
              @clear="clearWorkflow"
              @auto-layout="autoLayout"
              @update-status="updateStatusWorkflow"
            />
          </template>
        </WorkflowCanvas>
      </section>
    </div>
    <!-- ─── ApiFlowPanel (dev tool) ─────────── -->
    <ApiFlowPanel :stages="stages" :meta="meta" :error="trackerError" :show-data="true" />
    <!-- ════════════════════════════════════════════
    PANELS & DIALOGS (position: fixed / teleport)
    ═════════════════════════════════════════════ -->

    <!-- ─── Action Panel ────────────────────── -->
    <ActionPanel
      :show="showActionPanel"
      :selected-node="selectedNode"
      :new-action-type-for-panel="newActionTypeForPanel"
      @close="showActionPanel = false"
      @create-action="createNodeAction"
      @update-action="updateNodeAction"
      @delete-action="deleteNodeAction"
    />

    <div class="automation-bottom">
      <!-- ─── Live Console (fixed bottom) ──────── -->

      <LiveConsole
        v-if="taskStore.taskRunId"
        :task-run-id="taskStore.taskRunId"
        @close="taskStore.clearTaskRunId()"
        @done="showToast('success', 'Workflow Done', '✅ اكتمل بنجاح')"
      />
      <!-- ─── Realtime Graph ───────────────────── -->

      <RealtimeGraph
        :task-run-id="taskStore.taskRunId"
        :nodes="workflowStore.nodes"
        :visible="showRealtimeGraph"
        @close="showRealtimeGraph = false"
      />
    </div>

    <!-- ─── Workflow Versions ────────────────── -->
    <WorkflowVersions
      :visible="showVersions"
      :workflow-id="workflowStore.currentWorkflowId"
      @restore="(v) => workflowStore.loadWorkflowEvents(v.workflow_id)"
    />

    <!-- ─── Node Visual Builder ──────────────── -->
    <NodeVisualBuilder
      :visible="showBuilder"
      :plugin="builderPlugin"
      @confirm="onBuilderConfirm"
      @cancel="showBuilder = false"
    />

    <!-- ─── Create Program ───────────────────── -->
    <CreateProgram
      :visible="createProgramVisible"
      :form="programStore.form"
      :loading="programAction.loading.value"
      @image-change="programStore.onImageChange"
      @submit="createProgram"
      @cancel="createProgramVisible = false"
    />

    <!-- ─── Edit Program ─────────────────────── -->
    <EditProgram
      :visible="editProgramVisible"
      :form="programStore.form"
      :loading="programAction.loading.value"
      @image-change="programStore.onImageChange"
      @submit="editProgram"
      @cancel="editProgramVisible = false"
    />

    <!-- ─── Create/Edit Program Element ──────── -->
    <!-- (Dialogs — مبسطة بدون duplicated HTML ضخم) -->
    <prime_dialog
      :visible="createProgramElementVisible"
      modal
      header="إنشاء عنصر جديد"
      :style="{ width: '640px' }"
    >
      <div class="flex flex-col gap-4 py-2">
        <div class="grid grid-cols-2 gap-3">
          <div class="field">
            <label class="font-semibold text-sm mb-1 block">الاسم *</label>
            <prime_input_text
              v-model="elementStore.form.name"
              placeholder="اسم العنصر"
              class="w-full"
            />
          </div>
          <div class="field">
            <label class="font-semibold text-sm mb-1 block">البرنامج *</label>

            <!-- Step 1: اختار النافذة المفتوحة -->
            <prime_select
              v-model="selectedWindow"
              :options="programStore.openWindows"
              optionLabel="title"
              placeholder="1️⃣ اختر النافذة المفتوحة"
              class="w-full mb-2"
            >
              <template #option="{ option }">
                <div class="flex flex-col">
                  <span class="font-semibold text-sm">{{ option.app_name }}</span>
                  <span class="text-xs text-gray-400 truncate">{{ option.title }}</span>
                </div>
              </template>
            </prime_select>

            <!-- عرض الـ pattern المختار -->
            <div v-if="selectedWindow" class="text-xs text-green-400 mb-2 px-1">
              ✅ App: <strong>{{ selectedWindow.app_name }}</strong> — Pattern:
              <code>{{ selectedWindow.suggested_pattern }}</code>
            </div>

            <!-- Step 2: اختار البرنامج من الـ DB -->
            <prime_select
              v-model="elementStore.form.program"
              :options="programStore.programs"
              optionLabel="name"
              optionValue="id"
              placeholder="2️⃣ اختر البرنامج"
              class="w-full mb-2"
            />

            <!-- زر المسح — يظهر لما يتم اختيار برنامج ونافذة معاً -->
            <prime_button
              v-if="elementStore.form.program && selectedWindow"
              icon="pi pi-search-plus"
              label="مسح العناصر"
              v-tooltip.top="'مسح عناصر هذا البرنامج تلقائياً'"
              severity="help"
              :loading="programStore.isScanning"
              @click="handleSmartScan"
            />

            <!-- تحذير لو اختار برنامج بس ما اختارش نافذة -->
            <small v-if="elementStore.form.program && !selectedWindow" class="text-yellow-400">
              ⚠️ اختر النافذة المفتوحة عشان تقدر تمسح العناصر
            </small>
          </div>

          <div class="field">
            <label class="font-semibold text-sm mb-1 block">Selector Type *</label>
            <prime_select
              v-model="elementStore.form.selector_type"
              :options="elementStore.SELECTOR_TYPES"
              optionLabel="label"
              optionValue="value"
              placeholder="اختر النوع"
              class="w-full"
            />
          </div>
          <div class="field">
            <label class="font-semibold text-sm mb-1 block">Selector Value</label>
            <prime_input_text
              v-model="elementStore.form.selector_value"
              placeholder="xpath / image path"
              class="w-full"
            />
          </div>
          <div class="field">
            <label class="font-semibold text-sm mb-1 block">X</label>
            <prime_input_number v-model="elementStore.form.x" :min="0" class="w-full" />
          </div>
          <div class="field">
            <label class="font-semibold text-sm mb-1 block">Y</label>
            <prime_input_number v-model="elementStore.form.y" :min="0" class="w-full" />
          </div>
          <div class="field col-span-2">
            <label class="font-semibold text-sm mb-1 block">صورة العنصر</label>
            <input type="file" accept="image/*" @change="elementStore.onImageChange" />
          </div>
        </div>
        <template v-if="activeTab === 0">
          <div class="section-header">
            <span>🖥️ Programs</span>
            <prime_button
              icon="pi pi-plus"
              size="small"
              text
              rounded
              @click="emit('create-program')"
            />
          </div>

          <div
            v-for="p in filteredPrograms"
            :key="p.id"
            class="item-card"
            @mouseenter="checkStatus(p.id)"
          >
            <img v-if="p.get_image" :src="p.get_image" class="item-card__img" />
            <i v-else class="pi pi-desktop item-card__icon"></i>

            <div class="flex flex-col flex-1">
              <span class="item-card__name">{{ p.name }}</span>

              <prime_button
                v-if="programStore.programsStatus[p.id] === 'running'"
                label="مسح العناصر"
                icon="pi pi-search-plus"
                class="p-button-xs p-button-help mt-1"
                :loading="programStore.loadingScan"
                @click.stop="programStore.scanElements(p.id)"
              />
            </div>

            <div class="item-card__actions">
              <prime_button
                v-if="programStore.programsStatus[p.id] !== 'running'"
                icon="pi pi-play"
                text
                rounded
                @click.stop="programStore.openProgram(p)"
              />
              <prime_button
                icon="pi pi-pencil"
                text
                rounded
                @click.stop="emit('edit-program', p.id)"
              />
            </div>
          </div>
        </template>
      </div>
      <template #footer>
        <prime_button
          label="إلغاء"
          severity="secondary"
          outlined
          @click="createProgramElementVisible = false"
        />
        <prime_button
          label="إنشاء"
          icon="pi pi-check"
          :loading="elementAction.loading.value"
          @click="createProgramElement"
        />
      </template>
    </prime_dialog>

    <prime_dialog
      :visible="editProgramElementVisible"
      modal
      header="تعديل عنصر"
      :style="{ width: '640px' }"
    >
      <!-- نفس الـ fields بالضبط -->
      <div class="flex flex-col gap-4 py-2">
        <div class="grid grid-cols-2 gap-3">
          <div class="field">
            <label class="font-semibold text-sm mb-1 block">الاسم *</label>
            <prime_input_text v-model="elementStore.form.name" class="w-full" />
          </div>
          <div class="field">
            <label class="font-semibold text-sm mb-1 block">البرنامج *</label>
            <prime_select
              v-model="elementStore.form.program"
              :options="programStore.programs"
              optionLabel="name"
              optionValue="id"
              class="w-full"
            />
          </div>
          <div class="field">
            <label class="font-semibold text-sm mb-1 block">Selector Type *</label>
            <prime_select
              v-model="elementStore.form.selector_type"
              :options="elementStore.SELECTOR_TYPES"
              optionLabel="label"
              optionValue="value"
              class="w-full"
            />
          </div>
          <div class="field">
            <label class="font-semibold text-sm mb-1 block">Selector Value</label>
            <prime_input_text v-model="elementStore.form.selector_value" class="w-full" />
          </div>
          <div class="field">
            <label class="font-semibold text-sm mb-1 block">X</label
            ><prime_input_number v-model="elementStore.form.x" :min="0" class="w-full" />
          </div>
          <div class="field">
            <label class="font-semibold text-sm mb-1 block">Y</label
            ><prime_input_number v-model="elementStore.form.y" :min="0" class="w-full" />
          </div>
          <div class="field col-span-2">
            <label class="font-semibold text-sm mb-1 block">صورة العنصر</label>
            <input type="file" accept="image/*" @change="elementStore.onImageChange" />
          </div>
        </div>
      </div>
      <template #footer>
        <prime_button
          label="إلغاء"
          severity="secondary"
          outlined
          @click="editProgramElementVisible = false"
        />
        <prime_button
          label="حفظ التغييرات"
          icon="pi pi-check"
          :loading="elementAction.loading.value"
          @click="editProgramElement"
        />
      </template>
    </prime_dialog>

    <!-- ─── Create/Edit Task ────────────────── -->
    <prime_dialog
      :visible="createTaskVisible"
      modal
      header="إنشاء Task جديد"
      :style="{ width: '480px' }"
    >
      <div class="flex flex-col gap-4 py-2">
        <div class="field">
          <label class="font-semibold text-sm mb-1 block">اسم الـ Task *</label>
          <prime_input_text
            v-model="taskStore.form.name"
            placeholder="اسم الـ Task"
            class="w-full"
          />
        </div>
        <div class="field">
          <label class="font-semibold text-sm mb-1 block">البرنامج *</label>
          <prime_select
            v-model="taskStore.form.program"
            :options="programStore.programs"
            optionLabel="name"
            optionValue="id"
            placeholder="اختر البرنامج"
            class="w-full"
          />
        </div>
        <div class="field">
          <label class="font-semibold text-sm mb-1 block">الوصف</label>
          <prime_textarea v-model="taskStore.form.description" rows="2" class="w-full" />
        </div>
      </div>
      <template #footer>
        <prime_button
          label="إلغاء"
          severity="secondary"
          outlined
          @click="createTaskVisible = false"
        />
        <prime_button
          label="إنشاء"
          icon="pi pi-check"
          :loading="taskAction.loading.value"
          @click="createTask"
        />
      </template>
    </prime_dialog>

    <prime_dialog :visible="editTaskVisible" modal header="تعديل Task" :style="{ width: '480px' }">
      <div class="flex flex-col gap-4 py-2">
        <div class="field">
          <label class="font-semibold text-sm mb-1 block">اسم الـ Task *</label>
          <prime_input_text v-model="taskStore.form.name" class="w-full" />
        </div>
        <div class="field">
          <label class="font-semibold text-sm mb-1 block">البرنامج *</label>
          <prime_select
            v-model="taskStore.form.program"
            :options="programStore.programs"
            optionLabel="name"
            optionValue="id"
            class="w-full"
          />
        </div>
        <div class="field">
          <label class="font-semibold text-sm mb-1 block">الوصف</label>
          <prime_textarea v-model="taskStore.form.description" rows="2" class="w-full" />
        </div>
      </div>
      <template #footer>
        <prime_button
          label="إلغاء"
          severity="secondary"
          outlined
          @click="editTaskVisible = false"
        />
        <prime_button
          label="حفظ التغييرات"
          icon="pi pi-check"
          :loading="taskAction.loading.value"
          @click="editTask"
        />
      </template>
    </prime_dialog>

    <!-- ─── PrimeVue Confirm Dialog ──────────── -->
    <prime_confirm_dialog />
  </main>
</template>

<style scoped>
.automation-view {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* ✅ مش height — عشان يسمح بالـ scroll */
  background: #0a0f1a;
  overflow-y: auto; /* ✅ الـ scroll على الـ view كلها */
}

/* ── Top Layout (sidebar + canvas) ────────── */
.automation-layout {
  display: grid;
  grid-template-columns: 340px 1fr;
  height: 100vh; /* ✅ يأخذ كامل ارتفاع الشاشة */
  gap: 0;
  flex-shrink: 0; /* ✅ مش بيتضغط */
}

/* ── Bottom Strip ──────────────────────────── */
.automation-bottom {
  flex-shrink: 0;
  border-top: 2px solid #21262d;
  background: #0d1117;
  /* ✅ بيظهر بالـ scroll — مفيش position fixed */
}

/* ── Sidebar ───────────────────────────────── */
.automation-sidebar {
  height: 100%;
  overflow-y: auto; /* ✅ scroll داخلي للـ sidebar لو المحتوى أطول */
  border-right: 1px solid #1e293b;
}

/* ── Canvas ────────────────────────────────── */
.automation-canvas {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

/* ── Workflow Header ───────────────────────── */
.workflow-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: #0f172a;
  border-bottom: 1px solid #1e293b;
  gap: 12px;
  flex-shrink: 0; /* ✅ مش بيتضغط */
}

.workflow-header__fields {
  display: flex;
  gap: 8px;
  flex: 1;
}

.workflow-header__actions {
  display: flex;
  gap: 6px;
  align-items: center;
}

/* ── VueFlow ───────────────────────────────── */
:deep(.workflow-canvas),
:deep(.vue-flow) {
  flex: 1;
  min-height: 0; /* ✅ ضروري */
}
</style>

<style scoped lang="scss">
.btn-white {
  @apply p-2 border rounded bg-white hover:bg-gray-100;
}

.wrapper_name_description .inner_name_description {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(calc(100% / 4), 1fr));
  align-items: center;
}

.wrapper_programs,
.wrapper_delays,
.wrapper_program_element {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100%, 1fr));
  gap: 1.5% 1.5%;

  .link_aside {
    display: flex;
    grid-template-columns: repeat(auto-fill, minmax(25px, 1fr));
    align-items: center;
    justify-content: space-between;
    text-align: center;
    border: 0.1rem solid #22222223;
    background-color: #2222220e;

    img {
      height: 35px;
      width: 35px;
      display: block;
      border-radius: 10px;
      margin: 5px 10px 5px auto;
    }
  }
}
/* Transition للـ Panel */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.25s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}
.bt {
  border: 0.5rem solid #f00;
}
</style>
