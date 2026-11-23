import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as challengesApi from '@/services/Challenges/challenges'

// Resource name -> service collection. Every mutation re-reads server state.
const RESOURCES = {
  challenges: challengesApi.challenges,
  steps: challengesApi.steps,
  attempts: challengesApi.attempts,
  progress: challengesApi.progress,
}

export const useChallengesStore = defineStore('challenges', () => {
  const challenges = ref([])
  const attempts = ref([])
  const progress = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function run(fn) {
    loading.value = true
    error.value = null
    try {
      return await fn()
    } catch (cause) {
      error.value = cause
      throw cause
    } finally {
      loading.value = false
    }
  }

  async function fetchAll() {
    return run(async () => {
      const [c, a, p] = await Promise.all([
        challengesApi.challenges.list(),
        challengesApi.attempts.list(),
        challengesApi.progress.list(),
      ])
      challenges.value = c
      attempts.value = a
      progress.value = p
    })
  }

  async function save(resource, payload, id = null) {
    const api = RESOURCES[resource]
    const saved = await run(() => (id ? api.update(id, payload) : api.create(payload)))
    await fetchAll()
    return saved
  }

  async function remove(resource, id) {
    await run(() => RESOURCES[resource].remove(id))
    await fetchAll()
  }

  async function completeStep(id) {
    const row = await run(() => challengesApi.completeStep(id))
    await fetchAll()
    return row
  }

  return { challenges, attempts, progress, loading, error, fetchAll, save, remove, completeStep }
})
