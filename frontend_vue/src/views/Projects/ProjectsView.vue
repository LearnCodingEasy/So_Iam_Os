<template>
  <div class="os-page">
    <Card
      ><template #title>Projects</template
      ><template #content
        ><div class="toolbar">
          <Button label="New Project" icon="pi pi-plus" @click="open = true" />
        </div>
        <DataTable :value="items" :loading="loading" stripedRows
          ><Column field="title" header="Project" /><Column field="status" header="Status" /><Column
            field="description"
            header="Description" /></DataTable
        ><Dialog v-model:visible="open" modal header="Create Project"
          ><div class="form">
            <InputText v-model="form.title" placeholder="Project title" /><Textarea
              v-model="form.description"
              rows="5"
              placeholder="Description"
            /><Button label="Create" @click="create" /></div></Dialog></template
    ></Card>
  </div>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import { projectsApi } from '@/services/osDomains'
const items = ref([]),
  loading = ref(false),
  open = ref(false),
  form = ref({ title: '', description: '' })
const load = async () => {
  loading.value = true
  try {
    items.value = await projectsApi.list()
  } finally {
    loading.value = false
  }
}
const create = async () => {
  if (!form.value.title) return
  await projectsApi.create(form.value)
  form.value = { title: '', description: '' }
  open.value = false
  await load()
}
onMounted(load)
</script>
<style scoped>
.os-page {
  padding: 1rem;
}
.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}
.form {
  display: grid;
  gap: 1rem;
  min-width: 320px;
}
</style>
