<template>
  <header class="topbar">
    <div class="topbar-start">
      <button class="mobile-menu" type="button" @click="$emit('toggle-sidebar')" aria-label="فتح القائمة">☰</button>
      <div>
        <h1>{{ pageTitle }}</h1>
        <p>{{ pageDescription }}</p>
      </div>
    </div>

    <div class="topbar-actions">
      <RouterLink class="icon-btn" to="/notifications" title="الإشعارات" aria-label="الإشعارات">♧</RouterLink>
      <button class="icon-btn" type="button" @click="toggleTheme" :title="isDark ? 'الوضع الفاتح' : 'الوضع الداكن'" aria-label="تبديل المظهر">
        {{ isDark ? '☀' : '☾' }}
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

defineEmits(['toggle-sidebar'])
const route = useRoute()
const isDark = ref(false)
const pageTitle = computed(() => route.meta?.title || ({
  dashboard: 'لوحة التحكم', goals: 'الأهداف', 'today-tasks': 'مهام اليوم',
  learning: 'التعلم', knowledge: 'المعرفة', memory: 'الذاكرة', jobs: 'الوظائف',
  projects: 'المشروعات', challenges: 'التحديات', finance: 'المالية',
  'ai-chat': 'المساعد الذكي', automation: 'الأتمتة', settings: 'الإعدادات',
}[String(route.name)] || 'SO_IAM_OS'))
const pageDescription = computed(() => route.meta?.description || 'مساحة العمل الشخصية')

function applyTheme(value) {
  isDark.value = value
  document.documentElement.classList.toggle('p-dark', value)
  document.documentElement.dataset.theme = value ? 'dark' : 'light'
  try { localStorage.setItem('so-iam-os-theme', value ? 'dark' : 'light') } catch { /* storage may be unavailable */ }
}
function toggleTheme() { applyTheme(!isDark.value) }
onMounted(() => {
  let saved = 'light'
  try { saved = localStorage.getItem('so-iam-os-theme') || 'light' } catch { /* ignore */ }
  applyTheme(saved === 'dark')
})
watch(() => route.meta?.theme, (value) => {
  if (value === 'dark') applyTheme(true)
  if (value === 'light') applyTheme(false)
})
</script>
