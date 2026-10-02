<!-- <script setup>
// ==================================================
// 📦 1️⃣ Imports (المكتبات المستخدمة)
// ==================================================
// 🧠 Vue Composition API
import { ref, onMounted, computed, watch, reactive } from 'vue'
// 💾 Service  مسؤولة عن التواصل مع الباك
import automationService from '@/services/AutomationService'
// VueFlow
import { VueFlow, Panel, useVueFlow } from '@vue-flow/core'
// 🎨 خلفية الشبكة (Grid Background)
import { Background } from '@vue-flow/background'
// عناصر تحكم لتحكم في حالة المخطط 🎛️
import { Controls } from '@vue-flow/controls'
// 🗺️ MiniMap (خريطة مصغرة للمخطط)
import { MiniMap } from '@vue-flow/minimap'
// أدوات سحب وإفلات لواجهة المستخدم 📦
import vuedraggable from 'vuedraggable'
// مكون مخصص لنموذج عقدة مخصصة 📌
import CustomNode from '@/components/Automation/Node/CustomNode.vue'
// مكون مخصص لحافة مخصصة ↔️
import CustomEdge from '@/components/Automation/Edge/CustomEdge.vue'
import ActionPanel from '@/components/Automation/Action/ActionPanel.vue'
import CreateProgram from '@/components/Automation/Program/CreateProgram.vue'
import EditProgram from '@/components/Automation/Program/EditProgram.vue'
import { debounce } from 'lodash'
// Toast
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import LiveConsole from '@/components/Automation/Execution/LiveConsole.vue'
// Contract arrangement automatically
import dagre from 'dagre'
import { useApiTracker } from '@/composables/useApiTracker'
import ApiFlowPanel from '@/components/Automation/ApiFlowPanel.vue'
import { useProgramStore } from '@/stores/useProgramStore'
import { useProgramElementStore } from '@/stores/useProgramElementStore'
import { useWorkflowStore } from '@/stores/useWorkflowStore'
import { useTaskStore } from '@/stores/useTaskStore'
import { storeToRefs } from 'pinia'

// ==================================================
// 🔌 Init
// ==================================================
const toast = useToast()
const confirm = useConfirm()
const { project } = useVueFlow()
const tracker = useApiTracker()

const programStore = useProgramStore()
const { programs, form, loading, currentProgramId } = storeToRefs(programStore)

const elementStore = useProgramElementStore()
const workflowStore = useWorkflowStore()
const taskStore = useTaskStore()

// ==================================================

// 🛠️ INLINE UX ENGINE — useAsyncAction
// ==================================================
// Replaces all try/catch/finally blocks with a single pattern.
//
// FIXES APPLIED:
//  ❌ Before: success toast fired in `finally` → fires even on errors
//  ✅ After:  success only in `try` via onSuccess callback
//
//  ❌ Before: dialogs closed in `finally` → closes even on errors
//  ✅ After:  dialogs close only inside onSuccess
//
//  ❌ Before: no guard against double-clicking submit
//  ✅ After:  `if (loading.value) return` prevents duplicate submissions
//
//  ❌ Before: generic error.message shown to user (useless)
//  ✅ After:  reads Django 400 validation errors field-by-field
// ==================================================
function useAsyncAction() {
  const loading = ref(false)

  const run = async (apiFn, options = {}) => {
    if (loading.value) return

    const {
      validate = null,
      successSummary = null,
      successDetail = null,
      errorSummary = 'حصل خطأ',
      onSuccess = null,
      onError = null,
      onFinally = null,
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

      if (successSummary) {
        toast.add({
          severity: 'success',
          summary: `✅ ${successSummary}`,
          detail: successDetail,
          life: 4000,
        })
      }
      if (onSuccess) await onSuccess(result)
      return result
    } catch (err) {
      // ✅ Smart error: reads Django validation errors automatically
      const status = err?.response?.status
      const body = err?.response?.data
      let detail = err?.message || 'خطأ غير متوقع'

      if (status === 400 && body && typeof body === 'object') {
        detail = Object.entries(body)
          .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs[0] : msgs}`)
          .slice(0, 3)
          .join(' | ')
      } else if (status === 401) {
        detail = 'انتهت جلستك — سجّل دخول من جديد'
      } else if (status === 403) {
        detail = 'مش عندك صلاحية لهذه العملية'
      } else if (status === 404) {
        detail = 'العنصر المطلوب غير موجود'
      } else if (status === 413) {
        detail = 'الملف كبير جداً — الحد الأقصى 5MB'
      } else if (status === 500) {
        detail = 'خطأ في السيرفر — حاول مرة أخرى'
      }

      toast.add({ severity: 'error', summary: `❌ ${errorSummary}`, detail, life: 6000 })
      if (onError) onError(err)
      throw err
    } finally {
      loading.value = false
      if (onFinally) onFinally()
    }
  }

  return { run, loading }
}

// One async runner per domain → independent loading states
const programAction = useAsyncAction()
const programElementAction = useAsyncAction()
const workflowAction = useAsyncAction()
const taskAction = useAsyncAction()
const nodeAction = useAsyncAction()

// ② في setup()

const { execute, stages, result, error, meta } = useApiTracker()
console.log('result: ', result)

// =======================
// 🍞 Toast Helpers shorthand
// =======================
const showToast = (severity, summary, detail, life) => {
  toast.add({
    severity,
    summary: `${severity === 'success' ? '✅' : severity === 'error' ? '❌' : '⚠️'} ${summary}`,
    detail,
    life,
  })
}

// ==================================================
// ✅ Form Validators
// ==================================================
const validateProgramElement = (form) => {
  if (!form.name?.trim()) return 'الاسم مطلوب'
  if (!form.program) return 'لازم تختار برنامج'
  if (!form.selector_type) return 'لازم تختار Selector Type'
  return null
}
const validateTask = (form) => {
  if (!form.name?.trim()) return 'اسم الـ Task مطلوب'
  if (!form.program) return 'لازم تختار برنامج'
  return null
}
const validateImageSize = (file, maxMB = 5) => {
  if (file && file.size > maxMB * 1024 * 1024) {
    showToast('warn', 'الملف كبير', `الحد الأقصى ${maxMB}MB`)
    return false
  }
  return true
}

// ==============================================
// =================== State ===================
// ==============================================
// 1️⃣ programs
const createProgramVisible = ref(false)
const editProgramVisible = ref(false)

// 2️⃣ programsElement
const programsElement = ref([])
const loadingProgramElements = ref(false)
const currentProgramElementId = ref(null)
const createProgramElementsVisible = ref(false)
const editProgramElementsVisible = ref(false)
const programElementselectorTypes = [
  { label: 'Image Recognition', value: 'image' },
  { label: 'Screen Coordinates', value: 'coords' },
  { label: 'Text OCR', value: 'text' },
  { label: 'UI Automation', value: 'ui' },
]
const formProgramElement = ref({
  // Text
  name: '',
  description: '',
  executable_path: '',
  project_path: '',
  working_directory: '',
  window_title_pattern: '',
  // // Files & Image
  image: null,
  program: null,
  element_type: 'button',
  selector_type: null,
  selector_value: 'xpath',
  x: 0,
  y: 0,
  width: 0,
  height: 0,
  shortcut: '',
  confidence: 0,
})
// 3️⃣ Workflows
const workflows = ref([])
const loadingWorkflows = ref(false)
const isLoadingWorkflow = ref(false)
const isInitialized = ref(false)
const isLayoutingWorkflow = ref(false)
const currentWorkflowId = ref(null)
const isSavingWorkflow = ref(false)
const formWorkflow = ref({
  name: '',
  description: '',
  status: 'draft',
})
const workflowState = reactive({
  nodesMap: new Map(),
  edgesMap: new Map(),
  updateQueue: [],
  isSyncing: false,
})
// 4️⃣ Nodes
const nodes = ref([])
const loadingNodes = ref(false)
const selectedNode = ref(null)
const currentNodeId = ref(null)
const nodeTypes = computed(() => ({ custom: CustomNode }))
const draggedItem = ref(null)
// 5️⃣ Edges
const edges = ref([])
const edgeTypes = computed(() => ({ custom: CustomEdge }))
// 6️⃣ ACTIONS
const showActionPanel = ref(false)
const newActionTypeForPanel = ref('open_program')
// 7️⃣ Tasks
const tasks = ref([])
const loadingTasks = ref(false)
const currentTaskId = ref(null)
const taskRunId = ref(null)
const currentTaskRunId = ref(null)
const createTaskVisible = ref(false)
const editTaskVisible = ref(false)
const formTask = ref({
  // Text
  name: '',
  description: '',
  program: null,
})
// 🔟 Delays
const delays = ref([])
const loadingDelays = ref([])
// ==============================================
// ================ 1️⃣ PROGRAMS ================
// ==============================================

// 2️⃣ Get Single

const loadProgram = async (id) => {
  await programStore.loadProgram(id)
}
// 3️⃣ Create Program
const createProgram = async () => {
  if (!programStore.validateForm()) return
  await programStore.createProgram()
}
// 4️⃣ update Program
const openEditProgram = async (id) => {
  await programStore.loadProgram(id)
  editProgramVisible.value = true
}
const editProgram = () =>
  programAction.run(() => programStore.updateProgram(), {
    successSummary: 'تم تحديث البرنامج',
    errorSummary: 'فشل تحديث البرنامج',
    onSuccess: () => {
      editProgramVisible.value = false
    },
  })
// 5️⃣ Delete Program
const confirmDeleteProgram = (program) => {
  console.log('🗑️ Delete Program:', program)
  confirm.require({
    message: `Are you sure you've deleted the program? "${program.name}"؟`,
    header: '⚠️ Confirm deletion',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Yes, delete',
    rejectLabel: 'Cancel order',
    accept: async () => {
      await deleteProgram(program.id)
    },
    reject: () => {
      toast.add({
        severity: 'info',
        summary: 'Cancelled',
        detail: 'The program was not deleted',
        life: 2000,
      })
    },
  })
}
const deleteProgram = async (id) => {
  await programStore.deleteProgram(id)
}
// 6️⃣ Open Program
const openProgram = (id) => programStore.openProgram(id)
// 7️⃣ Close Program
const closeProgram = (id) => programStore.closeProgram(id)
// 8️⃣ Status Program
const statusProgram = (id) => programStore.statusProgram(id).then((r) => r.data)
const focusProgram = (id) => programStore.focusProgram(id)
const maximizeProgram = (id) => programStore.maximizeProgram(id)
// ==============================================
// ============= 2️⃣ Program Elements ===========
// ==============================================
// 1️⃣ GET ALL
const loadProgramElements = async () => {
  loadingProgramElements.value = true
  try {
    const { data } = await automationService.listProgramElements()
    programsElement.value = data
  } catch (err) {
    showToast('error', 'فشل تحميل العناصر', err?.message)
  } finally {
    loadingProgramElements.value = false
  }
}
// 2️⃣ Get Single
const selectProgramElement = async (id) => {
  if (!id) return
  currentProgramElementId.value = id
  await loadProgramElement(id)
}
const loadProgramElement = async (id) => {
  const { data } = await automationService.getProgramElement(id)
  currentProgramElementId.value = data.id
  formProgramElement.value = {
    name: data.name,
    description: data.description,
    program: data.program,
    element_type: data.element_type,
    selector_type: data.selector_type,
    selector_value: data.selector_value,
    x: data.x,
    y: data.y,
    width: data.width,
    height: data.height,
    shortcut: data.shortcut,
    confidence: data.confidence,
    image: null,
  }
  return data
}
// 3️⃣ Create Program Element
const onImageChangeProgramElement = (e) => {
  const file = e.target.files[0]
  if (!file || !validateImageSize(file)) {
    e.target.value = ''
    return
  }
  formProgramElement.value.image = file
}
const buildElementFormData = (form) => {
  const fd = new FormData()
  fd.append('name', form.name)
  fd.append('description', form.description)
  fd.append('program', form.program)
  fd.append('element_type', form.element_type)
  fd.append('selector_type', form.selector_type)
  fd.append('selector_value', form.selector_value)
  fd.append('x', Number(form.x))
  fd.append('y', Number(form.y))
  fd.append('width', Number(form.width))
  fd.append('height', Number(form.height))
  fd.append('shortcut', form.shortcut)
  fd.append('confidence', parseFloat(form.confidence))
  if (form.image instanceof File) fd.append('image', form.image)
  return fd
}
const createProgramElement = () =>
  programElementAction.run(
    () => {
      const err = validateProgramElement(formProgramElement.value)
      if (err) {
        showToast('warn', 'تحقق من البيانات', err)
        throw new Error(err)
      }
      return automationService.createProgramElement(buildElementFormData(formProgramElement.value))
    },
    {
      successSummary: 'تم إنشاء العنصر',
      errorSummary: 'فشل إنشاء العنصر',
      onSuccess: async ({ data }) => {
        programsElement.value.unshift(data)
        createProgramElementsVisible.value = false
        // ✅ closes ONLY on success
        await loadProgramElements()
      },
    },
  )

// 4️⃣ update Program Element
const openEditProgramElement = async (id) => {
  if (!id) return
  try {
    currentProgramElementId.value = id
    await loadProgramElement(id)
    editProgramElementsVisible.value = true
    console.log('🟢 Edit Program ID:', id)
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
    console.error('❌ Failed to open edit Program Element', err)
  }
}
const editProgramElement = () =>
  programElementAction.run(
    () => {
      const err = validateProgramElement(formProgramElement.value)
      if (err) {
        showToast('warn', 'تحقق من البيانات', err)
        throw new Error(err)
      }
      return automationService.updateProgramElement(
        currentProgramElementId.value,
        buildElementFormData(formProgramElement.value),
      )
    },
    {
      successSummary: 'تم تحديث العنصر',
      errorSummary: 'فشل تحديث العنصر',
      onSuccess: async ({ data }) => {
        const idx = programsElement.value.findIndex((e) => e.id === data.id)
        if (idx !== -1) programsElement.value[idx] = { ...programsElement.value[idx], ...data }
        editProgramElementsVisible.value = false // ✅ closes ONLY on success
      },
    },
  )

// 5️⃣ Delete Program Element
const confirmDeleteProgramElement = (program) => {
  confirm.require({
    message: `Are you sure you've deleted the program? "${program.name}"؟`,
    header: '⚠️ Confirm deletion',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Yes, delete',
    rejectLabel: 'Cancel order',
    accept: async () => {
      await deleteProgramElement(program.id)
    },

    reject: () => {
      toast.add({
        severity: 'info',
        summary: 'Cancelled',
        detail: 'The program was not deleted',
        life: 2000,
      })
    },
  })
}
const deleteProgramElement = (id) =>
  programElementAction.run(() => automationService.deleteProgramElement(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      programsElement.value = programsElement.value.filter((p) => p.id !== id)
      if (currentProgramElementId.value === id) {
        currentProgramElementId.value = null
        formProgramElement.value = {}
      }
    },
  })
// ==============================================
// ================ 3️⃣ WORKFLOWS ===============
// ==============================================
// 1️⃣ GET ALL
const loadWorkflows = async () => {
  try {
    const { data } = await automationService.listWorkflows()
    workflows.value = data
  } catch (error) {
    showToast('error', 'فشل تحميل الـ Workflows', error?.message)
  } finally {
    loadingWorkflows.value = false
  }
}
// 2️⃣ Get Single
const loadWorkflowEvents = async (workflowId) => {
  if (!workflowId) return
  nodes.value = []
  edges.value = []
  const { data: wfData } = await automationService.getWorkflow(workflowId)
  currentWorkflowId.value = wfData.id
  formWorkflow.value = { name: wfData.name, description: wfData.description, status: wfData.status }
  try {
    const { data } = await automationService.getWorkflow_full_events(workflowId)
    nodes.value = (data.nodes || []).map((n) => ({
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
    }))
    edges.value = (data.edges || []).map((e) => ({
      id: e.id,
      source: e.source,
      target: e.target,
      type: e.type || 'custom',
      data: e.data || {},
    }))
  } catch (err) {
    showToast('error', 'فشل تحميل الـ Workflow Events', err?.message)
  }
}
// SELECT WORKFLOW
const selectWorkflow = async (id) => {
  if (!id) return
  isLoadingWorkflow.value = true
  debouncedAutoSave.cancel()
  currentWorkflowId.value = id
  await loadWorkflowEvents(id)
  isLoadingWorkflow.value = false
}
// 3️⃣ Create New Workflow
/*
const createWorkflow = () =>
  workflowAction.run(
    () => {
      if (!formWorkflow.value.name?.trim()) {
        showToast('warn', 'الاسم مطلوب', 'أدخل اسم الـ Workflow')
        throw new Error('Name required')
      }
      return automationService.createWorkflow({
        name: formWorkflow.value.name,
        description: formWorkflow.value.description,
        status: formWorkflow.value.status,
      })
    },
    {
      successSummary: 'تم إنشاء الـ Workflow',
      errorSummary: 'فشل إنشاء الـ Workflow',
      onSuccess: async ({ data }) => {
        workflows.value.unshift(data)
        currentWorkflowId.value = data.id
        nodes.value = []
        edges.value = []
        await loadWorkflowEvents(data.id)
      },
    },
  )
*/
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

