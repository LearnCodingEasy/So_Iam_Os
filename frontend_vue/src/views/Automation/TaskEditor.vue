<template>
  <div class="p-4">
    <button @click="$router.back()">Back</button>
    <h2>Edit Task: {{ task?.name }}</h2>

    <div v-for="a in actions" :key="a.id" class="p-card p-mb-2">
      <div><b>{{ a.order }} - {{ a.action_type }}</b></div>
      <div>{{ a.value }}</div>
    </div>

    <button @click="runTask">Run Task</button>

    <h3>Runs</h3>
    <div v-for="r in runs" :key="r.id">{{ r.id }} - {{ r.status }} - {{ r.started_at }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'
import { useRoute } from 'vue-router'
const route = useRoute()
const taskId = route.params.id
const task = ref(null)
const actions = ref([])
const runs = ref([])

const load = async ()=>{
  const t = await api.get(`/tasks/${taskId}/`)
  task.value = t.data
  const a = await api.get(`/tasks/${taskId}/actions/`)
  actions.value = a.data
  const tr = await api.get(`/taskruns/?task=${taskId}`)
  runs.value = tr.data
}
const runTask = async ()=>{
  const res = await api.post(`/tasks/${taskId}/run/`)
  // if started return run_id
  if (res.data.run_id) {
    pollLogs(res.data.run_id)
  } else {
    alert(JSON.stringify(res.data))
  }
}
const pollLogs = async (run_id) => {
  const interval = setInterval(async ()=>{
    const r = await api.get(`/taskruns/${run_id}/logs/`)
    if (r.data.status !== 'running') clearInterval(interval)
    console.log('logs', r.data.logs)
  }, 1500)
}
onMounted(load)
</script>
