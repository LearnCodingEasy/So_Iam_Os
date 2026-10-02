// ============================================================
//  useNodeDragDrop.js
//  src/composables/useNodeDragDrop.js
//
//  مسؤول عن كل حاجة خاصة بالـ drag & drop على الـ VueFlow canvas:
//
//  1️⃣ Sidebar drag     → startDrag / onDragOver / onDrop
//  2️⃣ Node creation    → createNodeOnCanvas (بيكلم الـ backend)
//  3️⃣ Position sync    → onNodeDragStop + debounced queue
//                          (بيـ bypass الـ tracker عشان مش محتاج يظهر في ApiFlowPanel)
//
//  الاستخدام في AutomationView:
//  ─────────────────────────────────────────
//  const {
//    draggedItem,
//    startDrag,
//    onDragOver,
//    onDrop,
//    onNodeDragStop,
//  } = useNodeDragDrop({ workflowStore, programStore, tracker, project, showToast })
// ============================================================

import { ref, reactive } from 'vue'
import { debounce }       from 'lodash'
import automationService  from '@/services/AutomationService'

export function useNodeDragDrop({ workflowStore, programStore, tracker, project, showToast }) {

  // ─────────────────────────────────────────
  // State
  // ─────────────────────────────────────────
  const draggedItem = ref(null)   // الـ item اللي بيتسحب من الـ sidebar

  const syncState = reactive({
    updateQueue: [],
    isSyncing:   false,
  })

  // ─────────────────────────────────────────
  // 1️⃣ Sidebar Drag Handlers
  // ─────────────────────────────────────────

  // بيتفعّل لما المستخدم يبدأ يسحب item من الـ sidebar
  const startDrag = (item) => {
    draggedItem.value = item
  }

  // يمنع الـ default browser behavior ويسمح بالـ drop
  const onDragOver = (e) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
  }

  // بيتفعّل لما المستخدم يرمي الـ item على الـ Canvas
  const onDrop = async (e) => {
    e.preventDefault()
    if (!draggedItem.value) return
    await createNodeOnCanvas(draggedItem.value, e)
    draggedItem.value = null
  }

  // ─────────────────────────────────────────
  // 2️⃣ Node Creation (Drag & Drop → Backend)
  //
  // الـ flow:
  //   1. احسب الـ position على الـ canvas
  //   2. حدد الـ action_type حسب نوع الـ item
  //   3. POST /api/automation/workflow-nodes/
  //   4. POST /api/automation/actions/
  //   5. أضف الـ node للـ canvas فوراً
  // ─────────────────────────────────────────
  const createNodeOnCanvas = async (item, dropEvent) => {
    if (!workflowStore.currentWorkflowId) {
      showToast('warn', 'لا يوجد Workflow', 'اختر Workflow الأول', 9000)
      return
    }

    workflowStore.isLoading = true
    workflowStore.cancelAutoSave()

    try {
      // 📍 احسب مكان الـ drop على الـ canvas
      const position = project({ x: dropEvent.clientX, y: dropEvent.clientY })

      // 🗺️ حدد نوع الـ action حسب نوع الـ item
      const ACTION_TYPE_MAP = {
        'program':         'open_program',
        'program-element': 'press',
        'delay':           'wait',
      }
      const actionType = ACTION_TYPE_MAP[item.type] ?? 'custom'

      // 🏷️ جيب اسم الـ node من الـ store (من غير API call زيادة)
      const programData = programStore.programById(item.id)
      const nodeLabel   = programData?.name ?? item.name ?? actionType

      // 🎨 الـ UI config الافتراضي للـ node
      const defaultConfig = {
        ui: {
          theme:  { background: '#0f172a', border: '#334155', shadow: '#334155' },
          layout: { width: 260, height: 240, rounded: true },
        },
        inputs: [
          { key: 'text',  label: 'Text',       type: 'string', value: '' },
          { key: 'delay', label: 'Delay (ms)', type: 'number', value: 0 },
        ],
        ai: { enabled: false, context: {}, memory: [], suggestions: [] },
      }

      // ─────────────────────────────────────
      // Step 1: إنشاء الـ Node في الـ Backend
      // ─────────────────────────────────────
      const nodeResult = await tracker.execute({
        serviceFn: () => automationService.createWorkflowNode({
          workflow:   workflowStore.currentWorkflowId,
          node_type:  item.type,
          label:      nodeLabel,
          program:    item.type === 'program'          ? item.id : null,
          element:    item.type === 'program-element'  ? item.id : null,
          position_x: position.x,
          position_y: position.y,
          config:     defaultConfig,
        }),
      })
      const nodeData = nodeResult.data

      // ─────────────────────────────────────
      // Step 2: إنشاء الـ Action وربطه بالـ Node
      // ─────────────────────────────────────
      const actionResult = await tracker.execute({
        serviceFn: () => automationService.createAction({
          node:        nodeData.id,
          action_type: actionType,
          payload:     buildDefaultPayload(actionType),
        }),
      })
      const actionData = actionResult.data

      // ─────────────────────────────────────
      // Step 3: أضف الـ Node للـ Canvas فوراً
      //         نفس structure بتاعة loadWorkflowEvents
      // ─────────────────────────────────────
      workflowStore.nodes.push({
        id:       nodeData.id,
        type:     'custom',
        position: { x: nodeData.position_x, y: nodeData.position_y },
        data: {
          label: nodeData.label,
          node: {
            backend_id:   nodeData.id,
            id:           nodeData.id,
            program_name: nodeData.program_name ?? '',
            element_name: nodeData.element_name ?? '',
            node_type:    nodeData.node_type,
            label:        nodeData.label,
            config:       nodeData.config,
            program:      nodeData.program,
            element:      nodeData.element,
            status:       'idle',
          },
          actions: actionData ? [actionData] : [],
        },
      })

      showToast('success', 'تم إنشاء الـ Node', nodeData.label, 4000)

    } catch (err) {
      showToast('error', 'فشل إنشاء الـ Node', err?.message, 6000)
    } finally {
      workflowStore.isLoading = false
    }
  }

  // ─────────────────────────────────────────
  // 3️⃣ Node Position Sync (Drag Stop)
  //
  // bypass الـ tracker عشان:
  // - مش محتاج يظهر في ApiFlowPanel
  // - بيتنفذ كتير أوي (مع كل drag)
  // - queue + debounce عشان نقلل الـ API calls
  // ─────────────────────────────────────────

  const onNodeDragStop = ({ node }) => {
    // ✅ دايماً استخدم backend_id مش VueFlow id
    const backendId = node.data?.node?.backend_id ?? node.id
    if (!backendId) return

    // أضف للـ queue وشغّل الـ debounced sync
    syncState.updateQueue.push({
      id:         backendId,
      position_x: node.position.x,
      position_y: node.position.y,
    })
    debouncedPositionSync()
  }

  const processPositionQueue = async () => {
    if (syncState.isSyncing) return
    syncState.isSyncing = true

    while (syncState.updateQueue.length > 0) {
      // خد آخر update للـ node ده بس (skip القديم)
      const job = deduplicateQueue()
      if (!job) break

      try {
        await automationService.updateWorkflowNode(job.id, {
          position_x: job.position_x,
          position_y: job.position_y,
        })
      } catch (err) {
        console.warn('Position sync failed:', err?.message)
      }
    }

    syncState.isSyncing = false
  }

  // لو نفس الـ node اتحرك أكتر من مرة → خد آخر position بس
  const deduplicateQueue = () => {
    if (syncState.updateQueue.length === 0) return null
    const uniqueMap = new Map()
    syncState.updateQueue.forEach(job => uniqueMap.set(job.id, job))
    syncState.updateQueue = []
    const jobs = [...uniqueMap.values()]
    return jobs.shift()
  }

  const debouncedPositionSync = debounce(processPositionQueue, 300)

  // ─────────────────────────────────────────
  // Helpers
  // ─────────────────────────────────────────

  // بيبني الـ default payload حسب نوع الـ action
  const buildDefaultPayload = (actionType) => ({
    open_program:  {},
    close_program: {},
    press:         { key: '' },
    hotkey:        { keys: [] },
    wait:          { seconds: 1 },
    click_element: { element_id: null },
    type_text:     { text: '' },
  }[actionType] ?? {})

  // ─────────────────────────────────────────
  // Return
  // ─────────────────────────────────────────
  return {
    draggedItem,
    startDrag,
    onDragOver,
    onDrop,
    onNodeDragStop,
    createNodeOnCanvas,
  }
}