// 4️⃣ SAVE Workflow
const saveWorkflow = async () => {
  if (!currentWorkflowId.value || isLoadingWorkflow.value || isSavingWorkflow.value) return
  const exists = workflows.value.find((w) => w.id === currentWorkflowId.value)
  if (!exists) return
  isSavingWorkflow.value = true
  isLoadingWorkflow.value = true
  debouncedAutoSave.cancel()
  const openNodeLabel = showActionPanel.value
    ? (selectedNode.value?.data?.node?.label ?? null)
    : null
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
    isLoadingWorkflow.value = true
    await loadWorkflowEvents(currentWorkflowId.value)
    isLoadingWorkflow.value = false
    if (openNodeLabel && showActionPanel.value) {
      const refreshed = nodes.value.find((n) => n.data?.node?.label === openNodeLabel)
      if (refreshed) selectedNode.value = refreshed
    }
    showToast('success', 'saved', 'Workflow saved', 12000)
  } catch (err) {
    showToast('error', 'فشل الحفظ', err?.message, 12000)
  } finally {
    isLoadingWorkflow.value = false
    // isSavingWorkflow.value = false
  }
}

const updateStatusWorkflow = (status) =>
  workflowAction.run(() => automationService.updateWorkflow(currentWorkflowId.value, { status }), {
    successSummary: 'تم تحديث الحالة',
    successDetail: `Status: ${status}`,
    errorSummary: 'فشل تحديث الحالة',
    onSuccess: () => {
      const wf = workflows.value.find((w) => w.id === currentWorkflowId.value)
      if (wf) wf.status = status
    },
  })

// 5️⃣ Delete Workflow
const deleteWorkflow = (id) =>
  workflowAction.run(() => automationService.deleteWorkflow(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: async () => {
      workflows.value = workflows.value.filter((w) => w.id !== id)
      if (currentWorkflowId.value === id) {
        currentWorkflowId.value = null
        nodes.value = []
        edges.value = []
      }
      await loadWorkflows()
    },
  })

const clearWorkflow = () => {
  nodes.value = []
  edges.value = []
}
/* ===================================================
📐 7️⃣ AUTO LAYOUT (Dagre)
=================================================== */
function autoLayout(dir = 'TB') {
  isLayoutingWorkflow.value = true
  const g = new dagre.graphlib.Graph()
  g.setGraph({ rankdir: dir, nodesep: 50, ranksep: 80 })
  g.setDefaultEdgeLabel(() => ({}))
  nodes.value.forEach((n) => g.setNode(n.id, { width: 180, height: 60 }))
  edges.value.forEach((e) => g.setEdge(e.source, e.target))
  dagre.layout(g)
  nodes.value = nodes.value.map((node) => {
    const pos = g.node(node.id)
    return { ...node, position: { x: pos.x - 90, y: pos.y - 30 } }
  })
  setTimeout(() => {
    isLayoutingWorkflow.value = false
  }, 400)
}

// ==============================================
// =================== 4️ Node =================
// ==============================================

// 1️⃣ GET ALL
const loadlistWorkflowNodes = async () => {
  try {
    const { data } = await automationService.listWorkflowNodes()
    nodes.value = data.map((n) => ({
      ...n,
      type: 'custom',
      position: {
        x: n.position_x,
        y: n.position_y,
      },
      data: n.data,
    }))
    nodes.value.forEach((n) => {
      workflowState.nodesMap.set(n.id, n)
    })
  } catch (error) {
    showToast('error', 'فشل تحميل الـ Workflows', error?.message, 12000)
  } finally {
    loadingNodes.value = false
  }
}

