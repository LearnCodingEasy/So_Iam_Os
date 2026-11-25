<script setup>
import AnimatedCounter from './AnimatedCounter.vue'

defineProps({
  label: { type: String, required: true },
  value: { type: [Number, String], default: null },
  suffix: { type: String, default: '' },
  icon: { type: String, default: 'pi pi-chart-bar' }, // primeicons class
  tone: { type: String, default: 'primary' }, // primary | success | warn | danger | info
  hint: { type: String, default: '' }, // only real, caller-provided context (no fabricated trends)
  loading: Boolean,
})
</script>

<template>
  <article class="ds-stat" :class="`ds-tone-${tone}`">
    <span class="ds-stat__icon" aria-hidden="true"><i :class="icon" /></span>
    <div class="ds-stat__body">
      <span class="ds-stat__label">{{ label }}</span>
      <prime_skeleton v-if="loading" width="4rem" height="1.8rem" />
      <strong v-else class="ds-stat__value"
        ><AnimatedCounter :value="value" :suffix="suffix"
      /></strong>
      <small v-if="hint" class="ds-stat__hint">{{ hint }}</small>
    </div>
  </article>
</template>
