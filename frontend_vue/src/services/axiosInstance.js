import axios from 'axios';
import { useToast } from 'primevue/usetoast';

// إنشاء نسخة مخصصة من Axios
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Interceptor للطلبات (إضافة الـ Token إذا وجد)
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor للاستجابات والأخطاء (هنا يتم التقاط فشل الشبكة والخادم)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // استدعاء نظام الـ Toast (نظراً لأننا خارج نطاق الـ Setup المباشر، يمكننا استخدام الـ Hook بحذر أو تمرير الحدث)
    const errorMessage = getErrorMessage(error);

    // يمكنك استخدام الحدث العام أو إطلاق Custom Event ليعرضه الـ Toast
    triggerGlobalToast('error', 'خطأ في النظام', errorMessage);

    return Promise.reject(error);
  }
);

// دالة لتحديد رسالة الخطأ بناءً على حالة الاستجابة
function getErrorMessage(error) {
  if (!error.response) {
    return 'تعذر الاتصال بالخادم. يرجى التحقق من اتصالك بالإنترنت.';
  }

  const { status, data } = error.response;

  switch (status) {
    /**** أخطاء الخادم والتحقق ****/
    case 400:
      return data.message || formatDjangoErrors(data) || 'البيانات المدخلة غير صالحة.';
    case 401:
      return 'انتهت صلاحية الجلسة أو أنك غير مصرح لك بالوصول. يرجى تسجيل الدخول مجدداً.';
    case 403:
      return 'عذراً، لا تمتلك الصلاحيات الكافية لتنفيذ هذا الإجراء.';
    case 404:
      return 'المورد المطلوب غير موجود على الخادم.';
    case 500:
    case 502:
    case 503:
      return 'خطأ داخلي في الخادم. يرجى المحاولة لاحقاً أو إبلاغ الدعم الفني.';
    default:
      return data.message || 'حدث خطأ غير متوقع أثناء معالجة طلبك.';
  }
}

// دالة مساعدة لدمج أخطاء Django REST Framework إذا جاءت على شكل حقول
function formatDjangoErrors(data) {
  if (typeof data === 'object' && data !== null) {
    const errors = [];
    for (const [key, value] of Object.entries(data)) {
      if (Array.isArray(value)) {
        errors.push(`${key}: ${value.join(', ')}`);
      } else if (typeof value === 'string') {
        errors.push(`${key}: ${value}`);
      }
    }
    if (errors.length > 0) return errors.join(' | ');
  }
  return null;
}

// إطلاق الحدث لعرض التنبيه (يمتثل لـ EventBus أو PrimeVue Toast مباشر)
function triggerGlobalToast(severity, summary, detail) {
  window.dispatchEvent(new CustomEvent('app:notify', {
    detail: { severity, summary, detail }
  }));
}

export default api;