// 2️⃣ Get Single Node
const loadNode = async (id) => {
  const { data } = await automationService.getWorkflowNode(id)
  currentNodeId.value = data.id
}
// ==================================================
// 🎯 Helper — اجيب الـ fresh node من الـ state مش الـ stale
// ==================================================
const getFreshNode = (nodeId) => {
  return (
    nodes.value.find((n) => n.id === nodeId || n.data?.node?.backend_id === nodeId) ??
    selectedNode.value
  )
}
// ==================================================
// 🖱️ onNodeSelect — عند الضغط على Node
// ==================================================
const onNodeSelect = async ({ node }) => {
  const freshNode = getFreshNode(node.id)
  selectedNode.value = freshNode ?? node
  showActionPanel.value = true
  if (node.id) await loadNode(node.id)
}
// 3️⃣ createNode
const createNode = async (item, dropEvent) => {
  if (!currentWorkflowId.value) {
    showToast('warn', 'لا يوجد Workflow', 'اختر Workflow الأول', 9000)
    return
  }
  isLoadingWorkflow.value = true
  debouncedAutoSave.cancel()
  try {
    const position = project({ x: dropEvent.clientX, y: dropEvent.clientY })
    const baseActionMap = { program: 'open_program', 'program-element': 'press', delay: 'wait' }
    const actionType = baseActionMap[item.type] || 'custom'
    await loadProgram(item.id)
    // ==============================
    // 🎨 3️⃣ UI Config - شكل النود
    // ==============================
    const uiConfig = {
      ui: {
        theme: {
          background: '#0f172a',
          border: '#334155',
          shadow: '#334155',
        },
        layout: {
          width: 260,
          height: 240,
          rounded: true,
        },
      },
      inputs: [
        { key: 'text', label: 'Text', type: 'string', value: '' },
        { key: 'delay', label: 'Delay (ms)', type: 'number', value: 0 },
        { key: 'color', label: 'Background Color', type: 'color', value: '#0f172a' },
      ],
      ai: {
        enabled: false,
        context: {},
        memory: [],
        suggestions: [],
      },
    }

    // =============================
    // 2️⃣ NODE PAYLOAD (NO ACTION)
    // =============================
    // ==============================
    // 📦 4️⃣ Node Payload للباك اند
    // ==============================

    const nodePayload = {
      // 1️⃣ WorkflowId:
      workflow: currentWorkflowId.value,
      // 2️⃣
      node_type: item.type,
      // 3️⃣
      label: `${actionType}` || 'New Node',
      // 4️⃣
      program: item.type === 'program' ? item.id : null,
      // 5️⃣
      element: item.type === 'program-element' ? item.id : null,
      //
      position_x: position.x,
      // 7️⃣
      position_y: position.y,
      config: uiConfig,
    }

    // =============================
    // 3️⃣ CREATE NODE IN BACKEND
    // =============================
    // ==============================
    // 💾 5️⃣ إنشاء Node في الباك اند
    // ==============================

    const { data: nodeData } = await automationService.createWorkflowNode(nodePayload)

    // ==============================
    // ⚡ 6️⃣ إنشاء Action وربطه بالنود
    //    لازم يخلص قبل الـ push
    //    عشان save_all ميمسحوش
    // ==============================
    const actionResponse = await createAction({
      node: nodeData.id,
      action_type: actionType,
      payload: {},
    })

    // ==============================
    // 🖼️ 8️⃣ إضافة النود للـ Canvas فورًا
    //    بنفس structure بتاعة loadWorkflowEvents
    //    عشان CustomNode يقدر يقراها
    // ==============================
    nodes.value.push({
      id: nodeData.id,
      type: 'custom',
      position: {
        x: nodeData.position_x,
        y: nodeData.position_y,
      },
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

    showToast('success', 'Node Created ', nodeData.label, 9000)
  } catch (err) {
    showToast('error', 'فشل إنشاء الـ Node', err?.message, 9000)
  } finally {
    isLoadingWorkflow.value = false
  }
}
// 4️⃣ updateNode
const enqueueUpdate = (job) => {
  workflowState.updateQueue.push(job)
  debouncedSync()
}
const processQueue = async () => {
  if (workflowState.isSyncing) return
  workflowState.isSyncing = true

  while (workflowState.updateQueue.length > 0) {
    const job = workflowState.updateQueue.shift()

    try {
      if (job.type === 'node-position') {
        await automationService.updateWorkflowNode(job.id, {
          position_x: job.position_x,
          position_y: job.position_y,
        })
      }

      if (job.type === 'node-config') {
        await automationService.updateWorkflowNode(job.id, job.data)
      }

      if (job.type === 'action') {
        await automationService.updateAction(job.id, job.data)
      }
    } catch (err) {
      console.error('Sync error:', err)
    }
  }

  workflowState.isSyncing = false
}
const debouncedSync = debounce(() => {
  processQueue()
}, 300)
/* ----------------- DRAG & DROP ----------------- */
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

const runTaskFromNode = async (nodeData) => {
  console.log('Run Node:', nodeData)

  const backendId = nodeData?.backend_id

  if (!backendId) {
    console.error('❌ Backend node ID missing', nodeData)
    toast.add({
      severity: 'error',
      summary: 'Node Error',
      detail: 'Backend ID not found',
      life: 3000,
    })
    return
  }

  try {
    const res = await automationService.runWorkflowNode(backendId)
    const action = nodeData.config?.action || 'open'

    switch (action) {
      case 'open':
        openProgram(nodeData.programId)
        break
      case 'close':
        closeProgram(nodeData.programId)
        break
      case 'status':
        statusProgram(nodeData.programId)
        break
      case 'focus':
        focusProgram(nodeData.programId)
        break
      case 'maximize':
        maximizeProgram(nodeData.programId)
        break
    }

    console.log('Node Result:', res.data)
    toast.add({
      severity: 'success',
      summary: 'Node Running',
      detail: 'Task executed successfully',
      life: 2500,
    })
  } catch (e) {
    console.error(e)
    toast.add({
      severity: 'error',
      summary: 'Execution Failed',
      detail: e.response?.data || e.message,
      life: 4000,
    })
  }
}

const deleteNodeOnWorkflow = async (id) => {
  if (!id) return

  try {
    await automationService.deleteWorkflowNode(id)

    toast.add({
      severity: 'success',
      summary: '✅ Deleted',
      detail: 'The program was successfully deleted',
      life: 3000,
    })
    nodes.value = nodes.value.filter((n) => n.id !== id)
    edges.value = edges.value.filter((e) => e.source !== id && e.target !== id)
  } catch (err) {
    console.error(err)
    toast.add({
      severity: 'error',
      summary: '❌ mistake',
      detail: 'Program deletion failed',
      life: 3000,
    })
  }
}
// ==================================================
// ⚡ createNodeAction — FIX إنشاء Action جديد للـ Node المختار
// ==================================================
const createNodeAction = async ({ nodeId, action_type, payload }) => {
  // ✅ اجيب الـ node الحالي من الـ state (مش selectedNode القديم)
  const freshNode = getFreshNode(nodeId)
  const realId = freshNode?.data?.node?.backend_id ?? freshNode?.id

  console.log('⚡ createNodeAction realId:', realId)

  if (!realId) {
    toast.add({ severity: 'error', summary: '❌ Node ID missing', life: 3000 })
    return
  }

  try {
    const varPayload = {
      ai: {
        memory: [],
        context: {},
        enabled: false,
        suggestions: [],
      },
      ui: {
        theme: {
          border: '#334155',
          shadow: '#334155',
          background: '#0f172a',
        },
        layout: {
          width: 260,
          height: 240,
          rounded: true,
        },
      },
      inputs: [
        {
          key: 'text',
          type: 'string',
          label: 'Text',
          value: '',
        },
        {
          key: 'delay',
          type: 'number',
          label: 'Delay (ms)',
          value: 0,
        },
        {
          key: 'color',
          type: 'color',
          label: 'Background Color',
          value: '#0f172a',
        },
      ],
    }
    const actionResponse = await createAction({
      node: realId,
      action_type: action_type,
      payload: varPayload,
    })
    if (!actionResponse) return

    // ✅ تحديث الـ state
    const idx = nodes.value.findIndex((n) => n.id === realId || n.data?.node?.backend_id === realId)
    if (idx !== -1) {
      nodes.value[idx] = {
        ...nodes.value[idx],
        data: {
          ...nodes.value[idx].data,
          actions: [...(nodes.value[idx].data.actions ?? []), actionResponse],
        },
      }
      // ✅ تحديث الـ Panel بالـ node الجديد
      selectedNode.value = nodes.value[idx]
    }

    toast.add({
      severity: 'success',
      summary: '✅ Action Created',
      detail: action_type,
      life: 2000,
    })
    console.log('payload: ', payload)
  } catch (err) {
    console.error('❌ createNodeAction:', err)
  }
  // console.log('payload: ', payload)
}
// ==================================================
// ✏️ updateNodeAction — تعديل Action موجود
// ==================================================
const updateNodeAction = async ({ nodeId, actionId, newActionType }) => {
  try {
    const payload = buildPayloadFromUI(newActionType, {})

    // ✅ تحديث UI فوراً
    const idx = nodes.value.findIndex((n) => n.id === nodeId)
    if (idx !== -1) {
      const updated = { ...nodes.value[idx] }
      updated.data = { ...updated.data }
      updated.data.actions = updated.data.actions.map((a) =>
        a.id === actionId ? { ...a, action_type: newActionType, payload } : a,
      )
      nodes.value[idx] = updated
      selectedNode.value = nodes.value[idx] // ✅ تحديث الـ panel
    }

    // ✅ تحديث الباك اند
    await automationService.updateAction(actionId, { action_type: newActionType, payload })

    toast.add({
      severity: 'success',
      summary: '✅ Action Updated',
      detail: newActionType,
      life: 2000,
    })
  } catch (err) {
    console.error('❌ updateNodeAction:', err)
  }
}
// ==================================================
// 🗑️ deleteNodeAction — حذف Action
// ==================================================
const deleteNodeAction = async ({ nodeId, actionId }) => {
  try {
    await automationService.deleteAction(actionId)

    const idx = nodes.value.findIndex((n) => n.id === nodeId)
    if (idx !== -1) {
      const updated = { ...nodes.value[idx] }
      updated.data = { ...updated.data }
      updated.data.actions = updated.data.actions.filter((a) => a.id !== actionId)
      nodes.value[idx] = updated
      selectedNode.value = nodes.value[idx]
    }

    toast.add({ severity: 'success', summary: '🗑️ Deleted', life: 2000 })
  } catch (err) {
    console.error('❌ deleteNodeAction:', err)
  }
}
// ==============================================
// =================== 5️⃣ Edge =================
// =============================================
/* ----------------- CONNECT ----------------- */
const onConnect = async (params) => {
  if (!currentWorkflowId.value) return
  // 🧠 جهز Payload
  const nodePayload = {
    workflow: currentWorkflowId.value,
    source_node: params.source,
    target_node: params.target,
    condition: 'success',
    // type: 'custom',
    // data: {
    //   label: 'Next',
    // },
  }

  try {
    // 💾 حفظ في الباك إند
    const { data } = await automationService.createWorkflowEdge(nodePayload)

    // 🔗 إنشاء Edge في الفرونت
    const edge = {
      id: data.id,
      source: data.source_node,
      target: data.target_node,
      sourceHandle: 'source', // 🟢 مهم
      targetHandle: 'target', // 🔴 مهم

      type: 'default',

      data: {
        label: data.condition,
      },
      animated: true,
      style: {
        stroke: '#4CAF50',
        strokeWidth: 2,
      },
    }

    edges.value.push(edge)

    toast.add({
      severity: 'success',
      summary: '✅ Edge Created',
      detail: 'Nodes connected successfully',
      life: 2500,
    })
  } catch (err) {
    console.error(err)
    toast.add({
      severity: 'error',
      summary: '❌ Error',
      detail: 'Failed to create edge',
      life: 3000,
    })
  }
}
/* --------------- NODE DRAG STOP --------------- */
const onNodeDragStop = (node) => {
  // if (!node?.data?.backend_id) return
  const backendId = node.data?.node?.backend_id ?? node.id
  if (!backendId) return

  enqueueUpdate({
    type: 'node-position',
    // id: node.data.backend_id,
    id: backendId,
    position_x: node.position.x,
    position_y: node.position.y,
  })
}
const startWorkflow = async () => {
  if (!currentWorkflowId.value) {
    alert('اختر Workflow الأول')
    return
  }

  try {
    const { data } = await automationService.runWorkflow(currentWorkflowId.value)
    alert('🚀 Workflow Started')
    currentTaskRunId.value = data.task_run_id

    toast.add({
      severity: 'success',
      summary: '🚀 Workflow Started ',
      detail: 'Workflow Started successfully',
      life: 2500,
    })
  } catch (err) {
    console.error(err)
    alert('❌ Error starting workflow')
  }
}
// ==============================================
// ================== 6️⃣ ACTIONS ===============
// ==============================================
// 3️⃣ Create ACTION
const createAction = async ({ node, action_type, payload }) => {
  try {
    const res = await automationService.createAction({ node, action_type, payload })
    console.log('✅ Action created:', res.data)
    toast.add({
      severity: 'success',
      summary: `✅ Action created`,
      detail: `${action_type}`,
      life: 3000,
    })
    return res.data
  } catch (error) {
    console.error(error)
    console.error('❌ createAction 400 DETAILS:', error.response?.data)
    toast.add({ severity: 'error', summary: '❌ Error', detail: error.message, life: 3000 })
  }
}
const getColorFromAction = (type) => {
  switch (type) {
    case 'open_program':
      return '#16a34a'
    case 'close_program':
      return '#dc2626'
    case 'wait':
      return '#0ea5e9'
    case 'press':
      return '#64748b'
    case 'hotkey':
      return '#f59e0b'
    default:
      return '#334155'
  }
}
const buildPayloadFromUI = (type, extraData = {}) => {
  switch (type) {
    case 'wait':
      return {
        seconds: Number(extraData.delay || 0),
      }

    case 'press':
      return {
        key: extraData.key,
      }

    case 'hotkey':
      return {
        keys: extraData.keys,
      }

    case 'click_element':
      return {
        element_id: extraData.element_id,
      }

    case 'open_program':
      return {}

    default:
      return {}
  }
}
const handleUpdateNodeAction = async ({ nodeId, newActionType, extraData }) => {
  const node = workflowState.nodesMap.get(nodeId)
  if (!node) return

  // ===============================
  // 1️⃣ Update Local UI Immediately
  // ===============================

  const payload = buildPayloadFromUI(newActionType, extraData)

  node.data.actions.action_type = newActionType
  node.data.actions.payload = payload

  node.data.config.ui.background = getColorFromAction(newActionType)

  // force reactivity
  nodes.value = [...nodes.value]

  // ===============================
  // 2️⃣ Queue Backend Sync
  // ===============================

  workflowState.updateQueue.push({
    type: 'action',
    nodeId,
    actionId: node.data.actions.id,
    action_type: newActionType,
    payload,
  })

  syncWithBackend()
}
const syncWithBackend = async () => {
  if (workflowState.isSyncing) return
  workflowState.isSyncing = true

  while (workflowState.updateQueue.length) {
    const job = workflowState.updateQueue.shift()

    try {
      if (job.type === 'action') {
        await automationService.updateAction(job.actionId, {
          action_type: job.action_type,
          payload: job.payload,
        })
      }

      if (job.type === 'node-position') {
        await automationService.updateWorkflowNode(job.nodeId, job.data)
      }
    } catch (err) {
      console.error('Sync failed:', err)
    }
  }

  workflowState.isSyncing = false
}
// ==============================================
// ================== 7️⃣ Load ===============
// ==============================================
const loadTasks = async () => {
  loadingTasks.value = true
  try {
    const { data } = await automationService.listTasks()
    tasks.value = data
  } finally {
    loadingTasks.value = false
    console.log('Tasks STORE DATA 👉', tasks.value)
  }
}
// 2️⃣ Get Single
const selectTask = async (id) => {
  if (!id) return
  currentTaskId.value = id
  console.log('selectProgram currentTaskId: ', currentTaskId.value)
  await loadTask(id)
}
const loadTask = async (id) => {
  console.log('load Task By id: ', id)
  const { data } = await automationService.getTask(id)
  currentTaskId.value = data.id
  formTask.value = {
    name: data.name,
    description: data.description,
    program: data.program,
  }
}
// 3️⃣ Create Task
const createTask = () =>
  taskAction.run(
    () => {
      const err = validateTask(formTask.value)
      if (err) {
        showToast('warn', 'تحقق من البيانات', err)
        throw new Error(err)
      }
      const fd = new FormData()
      fd.append('name', formTask.value.name)
      fd.append('description', formTask.value.description)
      fd.append('program', formTask.value.program)
      return automationService.createTask(fd)
    },
    {
      successSummary: 'تم إنشاء الـ Task',
      errorSummary: 'فشل إنشاء الـ Task',
      onSuccess: async ({ data }) => {
        tasks.value.unshift(data)
        currentTaskId.value = data.id
        createTaskVisible.value = false // ✅ closes ONLY on success
        await loadTasks()
      },
    },
  )

// 4️⃣ update Task
const openEditTask = async (id) => {
  if (!id) return

  try {
    // 1️⃣ حدد البرنامج
    currentProgramElementId.value = id

    // 2️⃣ حمّل بياناته
    await loadProgramElement(id)

    // 3️⃣ افتح المودال
    editProgramElementsVisible.value = true

    console.log('🟢 Edit Program ID:', id)
  } catch (err) {
    console.error('❌ Failed to open edit program', err)
  }
}
const editTask = () =>
  taskAction.run(
    () => {
      const fd = new FormData()
      fd.append('name', formProgramElement.value.name)
      fd.append('description', formProgram.value.description)
      fd.append('program', formProgramElement.value.program)
      if (formProgramElement.value.image instanceof File)
        fd.append('image', formProgramElement.value.image)
      return automationService.updateProgramElement(currentProgramElementId.value, fd)
    },
    {
      successSummary: 'تم تحديث الـ Task',
      errorSummary: 'فشل تحديث الـ Task',
      onSuccess: async () => {
        editTaskVisible.value = false // ✅ closes ONLY on success
        await loadProgramElements()
      },
    },
  )

// 5️⃣ Delete Task
const confirmDeleteTask = (program) => {
  console.log('🗑️ Delete Task:', program)

  confirm.require({
    message: `Are you sure you've deleted the Task? "${program.name}"؟`,
    header: '⚠️ Confirm deletion',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Yes, delete',
    rejectLabel: 'Cancel order',

    accept: async () => {
      await deleteTask(program.id)
    },

    reject: () => {
      toast.add({
        severity: 'info',
        summary: 'Cancelled',
        detail: 'The program was not deleted',
        life: 2000,
      })
    },
  })
}
const deleteTask = (id) =>
  taskAction.run(() => automationService.deleteTask(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      programsElement.value = programsElement.value.filter((p) => p.id !== id)
      if (currentProgramElementId.value === id) {
        currentProgramElementId.value = null
        formProgramElement.value = {}
      }
    },
  })

// ==============================================
// ================== 🔟 Delays ================
// ==============================================
const loadDelays = async () => {
  loadingDelays.value = true
  try {
    const { data } = await automationService.listDelays()
    delays.value = data
  } catch (error) {
    console.log('Error Delays STORE DATA 👉: ', error)
  } finally {
    loadingDelays.value = false
    //console.log('Delays STORE DATA 👉', delays.value)
  }
}
// ==================================================
// 💾 6️⃣ Auto Save (حفظ تلقائي)
// ==================================================
/* ----------------- watch ----------------- */
// ⏳ debounce يمنع التنفيذ المتكرر
const debouncedAutoSave = debounce(() => {
  console.log('💾 Auto Saving...')
  if (!isInitialized.value) return
  if (!currentWorkflowId.value) return
  if (isLoadingWorkflow.value) return
  // if (isSavingWorkflow.value) return
  /* --------------------------
  🔗 3️⃣ مزامنة Program ID
  ---------------------------*/
  if (currentProgramId.value) {
    formProgramElement.value.program = currentProgramId.value
  }

  const exists = workflows.value.find((w) => w.id === currentWorkflowId.value)
  if (!exists) return
  saveWorkflow()

  /* --------------------------
  🧠 Debug Logs
  ---------------------------*/
  console.log('Nodes:', nodes.value)
  console.log('formWorkflow:', formWorkflow.value)
}, 500)
// ==================================================
// 👀 مراقبة التغييرات
// ==================================================
watch([nodes, edges], debouncedAutoSave, { deep: true })
watch(currentProgramId, (newId) => {
  if (newId) formProgramElement.value.program = newId
})
/* ----------------- MOUNT ----------------- */
onMounted(async () => {
  await Promise.all([
    // 1️⃣ Program
    await programStore.loadPrograms(),
    // 2️⃣ ProgramElements
    loadProgramElements(),
    // 3️⃣ Workflows
    loadWorkflows(),
    // 4️⃣
    loadlistWorkflowNodes(),
    // 5️⃣ Delays
    loadDelays(),

    loadTasks(),
  ])
  isInitialized.value = true
  // 👇 لو فيه Workflow مختار
  if (currentWorkflowId.value) {
    await loadWorkflowEvents(currentWorkflowId.value)
  }

  console.log('🟢 APP READY')
})

// ③ استخدم execute() بدل axios مباشرة
async function createProduct() {
  try {
    const data = await execute({
      url: '/api/automation/programs/',
      method: 'POST',
      data: formProgram.value,
    })
    // products.value.push(data)
    // ✅ استخدم البيانات عادي
    console.log('e: ', data)
  } catch (e) {
    console.log('e: ', e)
    // الـ ApiFlowPanel بيعرض الخطأ تلقائياً
  }
}
</script>

<template>
  <main class="h-screen p-4">
    <div class="grid grid-cols-12 gap-4 h-full">
      <aside class="col-span-3 border rounded p-4 overflow-auto space-y-6">
        <div>
          <div class="flex justify-between items-center my-3">
            <h3 class="text-lg font-bold">
              <prime_tag value="🖥️ Programs" />
            </h3>
            <prime_button
              icon="pi pi-plus"
              @click="createProgramVisible = true"
              style="background-color: transparent; padding: 0; border: none"
            >
              <prime_tag icon="pi pi-plus" />
            </prime_button>
          </div>
          <div class="wrapper_programs">
            <div class="" v-if="loadingPrograms">
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              >
              </prime_skeleton>
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              >
              </prime_skeleton>
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              >
              </prime_skeleton>
            </div>
            <div
              v-for="p in programs"
              :key="p.id"
              class="p-1 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'program', id: p.id })"
              v-else
              @click="selectProgram(p.id)"
            >
              <prime_image alt="Image" preview>
                <template #previewicon> <i class="pi pi-search"></i> </template>
                <template #image>
                  <img :src="p.get_image" alt="image" />
                </template>
                <template #preview="slotProps">
                  <img
                    :src="p.get_image"
                    alt="preview"
                    :style="slotProps.style"
                    @click="slotProps.onClick"
                  />
                </template>
              </prime_image>
              <prime_tag :value="p.name" />
              <div class="">
                <prime_button
                  icon="pi pi-plus"
                  @click.stop="openEditProgram(p.id)"
                  style="background-color: transparent; padding: 0; border: none"
                >
                  <prime_tag icon="pi pi-file-edit" />
                </prime_button>
                <prime_button
                  icon="pi pi-plus"
                  @click.stop="confirmDeleteProgram(p)"
                  style="background-color: transparent; padding: 0; border: none"
                >
                  <prime_tag icon="pi pi-trash" />
                </prime_button>
              </div>
            </div>
          </div>
        </div>
        <div>
          <div class="flex justify-between items-center my-3">
            <h3 class="text-lg font-bold">
              <prime_tag value="🧩 Program Elements" />
            </h3>
            <prime_button
              icon="pi pi-plus"
              @click="createProgramElementsVisible = true"
              style="background-color: transparent; padding: 0; border: none"
            >
              <prime_tag icon="pi pi-plus" />
            </prime_button>
          </div>
          <div class="wrapper_programs">
            <div class="" v-if="loadingProgramElements">
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              >
              </prime_skeleton>
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              >
              </prime_skeleton>
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              >
              </prime_skeleton>
            </div>
            <div
              v-for="p in programsElement"
              :key="p.id"
              class="p-1 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'program-element', id: p.id })"
              v-else
              @click="selectProgramElement(p.id)"
            >
              <prime_image alt="Image" preview>
                <template #previewicon> <i class="pi pi-search"></i> </template>
                <template #image> <img :src="p.get_image" alt="image" /> </template>
                <template #preview="slotProps">
                  <img
                    :src="p.get_image"
                    alt="preview"
                    :style="slotProps.style"
                    @click="slotProps.onClick"
                  />
                </template>
              </prime_image>
              <prime_tag :value="p.name" />
              <div class="">
                <prime_button
                  icon="pi pi-plus"
                  @click.stop="openEditProgramElement(p.id)"
                  style="background-color: transparent; padding: 0; border: none"
                >
                  <prime_tag icon="pi pi-file-edit" />
                </prime_button>
                <prime_button
                  icon="pi pi-plus"
                  @click.stop="confirmDeleteProgramElement(p)"
                  style="background-color: transparent; padding: 0; border: none"
                >
                  <prime_tag icon="pi pi-trash" />
                </prime_button>
              </div>
            </div>
          </div>
        </div>
        <div>
          <div class="flex justify-between items-center my-3">
            <h3 class="text-lg font-bold">
              <prime_tag value="Delays" />
            </h3>
            <RouterLink to="/">
              <prime_tag icon="pi pi-plus" />
            </RouterLink>
          </div>
          <div class="wrapper_delays">
            <div class="" v-if="loadingDelays">
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              >
              </prime_skeleton>
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              >
              </prime_skeleton>
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              >
              </prime_skeleton>
            </div>
            <div
              v-for="d in delays"
              :key="d.id"
              class="p-2 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'delay', id: d.id })"
              v-else
            >
              <i class="pi pi-stopwatch"></i>
              <prime_tag :value="d.seconds + 's'" />
              <prime_tag value="Delay" />
            </div>
          </div>
        </div>
        <div>
          <h3 class="text-lg font-bold mb-3">Workflows</h3>
          <div class="space-y-2">
            <div
              v-for="w in workflows"
              :key="w.id"
              class="p-2 bg-white border rounded cursor-pointer align-content-between"
              @click="selectWorkflow(w.id)"
            >
              <span>{{ w.name }}</span>
              <span
                class="text-xs px-2 py-1 rounded"
                :class="{
                  'bg-gray-200': w.status === 'draft',
                  'bg-green-200': w.status === 'active',
                  'bg-yellow-200': w.status === 'paused',
                }"
              >
                {{ w.status }}
              </span>
            </div>
          </div>
        </div>
        <div>
          <div class="flex justify-between items-center mb-3">
            <h3 class="text-lg font-bold">
              <prime_tag value="Tasks Templates" />
            </h3>
            <prime_button
              icon="pi pi-plus"
              @click="createTaskVisible = true"
              style="background-color: transparent; padding: 0; border: none"
            >
              <prime_tag icon="pi pi-plus" />
            </prime_button>
          </div>
          <div class="wrapper_programs">
            <div class="" v-if="loadingTasks">
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              >
              </prime_skeleton>
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              >
              </prime_skeleton>
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              >
              </prime_skeleton>
            </div>
            <div
              v-for="t in tasks"
              :key="t.id"
              class="p-1 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'task', id: t.id })"
              v-else
              @click="selectTask(t.id)"
            >
              <prime_tag :value="t.name" />
              <div class="">
                <prime_button
                  icon="pi pi-plus"
                  @click.stop="openEditTask(t.id)"
                  style="background-color: transparent; padding: 0; border: none"
                >
                  <prime_tag icon="pi pi-file-edit" />
                </prime_button>
                <prime_button
                  icon="pi pi-plus"
                  @click.stop="confirmDeleteTask(t)"
                  style="background-color: transparent; padding: 0; border: none"
                >
                  <prime_tag icon="pi pi-trash" />
                </prime_button>
              </div>
            </div>
          </div>
        </div>
        <div class="">
          <vuedraggable :list="programs" group="tasks" class="draggable-list">
            <template #item="{ element }">
              <div
                class="draggable-item"
                draggable="true"
                @dragstart="(event) => onDragStart(event, element)"
              >
                <div
                  v-for="p in programs"
                  :key="p.id"
                  class="p-1 rounded cursor-grab link_aside"
                  draggable="true"
                  @dragstart="startDrag({ type: 'program', id: p.id })"
                  @click="selectProgram(p.id)"
                >
                  <prime_image alt="Image" preview>
                    <template #previewicon> <i class="pi pi-search"></i> </template>
                    <template #image>
                      <img :src="p.get_image" alt="image" />
                    </template>
                    <template #preview="slotProps">
                      <img
                        :src="p.get_image"
                        alt="preview"
                        :style="slotProps.style"
                        @click="slotProps.onClick"
                      />
                    </template>
                  </prime_image>
                  <prime_tag :value="p.name" />
                  <div class="">
                    <prime_button
                      icon="pi pi-plus"
                      @click.stop="openEditProgram(p.id)"
                      style="background-color: transparent; padding: 0; border: none"
                    >
                      <prime_tag icon="pi pi-file-edit" />
                    </prime_button>
                    <prime_button
                      icon="pi pi-plus"
                      @click.stop="confirmDeleteProgram(p)"
                      style="background-color: transparent; padding: 0; border: none"
                    >
                      <prime_tag icon="pi pi-trash" />
                    </prime_button>
                  </div>
                </div>
              </div>
            </template>
          </vuedraggable>
        </div>
      </aside>
      <section class="col-span-9 mb-16">
        <div class="wrapper_name_description">
          <div class="inner_name_description">
            <div>
              <label class="block font-semibold mb-1">Name</label>
              <input
                v-model="formWorkflow.name"
                type="text"
                class="input"
                placeholder="Program name"
              />
            </div>
            <div>
              <label class="block font-semibold mb-1">Description</label>
              <textarea
                v-model="formWorkflow.description"
                placeholder="Program description"
                name=""
                id=""
                class="textarea"
                cols="30"
                rows="1"
              ></textarea>
            </div>
            <div>
              <label class="block font-semibold mb-1">Status</label>
              <select v-model="formWorkflow.status" class="input">
                <option value="draft">📝 Draft</option>
                <option value="active">✅ Active</option>
                <option value="paused">⏸ Paused</option>
              </select>
            </div>
            <div>
              <prime_button
                label="🗑️"
                @click="deleteWorkflow(currentWorkflowId)"
                class="class_name"
              />
            </div>
          </div>
        </div>
        <VueFlow
          class="border rounded"
          v-model:nodes="nodes"
          v-model:edges="edges"
          :node-types="nodeTypes"
          :edge-types="edgeTypes"
          @node-click="onNodeSelect"
          @dragover="onDragOver"
          @drop="onDrop"
          @connect="onConnect"
          @nodeDragStop="onNodeDragStop"
          :pan-on-drag="[1]"
          :pan-on-scroll="true"
          :zoom-on-scroll="false"
        >
          <Background variant="dots" pattern-color="#aaa" :gap="10" />
          <Controls />
          <template #node-custom="props">
            <CustomNode
              v-bind="props"
              @run-task="runTaskFromNode"
              @open-program="openProgram"
              @close-program="closeProgram"
              @status-program="statusProgram"
              @delete-node="deleteNodeOnWorkflow"
              @update-node-action="handleUpdateNodeAction"
            />
          </template>
          <template #edge-custom="props">
            <CustomEdge v-bind="props" />
          </template>
          <MiniMap />
          <Panel position="top-left">
            <div class="flex gap-2">
              <button @click="createWorkflow" class="btn-white">➕ إنشاء Workflow جديد</button>
              <button @click="saveWorkflow" class="btn-white">💾 Save Workflow</button>
              <button @click="clearWorkflow" class="btn-white">🗑️ مسح الكل</button>
              <button @click="updateStatusWorkflow('active')">▶ Activate</button>
              <button @click="updateStatusWorkflow('paused')">⏸ Pause</button>
              <prime_button
                label="Start Workflow"
                icon="pi pi-play"
                class="p-button-success"
                :disabled="!currentWorkflowId"
                @click.once="startWorkflow"
              />
            </div>
            <div class="inner_control_node_layout_buttons">
              <button @click="autoLayout('LR')">LR 📐</button>
              <button @click="autoLayout('RL')">RL 📐</button>
              <button @click="autoLayout('TB')">TB 📐</button>
              <button @click="autoLayout('BT')">BT 📐</button>
              <button type="button" @click="findIsolatedNodes">find Isolated Nodes</button>
            </div>
          </Panel>
        </VueFlow>
      </section>
    </div>
    <LiveConsole v-if="taskRunId" :taskRunId="currentTaskRunId" />
    <ApiFlowPanel :stages="stages" :meta="meta" :error="error" :show-data="true" />
    <button @click="createProduct">إضافة منتج</button>

    <ActionPanel
      :show="showActionPanel"
      :selected-node="selectedNode"
      v-model:new-action-type-for-panel="newActionTypeForPanel"
      @close="showActionPanel = false"
      @create-action="createNodeAction"
      @update-action="updateNodeAction"
      @delete-action="deleteNodeAction"
    />
    <CreateProgram
      v-model:visible="createProgramVisible"
      :form="form"
      @image-change="programStore.onImageChange"
      @submit="createProgram"
    />
    <EditProgram v-model:visible="editProgramVisible" :progrm="form" @submit="editProgram" />

    <div class="card flex justify-center" style="overflow-y: auto">
      <prime_dialog
        v-model:visible="createProgramElementsVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div class="" style="margin: auto; font-size: 2rem; font-weight: bolder">
              Create Program Element
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="programName" class="text-primary-50 font-semibold">Program Name</label>
                <prime_input_text
                  id="programName"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.name"
                  type="text"
                  placeholder="Program name"
                ></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="description" class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  id="description"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.description"
                  placeholder="Program description"
                ></prime_textarea>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="description" class="text-primary-50 font-semibold">Image</label>
                <input type="file" accept="image/*" @change="onImageChangeProgramElement" />
              </div>

              <div class="inline-flex flex-col gap-2">
                <label for="program" class="text-primary-50 font-semibold"
                  >Program Project Id</label
                >
                <select v-model="formProgramElement.program" class="input">
                  <option disabled value="">اختر البرنامج</option>
                  <option v-for="p in programs" :key="p.id" :value="p.id">
                    {{ p.name }}
                  </option>
                </select>
              </div>

              <div class="inline-flex flex-col gap-2">
                <label for="selector_value" class="text-primary-50 font-semibold"
                  >Selector Value</label
                >
                <select v-model="formProgramElement.selector_type">
                  <option disabled value="">Choose selector type</option>

                  <option
                    v-for="type in programElementselectorTypes"
                    :key="type.value"
                    :value="type.value"
                  >
                    {{ type.label }}
                  </option>
                </select>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="Program_element_x" class="text-primary-50 font-semibold"
                  >Program Element X</label
                >

                <prime_input_number
                  id="Program_element_x"
                  v-model="formProgramElement.x"
                  inputId="integeronly"
                  fluid
                />
                --
                <prime_input_text
                  id="Program_element_x"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.x"
                  type="text"
                  placeholder="Project Element X"
                ></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="Program_element_y" class="text-primary-50 font-semibold"
                  >Program Element Y</label
                >
                --
                <prime_input_number
                  id="Program_element_y"
                  v-model="formProgramElement.y"
                  inputId="integeronly"
                  fluid
                />
                --
                <prime_input_text
                  id="Program_element_y"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.y"
                  type="text"
                  placeholder="Project Element Y"
                ></prime_input_text>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="Program_element_width" class="text-primary-50 font-semibold"
                  >Program Element Width</label
                >
                --
                <prime_input_number
                  id="Program_element_width"
                  v-model="formProgramElement.width"
                  inputId="integeronly"
                  fluid
                />
                --
                <prime_input_text
                  id="Program_element_width"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.width"
                  type="text"
                  placeholder="Project Element Width"
                ></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="Program_element_y" class="text-primary-50 font-semibold"
                  >Program Element Height</label
                >
                --
                <prime_input_number
                  id="Program_element_height"
                  v-model="formProgramElement.height"
                  inputId="integeronly"
                  fluid
                />
                --
                <prime_input_text
                  id="Program_element_height"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.height"
                  type="text"
                  placeholder="Project Element Height"
                >
                </prime_input_text>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="Program_window_title_pattern" class="text-primary-50 font-semibold"
                  >Program Element shortcut</label
                >
                <prime_input_text
                  id="Program_element_shortcut"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.shortcut"
                  type="text"
                  placeholder="Project Elemmment shortcut"
                ></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="Program_element_confidence" class="text-primary-50 font-semibold"
                  >Program Element confidence</label
                >
                --
                <prime_input_number
                  id="Program_element_confidence"
                  v-model="formProgramElement.confidence"
                  inputId="integeronly"
                  fluid
                />
                --
                <prime_input_text
                  id="Program_element_confidence"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.confidence"
                  type="text"
                  placeholder="Project Element confidence"
                ></prime_input_text>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              ></prime_button>
              <prime_button
                label="Create"
                @click="createProgramElement"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              ></prime_button>
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>
    <div class="card flex justify-center">
      <prime_dialog
        v-model:visible="editProgramElementsVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div class="" style="margin: auto; font-size: 2rem; font-weight: bolder">
              Edit Program Element
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="programName" class="text-primary-50 font-semibold"
                  >Program Element Name</label
                >
                <prime_input_text
                  id="programName"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.name"
                  type="text"
                  placeholder="Program name"
                ></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="description" class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  id="description"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.description"
                  placeholder="Program description"
                ></prime_textarea>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="description" class="text-primary-50 font-semibold">Image</label>
                <input type="file" accept="image/*" @change="onImageChangeProgramElement" />
              </div>

              <div class="inline-flex flex-col gap-2">
                <label for="program" class="text-primary-50 font-semibold">Program Id</label>
                <select v-model="formProgramElement.program" class="input">
                  <option disabled value="">اختر البرنامج</option>
                  <option v-for="p in programs" :key="p.id" :value="p.id">
                    {{ p.name }}
                  </option>
                </select>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="selector_value" class="text-primary-50 font-semibold"
                  >Selector Value</label
                >
                <select v-model="formProgramElement.selector_type">
                  <option disabled value="">Choose selector type</option>

                  <option
                    v-for="type in programElementselectorTypes"
                    :key="type.value"
                    :value="type.value"
                  >
                    {{ type.label }}
                  </option>
                </select>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="Program_element_x" class="text-primary-50 font-semibold"
                  >Program Element X</label
                >
                --
                <prime_input_number
                  id="Program_element_x"
                  v-model="formProgramElement.x"
                  inputId="integeronly"
                  fluid
                />
                --
                <prime_input_text
                  id="Program_element_x"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.x"
                  type="text"
                  placeholder="Project Element X"
                ></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="Program_element_y" class="text-primary-50 font-semibold"
                  >Program Element Y</label
                >
                --
                <prime_input_number
                  id="Program_element_y"
                  v-model="formProgramElement.y"
                  inputId="integeronly"
                  fluid
                />
                --
                <prime_input_text
                  id="Program_element_y"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.y"
                  type="text"
                  placeholder="Project Element Y"
                ></prime_input_text>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="Program_element_width" class="text-primary-50 font-semibold"
                  >Program Element Width</label
                >
                --
                <prime_input_number
                  id="Program_element_width"
                  v-model="formProgramElement.width"
                  inputId="integeronly"
                  fluid
                />
                --
                <prime_input_text
                  id="Program_element_width"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.width"
                  type="text"
                  placeholder="Project Element Width"
                ></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="Program_element_y" class="text-primary-50 font-semibold"
                  >Program Element Height</label
                >
                --
                <prime_input_number
                  id="Program_element_height"
                  v-model="formProgramElement.height"
                  inputId="integeronly"
                  fluid
                />
                --
                <prime_input_text
                  id="Program_element_height"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.height"
                  type="text"
                  placeholder="Project Element Height"
                >
                </prime_input_text>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="Program_window_title_pattern" class="text-primary-50 font-semibold"
                  >Program Element shortcut</label
                >
                <prime_input_text
                  id="Program_element_shortcut"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.shortcut"
                  type="text"
                  placeholder="Project Elemmment shortcut"
                ></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="Program_element_confidence" class="text-primary-50 font-semibold"
                  >Program Element confidence</label
                >
                --
                <prime_input_number
                  id="Program_element_confidence"
                  v-model="formProgramElement.confidence"
                  inputId="integeronly"
                  fluid
                />
                --
                <prime_input_text
                  id="Program_element_confidence"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.confidence"
                  type="text"
                  placeholder="Project Element confidence"
                ></prime_input_text>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              ></prime_button>
              <prime_button
                label="Create"
                @click="editProgramElement"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              ></prime_button>
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <div class="card flex justify-center" style="overflow-y: auto">
      <prime_dialog
        v-model:visible="createTaskVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div class="" style="margin: auto; font-size: 2rem; font-weight: bolder">
              Create Task
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="taskName" class="text-primary-50 font-semibold">Task Name</label>
                <prime_input_text
                  id="taskName"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formTask.name"
                  type="text"
                  placeholder="Task Name"
                ></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="description" class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  id="description"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formTask.description"
                  placeholder="Program description"
                ></prime_textarea>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="program" class="text-primary-50 font-semibold"
                  >Program Project Id</label
                >
                <select v-model="formTask.program" class="input">
                  <option disabled value="">اختر البرنامج</option>
                  <option v-for="p in programs" :key="p.id" :value="p.id">
                    {{ p.name }}
                  </option>
                </select>
              </div>
            </div>

            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              ></prime_button>
              <prime_button
                label="Create"
                @click="createTask"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              ></prime_button>
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <div class="card flex justify-center">
      <prime_dialog
        v-model:visible="editTaskVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div class="" style="margin: auto; font-size: 2rem; font-weight: bolder">Edit Task</div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="taskName" class="text-primary-50 font-semibold">Task Name</label>
                <prime_input_text
                  id="taskName"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formTask.name"
                  type="text"
                  placeholder="Task Name"
                ></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="description" class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  id="description"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formTask.description"
                  placeholder="Task description"
                ></prime_textarea>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="program" class="text-primary-50 font-semibold">Program Id</label>
                <select v-model="formTask.program" class="input">
                  <option disabled value="">اختر البرنامج</option>
                  <option v-for="p in programs" :key="p.id" :value="p.id">
                    {{ p.name }}
                  </option>
                </select>
              </div>
            </div>

            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              ></prime_button>
              <prime_button
                label="Create"
                @click="editTask"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              ></prime_button>
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>
  </main>
