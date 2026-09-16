<template>
  <div class="skill-row">
    <div class="skill-meta">
      <span>{{ name }}</span>
      <strong>{{ value }}%</strong>
    </div>
    <div class="skill-track">
      <span :style="{ width: `${value}%` }"></span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  name: String,
  value: [String, Number],
});
</script>
