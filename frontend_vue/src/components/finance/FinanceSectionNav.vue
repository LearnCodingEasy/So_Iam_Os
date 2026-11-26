<template>
  <SelectButton
    :modelValue="modelValue"
    :options="sections"
    optionLabel="label"
    optionValue="value"
    class="section-switch"
    @update:modelValue="$emit('update:modelValue', $event)"
  />
</template>

<script setup>
import SelectButton from 'primevue/selectbutton'

defineProps({
  modelValue: {
    type: String,
    default: 'overview',
  },

  sections: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['update:modelValue'])
</script>
