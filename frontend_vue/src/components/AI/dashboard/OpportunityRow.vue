<template>
  <div class="opportunity-row">
    <div class="company-icon">{{ icon }}</div>
    <div class="opportunity-main">
      <strong>{{ title }}</strong>
      <span>{{ company }} · {{ salary }}</span>
    </div>
    <div class="score">
      <strong>{{ score }}</strong>
      <span>Match</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  company: String,
  score: String,
  salary: String,
  icon: String,
});
</script>
