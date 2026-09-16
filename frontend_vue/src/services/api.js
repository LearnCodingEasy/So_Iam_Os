import axios from 'axios'

// ====================================================
// 🌐 API Configuration
// ====================================================

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',

  headers: {
    'Content-Type': 'application/json',
  },
})

// ====================================================
// 🔐 Request Interceptor
// ====================================================

api.interceptors.request.use(
  (config) => {
    // -----------------------------------------------
    // 🔑 Get Access Token
    // -----------------------------------------------

    const accessToken = localStorage.getItem('user.access')

    // -----------------------------------------------
    // 🪪 Attach Authorization Header
    // -----------------------------------------------

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }

    // -----------------------------------------------
    // 🧪 Development Debug
    // -----------------------------------------------

    console.group('🔐 API REQUEST')

    console.log('➡️ Method:', config.method?.toUpperCase())

    console.log('🌐 URL:', `${config.baseURL}${config.url}`)

    console.log('🔑 Has Access Token:', Boolean(accessToken))

    console.log(
      '🪪 Authorization:',
      config.headers.Authorization ? 'Bearer ********' : '❌ Missing',
    )

    console.log('📦 Request Headers:', config.headers)

    console.groupEnd()

    return config
  },

  (error) => {
    console.error('❌ Request Interceptor Error:', error)

    return Promise.reject(error)
  },
)

// ====================================================
// 📥 Response Interceptor
// ====================================================

api.interceptors.response.use(
  (response) => {
    // -----------------------------------------------
    // 🟢 Successful Response
    // -----------------------------------------------

    console.group('📥 API RESPONSE')

    console.log('✅ Status:', response.status)

    console.log('🌐 URL:', response.config.url)

    console.log('📦 Data:', response.data)

    console.groupEnd()

    return response
  },

  (error) => {
    // -----------------------------------------------
    // ❌ Error Response
    // -----------------------------------------------

    console.group('🚨 API ERROR')

    console.log('❌ Status:', error.response?.status)

    console.log('🌐 URL:', error.config?.url)

    console.error('📦 Response:', JSON.stringify(error.response?.data, null, 2))

    console.log('📋 Headers:', error.response?.headers)

    console.groupEnd()

    // -----------------------------------------------
    // 🔐 Unauthorized
    // -----------------------------------------------

    if (error.response?.status === 401) {
      console.warn('🔐 Access Token Unauthorized')

      // ⚠️ مهم:
      // لا تمسح user.access هنا حاليًا
      // لأننا سنعمل Refresh Token mechanism
      // بعد التأكد من المشكلة الأساسية.
    }

    // -----------------------------------------------
    // 🚫 Forbidden
    // -----------------------------------------------

    if (error.response?.status === 403) {
      console.warn('🚫 Forbidden')

      console.warn('⚠️ Django رفض الطلب. افحص Authorization + JWT Authentication.')
    }

    return Promise.reject(error)
  },
)

export default api
