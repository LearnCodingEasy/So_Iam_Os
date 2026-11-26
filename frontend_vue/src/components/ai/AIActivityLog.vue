<template>
  <div class="ai-activity-log">
    <div v-if="!events.length" class="empty">لا توجد أحداث AI مسجلة بعد.</div>
    <article v-for="event in events" :key="event.id" class="event">
      <div class="event-head">
        <strong>{{ event.title }}</strong>
        <time>{{ formatTime(event.timestamp) }}</time>
      </div>
      <div class="event-meta">
        <span v-if="event.method">{{ event.method }}</span>
        <span v-if="event.status">HTTP {{ event.status }}</span>
        <span v-if="event.duration != null">{{ event.duration }}ms</span>
      </div>
    </article>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const events = ref([])
let handler = null
let sequence = 0

function addEvent(detail = {}) {
  const phase = detail.phase
  if (!phase) return
  events.value.unshift({
    id: ++sequence,
    title: phase === 'request' ? 'بدأ طلب API' : phase === 'response' ? 'اكتمل الطلب' : 'فشل الطلب',
    timestamp: Date.now(),
    method: detail.method,
    status: detail.status,
    duration: detail.duration,
  })
  events.value = events.value.slice(0, 50)
}

function formatTime(value) {
  return new Date(value).toLocaleTimeString()
}

onMounted(() => {
  handler = (event) => addEvent(event.detail)
  window.addEventListener('so-iam-api-log', handler)
})
onBeforeUnmount(() => handler && window.removeEventListener('so-iam-api-log', handler))
</script>

<style scoped>
.ai-activity-log {
  display: grid;
  gap: 0.65rem;
}
.event {
  padding: 0.7rem;
  border: 1px solid var(--surface-border, #e2e8f0);
  border-radius: 0.65rem;
}
.event-head,
.event-meta {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
}
.event-meta {
  margin-top: 0.25rem;
  font-size: 0.75rem;
  opacity: 0.7;
}
.empty {
  opacity: 0.7;
}
</style>
