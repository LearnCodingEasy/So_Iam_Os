# social services and API

Service files found under services/Social. Endpoint ownership and payload compatibility require tracing against backend URLs/views/serializers; this source inventory does not imply successful requests.


## services/Social/social.js
L3: const dataOf = (r) => r?.data?.results ?? r?.data ?? []
L4: export const getSocialProfile = async () => dataOf(await api.get(endpoints.social.profile))
L5: export const updateSocialProfile = async (payload) => dataOf(await api.patch(endpoints.social.profile, payload))
L6: export const getRecommendations = async (params = {}) => dataOf(await api.get(endpoints.social.recommendations, { params }))
L7: export const sendFriendRequest = async (id) => dataOf(await api.post(endpoints.social.request(id)))


Shared endpoint registry: frontend_vue/src/services/Shared/endpoints.js. Backend mount: backend_django/backend_django/urls.py. See project [API catalog](../../05-complete-api-catalog.md).
