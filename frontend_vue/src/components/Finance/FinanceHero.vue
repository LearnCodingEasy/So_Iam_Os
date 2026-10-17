<template>
  <header class="hero">
    <div class="hero-copy">
      <span class="eyebrow">
        SO_IAM_OS · PERSONAL FINANCE OS
      </span>

      <h1>مركز القيادة المالية 🧠💰</h1>

      <p>
        لوحة مالية حقيقية متصلة بـ Django REST API،
        تعرض بيانات المستخدم وتسمح بإدارتها مباشرة من الواجهة.
      </p>
    </div>

    <div class="hero-actions">
      <Button
        label="تحديث"
        icon="pi pi-refresh"
        :loading="loading"
        @click="$emit('refresh')"
      />

      <Button
        label="فحص APIs"
        icon="pi pi-bolt"
        severity="secondary"
        outlined
        :loading="apiChecking"
        @click="$emit('check-apis')"
      />

      <Button
        label="إضافة معاملة"
        icon="pi pi-plus"
        severity="success"
        @click="$emit('add-transaction')"
      />
    </div>
  </header>
</template>

<script setup>
import Button from 'primevue/button'

defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
  apiChecking: {
    type: Boolean,
    default: false,
  },
})

defineEmits([
  'refresh',
  'check-apis',
  'add-transaction',
])
</script>
