<template>
  <div class="ai-status-indicator" :data-status="status">
    <span class="dot" />
    <span>{{ label }}</span>
    <small v-if="provider">{{ provider }}</small>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import api from '@/services/Shared/api'

defineProps({
  provider: { type: String, default: '' },
  pollMs: { type: Number, default: 30000 },
})

const status = ref('checking')
let timer = null

const label = computed(
  () =>
    ({
      connected: 'متصل',
      processing: 'جاري المعالجة',
      disconnected: 'الخادم غير متاح',
      error: 'خطأ',
      checking: 'جاري الفحص',
    })[status.value] || status.value,
)

async function check() {
  try {
    await api.get('/health/', { timeout: 5000 })
    status.value = 'connected'
  } catch (error) {
    status.value = error?.response ? 'error' : 'disconnected'
  }
}

onMounted(() => {
  check()
  timer = window.setInterval(check, 30000)
})
onBeforeUnmount(() => timer && window.clearInterval(timer))
</script>

<style scoped>
.ai-status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
}
.dot {
  width: 0.6rem;
  height: 0.6rem;
  border-radius: 50%;
  background: currentColor;
}
.ai-status-indicator[data-status='connected'] {
  color: #16a34a;
}
.ai-status-indicator[data-status='processing'] {
  color: #ca8a04;
}
.ai-status-indicator[data-status='error'],
.ai-status-indicator[data-status='disconnected'] {
  color: #dc2626;
}
.ai-status-indicator[data-status='checking'] {
  color: #64748b;
}
small {
  opacity: 0.75;
}
</style>
