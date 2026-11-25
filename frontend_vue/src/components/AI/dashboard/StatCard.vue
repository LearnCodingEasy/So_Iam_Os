<template>
  <StatTile :label="label" :value="numeric" :icon="icon" :hint="caption" />
</template>

<script setup>
// Thin adapter kept for backward compatibility. It no longer renders a fabricated
// "from last month" trend: only the caption supplied by the caller is shown.
import { computed } from 'vue'
import StatTile from '@/components/ui/StatTile.vue'

const props = defineProps({
  label: String,
  value: [String, Number],
  change: String, // legacy prop, ignored unless caption is empty
  caption: { type: String, default: '' },
  icon: { type: String, default: 'pi pi-chart-bar' },
})
const numeric = computed(() => props.value)
const caption = computed(() => props.caption || props.change || '')
</script>