</template> -->

<!--



/* Soner



/*
const openProgram = async (programId) => {
  // 🚀 فتح البرنامج
  await automationService.openProgram(programId)
}

const closeProgram = async (programId) => {
  // ❌ غلق البرنامج
  await automationService.closeProgram(programId)
}
const statusProgram = async (programId) => {
  // ℹ️ حالة البرنامج
  const { data } = await automationService.statusProgram(programId)
  return data
}

const focusProgram = async (programId) => {
  try {
    const { data } = await automationService.focusProgram(programId)
    console.log('data: ', data)
    toast.add({
      severity: 'success',
      summary: '✅ Focused',
      detail: `Program focused successfully`,
      life: 2000,
    })
  } catch (err) {
    console.error(err)
    toast.add({
      severity: 'error',
      summary: '❌ Focus failed',
      detail: err.message,
      life: 3000,
    })
  }
}
const maximizeProgram = async (programId) => {
  try {
    const { data } = await automationService.maximizeProgram(programId)
    console.log('data: ', data)

    toast.add({
      severity: 'success',
      summary: '✅ Maximized',
      detail: `Program maximized successfully`,
      life: 2000,
    })
  } catch (err) {
    console.error(err)
    toast.add({
      severity: 'error',
      summary: '❌ Maximize failed',
      detail: err.message,
      life: 3000,
    })
  }
}
*/

const createProgram = async () => {
  try {
    const formData = new FormData()

    // ======================
    // Basic Info
    // ======================
    formData.append('name', formProgram.value.name)
    formData.append('description', formProgram.value.description)

    // ======================
    // Execution
    // ======================
    formData.append('executable_path', formProgram.value.executable_path)
    formData.append('project_path', formProgram.value.project_path || '')
    formData.append('working_directory', formProgram.value.working_directory || '')
    formData.append('window_title_pattern', formProgram.value.window_title_pattern || '')

    // ======================
    // Image
    // ======================
    if (formProgram.value.image) {
      formData.append('image', formProgram.value.image)
    }
    const res = await automationService.createProgram(formData)

    console.log(res.data)

    showToast('success', 'Program Successfully', '✅ Program Created Successfully', 12000)
    createProgramVisible.value = false
  } catch (error) {
    console.error(error)
    showToast('error', '❌ Error creating program', error.message, 3000)
  } finally {
    await loadPrograms()

    console.log('DB DJANGO Programs STORE DATA 👉', programs.value)
  }
}

const editProgram = async () => {
  try {
    const formData = new FormData()
    // ======================
    // Basic Info
    // ======================
    formData.append('name', formProgram.value.name)
    formData.append('description', formProgram.value.description)
    // ======================
    // Execution
    // ======================
    formData.append('executable_path', formProgram.value.executable_path)
    formData.append('project_path', formProgram.value.project_path || '')
    formData.append('working_directory', formProgram.value.working_directory || '')
    formData.append('window_title_pattern', formProgram.value.window_title_pattern || '')
    // ======================
    // Image
    // ======================
    if (formProgram.value.image) {
      formData.append('image', formProgram.value.image)
    }

    const res = await automationService.updateProgram(currentProgramId.value, formData)
    console.log('editProgram currentProgramId: ', currentProgramId.value)
    console.log(res.data)
    editProgramVisible.value = false
    toast.add({
      severity: 'success',
      summary: `✅ Program Successfully`,
      detail: `✅ Program Edit Successfully`,
      life: 3000,
    })
  } catch (errorCode) {
    console.error(errorCode)
    showToast('error', '❌ Error edit program', errorCode.message, 12000)
  } finally {
    console.log('DB DJANGO Programs STORE DATA 👉', programs.value)
    await loadPrograms()
  }
}


const deleteProgram = async (id) => {
  if (!id) return
  try {
    await automationService.deleteProgram(id)
    toast.add({
      severity: 'success',
      summary: '✅ Deleted',
      detail: 'The program was successfully deleted',
      life: 3000,
    })
    // تحديث القائمة
    programs.value = programs.value.filter((p) => p.id !== id)
    // لو البرنامج المحذوف كان محدد
    if (currentProgramId.value === id) {
      currentProgramId.value = null
      formProgram.value = {}
    }
  } catch (err) {
    console.error(err)
    toast.add({
      severity: 'error',
      summary: '❌ mistake',
      detail: 'Program deletion failed',
      life: 3000,
    })
  }
}


const createProgramElement = async () => {
  try {
    if (!formProgramElement.value.program) {
      toast.add({
        severity: 'error',
        summary: '❌ Program Required',
        detail: 'لازم تختار برنامج',
        life: 3000,
      })
      return
    }

    const formData = new FormData()
    formData.append('name', formProgramElement.value.name)
    formData.append('description', formProgramElement.value.description)
    formData.append('program', formProgramElement.value.program)
    formData.append('element_type', formProgramElement.value.element_type)
    formData.append('selector_type', formProgramElement.value.selector_type)
    formData.append('selector_value', formProgramElement.value.selector_value)
    formData.append('x', Number(formProgramElement.value.x))
    formData.append('y', Number(formProgramElement.value.y))
    formData.append('width', Number(formProgramElement.value.width))
    formData.append('height', Number(formProgramElement.value.height))
    formData.append('shortcut', formProgramElement.value.shortcut)

    formData.append('confidence', parseFloat(formProgramElement.value.confidence))

    if (formProgramElement.value.image) {
      formData.append('image', formProgramElement.value.image)
    }

    const res = await automationService.createProgramElement(formData)
    console.log('res: ', res)
    currentProgramId.value = res.data.id

    toast.add({
      severity: 'success',
      summary: '✅ Success',
      detail: 'Program Element Created',
      life: 3000,
    })

    // await loadProgramElementsByProgram(formProgramElement.value.program)
    // createProgramElementsVisible.value = false
  } catch (error) {
    console.error(error.response?.data || error)

    toast.add({
      severity: 'error',
      summary: '❌ Error creating program element',
      detail: JSON.stringify(error.response?.data),
      life: 5000,
    })
  } finally {
    createProgramElementsVisible.value = false
    console.log('Programs element STORE DATA 👉', programs.value)
    toast.add({
      severity: 'success',
      summary: `✅ Program element Successfully`,
      detail: `✅ Program element Created Successfully`,
      life: 3000,
    })
    // console.log(`${parseInt(number)}`);

    await loadProgramElements()
  }
}


