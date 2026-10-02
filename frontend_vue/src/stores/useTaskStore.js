/*
===================================================
useTaskStore.js
src/stores/useTaskStore.js

المسؤوليات:
- CRUD الـ Tasks (Task Templates)
- Task Run tracking
===================================================

*/
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import automationService from '@/services/AutomationService'

export const useTaskStore = defineStore('task', () => {
  // ─────────────────────────────────────────
  // State
  // ─────────────────────────────────────────
  const tasks = ref([])
  const currentTask = ref(null)
  // بيتحدث لما يشتغل workflow
  const currentTaskRunId = ref(null)
  const isLoading = ref(false)

  const form = ref({
    name: '',
    description: '',
    program: null, // FK id
  })

  // ─────────────────────────────────────────
  // Getters
  // ─────────────────────────────────────────
  const currentTaskId = computed(() => currentTask.value?.id ?? null)

  const taskById = (id) => tasks.value.find((t) => t.id === id) ?? null

  // Tasks اللي مرتبطة ببرنامج معين
  const tasksByProgram = (programId) => tasks.value.filter((t) => t.program === programId)

  // ─────────────────────────────────────────
  // Validation
  // ─────────────────────────────────────────
  function validateForm(f = form.value) {
    if (!f.name?.trim()) return 'اسم الـ Task مطلوب'
    if (!f.program) return 'لازم تختار برنامج'
    return null
  }

  // ─────────────────────────────────────────
  // Helpers
  // ─────────────────────────────────────────
  function buildFormData(f = form.value) {
    const fd = new FormData()
    fd.append('name', f.name)
    fd.append('description', f.description || '')
    fd.append('program', f.program)
    return fd
  }

  function resetForm() {
    form.value = { name: '', description: '', program: null }
  }

  function fillFormFromData(data) {
    form.value = {
      name: data.name ?? '',
      description: data.description ?? '',
      program: data.program ?? null,
    }
  }

  // ─────────────────────────────────────────
  // CRUD
  // ─────────────────────────────────────────

  // GET ALL
  async function loadTasks() {
    isLoading.value = true
    try {
      const { data } = await automationService.listTasks()
      tasks.value = data
    } finally {
      isLoading.value = false
    }
  }

  // GET ONE
  async function loadTask(id) {
    const { data } = await automationService.getTask(id)
    currentTask.value = data
    fillFormFromData(data)
    return data
  }

  // SELECT
  async function selectTask(id) {
    if (!id) return
    return await loadTask(id)
  }

  // CREATE
  async function createTask() {
    const response = await automationService.createTask(buildFormData())
    const data = response.data
    tasks.value.unshift(data)
    currentTask.value = data
    resetForm()
    await loadTasks()
    return response // ✅ FIX
  }

  // UPDATE
  async function updateTask(id) {
    const response = await automationService.updateTask(id, buildFormData())
    const data = response.data
    const idx = tasks.value.findIndex((t) => t.id === id)
    if (idx !== -1) tasks.value[idx] = { ...tasks.value[idx], ...data }
    if (currentTask.value?.id === id) currentTask.value = { ...currentTask.value, ...data }
    await loadTasks()
    return response // ✅ FIX
  }

  // DELETE
  async function deleteTask(id) {
    const response = await automationService.deleteTask(id)
    tasks.value = tasks.value.filter((t) => t.id !== id)
    if (currentTask.value?.id === id) {
      currentTask.value = null
      resetForm()
    }
    return response // ✅ FIX
  }

  // ─────────────────────────────────────────
  // Task Run
  // ─────────────────────────────────────────

  // بيتحدث من الـ workflowStore لما الـ workflow يشتغل
  function setTaskRunId(runId) {
    currentTaskRunId.value = runId
  }

  function clearTaskRunId() {
    currentTaskRunId.value = null
  }

  // ─────────────────────────────────────────
  // Return
  // ─────────────────────────────────────────
  return {
    // state
    tasks,
    currentTask,
    currentTaskId,
    currentTaskRunId,
    isLoading,
    form,

    // ✅ Aliases — عشان AutomationView يشتغل بدون تغيير
    taskRunId: currentTaskRunId, // taskStore.taskRunId
    loading: isLoading, // taskStore.loading

    // getters
    taskById,
    tasksByProgram,

    // helpers
    validateForm,
    buildFormData,
    resetForm,
    fillFormFromData,

    // CRUD
    loadTasks,
    loadTask,
    selectTask,
    createTask,
    updateTask,
    deleteTask,

    // task run
    setTaskRunId,
    clearTaskRunId,
  }
})
