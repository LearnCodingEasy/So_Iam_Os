<template>
  <section class="section-grid">
    <Card class="panel wide">
      <template #title>
        <div class="section-head">
          <h2>السلف: أقرضت / اقترضت</h2>

          <Button label="إضافة" icon="pi pi-plus" @click="$emit('add')" />
        </div>
      </template>

      <template #content>
        <DataTable :value="loans" responsiveLayout="scroll">
          <Column field="person" header="الشخص" />

          <Column field="direction" header="الاتجاه">
            <template #body="{ data }">
              <Tag
                :value="data.direction === 'lent' ? 'لي عنده' : 'عليه لي'"
                :severity="data.direction === 'lent' ? 'success' : 'warn'"
              />
            </template>
          </Column>

          <Column field="amount" header="الإجمالي">
            <template #body="{ data }">
              {{ money(data.amount, data.currency) }}
            </template>
          </Column>

          <Column field="remaining" header="المتبقي">
            <template #body="{ data }">
              {{ money(data.remaining, data.currency) }}
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
      <template #title> ملخص السلف </template>

      <template #content>
        <div class="stack">
          <div class="mini-row">
            <span>لي عند الآخرين</span>

            <strong>
              {{ money(loanTotals.lent, baseCurrency) }}
            </strong>
          </div>

          <div class="mini-row">
            <span>عليّ للآخرين</span>

            <strong>
              {{ money(loanTotals.borrowed, baseCurrency) }}
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
import Tag from 'primevue/tag'

defineProps({
  loans: {
    type: Array,
    default: () => [],
  },

  loanTotals: {
    type: Object,
    default: () => ({
      lent: 0,
      borrowed: 0,
    }),
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
