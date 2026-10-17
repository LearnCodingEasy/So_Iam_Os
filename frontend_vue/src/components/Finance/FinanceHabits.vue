<template>
  <section class="section-grid">
    <Card class="panel wide">
      <template #title>
        <div class="section-head">
          <h2>العادات المالية</h2>

          <Button label="إضافة" icon="pi pi-plus" @click="$emit('add')" />
        </div>
      </template>

      <template #content>
        <DataTable :value="habits" responsiveLayout="scroll">
          <Column field="name" header="العادة" />

          <Column field="progress" header="التقدم" />

          <Column field="streak" header="Streak" />

          <Column field="status" header="الحالة" />

          <Column header="إجراءات">
            <template #body="{ data }">
              <Button text icon="pi pi-pencil" @click="$emit('edit', data)" />

              <Button text severity="danger" icon="pi pi-trash" @click="$emit('remove', data)" />
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>

    <Card class="panel">
      <template #title> ملاحظة </template>

      <template #content>
        <p class="muted">
          العادات هنا مرتبطة بالهدف والمدة والتقدم والـ streak، وليست حكمًا على المستخدم.
        </p>
      </template>
    </Card>
  </section>
</template>

<script setup>
import Card from 'primevue/card'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

defineProps({
  habits: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['add', 'edit', 'remove'])
</script>
