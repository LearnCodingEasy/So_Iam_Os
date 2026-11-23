import api from '@/services/Shared/api'

// Paths are relative to the axios base URL (".../api"). Mirrors architecture/api/urls.py.
const BASE = '/architecture'
export const architectureEndpoints = {
  architectures: `${BASE}/architectures/`,
  components: `${BASE}/components/`,
  dependencies: `${BASE}/dependencies/`,
  decisions: `${BASE}/decisions/`,
}

const data = (r) => r?.data ?? r
const asList = (r) => {
  const d = data(r)
  return Array.isArray(d) ? d : d?.results || []
}

function resource(url) {
  return {
    list: (params = {}) => api.get(url, { params }).then(asList),
    create: (payload) => api.post(url, payload).then(data),
    update: (id, payload) => api.patch(`${url}${id}/`, payload).then(data),
    remove: (id) => api.delete(`${url}${id}/`),
  }
}

const architectures = resource(architectureEndpoints.architectures)
export const listArchitectures = architectures.list
export const createArchitecture = architectures.create
export const updateArchitecture = architectures.update
export const deleteArchitecture = architectures.remove
export const getArchitectureGraph = (id) =>
  api.get(`${architectureEndpoints.architectures}${id}/graph/`).then(data)

const components = resource(architectureEndpoints.components)
export const listComponents = components.list
export const createComponent = components.create
export const updateComponent = components.update
export const deleteComponent = components.remove

const dependencies = resource(architectureEndpoints.dependencies)
export const listDependencies = dependencies.list
export const createDependency = dependencies.create
export const updateDependency = dependencies.update
export const deleteDependency = dependencies.remove

const decisions = resource(architectureEndpoints.decisions)
export const listDecisions = decisions.list
export const createDecision = decisions.create
export const updateDecision = decisions.update
export const deleteDecision = decisions.remove
