<template>
  <section class="section-grid">
    <Card class="panel wide">
      <template #title>
        <div class="section-head">
          <h2>الدخل والمصاريف المتكررة</h2>

          <Button label="إضافة" icon="pi pi-plus" @click="$emit('add')" />
        </div>
      </template>

      <template #content>
        <DataTable :value="recurring" responsiveLayout="scroll">
          <Column field="name" header="الاسم" />

          <Column field="kind" header="النوع">
            <template #body="{ data }">
              <Tag :value="kindLabel(data.kind)" :severity="kindSeverity(data.kind)" />
            </template>
          </Column>

          <Column field="amount" header="المبلغ">
            <template #body="{ data }">
              {{ money(data.amount, data.currency) }}
            </template>
          </Column>

          <Column field="frequency" header="التكرار" />

          <Column field="next_date" header="التاريخ القادم" />

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
      <template #title> الاشتراكات </template>

      <template #content>
        <div v-if="!subscriptions.length" class="empty">لا توجد اشتراكات.</div>

        <div v-for="item in subscriptions" :key="item.id" class="mini-row">
          <span>{{ item.name }}</span>

          <strong>
            {{ money(item.amount, item.currency) }}
          </strong>
        </div>
      </template>
    </Card>
  </section>
</template>

<script setup>
import Card from 'primevue/card'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'

defineProps({
  recurring: {
    type: Array,
    default: () => [],
  },

  subscriptions: {
    type: Array,
    default: () => [],
  },

  money: {
    type: Function,
    required: true,
  },

  kindLabel: {
    type: Function,
    required: true,
  },

  kindSeverity: {
    type: Function,
    required: true,
  },
})

defineEmits(['add', 'edit', 'remove'])
</script>
