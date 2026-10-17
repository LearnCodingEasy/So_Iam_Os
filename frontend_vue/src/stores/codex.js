import { defineStore } from 'pinia'
import codex from '@/services/codex'

export const useCodexStore = defineStore('codex', {
  state: () => ({
    overview: null,
    features: [],
    files: [],
    apis: [],
    protected: [],
    changes: [],
    snapshots: [],
    graph: { nodes: [], edges: [] },
    tools: [],
    policy: null,
    audit: [],
    agentRuns: [],
    capabilitySummary: null,
    capabilityHealth: null,
    capabilityFeatures: [],
    capabilityTools: [],
    capabilityAgents: [],
    capabilityRuns: [],
    loading: false,
    brainLoading: false,
    error: null,
    brainError: null,
  }),
  actions: {
    async loadAll() {
      this.loading = true
      this.error = null
      try {
        const [overview, features, files, apis, protectedFeatures, changes, snapshots] =
          await Promise.all([
            codex.overview(),
            codex.features(),
            codex.files(),
            codex.apis(),
            codex.protected(),
            codex.changes(),
            codex.snapshots(),
          ])
        Object.assign(this, {
          overview,
          features,
          files,
          apis,
          protected: protectedFeatures,
          changes,
          snapshots,
        })
      } catch (e) {
        this.error = e?.response?.data || e?.message || 'Codex loading failed'
        throw e
      } finally {
        this.loading = false
      }
    },
    async loadBrain() {
      this.brainLoading = true
      this.brainError = null
      try {
        const [graph, tools, policy, audit, agentRuns] = await Promise.all([
          codex.graph(),
          codex.tools(),
          codex.policy(),
          codex.audit(),
          codex.agentRuns(),
        ])
        Object.assign(this, { graph, tools, policy, audit, agentRuns })
      } catch (e) {
        this.brainError = e?.response?.data || e?.message || 'Codex Project Brain loading failed'
        throw e
      } finally {
        this.brainLoading = false
      }
    },
    async bootstrapBrain() {
      this.brainLoading = true
      this.brainError = null
      try {
        const result = await codex.bootstrap()
        await this.loadBrain()
        return result
      } catch (e) {
        this.brainError = e?.response?.data || e?.message || 'Codex Project Brain bootstrap failed'
        throw e
      } finally {
        this.brainLoading = false
      }
    },
    async loadCapabilities() {
      try {
        const [summary, health, features, tools, agents, runs] = await Promise.all([
          codex.registry.summary(), codex.registry.health(), codex.registry.features(),
          codex.registry.tools(), codex.registry.agents(), codex.registry.runs(),
        ])
        Object.assign(this, { capabilitySummary: summary, capabilityHealth: health, capabilityFeatures: features, capabilityTools: tools, capabilityAgents: agents, capabilityRuns: runs })
      } catch (e) {
        this.error = e?.response?.data || e?.message || 'Codex capability registry loading failed'
        throw e
      }
    },
    async bootstrapCapabilities() {
      const result = await codex.registry.bootstrap()
      await this.loadCapabilities()
      return result
    },
    async scan() {
      const result = await codex.scan()
      await this.loadAll()
      return result
    },
  },
})
