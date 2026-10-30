<template>
  <div class="auth-callback">
    <h1>جاري تسجيل الدخول...</h1>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'AuthCallback',
  async mounted() {
    try {
      const response = await api.get('/users/me/')
      this.$router.push('/dashboard')
    } catch (error) {
      console.error('❌ Login failed:', error)
      this.$router.push('/login')
    }
  },
}
</script>
