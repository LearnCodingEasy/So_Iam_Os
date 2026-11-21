import api from '@/services/Shared/api'
import { domainEndpoints as e } from '@/services/Shared/endpoints'
const data = r => r?.data ?? r
const list = r => Array.isArray(data(r)) ? data(r) : (data(r)?.results || [])
export const memoryApi = { list:()=>api.get(e.memory).then(list), create:p=>api.post(e.memory,p).then(data), update:(id,p)=>api.patch(`${e.memory}${id}/`,p).then(data), remove:id=>api.delete(`${e.memory}${id}/`) }
