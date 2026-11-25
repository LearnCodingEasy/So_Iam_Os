import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as projectsApi from '@/services/Projects/projects'

export const useProjectsStore = defineStore('projects', () => {
  const items = ref([])
  const count = ref(0)
  const next = ref(null)
  const previous = ref(null)
  const loading = ref(false)
  const saving = ref(false)
  const error = ref(null)

  async function fetchProjects(params = {}) {
    loading.value = true
    error.value = null
    try {
      const page = await projectsApi.listProjectsPage(params)
      items.value = Array.isArray(page) ? page : page?.results || []
      count.value = page?.count ?? items.value.length
      next.value = page?.next ?? null
      previous.value = page?.previous ?? null
      return items.value
    } catch (cause) {
      error.value = cause
      throw cause
    } finally {
      loading.value = false
    }
  }

  async function getProject(id) {
    return projectsApi.getProject(id)
  }

  async function createProject(payload) {
    saving.value = true
    try {
      const item = await projectsApi.createProject(payload)
      items.value = [item, ...items.value]
      count.value += 1
      return item
    } finally {
      saving.value = false
    }
  }

  async function updateProject(id, payload) {
    saving.value = true
    try {
      const item = await projectsApi.updateProject(id, payload)
      items.value = items.value.map((row) => (String(row.id) === String(id) ? item : row))
      return item
    } finally {
      saving.value = false
    }
  }

  async function deleteProject(id) {
    await projectsApi.deleteProject(id)
    items.value = items.value.filter((row) => String(row.id) !== String(id))
    count.value = Math.max(0, count.value - 1)
  }

  return {
    items,
    count,
    next,
    previous,
    loading,
    saving,
    error,
    fetchProjects,
    getProject,
    createProject,
    updateProject,
    deleteProject,
  }
})
