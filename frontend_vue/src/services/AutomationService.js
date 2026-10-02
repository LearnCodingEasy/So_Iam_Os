// services/AutomationService.js
import api from './api'

export default {
  /* ==================================================
   * 1️⃣ PROGRAMS (التعامل مع البرامج)
   * ================================================== */

  listPrograms() {
    return api.get('automation/programs/')
  },
  getProgram(id) {
    return api.get(`automation/programs/${id}/`)
  },
  createProgram(formData) {
    return api.post('automation/programs/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  updateProgram(id, data) {
    return api.patch(`automation/programs/${id}/`, data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  deleteProgram(id) {
    return api.delete(`automation/programs/${id}/`)
  },
  openProgram(id) {
    return api.post(`automation/programs/${id}/open/`)
  },
  closeProgram(id) {
    return api.post(`automation/programs/${id}/close/`)
  },
  statusProgram(id) {
    return api.get(`automation/programs/${id}/status/`)
  },
  focusProgram(programId) {
    return api.post(`/automation/programs/${programId}/focus/`)
  },
  maximizeProgram(programId) {
    return api.post(`/automation/programs/${programId}/maximize/`)
  },
  getOpenWindows() {
    return api.get('/automation/get_open_windows/')
  },
  scanProgramElements(id, windowTitlePattern = null) {
    return api.post(
      `/automation/programs/${id}/scan_elements/`,
      windowTitlePattern ? { window_title_pattern: windowTitlePattern } : {},
    )
  },
  /* ==================================================
   * 2️⃣ PROGRAM ELEMENTS (أزرار – عناصر – coords)
   * ================================================== */

  listProgramElements() {
    return api.get(`automation/program-elements/`)
  },
  listProgramIdElements(programId = null) {
    const q = programId ? `?program=${programId}` : ''
    return api.get(`automation/program-elements/${q}`)
  },
  getProgramElement(id) {
    return api.get(`automation/program-elements/${id}/`)
  },
  createProgramElement(data) {
    return api.post('automation/program-elements/', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  updateProgramElement(id, data) {
    return api.patch(`automation/program-elements/${id}/`, data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  deleteProgramElement(id) {
    return api.delete(`automation/program-elements/${id}/`)
  },
  /* ==================================================
   * 3️⃣ WORKFLOWS (العقل)
   * ================================================== */
  listWorkflows() {
    return api.get('automation/workflows/')
  },
  getWorkflow(id) {
    return api.get(`automation/workflows/${id}/`)
  },
  getWorkflow_full_events(id) {
    return api.get(`automation/workflows/${id}/full_events/`)
  },
  createWorkflow(data) {
    return api.post('automation/workflows/', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  saveWorkflowAll(id, payload) {
    return api.post(`automation/workflows/${id}/save_all/`, payload, {
      headers: { 'Content-Type': 'application/json' },
    })
  },
  updateWorkflow(id, data) {
    return api.patch(`automation/workflows/${id}/`, data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  deleteWorkflow(id) {
    return api.delete(`automation/workflows/${id}/`)
  },
  runWorkflow(id) {
    return api.post(`automation/workflows/${id}/run/`, {
      headers: { 'Content-Type': 'application/json' },
    })
  },
  /* ==================================================
   * 4️⃣ WORKFLOW NODES (Vue Flow Nodes)
   * ================================================== */
  listWorkflowNodes() {
    return api.get('automation/workflow-nodes/')
  },
  listWorkflowNodesById(workflowId = null) {
    const q = workflowId ? `?workflow=${workflowId}` : ''
    return api.get(`automation/workflow-nodes/${q}`)
  },
  getWorkflowNode(id) {
    return api.get(`automation/workflow-nodes/${id}/`)
  },
  createWorkflowNode(data) {
    return api.post('automation/workflow-nodes/', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  },
  updateWorkflowNode(id, data) {
    return api.patch(`automation/workflow-nodes/${id}/`, data, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  },
  deleteWorkflowNode(id) {
    return api.delete(`automation/workflow-nodes/${id}/`)
  },
  // ▶️ RUN SINGLE NODE
  runWorkflowNode(nodeId) {
    return api.post(`automation/workflow-nodes/${nodeId}/run/`)
  },
  /* ==================================================
   * 5️⃣ WORKFLOW EDGES (الربط)
   * ================================================== */
  listWorkflowEdges(workflowId = null) {
    const q = workflowId ? `?workflow=${workflowId}` : ''
    return api.get(`automation/workflow-edges/${q}`)
  },
  createWorkflowEdge(data) {
    return api.post('automation/workflow-edges/', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  },
  updateWorkflowEdge(id, data) {
    return api.patch(`automation/workflow-edges/${id}/`, data)
  },
  deleteWorkflowEdge(id) {
    return api.delete(`automation/workflow-edges/${id}/`)
  },
  /* ==================================================
   * 6️⃣ ACTIONS (Mouse / Keyboard / OS)
   * ================================================== */
  listActions(nodeId = null) {
    const q = nodeId ? `?node=${nodeId}` : ''
    return api.get(`automation/actions/${q}`)
  },
  getAction(id) {
    return api.get(`automation/actions/${id}/`)
  },
  createAction(data) {
    return api.post('automation/actions/', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  },
  updateAction(id, data) {
    return api.patch(`automation/actions/${id}/`, data, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  },
  deleteAction(id) {
    return api.delete(`automation/actions/${id}/`)
  },
  executeAction(id) {
    return api.post(`automation/actions/${id}/execute/`)
  },
  /* ==================================================
   * 7️⃣ TASKS (سيناريو جاهز)
   * ================================================== */
  listTasks() {
    return api.get('automation/tasks/')
  },
  getTask(id) {
    return api.get(`automation/tasks/${id}/`)
  },
  createTask(data) {
    return api.post('automation/tasks/', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  },
  updateTask(id, data) {
    return api.patch(`automation/tasks/${id}/`, data)
  },
  deleteTask(id) {
    return api.delete(`automation/tasks/${id}/`)
  },
  /* ==================================================
   * 8️⃣ TASK RUNS (التنفيذ + اللوج)
   * ================================================== */
  listTaskRuns() {
    return api.get('automation/task-runs/')
  },
  getTaskRun(id) {
    return api.get(`automation/task-runs/${id}/`)
  },
  /* ==================================================
   * 9️⃣ SCREEN STATE (مراقبة الشاشة)
   * ================================================== */
  listScreenStates(taskRunId = null) {
    const q = taskRunId ? `?task_run=${taskRunId}` : ''
    return api.get(`automation/screen-states/${q}`)
  },
  createScreenState(formData) {
    return api.post('automation/screen-states/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  bulkCreateScreenStates(dataArray) {
    return api.post('automation/screen-states/bulk_create/', dataArray)
  },
  /* ==================================================
   * 🔟 DELAYS (انتظار)
   * ================================================== */
  listDelays() {
    return api.get('automation/delays/')
  },
}
