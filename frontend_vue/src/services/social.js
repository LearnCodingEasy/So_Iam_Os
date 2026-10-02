import api from './api'
import { endpoints } from './endpoints'
const dataOf = (r) => r?.data?.results ?? r?.data ?? []
export const getSocialProfile = async () => dataOf(await api.get(endpoints.social.profile))
export const updateSocialProfile = async (payload) => dataOf(await api.patch(endpoints.social.profile, payload))
export const getRecommendations = async (params = {}) => dataOf(await api.get(endpoints.social.recommendations, { params }))
export const sendFriendRequest = async (id) => dataOf(await api.post(endpoints.social.request(id)))
