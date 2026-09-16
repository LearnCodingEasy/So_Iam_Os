<template>
  <article class="recommendation">
    <div class="rec-head">
      <span class="rec-icon">✦</span>
      <span class="match-badge">{{ score }} مناسب</span>
    </div>
    <h4>{{ title }}</h4>
    <p>{{ company }}</p>
    <div class="tags">{{ tags }}</div>
    <div class="match-line"><span :style="{ width: score }"></span></div>
  </article>
</template>

<script setup>
defineProps({
  title: String,
  company: String,
  score: String,
  tags: String,
});
</script>
