// ===================================================
//  useProgramStore.js
//  src/stores/useProgramStore.js
//
//  المسؤوليات:
//   - CRUD الـ Programs
//   - Image validation و FormData building
//   - Program controls (open / close / focus / maximize / status)
// ===================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import automationService from '@/services/AutomationService'

export const useProgramStore = defineStore('program', () => {
  // ─────────────────────────────────────────
  // State
  // ─────────────────────────────────────────
  const programs = ref([])
  const currentProgram = ref(null)
  const isLoading = ref(false)
  const isScanning = ref(false)

  const form = ref({
    name: '',
    description: '',
    executable_path: '',
    project_path: '',
    working_directory: '',
    window_title_pattern: '',
    image: null, // File | null
  })

  // ─────────────────────────────────────────
  // Getters
  // ─────────────────────────────────────────
  const currentProgramId = computed(() => currentProgram.value?.id ?? null)

  const programById = (id) => programs.value.find((p) => p.id === id) ?? null

  // ─────────────────────────────────────────
  // Validation
  // ─────────────────────────────────────────
  function validateForm(f = form.value) {
    if (!f.name?.trim()) return 'اسم البرنامج مطلوب'
    if (!f.executable_path?.trim()) return 'مسار التنفيذ مطلوب'
    return null // ← null = valid
  }

  function validateImageSize(file, maxMB = 5) {
    if (file && file.size > maxMB * 1024 * 1024) {
      return `الملف كبير جداً — الحد الأقصى ${maxMB}MB`
    }
    return null
  }

  // ─────────────────────────────────────────
  // Helpers
  // ─────────────────────────────────────────
  function buildFormData(f = form.value) {
    const fd = new FormData()
    fd.append('name', f.name)
    fd.append('description', f.description || '')
    fd.append('executable_path', f.executable_path)
    fd.append('project_path', f.project_path || '')
    fd.append('working_directory', f.working_directory || '')
    fd.append('window_title_pattern', f.window_title_pattern || '')
    if (f.image instanceof File) fd.append('image', f.image)
    return fd
  }

  function resetForm() {
    form.value = {
      name: '',
      description: '',
      executable_path: '',
      project_path: '',
      working_directory: '',
      window_title_pattern: '',
      image: null,
    }
  }

  function fillFormFromData(data) {
    form.value = {
      name: data.name ?? '',
      description: data.description ?? '',
      executable_path: data.executable_path ?? '',
      project_path: data.project_path ?? '',
      working_directory: data.working_directory ?? '',
      window_title_pattern: data.window_title_pattern ?? '',
      image: null,
    }
  }

  function onImageChange(event) {
    const file = event.target?.files?.[0]
    if (!file) return null
    const sizeErr = validateImageSize(file)
    if (sizeErr) {
      event.target.value = ''
      return sizeErr
    }
    form.value.image = file
    return null
  }

  // ─────────────────────────────────────────
  // CRUD
  // ─────────────────────────────────────────

  // GET ALL
  async function loadPrograms() {
    isLoading.value = true
    try {
      const { data } = await automationService.listPrograms()
      programs.value = data
    } finally {
      isLoading.value = false
    }
  }

  // GET ONE — وبيملي الـ form
  async function loadProgram(id) {
    const { data } = await automationService.getProgram(id)
    currentProgram.value = data
    fillFormFromData(data)
    return data
  }

  // SELECT — اختار برنامج وحمّل بياناته
  async function selectProgram(id) {
    if (!id) return
    return await loadProgram(id)
  }

  async function createProgram() {
    const response = await automationService.createProgram(buildFormData())
    const data = response.data
    programs.value.unshift(data) // ← optimistic update
    currentProgram.value = data
    resetForm()
    return response
  }

  // UPDATE
  async function updateProgram(id) {
    const response = await automationService.updateProgram(id, buildFormData())
    const data = response.data
    const idx = programs.value.findIndex((p) => p.id === id)
    if (idx !== -1) programs.value[idx] = { ...programs.value[idx], ...data }
    if (currentProgram.value?.id === id) currentProgram.value = { ...currentProgram.value, ...data }
    return response
  }

  // DELETE
  async function deleteProgram(id) {
    const response = await automationService.deleteProgram(id)
    programs.value = programs.value.filter((p) => p.id !== id)
    if (currentProgram.value?.id === id) {
      currentProgram.value = null
      resetForm()
    }
    return response // ← ✅ رجّع الـ response
  }

  // ─────────────────────────────────────────
  // Program Controls
  // ─────────────────────────────────────────
  async function openProgram(id) {
    return (await automationService.openProgram(id)).data
  }
  async function closeProgram(id) {
    return (await automationService.closeProgram(id)).data
  }
  async function focusProgram(id) {
    return (await automationService.focusProgram(id)).data
  }
  async function maximizeProgram(id) {
    return (await automationService.maximizeProgram(id)).data
  }
  async function statusProgram(id) {
    return (await automationService.statusProgram(id)).data
  }
  const openWindows = ref([])

  async function loadOpenWindows() {
    try {
      const res = await automationService.getOpenWindows()
      openWindows.value = res.data.data
      console.log('openWindows.value: ', openWindows.value)
    } catch (err) {
      console.error('WINDOWS ERROR:', err)
    }
  }
  async function scanProgramElements(id, windowTitlePattern = null) {
    isScanning.value = true
    try {
      const res = await automationService.scanProgramElements(id, windowTitlePattern)
      return res.data
    } catch (err) {
      throw err.response?.data || err
    } finally {
      isScanning.value = false
    }
  }

  // ─────────────────────────────────────────
  // Return
  // ─────────────────────────────────────────
  return {
    // state
    programs,
    currentProgram,
    currentProgramId,
    isLoading,
    form,
    // getters
    programById,
    // helpers
    validateForm,
    validateImageSize,
    buildFormData,
    resetForm,
    fillFormFromData,
    onImageChange,
    // CRUD
    loadPrograms,
    loadProgram,
    selectProgram,
    createProgram,
    updateProgram,
    deleteProgram,
    // controls
    openProgram,
    closeProgram,
    focusProgram,
    maximizeProgram,
    statusProgram,
    loadOpenWindows,
    scanProgramElements,
    isScanning,
    openWindows,
  }
})
