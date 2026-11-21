import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    enhancements: {
      title: 'Frontend Engineering Center',
      subtitle: 'Production-grade interaction, caching, accessibility and authoring capabilities.',
      cache: 'Server-state cache',
      editor: 'Rich text editor',
      files: 'File intake',
      reorder: 'Reorderable workspace',
      virtualization: 'Virtualized activity stream',
      notify: 'Notifications',
      theme: 'Theme preference',
    },
  },
  ar: {
    enhancements: {
      title: 'مركز هندسة الواجهة',
      subtitle: 'قدرات إنتاجية للكاش، الوصول، المحرر، الملفات والتفاعل.',
      cache: 'كاش بيانات الخادم',
      editor: 'محرر نصوص متقدم',
      files: 'رفع الملفات',
      reorder: 'ترتيب مساحة العمل',
      virtualization: 'قائمة نشاط افتراضية',
      notify: 'الإشعارات',
      theme: 'تفضيل المظهر',
    },
  },
}

export const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('so-iam-locale') || 'ar',
  fallbackLocale: 'en',
  messages,
})

export default i18n
