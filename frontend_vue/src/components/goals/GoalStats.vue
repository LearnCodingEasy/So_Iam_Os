<template>
  <section class="goal-stats" aria-label="إحصائيات الأهداف">
    <article class="stat-tile">
      <span>كل الأهداف</span><strong>{{ analytics?.total ?? '—' }}</strong
      ><i class="pi pi-bullseye" />
    </article>
    <article class="stat-tile">
      <span>نشطة ومخططة</span><strong>{{ analytics?.active ?? '—' }}</strong
      ><i class="pi pi-bolt" />
    </article>
    <article class="stat-tile">
      <span>مكتملة</span><strong>{{ analytics?.completed ?? '—' }}</strong
      ><i class="pi pi-check-circle" />
    </article>
    <article class="stat-tile">
      <span>تحتاج متابعة</span
      ><strong>{{ (analytics?.at_risk ?? 0) + (analytics?.overdue ?? 0) }}</strong
      ><i class="pi pi-exclamation-triangle" />
    </article>
    <article class="stat-tile">
      <span>متوسط التقدم</span><strong>{{ analytics?.average_progress ?? 0 }}%</strong
      ><i class="pi pi-chart-line" />
    </article>
  </section>
</template>

<script setup>
defineProps({
  analytics: {
    type: Object,
    default: () => ({}),
  },
})
</script>+
