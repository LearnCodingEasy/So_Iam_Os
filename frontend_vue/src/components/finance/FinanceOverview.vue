<template>
  <section class="section-grid">
    <!-- Cash Flow -->
    <Card class="panel wide">
      <template #title>
        <div class="panel-title">
          <span>التدفق النقدي</span>

          <Tag :value="periodLabel" severity="info" />
        </div>
      </template>

      <template #content>
        <div class="bars">
          <div v-for="item in flow" :key="item.label" class="bar-row">
            <div>
              <span>{{ item.label }}</span>

              <strong>
                {{ money(item.value, baseCurrency) }}
              </strong>
            </div>

            <ProgressBar :value="item.percent" :showValue="false" />
          </div>
        </div>
      </template>
    </Card>

    <!-- Insights -->
    <Card class="panel">
      <template #title> أهم التوصيات </template>

      <template #content>
        <div
          v-for="item in insights.insights || []"
          :key="`${item.type}-${item.title}`"
          class="insight"
        >
          <Tag
            :value="insightType(item.type)"
            :severity="item.type === 'warning' ? 'warn' : 'info'"
          />

          <div>
            <strong>{{ item.title }}</strong>
            <small>{{ item.detail }}</small>
          </div>
        </div>

        <div v-if="!(insights.insights || []).length" class="empty">لا توجد توصيات حالياً.</div>

        <Button
          class="w-full"
          label="تحليل بالـ AI"
          icon="pi pi-sparkles"
          :loading="aiLoading"
          @click="$emit('ask-ai')"
        />
      </template>
    </Card>

    <!-- Latest Transactions -->
    <Card class="panel wide">
      <template #title>
        <div class="panel-title">
          <span>آخر المعاملات</span>

          <Button label="كل المعاملات" text size="small" @click="$emit('go-transactions')" />
        </div>
      </template>

      <template #content>
        <DataTable :value="transactions.slice(0, 8)" responsiveLayout="scroll" :loading="loading">
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
        </DataTable>
      </template>
    </Card>

    <!-- Goals -->
    <Card class="panel">
      <template #title> الأهداف المالية </template>

      <template #content>
        <div v-if="!savings.length" class="empty">لا توجد أهداف ادخار.</div>

        <div v-for="goal in savings.slice(0, 4)" :key="goal.id" class="goal-mini">
          <div class="panel-title">
            <strong>{{ goal.name }}</strong>

            <Tag :value="`${goalPercent(goal)}%`" />
          </div>

          <ProgressBar :value="goalPercent(goal)" />

          <small>
            {{ money(goal.current_amount, goal.currency) }}
            /
            {{ money(goal.target_amount, goal.currency) }}
          </small>
        </div>
      </template>
    </Card>
  </section>
</template>

<script setup>
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import Button from 'primevue/button'
import ProgressBar from 'primevue/progressbar'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

defineProps({
  flow: {
    type: Array,
    default: () => [],
  },

  periodLabel: {
    type: String,
    default: '',
  },

  insights: {
    type: Object,
    default: () => ({
      insights: [],
    }),
  },

  transactions: {
    type: Array,
    default: () => [],
  },

  savings: {
    type: Array,
    default: () => [],
  },

  baseCurrency: {
    type: String,
    default: 'USD',
  },

  loading: {
    type: Boolean,
    default: false,
  },

  aiLoading: {
    type: Boolean,
    default: false,
  },

  money: {
    type: Function,
    required: true,
  },

  goalPercent: {
    type: Function,
    required: true,
  },

  insightType: {
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

defineEmits(['ask-ai', 'go-transactions'])
</script>
