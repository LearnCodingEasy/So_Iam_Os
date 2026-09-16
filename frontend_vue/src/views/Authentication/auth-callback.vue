<template>
  <div class="auth-callback">
    <h1>جاري تسجيل الدخول...</h1>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AuthCallback',
  async mounted() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/user/', {
        withCredentials: true,
      })
      console.log('✅ User Data:', response.data)
      this.$router.push('/dashboard')
    } catch (error) {
      console.error('❌ Login failed:', error)
      this.$router.push('/login')
    }
  },
}
</script>
