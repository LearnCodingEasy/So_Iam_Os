<template>
  <div class="delay-node">
    <p class="title">⏳ Delay</p>

    <input
      type="number"
      step="0.1"
      v-model.number="node.data.delay"
      @change="updateDelay"
      class="input"
    />
    <small>Seconds</small>
  </div>
</template>

<script setup>
import { useVueFlow } from '@vue-flow/core'
const props = defineProps(['id', 'data'])
const { findNode } = useVueFlow()

const updateDelay = () => {
  const node = findNode(props.id)
  node.data.delay = props.data.delay
}
</script>

<style scoped>
.delay-node {
  background: #fef3c7;
  border: 1px solid #f59e0b;
  padding: 10px;
  border-radius: 8px;
  text-align: center;
}
.title {
  font-weight: bold;
  margin-bottom: 8px;
}
.input {
  width: 70px;
  padding: 4px;
  border: 1px solid #ddd;
}
</style>
