<script setup>
/*
===================================================
WorkflowToolbar.vue
src/components/Automation/Workflow/WorkflowToolbar.vue

المسؤولية: أزرار التحكم في الـ Workflow (save, run, layout...)
❌ لا تحتوي على API calls — بس تطلع events
✅ تستقبل الحالة كـ props (isSaving, isRunning, hasWorkflow)

الاستخدام:
<WorkflowToolbar
  :has-workflow="!!currentWorkflowId"
  :is-saving="isSavingWorkflow"
  :is-running="isRunningWorkflow"
  :workflow-status="currentWorkflow?.status"
  @save="saveWorkflow"
  @run="startWorkflow"
  @create="createWorkflow"
  @auto-layout="autoLayout"
  @update-status="updateStatusWorkflow"
/>
===================================================

*/
defineProps({
  hasWorkflow: { type: Boolean, default: false },
  isSaving: { type: Boolean, default: false },
  isRunning: { type: Boolean, default: false },
  isLoading: { type: Boolean, default: false },
  workflowStatus: { type: String, default: 'draft' }, // draft | active | paused
})

const emit = defineEmits([
  'save', // 💾 حفظ الـ Workflow
  'run', // ▶️ تشغيل الـ Workflow
  'create', // ➕ إنشاء Workflow جديد
  'clear', // 🗑️ مسح الـ Canvas
  'auto-layout', // 📐 ترتيب تلقائي
  'update-status', // تغيير status (active/paused/draft)
])

// ─── Layout Directions ────────────────────────────────────
const layoutOptions = [
  { dir: 'TB', label: '↓ TB', title: 'Top → Bottom' },
  { dir: 'BT', label: '↑ BT', title: 'Bottom → Top' },
  { dir: 'LR', label: '→ LR', title: 'Left → Right' },
  { dir: 'RL', label: '← RL', title: 'Right → Left' },
]

// ─── Status Options ───────────────────────────────────────
const statusOptions = [
  { value: 'draft', label: '📝 Draft', severity: 'secondary' },
  { value: 'active', label: '✅ Active', severity: 'success' },
  { value: 'paused', label: '⏸ Paused', severity: 'warning' },
]
</script>

<template>
  <div class="workflow-toolbar">
    <!-- ── Row 1: Main Actions ─────────────────────────── -->
    <div class="toolbar-row">
      <!-- Create New Workflow -->
      <prime_button
        icon="pi pi-plus"
        label="Workflow جديد"
        size="small"
        severity="info"
        outlined
        @click="emit('create')"
        :disabled="isLoading"
        v-tooltip.bottom="'إنشاء Workflow جديد'"
      />

      <!-- Save -->
      <prime_button
        icon="pi pi-save"
        label="حفظ"
        size="small"
        severity="info"
        :loading="isSaving"
        :disabled="!hasWorkflow || isLoading"
        @click="emit('save')"
        v-tooltip.bottom="'حفظ التغييرات (Ctrl+S)'"
      />

      <!-- Run Workflow -->
      <prime_button
        icon="pi pi-play"
        label="تشغيل"
        size="small"
        severity="success"
        :loading="isRunning"
        :disabled="!hasWorkflow || isSaving"
        @click="emit('run')"
        v-tooltip.bottom="'تشغيل الـ Workflow'"
      />

      <!-- Divider -->
      <prime_divider layout="vertical" class="!mx-1 !h-6" />

      <!-- Status Buttons -->
      <template v-for="opt in statusOptions" :key="opt.value">
        <prime_button
          :label="opt.label"
          size="small"
          :severity="workflowStatus === opt.value ? opt.severity : 'secondary'"
          :outlined="workflowStatus !== opt.value"
          :disabled="!hasWorkflow"
          @click="emit('update-status', opt.value)"
          v-tooltip.bottom="`تغيير الحالة إلى ${opt.label}`"
        />
      </template>

      <!-- Divider -->
      <prime_divider layout="vertical" class="!mx-1 !h-6" />

      <!-- Clear Canvas -->
      <prime_button
        icon="pi pi-trash"
        size="small"
        severity="danger"
        outlined
        :disabled="!hasWorkflow"
        @click="emit('clear')"
        v-tooltip.bottom="'مسح كل الـ nodes'"
      />
    </div>

    <!-- ── Row 2: Layout ──────────────────────────────── -->
    <div class="toolbar-row mt-1">
      <span class="text-xs text-slate-400 mr-1">📐 Layout:</span>
      <prime_button
        v-for="opt in layoutOptions"
        :key="opt.dir"
        :label="opt.label"
        size="small"
        severity="secondary"
        outlined
        :disabled="!hasWorkflow"
        @click="emit('auto-layout', opt.dir)"
        v-tooltip.bottom="opt.title"
        class="!px-2 !py-1 !text-xs"
      />
    </div>
  </div>
</template>

<style scoped>
.workflow-toolbar {
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(8px);
  border: 1px solid #1e293b;
  border-radius: 10px;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.toolbar-row {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
</style>