const editProgramElement = async () => {
  try {
    const formData = new FormData()

    // ======================
    // Basic Info
    // ======================
    formData.append('name', formProgramElement.value.name)
    formData.append('description', formProgram.value.description)
    formData.append('program', formProgramElement.value.program)
    formData.append('element_type', formProgramElement.value.element_type)
    formData.append('selector_type', formProgramElement.value.selector_type)
    formData.append('selector_value', formProgramElement.value.selector_value)
    formData.append('x', formProgramElement.value.x)
    formData.append('y', formProgramElement.value.y)
    formData.append('width', formProgramElement.value.width)
    formData.append('height', formProgramElement.value.height)
    formData.append('shortcut', formProgramElement.value.shortcut)
    formData.append('confidence', formProgramElement.value.confidence)

    // // ======================
    // // Image
    // // ======================
    if (formProgramElement.value.image) {
      formData.append('image', formProgramElement.value.image)
    }
    // // =================
    // // JSON
    // // =================
    // formData.append('settings', JSON.stringify(form.value.settings))
    const res = await automationService.updateProgramElement(
      currentProgramElementId.value,
      formData,
    )
    console.log(res.data)
  } catch (errorCode) {
    console.error(errorCode)
    toast.add({
      severity: 'error',
      summary: `❌ Error creating program Element`,
      detail: `${errorCode.message}`,
      life: 3000,
    })
  } finally {
    editProgramElementsVisible.value = false
    console.log('Programs element STORE DATA 👉', programsElement.value)
    toast.add({
      severity: 'success',
      summary: `✅ Program element Successfully`,
      detail: `✅ Program element Edit Successfully`,
      life: 3000,
    })
    await loadProgramElements()
  }
}

const deleteProgramElement = async (id) => {
  if (!id) return

  try {
    await automationService.deleteProgramElement(id)

    toast.add({
      severity: 'success',
      summary: '✅ Deleted',
      detail: 'The program Element was successfully deleted',
      life: 3000,
    })

    // تحديث القائمة
    programsElement.value = programsElement.value.filter((p) => p.id !== id)

    // لو البرنامج المحذوف كان محدد
    if (currentProgramElementId.value === id) {
      currentProgramElementId.value = null
      formProgramElement.value = {}
    }
  } catch (err) {
    console.error(err)
    toast.add({
      severity: 'error',
      summary: '❌ mistake',
      detail: 'Program Element deletion failed',
      life: 3000,
    })
  }
}

const createWorkflow = async () => {
  try {
    // ✅ تحقق
    if (!formWorkflow.value.name) {
      toast.add({
        severity: 'error',
        summary: `Error`,
        detail: `❗ Name Is ...`,
        life: 3000,
      })
      return
    }

    // ✅ Payload موحد
    const payload = {
      name: formWorkflow.value.name,
      description: formWorkflow.value.description,
      status: formWorkflow.value.status,
    }

    // ✅ إنشاء في الباك اند
    const { data } = await automationService.createWorkflow(payload)

    // ✅ تحديث State
    workflows.value.unshift(data)
    currentWorkflowId.value = data.id

    // ✅ تفريغ الكانفاس
    nodes.value = []
    edges.value = []

    toast.add({
      severity: 'success',
      summary: `Successfully`,
      detail: `✅ Workflow created successfully`,
      life: 3000,
    })
    console.log('Workflow:', data)
    // await loadWorkflow(data.id)
    await loadWorkflowEvents(data.id)
  } catch (err) {
    console.error('❌ Create Workflow Error:', err)
    alert('❌ Failed to create Workflow')
  }
}


const updateStatusWorkflow = async (status) => {
  try {
    // ✅ فقط تحديث الحالة
    await automationService.updateWorkflow(currentWorkflowId.value, { status })
    // تحديث الـ state محلياً
    const wf = workflows.value.find((w) => w.id === currentWorkflowId.value)
    if (wf) wf.status = status
    toast.add({
      severity: 'success',
      summary: 'Workflow Updated',
      detail: `Status set to ${status}`,
      life: 2000,
    })
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: `❌ update Workflow Error`,
      detail: `${err.message}`,
      life: 3000,
    })
  }

  const wf = workflows.value.find((w) => w.id === currentWorkflowId.value)
  if (wf) wf.status = status
}


const deleteWorkflow = async (id) => {
  if (!id) return
  console.log('id: ', id)

  try {
    await automationService.deleteWorkflow(id)

    toast.add({
      severity: 'success',
      summary: '✅ Deleted',
      detail: 'The Workflow was successfully deleted',
      life: 3000,
    })

    // تحديث القائمة
    workflows.value = workflows.value.filter((p) => p.id !== id)

    // لو البرنامج المحذوف كان محدد
    if (currentWorkflowId.value === id) {
      currentWorkflowId.value = null
      workflows.value = []
    }
  } catch (err) {
    console.error(err)
    toast.add({
      severity: 'error',
      summary: '❌ mistake',
      detail: 'workflows deletion failed',
      life: 3000,
    })
  } finally {
    await loadWorkflows()
  }
}

const createTask = async () => {
  try {
    if (!formTask.value.program) {
      toast.add({
        severity: 'error',
        summary: '❌ Program Required',
        detail: 'لازم تختار برنامج',
        life: 3000,
      })
      return
    }

    const formData = new FormData()
    formData.append('name', formTask.value.name)
    formData.append('description', formTask.value.description)
    formData.append('program', formTask.value.program)
    const res = await automationService.createTask(formData)
    console.log('res: ', res)
    currentTaskId.value = res.data.id

    toast.add({
      severity: 'success',
      summary: '✅ Success',
      detail: 'Program Element Created',
      life: 3000,
    })

    // await loadProgramElementsByProgram(formProgramElement.value.program)
    // createProgramElementsVisible.value = false
  } catch (error) {
    console.error(error.response?.data || error)

    toast.add({
      severity: 'error',
      summary: '❌ Error creating program element',
      detail: JSON.stringify(error.response?.data),
      life: 5000,
    })
  } finally {
    createTaskVisible.value = false
    console.log('Programs element STORE DATA 👉', programs.value)
    toast.add({
      severity: 'success',
      summary: `✅ Program element Successfully`,
      detail: `✅ Program element Created Successfully`,
      life: 3000,
    })
    // console.log(`${parseInt(number)}`);

    await loadTasks()
  }
}

const editTask = async () => {
  try {
    const formData = new FormData()

    // ======================
    // Basic Info
    // ======================
    formData.append('name', formProgramElement.value.name)
    formData.append('description', formProgram.value.description)
    formData.append('program', formProgramElement.value.program)

    // // ======================
    // // Image
    // // ======================
    if (formProgramElement.value.image) {
      formData.append('image', formProgramElement.value.image)
    }
    // // =================
    // // JSON
    // // =================
    // formData.append('settings', JSON.stringify(form.value.settings))
    const res = await automationService.updateProgramElement(
      currentProgramElementId.value,
      formData,
    )
    console.log(res.data)
  } catch (errorCode) {
    console.error(errorCode)
    toast.add({
      severity: 'error',
      summary: `❌ Error creating program Element`,
      detail: `${errorCode.message}`,
      life: 3000,
    })
  } finally {
    editTaskVisible.value = false
    console.log('Programs element STORE DATA 👉', programsElement.value)
    toast.add({
      severity: 'success',
      summary: `✅ Program element Successfully`,
      detail: `✅ Program element Edit Successfully`,
      life: 3000,
    })
    await loadProgramElements()
  }
}

const deleteTask = async (id) => {
  if (!id) return

  try {
    await automationService.deleteTask(id)

    toast.add({
      severity: 'success',
      summary: '✅ Deleted',
      detail: 'The program Element was successfully deleted',
      life: 3000,
    })

    // تحديث القائمة
    programsElement.value = programsElement.value.filter((p) => p.id !== id)

    // لو البرنامج المحذوف كان محدد
    if (currentProgramElementId.value === id) {
      currentProgramElementId.value = null
      formProgramElement.value = {}
    }
  } catch (err) {
    console.error(err)
    toast.add({
      severity: 'error',
      summary: '❌ mistake',
      detail: 'Program Element deletion failed',
      life: 3000,
    })
  }
}


*/



























































/*

const createNode = async (item, dropEvent) => {
  if (!currentWorkflowId.value) return
  console.log('item: ', item)

  const position = project({
    x: dropEvent.clientX,
    y: dropEvent.clientY,
  })

  const baseActionMap = {
    program: 'open_program',
    'program-element': 'press',
    delay: 'wait',
  }

  await loadProgram(item.id)
  const actionType = baseActionMap[item.type] || 'custom'
  // =============================
  // 1️⃣ UI CONFIG ONLY
  // =============================
  const uiConfig = {
    ui: {
      theme: {
        background: '#0f172a',
        border: '#334155',
        shadow: '#334155',
      },
      layout: {
        width: 260,
        height: 240,
        rounded: true,
      },
    },
    inputs: [
      { key: 'text', label: 'Text', type: 'string', value: '' },
      { key: 'delay', label: 'Delay (ms)', type: 'number', value: 0 },
      { key: 'color', label: 'Background Color', type: 'color', value: '#0f172a' },
    ],
    ai: {
      enabled: false,
      context: {},
      memory: [],
      suggestions: [],
    },
  }

  // =============================
  // 2️⃣ NODE PAYLOAD (NO ACTION)
  // =============================

  const nodePayload = {
    // 1️⃣ WorkflowId:
    workflow: currentWorkflowId.value,
    // 2️⃣
    node_type: item.type,
    // 3️⃣
    label: `${actionType}` || 'New Node',
    // 4️⃣
    program: item.type === 'program' ? item.id : null,
    // 5️⃣
    element: item.type === 'program-element' ? item.id : null,
    // 6️⃣
    position_x: position.x,
    // 7️⃣
    position_y: position.y,
    // 8️⃣
    config: uiConfig,
  }

  try {
    // =============================
    // 3️⃣ CREATE NODE IN BACKEND
    // =============================
    const { data } = await automationService.createWorkflowNode(nodePayload)
    console.log('CREATE NODE IN BACKEND: ', data)

    // =============================
    // 4️⃣ CREATE DEFAULT ACTION
    // =============================
    const actionPayload = {
      node: data.id,
      action_type: actionType,
      payload: {},
    }
    const actionResponse = await createAction(actionPayload)
    console.log("Action Created:", actionResponse)
    // const actions = actionResponse ? [actionResponse] : []

    // 4️⃣ إضافة Node مع الـ Action للـ frontend state
    debouncedAutoSave.cancel()
    nodes.value.push({
      id: data.id,
      backend_id: data.id,
      type: 'custom',
      position: {
        x: data.position_x,
        y: data.position_y,
      },
      data: {
        // ...data,
        backend_id: data.id,
        id: data.id,
        program_name: data.program_name,
        node_type: data.node_type,
        label: data.label,
        config: data.config,
        program: data.program,
        element: data.element,
        status: 'idle',
        // actions: actions,
      },
      actions: actionResponse ? [actionResponse] : [],
    })

    toast.add({
      severity: 'success',
      summary: `Node Created ${data.program_name}`,
      detail: data.label,
      life: 3000,
    })
  } catch (err) {
    console.error(err)
  }
}
*/

/*
const onNodeDragStop = async (node) => {
  if (!node || !node.data) return
  const backendId = node.data.id
  if (!backendId) return
  try {
    await automationService.updateWorkflowNode(node.node.id, {
      position_x: node.node.position.x,
      position_y: node.node.position.y,
    })
    toast.add({ severity: 'success', summary: 'Node Updated', detail: node.data.label, life: 2000 })
  } catch (err) {
    console.error('Failed to update node position:', err)
  }
}
*/

<Controls position="top-left">
            <ControlButton title="Reset Transform" @click="resetTransform">
              <prime_button icon="pi pi-plus" label="reset" severity="info" class="class_name" />
            </ControlButton>

            <ControlButton title="Shuffle Node Positions" @click="updatePos">
              <prime_button icon="pi pi-plus" label="update" severity="info" class="class_name" />
            </ControlButton>

            <ControlButton title="Log `toObject`" @click="logToObject">
              <prime_button icon="pi pi-plus" label="log" severity="info" class="class_name" />
            </ControlButton>
          </Controls>

// 2️⃣ بناء Payload افتراضي للـ Action
    // const actionData = buildActionPayload(nodePayload)

    // 3️⃣ إنشاء Action مرتبط بالـ Node
    // const actions = await createAction({
    //   node: data.id,
    //   action_type: actionData.action_type,
    //   payload: actionData.payload
    // })

    // // حفظ الـ Node في Map للتحديثات لاحقًا
    // workflowState.nodesMap.set(data.id, nodes.value[nodes.value.length - 1])

    // =============================
    // 5️⃣ PUSH CLEAN NODE TO FRONT
    // =============================
    // const newNode = {
    //   id: data.id,
    //   type: 'custom',
    //   position: {
    //     x: data.position_x,
    //     y: data.position_y
    //   },
    //   data: {
    //     backend_id: data.id,
    //     node_type: data.node_type,
    //     label: data.label,
    //     config: data.config,        // UI
    //     // action: actionResponse,     // EXECUTION
    //     program: data.program,
    //     element: data.element,
    //     status: 'idle'
    //   }
    // }

    // nodes.value.push(newNode)
    // workflowState.nodesMap.set(data.id, newNode)
    // await loadlistWorkflowNodes()

/*
const buildActionPayload = (node) => {
  const executionType = node.config.execution.type
  const inputs = node.config.inputs || []

  const getInput = (key) =>
    inputs.find(i => i.key === key)?.value

  switch (executionType) {

    case 'wait':
      return {
        action_type: 'wait',
        payload: {
          seconds: Number(getInput('delay') || 0) / 1000
        }
      }

    case 'press':
      return {
        action_type: 'press',
        payload: {
          key: getInput('text')
        }
      }

    case 'typewrite':
      return {
        action_type: 'typewrite',
        payload: {
          text: getInput('text')
        }
      }

    case 'hotkey':
      return {
        action_type: 'hotkey',
        payload: {
          keys: getInput('text')
        }
      }

    case 'open_program':
      return {
        action_type: 'open_program',
        payload: {}
      }

    default:
      return {
        action_type: executionType,
        payload: {}
      }
  }
}
*/

// Auto Save مع VueFlow
const saveNode = async (node) => {
  if (!node) return

  if (!node.id) {
    const res = await automationService.createWorkflowNode(node)
    node.id = res.data.id
  } else {
    await automationService.updateWorkflowNode(`${node.id}`, node)
  }
}v

const updateNodeConfig = (id, data) => {
  enqueueUpdate({
    type: 'node-config',
    id,
    data,
  })
}


console.log('showToast: ', saveNode)
console.log('showToast: ', updateNodeConfig)

const saveNodes = debounce(async () => {
  for (let node of nodes.value) {
    await automationService.updateWorkflowNode(`${node.id}`, {
      data: node.data,
    })
  }
}, 500)


/*
const saveWorkflow = async () => {
  if (!currentWorkflowId.value) return

  try {
    const payload = {
      nodes: nodes.value.map(n => ({
        id: n.id,
        position: n.position,
        data: n.data
      })),
      edges: edges.value.map(e => ({
        id: e.id,
        source: e.source,
        target: e.target,
        data: e.data
      }))
    }

    await automationService.saveWorkflowAll(
      currentWorkflowId.value,
      payload
    )

    toast.add({
      severity: 'success',
      summary: 'Saved',
      detail: 'Workflow saved successfully',
      life: 2000,
    })

  } catch (err) {
    console.error(err)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: err.message,
      life: 3000,
    })
  }
}
*/

-->

<!--
learn
C:\\Users\learn\AppData\Local\Programs\Microsoft VS Code\Code.exe

AFAQE
C:\Users\AFAQE\AppData\Local\Programs\Microsoft VS Code\Code.exe


Vscode
C:\Users\AFAQE\AppData\Local\Programs\Microsoft VS Code\Code.exe

Chrome
C:\Program Files\Google\Chrome\Application\chrome.exe

D:\Test


-->

<!-- Project Structure
src/
├── stores/
│   ├── useWorkflowStore.js
│   ├── useProgramStore.js
│   ├── useProgramElementStore.js
│   └── useTaskStore.js
│
├── composables/
│   ├── useAsyncAction.js
│   ├── useApiTracker.js
│   └── useNodeDragDrop.js
│
├── services/
│   ├── AutomationService.js
│   └── WorkerService.js
│
├── plugins/
│   ├── PluginRegistry.js
│   ├── PluginSDK.js
│   └── builtin/
│       ├── OpenProgramPlugin.js
│       ├── ClickElementPlugin.js
│       ├── WaitPlugin.js
│       └── AIActionPlugin.js
│
├── views/
│   └── AutomationView.vue
│
└── components/Automation/
    ├── Workflow/
    │   ├── WorkflowCanvas.vue
    │   ├── WorkflowToolbar.vue
    │   └── WorkflowVersions.vue
    ├── Node/
    │   ├── NodeMarketplace.vue
    │   ├── NodeVisualBuilder.vue
    │   └── NodePluginCard.vue
    ├── Program/
    │   ├── CreateProgram.vue
    │   └── EditProgram.vue
    └── Execution/
        ├── LiveConsole.vue
        └── RealtimeGraph.vue
