<template>
  <section class="section-grid">
    <Card class="panel wide">
      <template #title>
        <div class="panel-title">
          <span>Financial Forecast</span>

          <Button label="تحديث" text icon="pi pi-refresh" @click="$emit('refresh')" />
        </div>
      </template>

      <template #content>
        <DataTable :value="forecastRows" responsiveLayout="scroll">
          <Column field="month" header="الشهر" />

          <Column field="income" header="الدخل">
            <template #body="{ data }">
              {{ money(data.income, baseCurrency) }}
            </template>
          </Column>

          <Column field="expenses" header="المصروفات">
            <template #body="{ data }">
              {{ money(data.expenses, baseCurrency) }}
            </template>
          </Column>

          <Column field="surplus" header="الفائض">
            <template #body="{ data }">
              <Tag
                :value="money(data.surplus, baseCurrency)"
                :severity="Number(data.surplus) >= 0 ? 'success' : 'danger'"
              />
            </template>
          </Column>

          <Column field="cumulative_surplus" header="التراكمي">
            <template #body="{ data }">
              {{ money(data.cumulative_surplus, baseCurrency) }}
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>

    <Card class="panel">
      <template #title> Scenario Simulator </template>

      <template #content>
        <div class="form-grid">
          <div class="field">
            <label>تغير الدخل %</label>

            <InputNumber v-model="scenarioForm.income_change_percent" suffix="%" class="w-full" />
          </div>

          <div class="field">
            <label>تغير المصروف %</label>

            <InputNumber v-model="scenarioForm.expense_change_percent" suffix="%" class="w-full" />
          </div>

          <div class="field">
            <label>سداد دين إضافي</label>

            <InputNumber v-model="scenarioForm.extra_debt_payment" class="w-full" />
          </div>

          <div class="field">
            <label>الحالة</label>

            <Select
              v-model="scenarioForm.case"
              :options="['best', 'expected', 'worst']"
              class="w-full"
            />
          </div>
        </div>

        <Button
          class="w-full"
          label="احسب السيناريو"
          icon="pi pi-chart-line"
          @click="$emit('scenario')"
        />

        <div v-if="scenarioResult" class="scenario">
          <strong>
            {{ money(scenarioResult.surplus, baseCurrency) }}
          </strong>

          <span>
            {{ scenarioResult.impact === 'surplus' ? 'فائض محتمل' : 'عجز محتمل' }}
          </span>
        </div>
      </template>
    </Card>
  </section>
</template>

<script setup>
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'

defineProps({
  forecastRows: {
    type: Array,
    default: () => [],
  },

  scenarioForm: {
    type: Object,
    required: true,
  },

  scenarioResult: {
    type: Object,
    default: null,
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

defineEmits(['refresh', 'scenario'])
</script>
