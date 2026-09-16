import api from './api'

const API_URL = 'http://127.0.0.1:8000/api'

export const usersAccountsAPI = {
  // ===============================
  // 👤 User Authentication
  // ===============================

  signup(data) {
    return api.post('/users/signup/', data)
  },

  login(data) {
    return api.post('/users/login/', data)
  },

  refresh(refreshToken) {
    return api.post('/users/refresh/', {
      refresh: refreshToken,
    })
  },

  me() {
    return api.get('/users/me/')
  },

  // ===============================
  // 👤 User Profile
  // ===============================

  profile(id) {
    return api.get(`/users/profile/${id}/`)
  },
  editProfile(formData) {
    return api.post('/users/editprofile/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  editPassword(data) {
    return api.post('/users/editpassword/', data)
  },

  // ===============================
  // 🔐 Logout
  // ===============================

  logout() {},
}
