# finance services and API

Service files found under services/Finance. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Finance/finance.js
L3: const data = r => r?.data ?? r
L4: const list = r => Array.isArray(data(r)) ? data(r) : (data(r)?.results || [])
L5: export const financeApi = {


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