-->

<!-- <script setup>
import { ref, onMounted, computed, watch, reactive } from 'vue'
import automationService from '@/services/AutomationService'
import { VueFlow, Panel, useVueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
// import vuedraggable from 'vuedraggable'
import CustomNode from '@/components/Automation/Node/CustomNode.vue'
import CustomEdge from '@/components/Automation/Edge/CustomEdge.vue'
import ActionPanel from '@/components/Automation/Action/ActionPanel.vue'
import CreateProgram from '@/components/Automation/Program/CreateProgram.vue'
import { debounce } from 'lodash'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import LiveConsole from '@/components/Automation/Execution/LiveConsole.vue'
import dagre from 'dagre'
import { useApiTracker } from '@/composables/useApiTracker'
import ApiFlowPanel from '@/components/Automation/ApiFlowPanel.vue' // ← ✅ مش composables

const toast = useToast()
const confirm = useConfirm()
const { project } = useVueFlow()

// ==================================================
// 🌐 tracker — instance واحدة لكل الـ app
//    بيتبعت لـ ApiFlowPanel وبيتحدث مع كل request
// ==================================================
const tracker = useApiTracker()

// ==================================================
// 🛠️ useAsyncAction v3
//
// ✅ التغيير الجوهري الوحيد عن v2:
//    بدل: const data = await asyncFn()
//    بقت: const data = await tracker.execute({ serviceFn: asyncFn })
//
//    النتيجة: كل API call في الـ app بيظهر في ApiFlowPanel تلقائياً
//
// ✅ validate انفصلت عن asyncFn
//    عشان validation errors ما تظهرش في الـ tracker كـ API errors
// ==================================================
function useAsyncAction() {
  const loading = ref(false)

  /**
   * @param {Function} apiFn      — API call فقط (بدون validation)
   * @param {Object}   options
   *   validate       {Function}  → string | null   ← جديد
   *   successSummary {string}
   *   successDetail  {string}
   *   errorSummary   {string}
   *   onSuccess      {async Function(result)}
   *   onError        {Function(err)}
   */
  const run = async (apiFn, options = {}) => {
    if (loading.value) return // ← منع double-submit

    const {
      validate = null, // ← ✅ جديد
      successSummary = null,
      successDetail = null,
      errorSummary = 'حصل خطأ',
      onSuccess = null,
      onError = null,
    } = options

    // ── Validation قبل الـ tracker ──────────────
    // مش بتظهر في ApiFlowPanel لأنها مش API error
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
      // ✅ هنا التغيير الأساسي:
      //    كل request بيمر عبر tracker.execute
      //    → بيظهر في ApiFlowPanel تلقائياً
      const result = await tracker.execute({ serviceFn: apiFn })

      if (successSummary) {
        toast.add({
          severity: 'success',
          summary: `✅ ${successSummary}`,
          detail: successDetail,
          life: 4000,
        })
      }
      if (onSuccess) await onSuccess(result)
      return result
    } catch (err) {
      // Smart Django error parser
      const status = err?.response?.status
      const body = err?.response?.data
      let detail = err?.message || 'خطأ غير متوقع'

      if (status === 400 && body && typeof body === 'object') {
        detail = Object.entries(body)
          .map(([f, m]) => `${f}: ${Array.isArray(m) ? m[0] : m}`)
          .slice(0, 3)
          .join(' | ')
      } else if (status === 401) {
        detail = 'انتهت جلستك — سجّل دخول من جديد'
      } else if (status === 403) {
        detail = 'مش عندك صلاحية لهذه العملية'
      } else if (status === 404) {
        detail = 'العنصر المطلوب غير موجود'
      } else if (status === 413) {
        detail = 'الملف كبير جداً — الحد الأقصى 5MB'
      } else if (status === 500) {
        detail = 'خطأ في السيرفر — حاول مرة أخرى'
      }

      toast.add({ severity: 'error', summary: `❌ ${errorSummary}`, detail, life: 6000 })
      if (onError) onError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return { run, loading }
}

// ✅ 4 instances مستقلة — loading states منفصلة
//    كلهم بيستخدموا نفس الـ tracker
const programAction = useAsyncAction()
const programElementAction = useAsyncAction()
const workflowAction = useAsyncAction()
const taskAction = useAsyncAction()
const nodeAction = useAsyncAction()

const showToast = (severity, summary, detail, life = 4000) => {
  toast.add({
    severity,
    summary: `${{ success: '✅', error: '❌', warn: '⚠️', info: 'ℹ️' }[severity] ?? ''} ${summary}`,
    detail,
    life,
  })
}

// ==================================================
// ✅ Validators (منفصلة تماماً عن الـ API calls)
// ==================================================
const validateProgram = (f) =>
  !f.name?.trim() ? 'اسم البرنامج مطلوب' : !f.executable_path?.trim() ? 'مسار التنفيذ مطلوب' : null
const validateProgramElement = (f) =>
  !f.name?.trim()
    ? 'الاسم مطلوب'
    : !f.program
      ? 'لازم تختار برنامج'
      : !f.selector_type
        ? 'لازم تختار Selector Type'
        : null
const validateTask = (f) =>
  !f.name?.trim() ? 'اسم الـ Task مطلوب' : !f.program ? 'لازم تختار برنامج' : null
const validateImageSize = (file, maxMB = 5) => {
  if (file && file.size > maxMB * 1024 * 1024) {
    showToast('warn', 'الملف كبير', `الحد الأقصى ${maxMB}MB`)
    return false
  }
  return true
}

// ==============================================
// =================== State ===================
// ==============================================
const programs = ref([])
const loadingPrograms = ref(false)
const currentProgramId = ref(null)
const createProgramVisible = ref(false)
const editProgramVisible = ref(false)
const formProgram = ref({
  name: '',
  description: '',
  executable_path: '',
  project_path: '',
  working_directory: '',
  window_title_pattern: '',
  image: null,
})

const programsElement = ref([])
const loadingProgramElements = ref(false)
const currentProgramElementId = ref(null)
const createProgramElementsVisible = ref(false)
const editProgramElementsVisible = ref(false)
const programElementselectorTypes = [
  { label: 'Image Recognition', value: 'image' },
  { label: 'Screen Coordinates', value: 'coords' },
  { label: 'Text OCR', value: 'text' },
  { label: 'UI Automation', value: 'ui' },
]
const formProgramElement = ref({
  name: '',
  description: '',
  image: null,
  program: null,
  element_type: 'button',
  selector_type: null,
  selector_value: 'xpath',
  x: 0,
  y: 0,
  width: 0,
  height: 0,
  shortcut: '',
  confidence: 0,
})

const workflows = ref([])
const loadingWorkflows = ref(false)
const isLoadingWorkflow = ref(false)
const isInitialized = ref(false)
const isLayoutingWorkflow = ref(false)
const currentWorkflowId = ref(null)
const isSavingWorkflow = ref(false)
const formWorkflow = ref({ name: '', description: '', status: 'draft' })
const workflowState = reactive({
  nodesMap: new Map(),
  edgesMap: new Map(),
  updateQueue: [],
  isSyncing: false,
})

const nodes = ref([])
const loadingNodes = ref(false)
const selectedNode = ref(null)
const currentNodeId = ref(null)
const nodeTypes = computed(() => ({ custom: CustomNode }))
const draggedItem = ref(null)

const edges = ref([])
const edgeTypes = computed(() => ({ custom: CustomEdge }))

const showActionPanel = ref(false)
const newActionTypeForPanel = ref('open_program')

const tasks = ref([])
const loadingTasks = ref(false)
const currentTaskId = ref(null)
const taskRunId = ref(null)
const currentTaskRunId = ref(null)
const createTaskVisible = ref(false)
const editTaskVisible = ref(false)
const formTask = ref({ name: '', description: '', program: null })

const delays = ref([])
const loadingDelays = ref(false)

// ==============================================
// ================ 1️⃣ PROGRAMS ================
// ==============================================

// GET ALL — read-only, no panel needed
const loadPrograms = async () => {
  loadingPrograms.value = true
  try {
    const { data } = await automationService.listPrograms()
    programs.value = data
  } catch (error) {
    showToast('error', 'فشل تحميل البرامج', error?.message, 12000)
  } finally {
    loadingPrograms.value = false
  }
}

const selectProgram = async (id) => {
  if (!id) return
  currentProgramId.value = id
  await loadProgram(id)
}
const loadProgram = async (id) => {
  const { data } = await automationService.getProgram(id)
  currentProgramId.value = data.id
  formProgram.value = {
    name: data.name,
    description: data.description,
    executable_path: data.executable_path,
    project_path: data.project_path,
    working_directory: data.working_directory,
    window_title_pattern: data.window_title_pattern,
    image: null,
  }
}

const onImageChangeProgram = (e) => {
  const file = e.target.files[0]
  if (!file || !validateImageSize(file)) {
    e.target.value = ''
    return
  }
  formProgram.value.image = file
}
const buildProgramFormData = (form) => {
  const fd = new FormData()
  fd.append('name', form.name)
  fd.append('description', form.description)
  fd.append('executable_path', form.executable_path)
  fd.append('project_path', form.project_path || '')
  fd.append('working_directory', form.working_directory || '')
  fd.append('window_title_pattern', form.window_title_pattern || '')
  if (form.image instanceof File) fd.append('image', form.image)
  return fd
}

// ✅ Create Program
// التغيير: validate انتقلت من جوه asyncFn لـ options.validate
// النتيجة: ApiFlowPanel بيشوف الـ request بس، مش الـ validation error
const createProgram = () =>
  programAction.run(
    () => automationService.createProgram(buildProgramFormData(formProgram.value)), // ← apiFn فقط
    {
      validate: () => validateProgram(formProgram.value), // ← ✅ validation هنا
      successSummary: 'تم إنشاء البرنامج',
      successDetail: `"${formProgram.value.name}" أُنشئ بنجاح`,
      errorSummary: 'فشل إنشاء البرنامج',
      onSuccess: async ({ data }) => {
        programs.value.unshift(data)
        currentProgramId.value = data.id
        createProgramVisible.value = false // ✅ يغلق بس لو نجح
      },
    },
  )

// ✅ Edit Program
const openEditProgram = async (id) => {
  if (!id) return
  try {
    currentProgramId.value = id
    await loadProgram(id)
    editProgramVisible.value = true
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
  }
}
const editProgram = () =>
  programAction.run(
    () =>
      automationService.updateProgram(
        currentProgramId.value,
        buildProgramFormData(formProgram.value),
      ),
    {
      validate: () => validateProgram(formProgram.value),
      successSummary: 'تم تحديث البرنامج',
      errorSummary: 'فشل تحديث البرنامج',
      onSuccess: async ({ data }) => {
        const idx = programs.value.findIndex((p) => p.id === data.id)
        if (idx !== -1) programs.value[idx] = { ...programs.value[idx], ...data }
        editProgramVisible.value = false
      },
    },
  )

// ✅ Delete Program
const confirmDeleteProgram = (program) => {
  confirm.require({
    message: `هل أنت متأكد من حذف "${program.name}"؟`,
    header: '⚠️ تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'نعم، احذف',
    rejectLabel: 'إلغاء',
    accept: async () => await deleteProgram(program.id),
    reject: () =>
      toast.add({ severity: 'info', summary: 'إلغاء', detail: 'لم يتم الحذف', life: 2000 }),
  })
}
const deleteProgram = (id) =>
  programAction.run(() => automationService.deleteProgram(id), {
    successSummary: 'تم الحذف',
    successDetail: 'تم حذف البرنامج بنجاح',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      programs.value = programs.value.filter((p) => p.id !== id)
      if (currentProgramId.value === id) {
        currentProgramId.value = null
        formProgram.value = {}
      }
    },
  })

// ✅ Program Controls — كلهم بيظهروا في ApiFlowPanel
const openProgram = (id) =>
  programAction.run(() => automationService.openProgram(id), { errorSummary: 'فشل فتح البرنامج' })
const closeProgram = (id) =>
  programAction.run(() => automationService.closeProgram(id), {
    errorSummary: 'فشل إغلاق البرنامج',
  })
const statusProgram = (id) => automationService.statusProgram(id).then((r) => r.data)
const focusProgram = (id) =>
  programAction.run(() => automationService.focusProgram(id), {
    successSummary: 'تم التركيز',
    errorSummary: 'فشل التركيز',
  })
const maximizeProgram = (id) =>
  programAction.run(() => automationService.maximizeProgram(id), {
    successSummary: 'تم التكبير',
    errorSummary: 'فشل التكبير',
  })

// ==============================================
// ============= 2️⃣ Program Elements ===========
// ==============================================
const loadProgramElements = async () => {
  loadingProgramElements.value = true
  try {
    const { data } = await automationService.listProgramElements()
    programsElement.value = data
  } catch (err) {
    showToast('error', 'فشل تحميل العناصر', err?.message)
  } finally {
    loadingProgramElements.value = false
  }
}
const selectProgramElement = async (id) => {
  if (!id) return
  currentProgramElementId.value = id
  await loadProgramElement(id)
}
const loadProgramElement = async (id) => {
  const { data } = await automationService.getProgramElement(id)
  currentProgramElementId.value = data.id
  formProgramElement.value = {
    name: data.name,
    description: data.description,
    program: data.program,
    element_type: data.element_type,
    selector_type: data.selector_type,
    selector_value: data.selector_value,
    x: data.x,
    y: data.y,
    width: data.width,
    height: data.height,
    shortcut: data.shortcut,
    confidence: data.confidence,
    image: null,
  }
  return data
}

const onImageChangeProgramElement = (e) => {
  const file = e.target.files[0]
  if (!file || !validateImageSize(file)) {
    e.target.value = ''
    return
  }
  formProgramElement.value.image = file
}
const buildElementFormData = (form) => {
  const fd = new FormData()
  fd.append('name', form.name)
  fd.append('description', form.description)
  fd.append('program', form.program)
  fd.append('element_type', form.element_type)
  fd.append('selector_type', form.selector_type)
  fd.append('selector_value', form.selector_value)
  fd.append('x', Number(form.x))
  fd.append('y', Number(form.y))
  fd.append('width', Number(form.width))
  fd.append('height', Number(form.height))
  fd.append('shortcut', form.shortcut)
  fd.append('confidence', parseFloat(form.confidence))
  if (form.image instanceof File) fd.append('image', form.image)
  return fd
}

// ✅ Create Element
const createProgramElement = () =>
  programElementAction.run(
    () => automationService.createProgramElement(buildElementFormData(formProgramElement.value)),
    {
      validate: () => validateProgramElement(formProgramElement.value),
      successSummary: 'تم إنشاء العنصر',
      errorSummary: 'فشل إنشاء العنصر',
      onSuccess: async ({ data }) => {
        programsElement.value.unshift(data)
        createProgramElementsVisible.value = false
      },
    },
  )

// ✅ Edit Element
const openEditProgramElement = async (id) => {
  if (!id) return
  try {
    currentProgramElementId.value = id
    await loadProgramElement(id)
    editProgramElementsVisible.value = true
    console.log('🟢 Edit Program ID:', id)
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
  }
}
const editProgramElement = () =>
  programElementAction.run(
    () =>
      automationService.updateProgramElement(
        currentProgramElementId.value,
        buildElementFormData(formProgramElement.value),
      ),
    {
      validate: () => validateProgramElement(formProgramElement.value),
      successSummary: 'تم تحديث العنصر',
      errorSummary: 'فشل تحديث العنصر',
      onSuccess: async ({ data }) => {
        const idx = programsElement.value.findIndex((e) => e.id === data.id)
        if (idx !== -1) programsElement.value[idx] = { ...programsElement.value[idx], ...data }
        editProgramElementsVisible.value = false
      },
    },
  )

// ✅ Delete Element
const confirmDeleteProgramElement = (program) => {
  confirm.require({
    message: `هل تريد حذف "${program.name}"؟`,
    header: '⚠️ تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'نعم، احذف',
    rejectLabel: 'إلغاء',
    accept: async () => await deleteProgramElement(program.id),
    reject: () =>
      toast.add({ severity: 'info', summary: 'إلغاء', detail: 'لم يتم الحذف', life: 2000 }),
  })
}
const deleteProgramElement = (id) =>
  programElementAction.run(() => automationService.deleteProgramElement(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      programsElement.value = programsElement.value.filter((p) => p.id !== id)
      if (currentProgramElementId.value === id) {
        currentProgramElementId.value = null
        formProgramElement.value = {}
      }
    },
  })

// ==============================================
// ================ 3️⃣ WORKFLOWS ===============
// ==============================================
const loadWorkflows = async () => {
  try {
    const { data } = await automationService.listWorkflows()
    workflows.value = data
  } catch (error) {
    showToast('error', 'فشل تحميل الـ Workflows', error?.message)
  } finally {
    loadingWorkflows.value = false
  }
}

