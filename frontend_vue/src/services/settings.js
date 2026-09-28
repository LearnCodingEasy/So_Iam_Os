import api from './api'
export const getLearningSettings = async () => (await api.get('/core/learning-settings/')).data
export const updateLearningSettings = async (payload) => (await api.patch('/core/learning-settings/', payload)).data
