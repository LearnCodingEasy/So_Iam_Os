<template>
  <div class="p-4">
    <h2>Programs</h2>
    <div class="p-grid">
      <div v-for="p in programs" :key="p.id" class="p-col-12 p-md-4">
        <div class="p-card">
          <h3>{{ p.name }}</h3>
          <small>{{ p.executable_path }}</small>
          <div class="p-mt-2">
            <button @click="open(p.id)" class="p-button">Open</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import programService from '../../services/AutomationService'
const programs = ref([])
const load = async () => {
  const res = await programService.list()
  programs.value = res.data
}
const open = async (id) => {
  await programService.open(id)
  alert('open request sent')
}
onMounted(load)
</script>