const loadWorkflowEvents = async (workflowId) => {
  if (!workflowId) return
  nodes.value = []
  edges.value = []
  const { data: wfData } = await automationService.getWorkflow(workflowId)
  currentWorkflowId.value = wfData.id
  formWorkflow.value = { name: wfData.name, description: wfData.description, status: wfData.status }
  try {
    const { data } = await automationService.getWorkflow_full_events(workflowId)
    nodes.value = (data.nodes || []).map((n) => ({
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
    }))
    edges.value = (data.edges || []).map((e) => ({
      id: e.id,
      source: e.source,
      target: e.target,
      type: e.type || 'custom',
      data: e.data || {},
    }))
  } catch (err) {
    showToast('error', 'فشل تحميل الـ Workflow Events', err?.message)
  }
}

const selectWorkflow = async (id) => {
  if (!id) return
  isLoadingWorkflow.value = true
  debouncedAutoSave.cancel()
  currentWorkflowId.value = id
  await loadWorkflowEvents(id)
  isLoadingWorkflow.value = false
}

// ✅ Create Workflow
const createWorkflow = () =>
  workflowAction.run(
    () =>
      automationService.createWorkflow({
        name: formWorkflow.value.name,
        description: formWorkflow.value.description,
        status: formWorkflow.value.status,
      }),
    {
      validate: () => (!formWorkflow.value.name?.trim() ? 'الاسم مطلوب' : null),
      successSummary: 'تم إنشاء الـ Workflow',
      errorSummary: 'فشل إنشاء الـ Workflow',
      onSuccess: async ({ data }) => {
        workflows.value.unshift(data)
        currentWorkflowId.value = data.id
        nodes.value = []
        edges.value = []
        await loadWorkflowEvents(data.id)
      },
    },
  )

// ✅ Save Workflow — يمر عبر tracker.execute مباشرة (لأن فيه logic خاص)
const saveWorkflow = async () => {
  if (!currentWorkflowId.value || isSavingWorkflow.value) return

  isSavingWorkflow.value = true
  try {
    const payload = {
      nodes: nodes.value.map((n) => ({
        id: n.id,
        position: n.position,
        data: n.data,
      })),
      edges: edges.value.map((e) => ({
        id: e.id,
        source: e.source,
        target: e.target,
      })),
    }

    // التنفيذ عبر الـ tracker عشان نشوفه في الـ Panel
    await tracker.execute({
      serviceFn: () => automationService.saveWorkflowAll(currentWorkflowId.value, payload),
    })

    // مش لازم نطلع Toast Success في كل مرة حفظ تلقائي عشان ميزعجش المستخدم
    console.log('✅ تم الحفظ التلقائي بنجاح')
  } catch (err) {
    showToast('error', 'فشل الحفظ التلقائي', err?.message)
  } finally {
    isSavingWorkflow.value = false
  }
}

// ✅ Update Status
const updateStatusWorkflow = (status) =>
  workflowAction.run(() => automationService.updateWorkflow(currentWorkflowId.value, { status }), {
    successSummary: 'تم تحديث الحالة',
    successDetail: `Status: ${status}`,
    errorSummary: 'فشل تحديث الحالة',
    onSuccess: () => {
      const wf = workflows.value.find((w) => w.id === currentWorkflowId.value)
      if (wf) wf.status = status
    },
  })

// ✅ Delete Workflow
const deleteWorkflow = (id) =>
  workflowAction.run(() => automationService.deleteWorkflow(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: async () => {
      workflows.value = workflows.value.filter((w) => w.id !== id)
      if (currentWorkflowId.value === id) {
        currentWorkflowId.value = null
        nodes.value = []
        edges.value = []
      }
      await loadWorkflows()
    },
  })

const clearWorkflow = () => {
  nodes.value = []
  edges.value = []
}

// Auto Layout
function autoLayout(dir = 'TB') {
  isLayoutingWorkflow.value = true
  const g = new dagre.graphlib.Graph()
  g.setGraph({ rankdir: dir, nodesep: 50, ranksep: 80 })
  g.setDefaultEdgeLabel(() => ({}))
  nodes.value.forEach((n) => g.setNode(n.id, { width: 180, height: 60 }))
  edges.value.forEach((e) => g.setEdge(e.source, e.target))
  dagre.layout(g)
  nodes.value = nodes.value.map((node) => {
    const pos = g.node(node.id)
    return { ...node, position: { x: pos.x - 90, y: pos.y - 30 } }
  })
  setTimeout(() => {
    isLayoutingWorkflow.value = false
  }, 400)
}

// ==============================================
// =================== 4️⃣ Nodes ================
// ==============================================
const loadlistWorkflowNodes = async () => {
  try {
    const { data } = await automationService.listWorkflowNodes()
    nodes.value = data.map((n) => ({
      ...n,
      type: 'custom',
      position: { x: n.position_x, y: n.position_y },
      data: n.data,
    }))
    nodes.value.forEach((n) => {
      workflowState.nodesMap.set(n.id, n)
    })
  } catch (error) {
    showToast('error', 'فشل تحميل الـ Workflows', error?.message, 12000)
  } finally {
    loadingNodes.value = false
  }
}

const loadNode = async (id) => {
  const { data } = await automationService.getWorkflowNode(id)
  currentNodeId.value = data.id
}

const getFreshNode = (nodeId) =>
  nodes.value.find((n) => n.id === nodeId || n.data?.node?.backend_id === nodeId) ??
  selectedNode.value

const onNodeSelect = async ({ node }) => {
  const freshNode = getFreshNode(node.id)
  selectedNode.value = freshNode ?? node
  showActionPanel.value = true
  const isRealUuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(node.id)

  if (isRealUuid) {
    try {
      await loadNode(node.id)
    } catch (err) {
      console.log('err: ', err)
      console.warn('الـ Node دي شكلها ممسوحة من السيرفر أو لسه مسمعتش')
    }
  } else {
    console.log('الـ Node دي لسه جديدة (Frontend Only)، مش محتاجة loadNode')
  }
  if (node.id) await loadNode(node.id)
}


// ✅ createNode — كل step بيظهر في ApiFlowPanel
const createNode = async (item, dropEvent) => {
  if (!currentWorkflowId.value) {
    showToast('warn', 'لا يوجد Workflow', 'اختر Workflow الأول', 9000)
    return
  }
  isLoadingWorkflow.value = true
  debouncedAutoSave.cancel()

  try {
    const position = project({ x: dropEvent.clientX, y: dropEvent.clientY })
    const baseActionMap = { program: 'open_program', 'program-element': 'press', delay: 'wait' }
    const actionType = baseActionMap[item.type] || 'custom'

    // ✅ بدل loadProgram(item.id) اللي كانت تكتب في formProgram
    const programData = programs.value.find((p) => p.id === item.id)
    const nodeLabel = programData?.name ?? item.name ?? actionType

    const uiConfig = {
      ui: {
        theme: { background: '#0f172a', border: '#334155', shadow: '#334155' },
        layout: { width: 260, height: 240, rounded: true },
      },
      inputs: [
        { key: 'text', label: 'Text', type: 'string', value: '' },
        { key: 'delay', label: 'Delay (ms)', type: 'number', value: 0 },
        { key: 'color', label: 'Background Color', type: 'color', value: '#0f172a' },
      ],
      ai: { enabled: false, context: {}, memory: [], suggestions: [] },
    }

    // ✅ Step 1 — يظهر في ApiFlowPanel
    const nodeResult = await tracker.execute({
      serviceFn: () =>
        automationService.createWorkflowNode({
          workflow: currentWorkflowId.value,
          node_type: item.type,
          label: nodeLabel,
          program: item.type === 'program' ? item.id : null,
          element: item.type === 'program-element' ? item.id : null,
          position_x: position.x,
          position_y: position.y,
          config: uiConfig,
        }),
    })
    const nodeData = nodeResult.data

    // ✅ Step 2 — يظهر في ApiFlowPanel
    const actionResponse = await createAction({
      node: nodeData.id,
      action_type: actionType,
      payload: {},
    })

    nodes.value.push({
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
    isLoadingWorkflow.value = false
  }
}

// ✅ Queue updates — بيمروا عبر tracker
const enqueueUpdate = (job) => {
  workflowState.updateQueue.push(job)
  debouncedSync()
}
const processQueue = async () => {
  if (workflowState.isSyncing) return
  workflowState.isSyncing = true
  while (workflowState.updateQueue.length > 0) {
    const job = workflowState.updateQueue.shift()
    try {
      if (job.type === 'node-position') {
        // ✅ يظهر في ApiFlowPanel
        await tracker.execute({
          serviceFn: () =>
            automationService.updateWorkflowNode(job.id, {
              position_x: job.position_x,
              position_y: job.position_y,
            }),
        })
      }
      if (job.type === 'node-config') {
        await tracker.execute({
          serviceFn: () => automationService.updateWorkflowNode(job.id, job.data),
        })
      }
      if (job.type === 'action') {
        await tracker.execute({ serviceFn: () => automationService.updateAction(job.id, job.data) })
      }
    } catch (err) {
      console.error('Sync error:', err)
    }
  }
  workflowState.isSyncing = false
}
const debouncedSync = debounce(() => {
  processQueue()
}, 300)

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

// ✅ runTaskFromNode — يظهر في ApiFlowPanel
const runTaskFromNode = async (nodeData) => {
  const backendId = nodeData?.backend_id
  if (!backendId) {
    toast.add({
      severity: 'error',
      summary: 'Node Error',
      detail: 'Backend ID not found',
      life: 3000,
    })
    return
  }

  await nodeAction.run(() => automationService.runWorkflowNode(backendId), {
    successSummary: 'Node Running',
    successDetail: 'Task executed successfully',
    errorSummary: 'Execution Failed',
  })

  const action = nodeData.config?.action || 'open'
  const actionMap = {
    open: openProgram,
    close: closeProgram,
    status: statusProgram,
    focus: focusProgram,
    maximize: maximizeProgram,
  }
  actionMap[action]?.(nodeData.programId)
}

// ✅ deleteNodeOnWorkflow — يظهر في ApiFlowPanel
const deleteNodeOnWorkflow = (id) =>
  nodeAction.run(() => automationService.deleteWorkflowNode(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      nodes.value = nodes.value.filter((n) => n.id !== id)
      edges.value = edges.value.filter((e) => e.source !== id && e.target !== id)
    },
  })

// ✅ createNodeAction — يظهر في ApiFlowPanel
const createNodeAction = async ({ nodeId, action_type, payload }) => {
  console.log('payload: ', payload)
  const freshNode = getFreshNode(nodeId)
  const realId = freshNode?.data?.node?.backend_id ?? freshNode?.id
  if (!realId) {
    toast.add({ severity: 'error', summary: '❌ Node ID missing', life: 3000 })
    return
  }

  await nodeAction.run(
    () =>
      automationService.createAction({
        node: realId,
        action_type,
        payload: payload || buildNodeActionPayload(),
      }),
    {
      successSummary: 'تم إنشاء الـ Action',
      successDetail: action_type,
      errorSummary: 'فشل إنشاء الـ Action',
      onSuccess: ({ data: actionResponse }) => {
        if (!actionResponse) return
        const idx = nodes.value.findIndex(
          (n) => n.id === realId || n.data?.node?.backend_id === realId,
        )
        if (idx !== -1) {
          nodes.value[idx] = {
            ...nodes.value[idx],
            data: {
              ...nodes.value[idx].data,
              actions: [...(nodes.value[idx].data.actions ?? []), actionResponse],
            },
          }
          selectedNode.value = nodes.value[idx]
        }
      },
    },
  )
}

function buildNodeActionPayload() {
  return {
    ai: { memory: [], context: {}, enabled: false, suggestions: [] },
    ui: {
      theme: { border: '#334155', shadow: '#334155', background: '#0f172a' },
      layout: { width: 260, height: 240, rounded: true },
    },
    inputs: [
      { key: 'text', type: 'string', label: 'Text', value: '' },
      { key: 'delay', type: 'number', label: 'Delay (ms)', value: 0 },
      { key: 'color', type: 'color', label: 'Background Color', value: '#0f172a' },
    ],
  }
}

// ✅ updateNodeAction — Optimistic UI + Rollback + tracker
const updateNodeAction = async ({ nodeId, actionId, newActionType }) => {
  const payload = buildPayloadFromUI(newActionType, {})
  const idx = nodes.value.findIndex((n) => n.id === nodeId)
  const oldActions = idx !== -1 ? [...nodes.value[idx].data.actions] : [] // ← للـ rollback

  // Optimistic Update
  if (idx !== -1) {
    const updated = { ...nodes.value[idx] }
    updated.data = { ...updated.data }
    updated.data.actions = updated.data.actions.map((a) =>
      a.id === actionId ? { ...a, action_type: newActionType, payload } : a,
    )
    nodes.value[idx] = updated
    selectedNode.value = nodes.value[idx]
  }

  await nodeAction.run(
    () => automationService.updateAction(actionId, { action_type: newActionType, payload }),
    {
      successSummary: 'تم تحديث الـ Action',
      successDetail: newActionType,
      errorSummary: 'فشل تحديث الـ Action',
      onError: () => {
        // ✅ Rollback لو الـ API فشل
        if (idx !== -1) {
          nodes.value[idx] = {
            ...nodes.value[idx],
            data: { ...nodes.value[idx].data, actions: oldActions },
          }
          selectedNode.value = nodes.value[idx]
        }
      },
    },
  )
}

// ✅ deleteNodeAction — يظهر في ApiFlowPanel
const deleteNodeAction = ({ nodeId, actionId }) =>
  nodeAction.run(() => automationService.deleteAction(actionId), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      const idx = nodes.value.findIndex((n) => n.id === nodeId)
      if (idx !== -1) {
        const updated = { ...nodes.value[idx] }
        updated.data = { ...updated.data }
        updated.data.actions = updated.data.actions.filter((a) => a.id !== actionId)
        nodes.value[idx] = updated
        selectedNode.value = nodes.value[idx]
      }
    },
  })

// ==============================================
// =================== 5️⃣ Edge =================
// ==============================================

// ✅ onConnect — يظهر في ApiFlowPanel
const onConnect = async (params) => {
  if (!currentWorkflowId.value) return
  await nodeAction.run(
    () =>
      automationService.createWorkflowEdge({
        workflow: currentWorkflowId.value,
        source_node: params.source,
        target_node: params.target,
        condition: 'success',
      }),
    {
      successSummary: 'تم ربط الـ Nodes',
      errorSummary: 'فشل إنشاء الـ Edge',
      onSuccess: ({ data }) => {
        edges.value.push({
          id: data.id,
          source: data.source_node,
          target: data.target_node,
          sourceHandle: 'source',
          targetHandle: 'target',
          type: 'default',
          data: { label: data.condition },
          animated: true,
          style: { stroke: '#4CAF50', strokeWidth: 2 },
        })
      },
    },
  )
}

const onNodeDragStop = (node) => {
  const backendId = node.data?.node?.backend_id ?? node.id
  if (!backendId) return
  enqueueUpdate({
    type: 'node-position',
    id: backendId,
    position_x: node.position.x,
    position_y: node.position.y,
  })
}

// ✅ startWorkflow — يظهر في ApiFlowPanel
const startWorkflow = () =>
  workflowAction.run(() => automationService.runWorkflow(currentWorkflowId.value), {
    validate: () => (!currentWorkflowId.value ? 'اختر Workflow الأول' : null),
    successSummary: '🚀 Workflow Started',
    successDetail: 'Workflow Started successfully',
    errorSummary: 'فشل تشغيل الـ Workflow',
    onSuccess: ({ data }) => {
      currentTaskRunId.value = data.task_run_id
    },
  })

// ==============================================
// ================== 6️⃣ ACTIONS ===============
// ==============================================

// ✅ createAction — يمر عبر tracker
const createAction = async ({ node, action_type, payload }) => {
  const result = await tracker.execute({
    serviceFn: () => automationService.createAction({ node, action_type, payload }),
  })
  return result.data
}

const getColorFromAction = (type) =>
  ({
    open_program: '#16a34a',
    close_program: '#dc2626',
    wait: '#0ea5e9',
    press: '#64748b',
    hotkey: '#f59e0b',
  })[type] ?? '#334155'

const buildPayloadFromUI = (type, extraData = {}) => {
  switch (type) {
    case 'wait':
      return { seconds: Number(extraData.delay || 0) }
    case 'press':
      return { key: extraData.key }
    case 'hotkey':
      return { keys: extraData.keys }
    case 'click_element':
      return { element_id: extraData.element_id }
    case 'open_program':
      return {}
    default:
      return {}
  }
}

const handleUpdateNodeAction = async ({ nodeId, newActionType, extraData }) => {
  const node = workflowState.nodesMap.get(nodeId)
  if (!node) return
  const payload = buildPayloadFromUI(newActionType, extraData)
  node.data.actions.action_type = newActionType
  node.data.actions.payload = payload
  node.data.config.ui.background = getColorFromAction(newActionType)
  nodes.value = [...nodes.value]
  workflowState.updateQueue.push({
    type: 'action',
    nodeId,
    actionId: node.data.actions.id,
    action_type: newActionType,
    payload,
  })
  debouncedSync()
}

