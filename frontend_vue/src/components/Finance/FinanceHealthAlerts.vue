<template>
  <section class="health-grid">
    <!-- Financial Health -->
    <Card class="panel">
      <template #title>
        <div class="panel-title">
          <span>الصحة المالية</span>

          <Tag :value="`${Number(health.score || 0)}/100`" :severity="healthSeverity" />
        </div>
      </template>

      <template #content>
        <ProgressBar :value="Number(health.score || 0)" :showValue="false" />

        <div class="health-metrics">
          <div v-for="(value, key) in health.components || {}" :key="key">
            <span>{{ healthLabel(key) }}</span>

            <strong> {{ Number(value || 0).toFixed(0) }}% </strong>
          </div>
        </div>

        <p class="muted health-note">الدرجة مبنية على مؤشرات قابلة للتفسير وليست قرارًا ماليًا.</p>
      </template>
    </Card>

    <!-- Alerts -->
    <Card class="panel">
      <template #title>
        <div class="panel-title">
          <span>التنبيهات الذكية</span>

          <Badge :value="String(alerts.length)" />
        </div>
      </template>

      <template #content>
        <div v-if="!alerts.length" class="empty">لا توجد تنبيهات غير مقروءة 🎉</div>

        <div v-for="alert in alerts.slice(0, 5)" :key="alert.id" class="alert-row">
          <Tag :value="alert.severity || 'info'" :severity="alertSeverity(alert.severity)" />

          <div>
            <strong>{{ alert.title }}</strong>
            <small>{{ alert.message }}</small>
          </div>

          <Button
            text
            rounded
            icon="pi pi-check"
            aria-label="قراءة"
            @click="$emit('mark-alert', alert)"
          />
        </div>
      </template>
    </Card>
  </section>
</template>

<script setup>
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import Badge from 'primevue/badge'
import ProgressBar from 'primevue/progressbar'
import Button from 'primevue/button'

defineProps({
  health: {
    type: Object,
    default: () => ({
      score: 0,
      components: {},
    }),
  },

  healthSeverity: {
    type: String,
    default: 'info',
  },

  alerts: {
    type: Array,
    default: () => [],
  },

  healthLabel: {
    type: Function,
    required: true,
  },

  alertSeverity: {
    type: Function,
    required: true,
  },
})

defineEmits(['mark-alert'])
</script>
