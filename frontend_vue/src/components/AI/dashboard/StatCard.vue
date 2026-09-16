<template>
  <article class="stat-card">
    <div class="stat-top">
      <span class="stat-label">{{ label }}</span>
      <div class="stat-icon">{{ icon }}</div>
    </div>
    <div class="stat-value">{{ value }}</div>
    <div class="stat-bottom">
      <span class="positive">↗ {{ change }}</span>
      <span>من الشهر الماضي</span>
    </div>
  </article>
</template>

<script setup>
defineProps({
  label: String,
  value: String,
  change: String,
  icon: String,
});
</script>
