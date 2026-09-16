<template>
  <prime_card class="auth-card">
    <template #title> Login </template>

    <template #content>
      <form @submit.prevent="submitFormLogin">
        <!-- Email -->
        <div class="field">
          <label>Email</label>

          <prime_input_text v-model="formLogin.email" type="email" class="w-full" />
        </div>

        <!-- Password -->
        <div class="field">
          <label>Password</label>

          <prime_input_password
            v-model="formLogin.password"
            :feedback="false"
            toggleMask
            class="w-full"
          />
        </div>

        <!-- Error -->
        <prime_message v-if="error" severity="error">
          {{ error }}
        </prime_message>

        <!-- Login -->
        <prime_button type="submit" label="Login" :loading="loading" class="w-full" />
      </form>

      <prime_divider align="center"> OR </prime_divider>

      <!-- Google -->
      <prime_button
        label="Continue with Google"
        severity="secondary"
        class="w-full mb-2"
        @click="loginWithGoogle"
      />

      <!-- Facebook -->
      <prime_button
        label="Continue with Facebook"
        severity="secondary"
        class="w-full"
        @click="loginWithFacebook"
      />
    </template>
  </prime_card>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { usersAccountsAPI } from '@/services/usersAccounts'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// ===============================
// 🔄 State
// ===============================

const loading = ref(false)
const error = ref(null)

const formLogin = ref({
  email: '',
  password: '',
})

// ===============================
// 🔐 Login
// ===============================

const submitFormLogin = async () => {
  loading.value = true
  error.value = null

  try {
    // 1️⃣ Login
    const response = await usersAccountsAPI.login({
      email: formLogin.value.email,
      password: formLogin.value.password,
    })

    // 2️⃣ Save JWT
    userStore.setToken(response.data)

    // 3️⃣ Get current user
    const userResponse = await usersAccountsAPI.me()

    // 4️⃣ Save user information
    userStore.setUserInfo(userResponse.data)

    // 5️⃣ Redirect
    await router.push('/')
  } catch (err) {
    console.error('❌ Login Error:', err)

    error.value =
      err.response?.data?.detail || err.response?.data?.message || 'Invalid email or password.'
  } finally {
    loading.value = false
  }
}

// ===============================
// 🌐 Google Login
// ===============================

const loginWithGoogle = () => {
  window.open('http://127.0.0.1:8000/accounts/google/login/', '_blank', 'width=500,height=700')
}

// ===============================
// 🌐 Facebook Login
// ===============================

const loginWithFacebook = () => {
  window.location.href = 'http://127.0.0.1:8000/accounts/facebook/login/'
}
</script>

<style lang="scss">
form {
  > div {
    display: block;
    flex-direction: column;
  }
}
</style>
