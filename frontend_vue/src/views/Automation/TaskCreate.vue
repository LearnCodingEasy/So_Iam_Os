
<template>
  <div class="p-4">
    <h2>Create Task</h2>

    <input v-model="name" placeholder="Task name" />

    <select v-model="programId">
      <option disabled value="">Select Program</option>
      <option v-for="p in programs" :value="p.id" :key="p.id">{{ p.name }}</option>
    </select>

    <textarea
      v-model="actionsJson"
      rows="8"
      placeholder='[{"action_type":"open_program","value":""}]'
    ></textarea>

    <button @click="create">Create</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const programs = ref([])
const name = ref('')
const programId = ref('')
const actionsJson = ref('[]')

onMounted(async () => {
  const r = await api.get('automation/programs/')
  programs.value = r.data
})

const create = async () => {
  if (!programId.value) {
    alert('Select program first!')
    return
  }

  // create task
  const payload = {
    name: name.value,
    program: programId.value,
    description: '',
  }

  const res = await api.post('automation/tasks/', payload)
  const taskId = res.data.id

  // convert JSON to actions
  const actions = JSON.parse(actionsJson.value || '[]')

  for (let i = 0; i < actions.length; i++) {
    await api.post('automation/actions/', {
      task: taskId,
      action_type: actions[i].action_type,
      value: actions[i].value,
      delay: actions[i].delay || 0.5,
      order: i,
    })
  }

  alert('Task created successfully')
}
</script>
