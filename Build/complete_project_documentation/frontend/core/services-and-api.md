# core services and API

Service files found under services/Core. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Core/dashboard.js
L4: export const dashboardService = {
L6: const response = await api.get(endpoints.core.dashboard)

## services/Core/settings.js
L2: export const getLearningSettings = async () => (await api.get('/core/learning-settings/')).data
L3: export const updateLearningSettings = async (payload) => (await api.patch('/core/learning-settings/', payload)).data


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
