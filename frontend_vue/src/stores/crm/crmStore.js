import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as crmApi from '@/services/CRM/CRM'

export const useCrmStore = defineStore('crm', () => {
  const companies = ref([])
  const contacts = ref([])
  const interactions = ref([])
  const relationships = ref([])
  const followUps = ref([])
  const pipeline = ref({ total: 0, stages: {} })
  const loading = ref(false)
  const error = ref(null)

  async function run(task) {
    loading.value = true
    error.value = null
    try {
      return await task()
    } catch (cause) {
      error.value = cause
      throw cause
    } finally {
      loading.value = false
    }
  }

  const fetchContacts = (params = {}) =>
    run(async () => (contacts.value = await crmApi.contacts.list(params)))
  const fetchCompanies = () => run(async () => (companies.value = await crmApi.companies.list()))
  const fetchInteractions = (params = {}) =>
    run(async () => (interactions.value = await crmApi.interactions.list(params)))
  const fetchRelationships = (params = {}) =>
    run(async () => (relationships.value = await crmApi.relationships.list(params)))
  const fetchFollowUps = (days = 7) =>
    run(async () => (followUps.value = await crmApi.listFollowUps(days)))
  const fetchPipeline = () => run(async () => (pipeline.value = await crmApi.getPipeline()))

  async function refresh() {
    await Promise.all([
      fetchContacts(),
      fetchCompanies(),
      fetchInteractions(),
      fetchRelationships(),
      fetchFollowUps(),
      fetchPipeline(),
    ])
  }

  // Generic mutations; the list is reloaded from the server so the UI never shows unsaved state.
  const api = { contacts: crmApi.contacts, companies: crmApi.companies, interactions: crmApi.interactions, relationships: crmApi.relationships }
  const reload = {
    contacts: () => fetchContacts(),
    companies: fetchCompanies,
    interactions: () => fetchInteractions(),
    relationships: async () => {
      await fetchRelationships()
      await fetchPipeline()
    },
  }

  async function save(resource, payload, id = null) {
    const saved = await run(() => (id ? api[resource].update(id, payload) : api[resource].create(payload)))
    await reload[resource]()
    if (resource === 'interactions') await fetchFollowUps()
    return saved
  }

  async function remove(resource, id) {
    await run(() => api[resource].remove(id))
    await reload[resource]()
    if (resource === 'contacts') await Promise.all([fetchInteractions(), fetchRelationships(), fetchPipeline(), fetchFollowUps()])
    if (resource === 'interactions') await fetchFollowUps()
  }

  return {
    companies, contacts, interactions, relationships, followUps, pipeline, loading, error,
    fetchContacts, fetchCompanies, fetchInteractions, fetchRelationships, fetchFollowUps, fetchPipeline,
    refresh, save, remove,
  }
})
