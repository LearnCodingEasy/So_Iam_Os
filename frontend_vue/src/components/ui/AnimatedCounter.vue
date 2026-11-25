<script setup>
// Animates numeric changes. Non-numeric values (e.g. '—') are rendered as-is.
import { onBeforeUnmount, ref, watch } from 'vue'
import { tweenNumber } from '@/composables/useMotion'

const props = defineProps({
  value: { type: [Number, String], default: null },
  suffix: { type: String, default: '' },
  decimals: { type: Number, default: 0 },
})

const display = ref(props.value)
let kill = () => {}

const isNum = (v) => v !== null && v !== '' && Number.isFinite(Number(v))

watch(
  () => props.value,
  (next, prev) => {
    kill()
    if (!isNum(next)) {
      display.value = next
      return
    }
    const from = isNum(prev) ? Number(prev) : 0
    kill = tweenNumber(from, Number(next), (v) => (display.value = v), { decimals: props.decimals })
  },
  { immediate: true },
)

onBeforeUnmount(() => kill())
</script>

<template>
  <span class="ds-counter"
    >{{
      isNum(display)
        ? Number(display).toLocaleString('ar-EG-u-nu-latn', { maximumFractionDigits: decimals })
        : (display ?? '—')
    }}{{ isNum(display) ? suffix : '' }}</span
  >
</template>
