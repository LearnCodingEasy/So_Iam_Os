<template>
  <div class="os-page">
    <Card
      ><template #title>AI Memory</template
      ><template #content
        ><div class="toolbar">
          <Button label="Remember" icon="pi pi-plus" @click="open = true" />
        </div>
        <DataTable :value="items" :loading="loading" stripedRows
          ><Column field="type" header="Type" /><Column field="key" header="Key" /><Column
            field="content"
            header="Memory" /><Column field="importance" header="Importance" /><Column
            ><template #body="{ data }"
              ><Button
                icon="pi pi-trash"
                text
                severity="danger"
                @click="remove(data.id)" /></template></Column></DataTable
        ><Dialog v-model:visible="open" modal header="Store Memory"
          ><div class="form">
            <Select v-model="form.type" :options="types" placeholder="Type" /><InputText
              v-model="form.key"
              placeholder="Key"
            /><Textarea
              v-model="form.content"
              rows="5"
              placeholder="What should the OS remember?"
            /><Button label="Save" @click="create" /></div></Dialog></template
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
import Select from 'primevue/select'
import { memoryApi } from '@/services/osDomains'
const items = ref([]),
  loading = ref(false),
  open = ref(false),
  types = ['preference', 'context', 'goal', 'project', 'learning', 'conversation', 'fact'],
  form = ref({ type: 'fact', key: '', content: '', importance: 50 })
const load = async () => {
  loading.value = true
  try {
    items.value = await memoryApi.list()
  } finally {
    loading.value = false
  }
}
const create = async () => {
  if (!form.value.key || !form.value.content) return
  await memoryApi.create(form.value)
  form.value = { type: 'fact', key: '', content: '', importance: 50 }
  open.value = false
  await load()
}
const remove = async (id) => {
  await memoryApi.remove(id)
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
