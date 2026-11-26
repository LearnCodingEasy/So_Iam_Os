<script setup>
import { Handle, Position } from '@vue-flow/core'

defineProps({
  data: Object,
  icon: String,
})
</script>

<template>
  <div class="node">
    <!-- 🔴 Handle دخول -->
    <Handle type="target" :position="Position.Left" id="target" />

    <div class="node-header">
      <i :class="icon"></i>
      <span>{{ data.label }}</span>
    </div>

    <div class="node-body">
      <slot />
    </div>

    <div class="node-footer">
      <button @click="$emit('run-task', data)">▶ Run</button>
    </div>

    <!-- 🟢 Handle خروج -->
    <Handle type="source" :position="Position.Right" id="source" />
  </div>
</template>
