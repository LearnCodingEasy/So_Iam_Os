<template>
  <section class="panel section-card">
    <div class="section-head">
      <div>
        <h2>API Contract & Connection Test</h2>

        <p>فحص GET للـ endpoints التي يعلن عنها Backend contract.</p>
      </div>

      <Tag
        :value="`${apiPassed}/${apiResults.length || 0}`"
        :severity="apiFailed ? 'danger' : 'success'"
      />
    </div>

    <DataTable :value="apiResults" responsiveLayout="scroll" :loading="apiChecking">
      <Column field="method" header="Method" />

      <Column field="path" header="Endpoint" />

      <Column field="status" header="Status" />

      <Column field="duration" header="ms" />

      <Column header="النتيجة">
        <template #body="{ data }">
          <Tag :value="data.ok ? 'PASS' : 'FAIL'" :severity="data.ok ? 'success' : 'danger'" />
        </template>
      </Column>

      <Column field="error" header="الخطأ" />
    </DataTable>
  </section>
</template>

<script setup>
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'

defineProps({
  apiResults: {
    type: Array,
    default: () => [],
  },

  apiChecking: {
    type: Boolean,
    default: false,
  },

  apiPassed: {
    type: Number,
    default: 0,
  },

  apiFailed: {
    type: Boolean,
    default: false,
  },
})
</script>
