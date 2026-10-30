<template>
  <div class="flex justify-center items-center h-screen">
    <p class="text-lg font-bold">جارٍ تسجيل الدخول...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

onMounted(async () => {
  const access = route.query.access
  const refresh = route.query.refresh

  if (access && refresh) {
    // تخزين التوكن
    userStore.setToken({ access, refresh })
    // تخزين بيانات المستخدم
    const userData = {
      id: route.query.user_id,
      name: route.query.name,
      surname: route.query.surname,
      email: route.query.email,
      get_avatar: route.query.avatar,
    }
    userStore.setUserInfo(userData)

    // إضافة الـ access token في headers الافتراضية
    axios.defaults.headers.common['Authorization'] = `Bearer ${access}`

    // توجيه المستخدم للصفحة الرئيسية
    router.push('/')
  } else {
    router.push('/login')
  }
})
</script>
