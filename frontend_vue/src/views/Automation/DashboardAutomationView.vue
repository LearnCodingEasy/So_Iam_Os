<template>
  <div class="p-4">
    <h2>Tasks</h2>
    <div class="p-grid p-mt-3">
      <div v-for="t in tasks" :key="t.id" class="p-col-12 p-md-4">
        <div class="p-card">
          <h3>{{ t.name }}</h3>
          <p>{{ t.description }}</p>
          <div class="p-mt-2">
            <button @click="run(t.id)" class="p-button p-button-success p-mr-2">Run</button>
            <router-link :to="`/task/${t.id}`" class="p-button p-button-secondary"
              >Edit</router-link
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import taskService from '../../services/taskService'
const tasks = ref([])
const load = async () => {
  const res = await taskService.list()
  tasks.value = res.data
  console.log('res.data: ', res.data);
}
const run = async (id) => {
  const res = await taskService.run(id)
  alert(JSON.stringify(res.data))
}
onMounted(load)
</script>
