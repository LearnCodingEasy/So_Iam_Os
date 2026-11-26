<template>
  <section class="section-grid">
    <Card class="panel wide">
      <template #title>
        <div class="section-head">
          <h2>الديون</h2>

          <Button label="إضافة دين" icon="pi pi-plus" @click="$emit('add')" />
        </div>
      </template>

      <template #content>
        <DataTable :value="debts" responsiveLayout="scroll">
          <Column field="name" header="الدين" />

          <Column field="balance" header="الرصيد">
            <template #body="{ data }">
              {{ money(data.balance, data.currency) }}
            </template>
          </Column>

          <Column field="minimum_payment" header="الحد الأدنى">
            <template #body="{ data }">
              {{ money(data.minimum_payment, data.currency) }}
            </template>
          </Column>

          <Column field="due_date" header="الاستحقاق" />

          <Column header="إجراءات">
            <template #body="{ data }">
              <Button text icon="pi pi-wallet" @click="$emit('payment', data)" />

              <Button text icon="pi pi-pencil" @click="$emit('edit', data)" />

              <Button text severity="danger" icon="pi pi-trash" @click="$emit('remove', data)" />
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>

    <Card class="panel">
      <template #title> ملخص الديون </template>

      <template #content>
        <div class="stack">
          <div class="mini-row">
            <span>إجمالي الدين</span>

            <strong>
              {{ money(totalDebt, baseCurrency) }}
            </strong>
          </div>

          <div class="mini-row">
            <span>عدد الديون</span>

            <strong>
              {{ debts.length }}
            </strong>
          </div>
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

defineProps({
  debts: {
    type: Array,
    default: () => [],
  },

  totalDebt: {
    type: Number,
    default: 0,
  },

  baseCurrency: {
    type: String,
    default: 'USD',
  },

  money: {
    type: Function,
    required: true,
  },
})

defineEmits(['add', 'payment', 'edit', 'remove'])
</script>
