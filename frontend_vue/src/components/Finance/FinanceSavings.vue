<template>
  <section class="section-grid">
    <Card class="panel wide">
      <template #title>
        <div class="section-head">
          <h2>الأهداف وخطط الادخار</h2>

          <Button label="إضافة هدف" icon="pi pi-plus" @click="$emit('add')" />
        </div>
      </template>

      <template #content>
        <div class="goal-grid">
          <div v-for="goal in savings" :key="goal.id" class="goal">
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

            <div class="row-actions">
              <Button size="small" label="خطة توفير" text @click="$emit('plan', goal)" />

              <Button size="small" text icon="pi pi-pencil" @click="$emit('edit', goal)" />

              <Button
                size="small"
                text
                severity="danger"
                icon="pi pi-trash"
                @click="$emit('remove', goal)"
              />
            </div>
          </div>
        </div>

        <div v-if="!savings.length" class="empty">لا توجد أهداف مالية بعد.</div>
      </template>
    </Card>

    <Card class="panel">
      <template #title> نتيجة آخر خطة توفير </template>

      <template #content>
        <div v-if="savingPlan" class="plan-result">
          <strong>
            يومي:
            {{ money(savingPlan.daily_amount, baseCurrency) }}
          </strong>

          <strong>
            أسبوعي:
            {{ money(savingPlan.weekly_amount, baseCurrency) }}
          </strong>

          <strong>
            شهري:
            {{ money(savingPlan.monthly_amount, baseCurrency) }}
          </strong>

          <small>
            الإتمام المتوقع:
            {{ savingPlan.expected_completion || '—' }}
          </small>
        </div>

        <div v-else class="empty">اختر هدفًا لإنشاء خطة.</div>
      </template>
    </Card>
  </section>
</template>

<script setup>
import Card from 'primevue/card'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import ProgressBar from 'primevue/progressbar'

defineProps({
  savings: {
    type: Array,
    default: () => [],
  },

  savingPlan: {
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

  goalPercent: {
    type: Function,
    required: true,
  },
})

defineEmits(['add', 'plan', 'edit', 'remove'])
</script>
