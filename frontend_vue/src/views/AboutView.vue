<template>
  <div class="q-pa-md">
    <h2 class="text-xl font-bold mb-4">فرص العمل المتاحة</h2>

    <!-- مؤشر التحميل -->
    <div v-if="loading" class="flex justify-center my-6">
      <ProgressSpinner />
    </div>

    <!-- عرض البيانات في جدول أو بطاقات باستخدام PrimeVue -->
    <div v-else>
      <DataTable :value="jobs" responsiveLayout="scroll" class="p-datatable-gridlines">
        <Column field="title" header="عنوان الوظيفة"></Column>
        <Column field="company" header="الشركة"></Column>
        <Column field="location" header="الموقع"></Column>
        <Column header="الرابط">
          <template #body="slotProps">
            <a :href="slotProps.data.url" target="_blank" class="text-blue-600 underline"
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
import axios from 'axios'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ProgressSpinner from 'primevue/progressspinner'

const jobs = ref([])
const loading = ref(true)

const fetchJobs = async () => {
  try {
    // استبدل الرابط بالـ Endpoint الخاص بالـ Backend لديك
    const response = await axios.get('http://127.0.0.1:8000/api/jobs/')
    jobs.value = response.data
  } catch (error) {
    console.error('حدث خطأ أثناء جلب البيانات:', error)
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
