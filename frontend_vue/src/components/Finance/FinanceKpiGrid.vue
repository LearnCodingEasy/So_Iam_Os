<template>
  <section class="metric-grid">
    <Card v-for="metric in metrics" :key="metric.label" class="metric">
      <template #content>
        <div class="metric-top">
          <i :class="metric.icon"></i>
          <span>{{ metric.label }}</span>
        </div>

        <strong>{{ metric.value }}</strong>

        <small>{{ metric.help }}</small>
      </template>
    </Card>
  </section>
</template>

<script setup>
import Card from 'primevue/card'

defineProps({
  metrics: {
    type: Array,
    default: () => [],
  },
})
</script>
