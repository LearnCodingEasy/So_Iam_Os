<template>
  <form @submit.prevent="submitFormSignup">
    <prime_card class="prime_card_form_signup">
      <!-- =============================== -->
      <!-- Header -->
      <!-- =============================== -->

      <template #header>
        <div class="flex justify-between items-center w-full">
          <div class="text font-bold text-5xl">Signup</div>

          <!--
          <img
            src="@/assets/Images/Messenger_80x80.png"
            alt="logo"
          />
          -->
        </div>
      </template>

      <!-- =============================== -->
      <!-- Content -->
      <!-- =============================== -->

      <template #content>
        <prime_fluid class="prime_card_form_signup_content">
          <!-- Name -->
          <div class="flex gap-2">
            <prime_input_text placeholder="First name" v-model="formSignup.name" />

            <prime_input_text placeholder="Surname" v-model="formSignup.surname" />
          </div>

          <!-- Email -->
          <prime_input_text placeholder="Email" v-model="formSignup.email" />

          <!-- Password -->
          <prime_input_password placeholder="Password" v-model="formSignup.password1" />

          <!-- Repeat Password -->
          <prime_input_password placeholder="Repeat Password" v-model="formSignup.password2" />

          <!-- Date of Birth -->
          <div>Date of birth</div>

          <div class="flex gap-2">
            <prime_date_picker v-model="day" view="day" dateFormat="dd" />

            <prime_date_picker v-model="month" view="month" dateFormat="mm" />

            <prime_date_picker v-model="year" view="year" dateFormat="yy" />
          </div>

          <!-- Gender -->
          <div>Gender</div>

          <div class="flex gap-2 gender">
            <prime_radio_button v-model="formSignup.gender" inputId="female" value="female" />

            <label for="female"> Female </label>

            <prime_radio_button v-model="formSignup.gender" inputId="male" value="male" />

            <label for="male"> Male </label>

            <prime_radio_button v-model="formSignup.gender" inputId="custom" value="custom" />

            <label for="custom"> Custom </label>
          </div>

          <!-- Errors -->
          <prime_message v-if="errorsSignup.length" severity="error" class="mt-3">
            <ul>
              <li v-for="(error, index) in errorsSignup" :key="index">
                {{ error }}
              </li>
            </ul>
          </prime_message>
        </prime_fluid>
      </template>

      <!-- =============================== -->
      <!-- Footer -->
      <!-- =============================== -->

      <template #footer>
        <prime_button type="submit" label="Signup" :loading="loading" class="w-full" />
      </template>
    </prime_card>
  </form>
</template>

<script setup>
import { ref } from 'vue'

import { usersAccountsAPI } from '@/services/usersAccounts'

// ===============================
// 🔄 Form State
// ===============================

const formSignup = ref({
  name: '',
  surname: '',
  email: '',
  date_of_birth: '',
  gender: '',
  password1: '',
  password2: '',
})

// ===============================
// 📅 Date State
// ===============================

const day = ref('')
const month = ref('')
const year = ref('')

// ===============================
// ⚠️ State
// ===============================

const errorsSignup = ref([])
const loading = ref(false)

// ===============================
// 📝 Signup
// ===============================

const submitFormSignup = async () => {
  errorsSignup.value = []

  // ===============================
  // 📅 Format Date
  // ===============================

  if (day.value && month.value && year.value) {
    formSignup.value.date_of_birth = `${year.value.getFullYear()}-${String(
      month.value.getMonth() + 1,
    ).padStart(2, '0')}-${String(day.value.getDate()).padStart(2, '0')}`
  } else {
    errorsSignup.value.push('Date of birth is missing')
  }

  // ===============================
  // 🔎 Required Fields
  // ===============================

  if (!formSignup.value.name || !formSignup.value.email || !formSignup.value.password1) {
    errorsSignup.value.push('Please fill all required fields')
  }

  // ===============================
  // 🔐 Password Confirmation
  // ===============================

  if (formSignup.value.password1 !== formSignup.value.password2) {
    errorsSignup.value.push('Passwords do not match')
  }

  // ===============================
  // ❌ Validation Failed
  // ===============================

  if (errorsSignup.value.length > 0) {
    return
  }

  // ===============================
  // 🚀 Send Request
  // ===============================

  loading.value = true

  try {
    const response = await usersAccountsAPI.signup({
      name: formSignup.value.name,
      surname: formSignup.value.surname,
      email: formSignup.value.email,
      date_of_birth: formSignup.value.date_of_birth,
      gender: formSignup.value.gender,
      password1: formSignup.value.password1,
      password2: formSignup.value.password2,
    })

    console.log('✅ Signup response:', response.data)

    // ===============================
    // ✅ Success
    // ===============================

    if (response.data.message === 'success') {
      alert('User registered successfully. Check your email to activate your account.')

      // Reset form
      formSignup.value = {
        name: '',
        surname: '',
        email: '',
        date_of_birth: '',
        gender: '',
        password1: '',
        password2: '',
      }

      day.value = ''
      month.value = ''
      year.value = ''
    }
  } catch (err) {
    console.error('❌ Signup Error:', err)

    // ===============================
    // Django / DRF Errors
    // ===============================

    if (err.response?.data) {
      const data = err.response.data

      if (typeof data === 'object') {
        errorsSignup.value = Object.entries(data).flatMap(([field, messages]) => {
          if (Array.isArray(messages)) {
            return messages.map((message) => `${field}: ${message}`)
          }

          return `${field}: ${messages}`
        })
      } else {
        errorsSignup.value = [String(data)]
      }
    } else {
      errorsSignup.value = ['Unable to connect to the server.']
    }
  } finally {
    loading.value = false
  }
}
</script>
