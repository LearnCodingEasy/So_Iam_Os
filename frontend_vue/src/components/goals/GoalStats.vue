<template>
  <section class="goal-stats" aria-label="إحصائيات الأهداف">
    <StatTile
      label="كل الأهداف"
      :value="analytics?.total ?? null"
      icon="pi pi-bullseye"
      tone="primary"
    />
    <StatTile
      label="نشطة ومخططة"
      :value="analytics?.active ?? null"
      icon="pi pi-bolt"
      tone="info"
    />
    <StatTile
      label="مكتملة"
      :value="analytics?.completed ?? null"
      icon="pi pi-check-circle"
      tone="success"
    />
    <StatTile
      label="تحتاج متابعة"
      :value="(analytics?.at_risk ?? 0) + (analytics?.overdue ?? 0)"
      icon="pi pi-exclamation-triangle"
      tone="warn"
    />
    <StatTile
      label="متوسط التقدم"
      :value="analytics?.average_progress ?? 0"
      suffix="%"
      icon="pi pi-chart-line"
      tone="primary"
    />
  </section>
</template>

<script setup>
import StatTile from '@/components/ui/StatTile.vue'

defineProps({
  analytics: {
    type: Object,
    default: () => ({}),
  },
})
</script>
