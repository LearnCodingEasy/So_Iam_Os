import api from '@/services/api'
import { endpoints } from '@/services/endpoints'

const list = (data) =>
  Array.isArray(data) ? data : Array.isArray(data?.results) ? data.results : []

const data = async (request) => (await request).data

export default {
  buildWorkspace: async () => data(api.get(endpoints.codex.buildWorkspace)),
  generateBuildManifest: async () => data(api.post(endpoints.codex.buildManifest)),
  overview: async () => data(api.get(endpoints.codex.overview)),
  scan: async () => data(api.post(endpoints.codex.scan)),
  context: async () => data(api.get(endpoints.codex.context)),
  projects: async () => list(await data(api.get(endpoints.codex.projects))),
  features: async () => list(await data(api.get(endpoints.codex.features))),
  files: async () => list(await data(api.get(endpoints.codex.files))),
  apis: async () => list(await data(api.get(endpoints.codex.apis))),
  protected: async () => list(await data(api.get(endpoints.codex.protected))),
  changes: async () => list(await data(api.get(endpoints.codex.changes))),
  snapshots: async () => list(await data(api.get(endpoints.codex.snapshots))),
  planChange: async (payload) => data(api.post(endpoints.codex.planChange, payload)),
  createSnapshot: async (payload) => data(api.post(endpoints.codex.createSnapshot, payload)),
  async askOpenAI(message, paths = []) {
    // Preserve selected-file context all the way to Django so Codex can reason
    // about the actual source files instead of receiving only their paths.
    return data(api.post(endpoints.codex.ai, { message, paths }))
  },

  // Codex V2 — Project Brain / Intelligence
  bootstrap: async () => data(api.post(endpoints.codex.intelligence.bootstrap)),
  search: async (query, limit = 50) =>
    data(api.get(endpoints.codex.intelligence.search, { params: { q: query, limit } })),
  graph: async () => data(api.get(endpoints.codex.intelligence.graph)),
  rebuildGraph: async () => data(api.post(endpoints.codex.intelligence.graph)),
  impact: async (query) => data(api.post(endpoints.codex.intelligence.impact, { query })),
  security: async () => data(api.get(endpoints.codex.intelligence.security)),
  runSecurityScan: async () => data(api.post(endpoints.codex.intelligence.security)),
  duplicates: async () => data(api.post(endpoints.codex.intelligence.duplicates)),
  review: async (path) => data(api.post(endpoints.codex.intelligence.review, { path })),
  testPlan: async (target) => data(api.post(endpoints.codex.intelligence.testPlan, { target })),

  // Safe Agent / Governance
  agentPlan: async (request) => data(api.post(endpoints.codex.agent.plan, { request })),
  agentRuns: async () => list(await data(api.get(endpoints.codex.agent.runs))),
  policy: async () => data(api.get(endpoints.codex.policy)),
  updatePolicy: async (permissions) => data(api.patch(endpoints.codex.policy, { permissions })),
  tools: async () => list(await data(api.get(endpoints.codex.tools))),
  audit: async () => list(await data(api.get(endpoints.codex.audit))),
  commands: async () => data(api.get(endpoints.codex.commands)),
  runCommand: async (key) => data(api.post(endpoints.codex.commands, { key, confirm: true })),
  automationIntent: async (intent) => data(api.post(endpoints.codex.automationIntent, { intent })),

  // Explain / debug / documentation
  explain: async (query) => data(api.post(endpoints.codex.intelligence.explain, { query })),
  debug: async (error) => data(api.post(endpoints.codex.intelligence.debug, { error })),
  documentation: async (target) => data(api.post(endpoints.codex.intelligence.docs, { target })),

  // Protected execution workflow
  applyChanges: async (payload) => data(api.post(endpoints.codex.changesApply, payload)),
  rollback: async (changesetId, confirm = true) =>
    data(api.post(endpoints.codex.rollback(changesetId), { confirm })),
  registry: {
    features: async (params = {}) => list(await data(api.get(endpoints.codex.registry.features, { params }))),
    tools: async (params = {}) => list(await data(api.get(endpoints.codex.registry.tools, { params }))),
    agents: async (params = {}) => list(await data(api.get(endpoints.codex.registry.agents, { params }))),
    summary: async () => data(api.get(endpoints.codex.registry.summary)),
    health: async () => data(api.get(endpoints.codex.registry.health)),
    bootstrap: async () => data(api.post(endpoints.codex.registry.bootstrap)),
    validate: async () => data(api.post(endpoints.codex.registry.validate)),
    runs: async () => list(await data(api.get(endpoints.codex.registry.runs))),
    executeTool: async (key, payload = {}) => data(api.post(endpoints.codex.registry.toolExecute(key), payload)),
    executeAgent: async (key, payload = {}) => data(api.post(endpoints.codex.registry.agentExecute(key), payload)),
  },
  exportContext: async (params = {}) => data(api.get(endpoints.codex.contextExport, { params })),
  fileContent: async (id) => data(api.get(endpoints.codex.fileContent(id))),
  filesContext: async (paths) => data(api.post(endpoints.codex.filesContext, { paths })),
  protectedItems: async () => list(await data(api.get(endpoints.codex.governance.protectedItems))),
  freezeProtectedItem: async (payload) => data(api.post(endpoints.codex.governance.protectedItems, payload)),
  generateManifest: async () => data(api.post(endpoints.codex.governance.manifest)),
  workflow: async () => data(api.get(endpoints.codex.workflow)),
  bootstrapWorkflow: async () => data(api.post(endpoints.codex.workflow)),
  localAIJobs: async () => list(await data(api.get(endpoints.codex.localAI.jobs))),
  createLocalAIJob: async (task_type, input_data = {}) =>
    data(api.post(endpoints.codex.localAI.jobs, { task_type, input_data })),
  localAIJob: async (id) => data(api.get(endpoints.codex.localAI.job(id))),
  generatePrompt: async (prompt_type, goal, paths = []) =>
    data(api.post(endpoints.codex.prompts, { prompt_type, goal, paths })),
  markdownNavigation: async (path = '') =>
    data(api.post(endpoints.codex.markdownNavigation, { path })),
  openLocalFile: async (path) => data(api.post(endpoints.codex.openLocalFile, { path })),
  architectureAnalyze: async (path) => data(api.post(endpoints.codex.architectureAnalyze, { path })),

}
