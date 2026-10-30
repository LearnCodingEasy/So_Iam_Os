<script setup>
import { ref } from 'vue'
import api from '@/services/api'
import { endpoints } from '@/services/endpoints'

const prompt = ref('')
const result = ref(null)
const loading = ref(false)
const error = ref('')

async function runPrompt() {
  if (!prompt.value.trim() || loading.value) return
  loading.value = true
  error.value = ''
  result.value = null
  try {
    const response = await api.post(endpoints.ai.agentPlan, { request: prompt.value.trim() })
    result.value = response.data
  } catch (e) {
    error.value = e?.response?.data?.detail || e?.response?.data?.error || 'Could not create a workflow plan.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="ai-panel">
    <label for="automation-plan-prompt">Describe the workflow</label>
    <textarea id="automation-plan-prompt" v-model="prompt" rows="4" placeholder="For example: Find new Python jobs every morning and create review tasks for the best matches."></textarea>
    <button :disabled="!prompt.trim() || loading" @click="runPrompt">
      {{ loading ? 'Planning…' : 'Create workflow plan' }}
    </button>
    <p class="hint">The API returns a draft plan only. It does not execute actions; review and configure the workflow in the existing automation editor.</p>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <section v-if="result" class="plan-result" aria-live="polite">
      <h3>Draft workflow</h3>
      <p>{{ result.explanation }}</p>
      <p class="plan-meta">Mode: {{ result.planning_mode }} · Execution: {{ result.execution_status }}</p>
      <ol>
        <li v-for="(node, index) in result.nodes" :key="`${node.type}-${index}`">
          <strong>{{ node.label }}</strong> <code>{{ node.type }}</code>
        </li>
      </ol>
      <pre>{{ JSON.stringify(result.edges, null, 2) }}</pre>
    </section>
  </section>
</template>

<style scoped>
.ai-panel { display: grid; gap: 0.75rem; }
textarea { width: 100%; resize: vertical; }
button { justify-self: start; }
.hint, .plan-meta { opacity: 0.75; font-size: 0.875rem; }
.error { color: var(--red-500, #b91c1c); }
.plan-result { border: 1px solid var(--surface-border, #ddd); border-radius: 0.75rem; padding: 1rem; }
.plan-result ol { display: grid; gap: 0.5rem; padding-left: 1.5rem; }
.plan-result li { display: flex; gap: 0.5rem; align-items: baseline; flex-wrap: wrap; }
.plan-result pre { white-space: pre-wrap; overflow-wrap: anywhere; }
</style>
