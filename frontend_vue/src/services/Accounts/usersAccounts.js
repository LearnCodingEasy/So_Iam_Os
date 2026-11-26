import api from '../Shared/api'
import { endpoints } from '../Shared/endpoints'

export const usersAccountsAPI = {
  // ===============================
  // 👤 User Authentication
  // ===============================

  signup(data) {
    return api.post(endpoints.users.signup, data)
  },

  login(data) {
    return api.post(endpoints.users.login, data)
  },

  refresh(refreshToken) {
    return api.post(endpoints.users.refresh, {
      refresh: refreshToken,
    })
  },

  me() {
    return api.get(endpoints.users.me)
  },

  // ===============================
  // 👤 User Profile
  // ===============================

  profile(id) {
    return api.get(endpoints.users.profile(id))
  },
  editProfile(formData) {
    return api.post(endpoints.users.editProfile, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  editPassword(data) {
    return api.post(endpoints.users.editPassword, data)
  },

  // ===============================
  // 🔐 Logout
  // ===============================

  logout() {},
}
