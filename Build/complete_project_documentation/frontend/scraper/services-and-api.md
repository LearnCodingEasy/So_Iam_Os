# scraper services and API

Service files found under services/Scraper. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Scraper/scraperApi.js
L4: const unwrap = (response) => response.data
L5: const list = (response) => {
L6: const data = response.data
L10: export const scraperApi = {


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
