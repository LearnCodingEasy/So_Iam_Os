# challenges services and API

Service files found under services/Challenges. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Challenges/challenges.js
L3: const data = r => r?.data ?? r
L4: const list = r => Array.isArray(data(r)) ? data(r) : (data(r)?.results || [])
L5: export const challengesApi = { list:()=>api.get(e.challenges).then(list), create:p=>api.post(e.challenges,p).then(data), update:(id,p)=>api.patch(`${e.challenges}${id}/`,p).then(data), remove:id=>api.delete(`${e.challenges}${id}/`) }


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
