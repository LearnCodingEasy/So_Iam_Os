<template>
  <section class="section-grid">
    <Card class="panel wide">
      <template #title> التقرير الأسبوعي </template>

      <template #content>
        <pre>{{ pretty(weeklyReport) }}</pre>
      </template>
    </Card>

    <Card class="panel">
      <template #title> التقرير الشهري </template>

      <template #content>
        <pre>{{ pretty(monthlyReport) }}</pre>
      </template>
    </Card>
  </section>
</template>

<script setup>
import Card from 'primevue/card'

defineProps({
  weeklyReport: {
    type: Object,
    default: () => ({}),
  },

  monthlyReport: {
    type: Object,
    default: () => ({}),
  },

  pretty: {
    type: Function,
    required: true,
  },
})
</script>
