<script setup>
// ============================================================
//  WorkflowVersions.vue
//  src/components/Automation/Workflow/WorkflowVersions.vue
//
//  المسؤولية: عرض سجل الـ versions للـ Workflow
//  الفكرة: كل ما المستخدم يضغط "Save" → يتحفظ snapshot
//
//  الحالة: Phase 3 — الـ UI جاهز، الـ backend endpoints
//  المطلوب لاحقاً:
//    GET  /api/automation/workflows/{id}/versions/
//    POST /api/automation/workflows/{id}/restore/{version_id}/
//
//  الاستخدام:
//    <WorkflowVersions
//      :workflow-id="currentWorkflowId"
//      :visible="showVersions"
//      @restore="onRestoreVersion"
//      @close="showVersions = false"
//    />
// ============================================================
import { ref, watch } from 'vue'
import automationService from '@/services/AutomationService'
import { useToast } from 'primevue/usetoast'

const props = defineProps({
  visible: { type: Boolean, default: false },
  workflowId: { type: String, default: null },
})

const emit = defineEmits(['restore', 'close', 'update:visible'])

const toast = useToast()
const versions = ref([])
const loading = ref(false)
const restoring = ref(null) // id of version being restored

// ─── Load versions when panel opens ──────────────────────
watch(
  () => props.visible,
  async (val) => {
    if (val && props.workflowId) await loadVersions()
  },
)

const loadVersions = async () => {
  loading.value = true
  try {
    // ⚠️ Endpoint مش موجود لسه — placeholder
    // const { data } = await automationService.listWorkflowVersions(props.workflowId)
    // versions.value = data

    // Mock data للعرض
    versions.value = [
      {
        id: 'v3',
        version_number: 3,
        label: 'Version 3',
        saved_at: new Date().toISOString(),
        nodes_count: 5,
        edges_count: 4,
        is_current: true,
      },
      {
        id: 'v2',
        version_number: 2,
        label: 'Version 2',
        saved_at: new Date(Date.now() - 3600000).toISOString(),
        nodes_count: 3,
        edges_count: 2,
        is_current: false,
      },
      {
        id: 'v1',
        version_number: 1,
        label: 'Version 1 (Initial)',
        saved_at: new Date(Date.now() - 86400000).toISOString(),
        nodes_count: 1,
        edges_count: 0,
        is_current: false,
      },
    ]
  } catch (err) {
    toast.add({ severity: 'error', summary: '❌ فشل تحميل الـ versions', life: 3000 })
  } finally {
    loading.value = false
  }
}

const restoreVersion = async (version) => {
  if (version.is_current) return
  restoring.value = version.id
  try {
    // ⚠️ Endpoint مش موجود لسه
    // await automationService.restoreWorkflowVersion(props.workflowId, version.id)
    toast.add({
      severity: 'info',
      summary: '🔄 Restore',
      detail: `سيتم استعادة ${version.label} قريباً`,
      life: 3000,
    })
    emit('restore', version)
    emit('update:visible', false)
  } finally {
    restoring.value = null
  }
}

// ─── Format Date ──────────────────────────────────────────
const formatDate = (iso) => {
  const d = new Date(iso)
  return d.toLocaleString('ar-EG', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<template>
  <prime_drawer
    :visible="visible"
    position="right"
    header="📋 سجل الـ Versions"
    :style="{ width: '320px' }"
    @update:visible="$emit('update:visible', $event)"
  >
    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-8">
      <i class="pi pi-spin pi-spinner text-3xl text-blue-400"></i>
    </div>

    <!-- No Workflow Selected -->
    <div v-else-if="!workflowId" class="empty-state">
      <i class="pi pi-sitemap text-3xl text-slate-600 mb-2"></i>
      <p class="text-slate-400 text-sm">اختر Workflow الأول</p>
    </div>

    <!-- Versions List -->
    <div v-else class="versions-list">
      <!-- Coming Soon Banner -->
      <div class="coming-soon-banner mb-4">
        <i class="pi pi-info-circle mr-2"></i>
        <span class="text-xs"> هذه الميزة في مرحلة التطوير — الـ versions الظاهرة للعرض فقط </span>
      </div>

      <!-- Version Card -->
      <div
        v-for="version in versions"
        :key="version.id"
        class="version-card"
        :class="{ 'version-card--current': version.is_current }"
      >
        <!-- Header -->
        <div class="version-card__header">
          <div class="version-card__title">
            <i class="pi pi-bookmark text-sm mr-1"></i>
            <span class="font-semibold text-sm">{{ version.label }}</span>
            <prime_tag
              v-if="version.is_current"
              value="الحالية"
              severity="success"
              class="!text-xs !px-1 !py-0 ml-2"
            />
          </div>
          <span class="version-card__date">{{ formatDate(version.saved_at) }}</span>
        </div>

        <!-- Stats -->
        <div class="version-card__stats">
          <span>
            <i class="pi pi-circle-fill text-blue-400 mr-1" style="font-size: 0.5rem"></i>
            {{ version.nodes_count }} nodes
          </span>
          <span>
            <i class="pi pi-circle-fill text-purple-400 mr-1" style="font-size: 0.5rem"></i>
            {{ version.edges_count }} edges
          </span>
        </div>

        <!-- Actions -->
        <div class="version-card__actions" v-if="!version.is_current">
          <prime_button
            label="استعادة"
            icon="pi pi-undo"
            size="small"
            outlined
            severity="warning"
            :loading="restoring === version.id"
            @click="restoreVersion(version)"
          />
        </div>
      </div>
    </div>

    <!-- Footer -->
    <template #footer>
      <div class="flex justify-end">
        <prime_button
          label="إغلاق"
          severity="secondary"
          outlined
          @click="$emit('update:visible', false)"
        />
      </div>
    </template>
  </prime_drawer>
</template>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48px 16px;
}

.coming-soon-banner {
  background: rgba(234, 179, 8, 0.1);
  border: 1px solid rgba(234, 179, 8, 0.3);
  border-radius: 8px;
  padding: 8px 12px;
  display: flex;
  align-items: center;
  color: #fbbf24;
}

.versions-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.version-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 12px;
  transition: border-color 0.2s;
}

.version-card--current {
  border-color: #22c55e;
  background: rgba(34, 197, 94, 0.05);
}

.version-card__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 6px;
}

.version-card__title {
  display: flex;
  align-items: center;
  color: #e2e8f0;
}

.version-card__date {
  font-size: 0.7rem;
  color: #64748b;
  white-space: nowrap;
}

.version-card__stats {
  display: flex;
  gap: 12px;
  font-size: 0.75rem;
  color: #94a3b8;
  margin-bottom: 8px;
}

.version-card__actions {
  display: flex;
  justify-content: flex-end;
}
</style>
