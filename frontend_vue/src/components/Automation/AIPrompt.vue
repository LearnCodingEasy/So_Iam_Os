<script setup>
import { ref } from 'vue'
import axios from 'axios'

const prompt = ref('')
const result = ref(null)

async function runPrompt() {
  const res = await axios.post('/api/ai/run/', {
    prompt: prompt.value,
    token: localStorage.getItem('mcp_token'),
  })

  result.value = res.data
}
</script>

<template>
  <div class="ai-panel">
    <textarea v-model="prompt" placeholder="Type automation prompt..." />

    <button @click="runPrompt">Run Automation</button>

    <pre>{{ result }}</pre>
  </div>
</template>
