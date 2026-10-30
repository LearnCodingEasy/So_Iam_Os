<template>
  <div class="q-pa-md">
    <h2 class="text-xl font-bold mb-4">فرص العمل المتاحة</h2>

    <!-- مؤشر التحميل -->
    <div v-if="loading" class="flex justify-center my-6">
      <ProgressSpinner />
    </div>

    <!-- عرض البيانات في جدول أو بطاقات باستخدام PrimeVue -->
    <div v-else>
      <p v-if="error" class="text-red-600" role="alert">{{ error }}</p>
      <p v-else-if="!jobs.length" class="text-gray-500">لا توجد وظائف محفوظة حتى الآن. أضف مصدرًا وابدأ المزامنة من صفحة الوظائف.</p>
      <DataTable v-else :value="jobs" responsiveLayout="scroll" class="p-datatable-gridlines">
        <Column field="title" header="عنوان الوظيفة"></Column>
        <Column field="company" header="الشركة"></Column>
        <Column field="location" header="الموقع"></Column>
        <Column header="الرابط">
          <template #body="slotProps">
            <a :href="slotProps.data.url" target="_blank" rel="noopener noreferrer" class="text-blue-600 underline"
              >رابط الوظيفة</a
            >
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { listJobs } from '@/services/jobs'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ProgressSpinner from 'primevue/progressspinner'

const jobs = ref([])
const loading = ref(true)
const error = ref('')

const fetchJobs = async () => {
  try {
    // استبدل الرابط بالـ Endpoint الخاص بالـ Backend لديك
    jobs.value = await listJobs()
  } catch (err) {
    error.value = err?.response?.data?.detail || 'تعذر تحميل الوظائف. حاول مرة أخرى.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchJobs()
})
</script>

<style scoped>
/* يمكنك إضافة تنسيقاتك الخاصة هنا أو الاعتماد على TailwindCSS */
</style>
