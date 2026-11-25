<script setup>
import { ref } from 'vue'
import { useReveal } from '@/composables/useMotion'
import HeroIllustration from './HeroIllustration.vue'

defineProps({
  eyebrow: { type: String, default: '' },
  title: { type: String, required: true },
  description: { type: String, default: '' },
  illustration: { type: String, default: '' }, // see HeroIllustration kinds; empty = none
})
const root = ref(null)
useReveal(root, { selector: '.ds-pagehead__copy > *', y: 10, stagger: 0.07 })
</script>

<template>
  <header ref="root" class="ds-pagehead">
    <div class="ds-pagehead__bg" aria-hidden="true"><span /><span /></div>
    <div class="ds-pagehead__copy">
      <span v-if="eyebrow" class="ds-eyebrow">{{ eyebrow }}</span>
      <h1 class="ds-gradient-text">{{ title }}</h1>
      <p v-if="description">{{ description }}</p>
      <div v-if="$slots.actions" class="ds-pagehead__actions"><slot name="actions" /></div>
    </div>
    <HeroIllustration v-if="illustration" :kind="illustration" class="ds-pagehead__art" />
  </header>
</template>
