<script setup>
// Unified Empty / Error / Loading state. Retry/action buttons are only shown when a handler is provided.
import HeroIllustration from './HeroIllustration.vue'

defineProps({
  state: { type: String, default: 'empty' }, // empty | error | loading
  title: { type: String, default: '' },
  message: { type: String, default: '' },
  illustration: { type: String, default: 'empty' },
  actionLabel: { type: String, default: '' },
  actionIcon: { type: String, default: '' },
})
defineEmits(['action'])
</script>

<template>
  <section
    class="ds-state"
    :class="`ds-state--${state}`"
    :role="state === 'error' ? 'alert' : 'status'"
    :aria-busy="state === 'loading'"
  >
    <prime_progress_spinner
      v-if="state === 'loading'"
      style="width: 2.4rem; height: 2.4rem"
      stroke-width="4"
    />
    <HeroIllustration
      v-else
      :kind="state === 'error' ? 'error' : illustration"
      class="ds-state__art"
    />
    <h3 v-if="title">{{ title }}</h3>
    <p v-if="message">{{ message }}</p>
    <prime_button
      v-if="actionLabel"
      :label="actionLabel"
      :icon="actionIcon"
      :severity="state === 'error' ? 'danger' : 'primary'"
      size="small"
      @click="$emit('action')"
    />
  </section>
</template>
