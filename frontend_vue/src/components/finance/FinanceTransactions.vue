<template>
  <section class="panel section-card">
    <div class="section-head">
      <div>
        <h2>المعاملات</h2>
        <p>الدخل والمصروفات والادخار وسداد الديون.</p>
      </div>

      <Button label="إضافة معاملة" icon="pi pi-plus" @click="$emit('add')" />
    </div>

    <DataTable
      :value="transactions"
      paginator
      :rows="10"
      responsiveLayout="scroll"
      :loading="loading"
    >
      <Column field="occurred_on" header="التاريخ" />

      <Column field="description" header="الوصف" />

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

      <Column field="currency" header="العملة" />

      <Column header="إجراءات">
        <template #body="{ data }">
          <Button text icon="pi pi-pencil" @click="$emit('edit', data)" />

          <Button text severity="danger" icon="pi pi-trash" @click="$emit('remove', data)" />
        </template>
      </Column>

      <template #empty>
        <div class="empty">لا توجد معاملات.</div>
      </template>
    </DataTable>
  </section>
</template>

<script setup>
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'

defineProps({
  transactions: {
    type: Array,
    default: () => [],
  },

  loading: {
    type: Boolean,
    default: false,
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
