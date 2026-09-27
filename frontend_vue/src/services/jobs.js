import api from './api'
import { endpoints } from './endpoints'
const list = (data) => (Array.isArray(data) ? data : data?.results || [])
export const listJobs = async (params={}) => list((await api.get(endpoints.jobs.opportunities,{params})).data)
export const createJob = async (payload) => (await api.post(endpoints.jobs.opportunities,payload)).data
export const updateJob = async (id,payload) => (await api.patch(endpoints.jobs.opportunity(id),payload)).data
export const deleteJob = async (id) => { await api.delete(endpoints.jobs.opportunity(id)); return true }
export const refreshJobMatch = async (id) => (await api.post(endpoints.jobs.refreshMatch(id))).data
export const listMatches = async (params={}) => list((await api.get(endpoints.jobs.matches,{params})).data)
export const refreshMatches = async () => list((await api.post(endpoints.jobs.refreshMatches)).data)
export const applyToJob = async (id,payload={}) => (await api.post(endpoints.jobs.apply(id),payload)).data
export const listSources = async () => list((await api.get(endpoints.jobs.sources)).data)
export const createSource = async (payload) => (await api.post(endpoints.jobs.sources,payload)).data
export const updateSource = async (id,payload) => (await api.patch(endpoints.jobs.source(id),payload)).data
export const deleteSource = async (id) => { await api.delete(endpoints.jobs.source(id)); return true }
export const testSource = async (id) => (await api.post(endpoints.jobs.sourceTest(id))).data
