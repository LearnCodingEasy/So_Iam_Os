<template>
  <prime_card class="goal-card">
    <template #title>
      <div class="goal-card-title">
        <span>{{ goal.title }}</span>
        <prime_tag
          :value="goal.status_display || statusLabel(goal.status)"
          :severity="statusSeverity(goal.status)"
        />
      </div>
    </template>
    <template #subtitle>
      <span>{{ categoryLabel(goal.category) }} · {{ priorityLabel(goal.priority) }}</span>
    </template>
    <template #content>
      <p class="goal-description">{{ goal.description || 'لم تتم إضافة وصف لهذا الهدف.' }}</p>
      <div class="progress-caption">
        <span>التقدم</span><strong>{{ goal.progress_percent }}%</strong>
      </div>
      <prime_progress_bar :value="goal.progress_percent" :show-value="false" />
      <div class="goal-facts">
        <span><i class="pi pi-calendar" /> {{ goal.target_date || 'دون موعد نهائي' }}</span>
        <span
          ><i class="pi pi-list-check" /> {{ goal.completed_task_count || 0 }}/{{
            goal.task_count || 0
          }}
          مهام</span
        >
        <span v-if="goal.milestone_count"
          ><i class="pi pi-flag" /> {{ goal.completed_milestone_count || 0 }}/{{
            goal.milestone_count
          }}
          مراحل</span
        >
      </div>
      <div v-if="goal.risk?.reasons?.length" class="risk-note">
        <i class="pi pi-exclamation-circle" /> {{ goal.risk.reasons[0].message }}
      </div>
    </template>
    <template #footer>
      <div class="goal-actions">
        <prime_button
          label="التفاصيل"
          icon="pi pi-arrow-up-right"
          text
          size="small"
          @click="$emit('details', goal)"
        />
        <prime_button
          icon="pi pi-pencil"
          severity="secondary"
          text
          rounded
          size="small"
          aria-label="تعديل"
          :disabled="goal.status === 'archived'"
          @click="$emit('edit', goal)"
        />
        <prime_button
          v-if="['active', 'at_risk', 'planned'].includes(goal.status)"
          icon="pi pi-pause"
          severity="secondary"
          text
          rounded
          size="small"
          aria-label="إيقاف مؤقت"
          @click="$emit('action', goal, 'pause')"
        />
        <prime_button
          v-else-if="goal.status === 'paused'"
          icon="pi pi-play"
          severity="success"
          text
          rounded
          size="small"
          aria-label="استئناف"
          @click="$emit('action', goal, 'resume')"
        />
        <prime_button
          v-if="goal.status !== 'completed'"
          icon="pi pi-check"
          severity="success"
          text
          rounded
          size="small"
          aria-label="إكمال الهدف"
          @click="$emit('action', goal, 'complete')"
        />
        <prime_button
          icon="pi pi-copy"
          severity="secondary"
          text
          rounded
          size="small"
          aria-label="نسخ الهدف"
          @click="$emit('duplicate', goal)"
        />
        <prime_button
          icon="pi pi-trash"
          severity="danger"
          text
          rounded
          size="small"
          aria-label="حذف الهدف"
          @click="$emit('remove', goal)"
        />
      </div>
    </template>
  </prime_card>
</template>

<script setup>
defineProps({
  goal: {
    type: Object,
    required: true,
  },
  statusLabel: Function,
  categoryLabel: Function,
  priorityLabel: Function,
  statusSeverity: Function,
})

defineEmits(['details', 'edit', 'action', 'duplicate', 'remove'])
</script>
