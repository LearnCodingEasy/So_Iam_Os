import api from '../Shared/api'
import { domainEndpoints } from '../Shared/endpoints'

const unwrap = (payload) => (Array.isArray(payload) ? payload : payload?.results || [])

export const listProjectsPage = async (params = {}) =>
  (await api.get(domainEndpoints.projects, { params })).data
export const listProjects = async (params = {}) => unwrap(await listProjectsPage(params))
export const getProject = async (id) => (await api.get(`${domainEndpoints.projects}${id}/`)).data
export const createProject = async (payload) =>
  (await api.post(domainEndpoints.projects, payload)).data
export const updateProject = async (id, payload) =>
  (await api.patch(`${domainEndpoints.projects}${id}/`, payload)).data
export const deleteProject = async (id) => {
  await api.delete(`${domainEndpoints.projects}${id}/`)
  return true
}

export default {
  listProjectsPage,
  listProjects,
  getProject,
  createProject,
  updateProject,
  deleteProject,
}
