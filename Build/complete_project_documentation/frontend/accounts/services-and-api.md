# accounts services and API

Service files found under services/Accounts. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Accounts/usersAccounts.js
L4: const API_URL = 'http://127.0.0.1:8000/api'
L6: export const usersAccountsAPI = {


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
