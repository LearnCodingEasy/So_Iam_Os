import api from '@/services/Shared/api'
import { domainEndpoints as e } from '@/services/Shared/endpoints'
const data = r => r?.data ?? r
const list = r => Array.isArray(data(r)) ? data(r) : (data(r)?.results || [])
export const challengesApi = { list:()=>api.get(e.challenges).then(list), create:p=>api.post(e.challenges,p).then(data), update:(id,p)=>api.patch(`${e.challenges}${id}/`,p).then(data), remove:id=>api.delete(`${e.challenges}${id}/`) }