// ==============================================
// ================== 7️⃣ Tasks ================
// ==============================================
const loadTasks = async () => {
  loadingTasks.value = true
  try {
    const { data } = await automationService.listTasks()
    tasks.value = data
  } finally {
    loadingTasks.value = false
  }
}
const selectTask = async (id) => {
  if (!id) return
  currentTaskId.value = id
  await loadTask(id)
}
const loadTask = async (id) => {
  const { data } = await automationService.getTask(id)
  currentTaskId.value = data.id
  formTask.value = { name: data.name, description: data.description, program: data.program }
}

// ✅ Create Task
const createTask = () =>
  taskAction.run(
    () => {
      const fd = new FormData()
      fd.append('name', formTask.value.name)
      fd.append('description', formTask.value.description)
      fd.append('program', formTask.value.program)
      return automationService.createTask(fd)
    },
    {
      validate: () => validateTask(formTask.value),
      successSummary: 'تم إنشاء الـ Task',
      errorSummary: 'فشل إنشاء الـ Task',
      onSuccess: async ({ data }) => {
        tasks.value.unshift(data)
        createTaskVisible.value = false
        await loadTasks()
      },
    },
  )

// ✅ Edit Task
const openEditTask = async (id) => {
  if (!id) return
  try {
    currentTaskId.value = id
    await loadTask(id)
    editTaskVisible.value = true
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
  }
}
const editTask = () =>
  taskAction.run(
    () => {
      const fd = new FormData()
      fd.append('name', formTask.value.name)
      fd.append('description', formTask.value.description)
      fd.append('program', formTask.value.program)
      return automationService.updateTask(currentTaskId.value, fd)
    },
    {
      validate: () => validateTask(formTask.value),
      successSummary: 'تم تحديث الـ Task',
      errorSummary: 'فشل تحديث الـ Task',
      onSuccess: async () => {
        editTaskVisible.value = false
        await loadTasks()
      },
    },
  )

// ✅ Delete Task
const confirmDeleteTask = (program) => {
  confirm.require({
    message: `هل تريد حذف "${program.name}"؟`,
    header: '⚠️ تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'نعم، احذف',
    rejectLabel: 'إلغاء',
    accept: async () => await deleteTask(program.id),
    reject: () =>
      toast.add({ severity: 'info', summary: 'إلغاء', detail: 'لم يتم الحذف', life: 2000 }),
  })
}
const deleteTask = (id) =>
  taskAction.run(() => automationService.deleteTask(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      tasks.value = tasks.value.filter((t) => t.id !== id)
      if (currentTaskId.value === id) {
        currentTaskId.value = null
      }
    },
  })

// ==============================================
// ================== 🔟 Delays ================
// ==============================================
const loadDelays = async () => {
  loadingDelays.value = true
  try {
    const { data } = await automationService.listDelays()
    delays.value = data
  } catch (error) {
    console.log('Error Delays:', error)
  } finally {
    loadingDelays.value = false
  }
}

// ==================================================
// 💾 Auto Save
// ==================================================
const debouncedAutoSave = debounce(() => {
  if (!isInitialized.value) return
  if (!currentWorkflowId.value) return
  if (isLoadingWorkflow.value) return
  if (currentProgramId.value) formProgramElement.value.program = currentProgramId.value
  const exists = workflows.value.find((w) => w.id === currentWorkflowId.value)
  if (!exists) return
  saveWorkflow()
}, 500)

watch([nodes, edges], debouncedAutoSave, { deep: true })
watch(currentProgramId, (newId) => {
  if (newId) formProgramElement.value.program = newId
})

onMounted(async () => {
  await Promise.all([
    loadPrograms(),
    loadProgramElements(),
    loadWorkflows(),
    loadlistWorkflowNodes(),
    loadDelays(),
    loadTasks(),
  ])
  isInitialized.value = true
  if (currentWorkflowId.value) await loadWorkflowEvents(currentWorkflowId.value)
  console.log('🟢 APP READY')
})
</script>

<template>
  <main class="h-screen p-4">
    <div class="grid grid-cols-12 gap-4 h-full">
      <aside class="col-span-3 border rounded p-4 overflow-auto space-y-6">
        <div>
          <div class="flex justify-between items-center my-3">
            <h3 class="text-lg font-bold"><prime_tag value="🖥️ Programs" /></h3>
            <prime_button
              icon="pi pi-plus"
              @click="createProgramVisible = true"
              style="background-color: transparent; padding: 0; border: none"
              ><prime_tag icon="pi pi-plus"
            /></prime_button>
          </div>
          <div class="wrapper_programs">
            <div v-if="loadingPrograms">
              <prime_skeleton
                v-for="i in 3"
                :key="i"
                height="3rem"
                width="100%"
                class="mt-2"
                borderRadius="16px"
              />
            </div>
            <div
              v-for="p in programs"
              :key="p.id"
              class="p-1 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'program', id: p.id })"
              v-else
              @click="selectProgram(p.id)"
            >
              <prime_image alt="Image" preview>
                <template #image><img :src="p.get_image" alt="image" /></template>
              </prime_image>
              <prime_tag :value="p.name" />
              <div>
                <prime_button
                  @click.stop="openEditProgram(p.id)"
                  style="background-color: transparent; padding: 0; border: none"
                  ><prime_tag icon="pi pi-file-edit"
                /></prime_button>
                <prime_button
                  @click.stop="confirmDeleteProgram(p)"
                  style="background-color: transparent; padding: 0; border: none"
                  ><prime_tag icon="pi pi-trash"
                /></prime_button>
              </div>
            </div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center my-3">
            <h3 class="text-lg font-bold"><prime_tag value="🧩 Program Elements" /></h3>
            <prime_button
              @click="createProgramElementsVisible = true"
              style="background-color: transparent; padding: 0; border: none"
              ><prime_tag icon="pi pi-plus"
            /></prime_button>
          </div>
          <div class="wrapper_programs">
            <div v-if="loadingProgramElements">
              <prime_skeleton
                v-for="i in 3"
                :key="i"
                height="3rem"
                width="100%"
                class="mt-2"
                borderRadius="16px"
              />
            </div>
            <div
              v-for="p in programsElement"
              :key="p.id"
              class="p-1 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'program-element', id: p.id })"
              v-else
              @click="selectProgramElement(p.id)"
            >
              <prime_image alt="Image" preview>
                <template #image><img :src="p.get_image" alt="image" /></template>
              </prime_image>
              <prime_tag :value="p.name" />
              <div>
                <prime_button
                  @click.stop="openEditProgramElement(p.id)"
                  style="background-color: transparent; padding: 0; border: none"
                  ><prime_tag icon="pi pi-file-edit"
                /></prime_button>
                <prime_button
                  @click.stop="confirmDeleteProgramElement(p)"
                  style="background-color: transparent; padding: 0; border: none"
                  ><prime_tag icon="pi pi-trash"
                /></prime_button>
              </div>
            </div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center my-3">
            <h3 class="text-lg font-bold"><prime_tag value="⏳ Delays" /></h3>
          </div>
          <div class="wrapper_delays">
            <div v-if="loadingDelays">
              <prime_skeleton
                v-for="i in 3"
                :key="i"
                height="3rem"
                width="100%"
                class="mt-2"
                borderRadius="16px"
              />
            </div>
            <div
              v-for="d in delays"
              :key="d.id"
              class="p-2 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'delay', id: d.id })"
              v-else
            >
              <i class="pi pi-stopwatch"></i><prime_tag :value="d.seconds + 's'" /><prime_tag
                value="Delay"
              />
            </div>
          </div>
        </div>

        <div>
          <h3 class="text-lg font-bold mb-3">Workflows</h3>
          <div class="space-y-2">
            <div
              v-for="w in workflows"
              :key="w.id"
              class="p-2 bg-white border rounded cursor-pointer align-content-between"
              @click="selectWorkflow(w.id)"
            >
              <span>{{ w.name }}</span>
              <span
                class="text-xs px-2 py-1 rounded"
                :class="{
                  'bg-gray-200': w.status === 'draft',
                  'bg-green-200': w.status === 'active',
                  'bg-yellow-200': w.status === 'paused',
                }"
                >{{ w.status }}</span
              >
            </div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-3">
            <h3 class="text-lg font-bold"><prime_tag value="Tasks Templates" /></h3>
            <prime_button
              @click="createTaskVisible = true"
              style="background-color: transparent; padding: 0; border: none"
              ><prime_tag icon="pi pi-plus"
            /></prime_button>
          </div>
          <div class="wrapper_programs">
            <div v-if="loadingTasks">
              <prime_skeleton
                v-for="i in 3"
                :key="i"
                height="3rem"
                width="100%"
                class="mt-2"
                borderRadius="16px"
              />
            </div>
            <div
              v-for="t in tasks"
              :key="t.id"
              class="p-1 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'task', id: t.id })"
              v-else
              @click="selectTask(t.id)"
            >
              <prime_tag :value="t.name" />
              <div>
                <prime_button
                  @click.stop="openEditTask(t.id)"
                  style="background-color: transparent; padding: 0; border: none"
                  ><prime_tag icon="pi pi-file-edit"
                /></prime_button>
                <prime_button
                  @click.stop="confirmDeleteTask(t)"
                  style="background-color: transparent; padding: 0; border: none"
                  ><prime_tag icon="pi pi-trash"
                /></prime_button>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <section class="col-span-9 mb-16">
        <div class="wrapper_name_description">
          <div class="inner_name_description">
            <div>
              <label class="block font-semibold mb-1">Name</label>
              <input
                v-model="formWorkflow.name"
                type="text"
                class="input"
                placeholder="Program name"
              />
            </div>
            <div>
              <label class="block font-semibold mb-1">Description</label>
              <textarea
                v-model="formWorkflow.description"
                class="textarea"
                cols="30"
                rows="1"
              ></textarea>
            </div>
            <div>
              <label class="block font-semibold mb-1">Status</label>
              <select v-model="formWorkflow.status" class="input">
                <option value="draft">📝 Draft</option>
                <option value="active">✅ Active</option>
                <option value="paused">⏸ Paused</option>
              </select>
            </div>
            <div><prime_button label="🗑️" @click="deleteWorkflow(currentWorkflowId)" /></div>
          </div>
        </div>

        <VueFlow
          class="border rounded"
          v-model:nodes="nodes"
          v-model:edges="edges"
          :node-types="nodeTypes"
          :edge-types="edgeTypes"
          @node-click="onNodeSelect"
          @dragover="onDragOver"
          @drop="onDrop"
          @connect="onConnect"
          @nodeDragStop="onNodeDragStop"
          :pan-on-drag="[1]"
          :pan-on-scroll="true"
          :zoom-on-scroll="false"
        >
          <Background variant="dots" pattern-color="#aaa" :gap="10" />
          <Controls />
          <template #node-custom="props">
            <CustomNode
              v-bind="props"
              @run-task="runTaskFromNode"
              @open-program="openProgram"
              @close-program="closeProgram"
              @status-program="statusProgram"
              @delete-node="deleteNodeOnWorkflow"
              @update-node-action="handleUpdateNodeAction"
            />
          </template>
          <template #edge-custom="props"><CustomEdge v-bind="props" /></template>
          <MiniMap />
          <Panel position="top-left">
            <div class="flex gap-2">
              <button @click="createWorkflow" class="btn-white">➕ إنشاء Workflow جديد</button>
              <button @click="saveWorkflow" class="btn-white">💾 Save Workflow</button>
              <button @click="clearWorkflow" class="btn-white">🗑️ مسح الكل</button>
              <button @click="updateStatusWorkflow('active')">▶ Activate</button>
              <button @click="updateStatusWorkflow('paused')">⏸ Pause</button>
              <prime_button
                label="Start Workflow"
                icon="pi pi-play"
                class="p-button-success"
                :disabled="!currentWorkflowId || workflowAction.loading.value"
                @click="startWorkflow"
              />
            </div>
            <div class="inner_control_node_layout_buttons">
              <button @click="autoLayout('LR')">LR 📐</button>
              <button @click="autoLayout('RL')">RL 📐</button>
              <button @click="autoLayout('TB')">TB 📐</button>
              <button @click="autoLayout('BT')">BT 📐</button>
            </div>
          </Panel>
        </VueFlow>
      </section>
    </div>

    <LiveConsole v-if="taskRunId" :taskRunId="currentTaskRunId" />


    <ApiFlowPanel
      :stages="tracker.stages"
      :meta="tracker.meta"
      :error="tracker.error"
      :show-data="true"
    />
    <ActionPanel
      :show="showActionPanel"
      :selected-node="selectedNode"
      v-model:new-action-type-for-panel="newActionTypeForPanel"
      @close="showActionPanel = false"
      @create-action="createNodeAction"
      @update-action="updateNodeAction"
      @delete-action="deleteNodeAction"
    />

    <CreateProgram
      v-model:visible="createProgramVisible"
      :form="formProgram"
      @image-change="onImageChangeProgram"
      @submit="createProgram"
    />

    <div class="card flex justify-center">
      <prime_dialog
        v-model:visible="editProgramVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">Edit Program</div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Program Name</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.name"
                  type="text"
                  placeholder="Program name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.description"
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Executable Path</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.executable_path"
                  placeholder="C:/Program Files/VSCode/Code.exe"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Project Path</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.project_path"
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Working Directory</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.working_directory"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Window Title Pattern</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.window_title_pattern"
                />
              </div>
            </div>
            <input type="file" accept="image/*" @change="onImageChangeProgram" />
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                label="Update"
                @click="editProgram"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <div class="card flex justify-center" style="overflow-y: auto">
      <prime_dialog
        v-model:visible="createProgramElementsVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">
              Create Program Element
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold"
                  >Program Name <span class="text-red-300">*</span></label
                >
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.name"
                  placeholder="Program name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.description"
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Image</label>
                <input type="file" accept="image/*" @change="onImageChangeProgramElement" />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold"
                  >Program <span class="text-red-300">*</span></label
                >
                <select v-model="formProgramElement.program" class="input">
                  <option disabled value="">اختر البرنامج</option>
                  <option v-for="p in programs" :key="p.id" :value="p.id">{{ p.name }}</option>
                </select>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold"
                  >Selector Type <span class="text-red-300">*</span></label
                >
                <select v-model="formProgramElement.selector_type">
                  <option disabled value="">Choose selector type</option>
                  <option
                    v-for="type in programElementselectorTypes"
                    :key="type.value"
                    :value="type.value"
                  >
                    {{ type.label }}
                  </option>
                </select>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">X</label
                ><prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.x"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Y</label
                ><prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.y"
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Width</label
                ><prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.width"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Height</label
                ><prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.height"
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Shortcut</label
                ><prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.shortcut"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Confidence</label
                ><prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.confidence"
                />
              </div>
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                label="Create"
                @click="createProgramElement"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <div class="card flex justify-center">
      <prime_dialog
        v-model:visible="editProgramElementsVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">
              Edit Program Element
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Name</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Program</label>
                <select v-model="formProgramElement.program" class="input">
                  <option disabled value="">اختر البرنامج</option>
                  <option v-for="p in programs" :key="p.id" :value="p.id">{{ p.name }}</option>
                </select>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Selector Type</label>
                <select v-model="formProgramElement.selector_type">
                  <option disabled value="">Choose selector type</option>
                  <option
                    v-for="type in programElementselectorTypes"
                    :key="type.value"
                    :value="type.value"
                  >
                    {{ type.label }}
                  </option>
                </select>
              </div>
            </div>
            <input type="file" accept="image/*" @change="onImageChangeProgramElement" />
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                label="Update"
                @click="editProgramElement"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <div class="card flex justify-center" style="overflow-y: auto">
      <prime_dialog
        v-model:visible="createTaskVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">Create Task</div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold"
                  >Task Name <span class="text-red-300">*</span></label
                >
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formTask.name"
                  placeholder="Task Name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formTask.description"
                />
              </div>
            </div>
            <div class="inline-flex flex-col gap-2">
              <label class="text-primary-50 font-semibold"
                >Program <span class="text-red-300">*</span></label
              >
              <select v-model="formTask.program" class="input">
                <option disabled value="">اختر البرنامج</option>
                <option v-for="p in programs" :key="p.id" :value="p.id">{{ p.name }}</option>
              </select>
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                label="Create"
                @click="createTask"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <div class="card flex justify-center">
      <prime_dialog
        v-model:visible="editTaskVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">Edit Task</div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Task Name</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formTask.name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formTask.description"
                />
              </div>
            </div>
            <div class="inline-flex flex-col gap-2">
              <label class="text-primary-50 font-semibold">Program</label>
              <select v-model="formTask.program" class="input">
                <option disabled value="">اختر البرنامج</option>
                <option v-for="p in programs" :key="p.id" :value="p.id">{{ p.name }}</option>
              </select>
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                label="Update"
                @click="editTask"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>
  </main>
</template> -->

<!--
/*
const createProgram = () =>
  programAction.run(
    () => {
      const err = validateProgram(formProgram.value)
      if (err) {
        showToast('warn', 'تحقق من البيانات', err, 4000)
        throw new Error(err)
      }
      return automationService.createProgram(buildProgramFormData(formProgram.value))
    },
    {
      successSummary: 'تم إنشاء البرنامج',
      successDetail: `"${formProgram.value.name}" أُنشئ بنجاح`,
      errorSummary: 'فشل إنشاء البرنامج',
      onSuccess: async ({ data }) => {
        programs.value.unshift(data) // optimistic update — no full reload
        currentProgramId.value = data.id
        createProgramVisible.value = false // ✅ closes ONLY on success
      },
      // No onError → dialog stays open so user can fix input
    },
  )
*/
 -->
