<template>
  <Toast position="bottom-right" />
</template>

<script setup>
import { useToast } from 'primevue/usetoast';
import { provide } from 'vue';

const toast = useToast();

// دالة عامة يمكن حقنها أو استدعاؤها لعرض التنبيهات
const showNotification = (severity, summary, detail) => {
  toast.add({
    severity: severity, // 'success', 'info', 'warn', 'error'
    summary: summary,
    detail: detail,
    life: 5000 // مدة بقاء التنبيه (5 ثوانٍ)
  });
};

// توفير الدالة عبر الـ Provide/Inject لتكون متاحة في أي مكان إذا لزم الأمر
provide('notify', showNotification);
</script>
