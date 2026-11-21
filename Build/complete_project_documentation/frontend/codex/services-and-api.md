# codex services and API

Service files found under services/Codex. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Codex/codex.js
L4: const list = (data) =>
L7: const data = async (request) => (await request).data


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
