<template>
  <section class="panel section-card">
    <div class="section-head">
      <div>
        <h2>الميزانيات</h2>
        <p>حدود الإنفاق والالتزام بها.</p>
      </div>

      <Button label="إضافة ميزانية" icon="pi pi-plus" @click="$emit('add')" />
    </div>

    <DataTable :value="budgets" paginator :rows="8" responsiveLayout="scroll">
      <Column field="name" header="الميزانية" />

      <Column field="period" header="الفترة" />

      <Column field="limit_amount" header="الحد">
        <template #body="{ data }">
          {{ money(data.limit_amount, data.currency) }}
        </template>
      </Column>

      <Column field="spent" header="المصروف">
        <template #body="{ data }">
          {{ money(data.spent, data.currency) }}
        </template>
      </Column>

      <Column field="remaining" header="المتبقي">
        <template #body="{ data }">
          <Tag
            :value="money(data.remaining, data.currency)"
            :severity="Number(data.remaining) < 0 ? 'danger' : 'success'"
          />
        </template>
      </Column>

      <Column header="إجراءات">
        <template #body="{ data }">
          <Button text icon="pi pi-pencil" @click="$emit('edit', data)" />

          <Button text severity="danger" icon="pi pi-trash" @click="$emit('remove', data)" />
        </template>
      </Column>
    </DataTable>
  </section>
</template>

<script setup>
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'

defineProps({
  budgets: {
    type: Array,
    default: () => [],
  },

  money: {
    type: Function,
    required: true,
  },
})

defineEmits(['add', 'edit', 'remove'])
</script>
