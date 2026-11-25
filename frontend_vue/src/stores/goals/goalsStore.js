import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as goalApi from '@/services/Goals/goals'

export const useGoalsStore = defineStore('goals', () => {
  const items = ref([])
  const analytics = ref(null)
  const count = ref(0)
  const next = ref(null)
  const previous = ref(null)
  const loading = ref(false)
  const analyticsLoading = ref(false)
  const error = ref(null)

  async function fetchGoals(params = {}) {
    loading.value = true
    error.value = null
    try {
      const pageData = await goalApi.listGoalsPage(params)
      items.value = Array.isArray(pageData) ? pageData : pageData?.results || []
      count.value = pageData?.count ?? items.value.length
      next.value = pageData?.next ?? null
      previous.value = pageData?.previous ?? null
      return items.value
    } catch (cause) {
      error.value = cause
      throw cause
    } finally {
      loading.value = false
    }
  }

  async function fetchAnalytics() {
    analyticsLoading.value = true
    try {
      analytics.value = await goalApi.getGoalAnalytics()
      return analytics.value
    } finally {
      analyticsLoading.value = false
    }
  }

  async function refresh() {
    await Promise.all([fetchGoals(), fetchAnalytics()])
  }

  return {
    items,
    analytics,
    count,
    next,
    previous,
    loading,
    analyticsLoading,
    error,
    fetchGoals,
    fetchAnalytics,
    refresh,
  }
})
