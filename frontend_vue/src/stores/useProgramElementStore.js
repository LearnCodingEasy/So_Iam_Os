// ============================================================
//  useProgramElementStore.js
//  src/stores/useProgramElementStore.js
//
//  المسؤوليات:
//   - CRUD الـ Program Elements
//   - Image validation و FormData building
//   - Selector types
// ============================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import automationService from '@/services/AutomationService'

export const useProgramElementStore = defineStore('programElement', () => {
  // ─────────────────────────────────────────
  // State
  // ─────────────────────────────────────────
  const elements = ref([])
  const currentElement = ref(null)
  const isLoading = ref(false)

  const form = ref({
    name: '',
    description: '',
    image: null, // File | null
    program: null, // FK id
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

  // ─────────────────────────────────────────
  // Constants
  // ─────────────────────────────────────────
  const SELECTOR_TYPES = [
    { label: 'Image Recognition', value: 'image' },
    { label: 'Screen Coordinates', value: 'coords' },
    { label: 'Text OCR', value: 'text' },
    { label: 'UI Automation', value: 'ui' },
  ]

  // ─────────────────────────────────────────
  // Getters
  // ─────────────────────────────────────────
  const currentElementId = computed(() => currentElement.value?.id ?? null)

  const elementById = (id) => elements.value.find((e) => e.id === id) ?? null

  // عناصر برنامج معين بس
  const elementsByProgram = (programId) => elements.value.filter((e) => e.program === programId)

  // ─────────────────────────────────────────
  // Validation
  // ─────────────────────────────────────────
  function validateForm(f = form.value) {
    if (!f.name?.trim()) return 'الاسم مطلوب'
    if (!f.program) return 'لازم تختار برنامج'
    if (!f.selector_type) return 'لازم تختار Selector Type'
    return null
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
    fd.append('program', f.program)
    fd.append('element_type', f.element_type)
    fd.append('selector_type', f.selector_type)
    fd.append('selector_value', f.selector_value)
    fd.append('x', Number(f.x))
    fd.append('y', Number(f.y))
    fd.append('width', Number(f.width))
    fd.append('height', Number(f.height))
    fd.append('shortcut', f.shortcut || '')
    fd.append('confidence', parseFloat(f.confidence) || 0)
    if (f.image instanceof File) fd.append('image', f.image)
    return fd
  }

  function resetForm(defaultProgramId = null) {
    form.value = {
      name: '',
      description: '',
      image: null,
      program: defaultProgramId,
      element_type: 'button',
      selector_type: null,
      selector_value: 'xpath',
      x: 0,
      y: 0,
      width: 0,
      height: 0,
      shortcut: '',
      confidence: 0,
    }
  }

  function fillFormFromData(data) {
    form.value = {
      name: data.name ?? '',
      description: data.description ?? '',
      program: data.program ?? null,
      element_type: data.element_type ?? 'button',
      selector_type: data.selector_type ?? null,
      selector_value: data.selector_value ?? 'xpath',
      x: data.x ?? 0,
      y: data.y ?? 0,
      width: data.width ?? 0,
      height: data.height ?? 0,
      shortcut: data.shortcut ?? '',
      confidence: data.confidence ?? 0,
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
  async function loadElements() {
    isLoading.value = true
    try {
      const { data } = await automationService.listProgramElements()
      elements.value = data
    } finally {
      isLoading.value = false
    }
  }

  // GET ONE — وبيملي الـ form
  async function loadElement(id) {
    const { data } = await automationService.getProgramElement(id)
    currentElement.value = data
    fillFormFromData(data)
    return data
  }

  // SELECT
  async function selectElement(id) {
    if (!id) return
    return await loadElement(id)
  }

  // CREATE
  async function createElement() {
    const response = await automationService.createProgramElement(buildFormData())
    const data = response.data
    elements.value.unshift(data)
    currentElement.value = data
    return response // ✅ FIX: رجّع response مش data
  }

  // UPDATE
  async function updateElement(id) {
    const response = await automationService.updateProgramElement(id, buildFormData())
    const data = response.data
    const idx = elements.value.findIndex((e) => e.id === id)
    if (idx !== -1) elements.value[idx] = { ...elements.value[idx], ...data }
    if (currentElement.value?.id === id) currentElement.value = { ...currentElement.value, ...data }
    return response // ✅ FIX
  }

  // DELETE
  async function deleteElement(id) {
    const response = await automationService.deleteProgramElement(id)
    elements.value = elements.value.filter((e) => e.id !== id)
    if (currentElement.value?.id === id) {
      currentElement.value = null
      resetForm()
    }
    return response // ✅ FIX
  }

  // ─────────────────────────────────────────
  // Return
  // ─────────────────────────────────────────
  return {
    // state
    elements,
    currentElement,
    currentElementId,
    isLoading,
    form,

    // constants
    SELECTOR_TYPES,

    // getters
    elementById,
    elementsByProgram,

    // helpers
    validateForm,
    validateImageSize,
    buildFormData,
    resetForm,
    fillFormFromData,
    onImageChange,

    // CRUD
    loadElements,
    loadElement,
    selectElement,
    createElement,
    updateElement,
    deleteElement,
  }
})
