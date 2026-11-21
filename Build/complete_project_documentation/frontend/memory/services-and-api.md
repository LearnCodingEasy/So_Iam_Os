# memory services and API

Service files found under services/Memory. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Memory/memory.js
L3: const data = r => r?.data ?? r
L4: const list = r => Array.isArray(data(r)) ? data(r) : (data(r)?.results || [])
L5: export const memoryApi = { list:()=>api.get(e.memory).then(list), create:p=>api.post(e.memory,p).then(data), update:(id,p)=>api.patch(`${e.memory}${id}/`,p).then(data), remove:id=>api.delete(`${e.memory}${id}/`) }


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
