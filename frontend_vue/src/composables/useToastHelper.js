// ============================================================
//  useToastHelper.js
//  src/composables/useToastHelper.js
//
//  ✅ Centralized toast — UX موحد في كل المكونات
//  ✅ Smart Django error parser — يقرأ الـ validation errors تلقائياً
//  ✅ Status-based messages — كل HTTP status ليه رسالة عربية
// ============================================================

import { useToast } from 'primevue/usetoast'

export function useToastHelper() {
  const toast = useToast()

  // ─────────────────────────────────────────
  // Base helpers
  // ─────────────────────────────────────────

  const success = (summary, detail, life = 3000) =>
    toast.add({ severity: 'success', summary: `✅ ${summary}`, detail, life })

  const error = (summary, detail, life = 5000) =>
    toast.add({ severity: 'error', summary: `❌ ${summary}`, detail, life })

  const warn = (summary, detail, life = 4000) =>
    toast.add({ severity: 'warn', summary: `⚠️ ${summary}`, detail, life })

  const info = (summary, detail, life = 3000) =>
    toast.add({ severity: 'info', summary: `ℹ️ ${summary}`, detail, life })

  const cancelled = (detail = 'لم يتم تنفيذ الإجراء') =>
    toast.add({ severity: 'info', summary: 'إلغاء', detail, life: 2000 })

  // ─────────────────────────────────────────
  // Smart API error
  // بيقرأ Django validation errors تلقائياً
  // ─────────────────────────────────────────
  const apiError = (err, fallbackSummary = 'حصل خطأ') => {
    const status = err?.response?.status
    const data   = err?.response?.data

    // ✅ Django 400 validation: { field: ["msg", ...], ... }
    if (status === 400 && data && typeof data === 'object' && !Array.isArray(data)) {
      const entries = Object.entries(data).slice(0, 3)
      const detail = entries
        .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs[0] : msgs}`)
        .join(' | ')
      error(`${fallbackSummary} (400)`, detail)
      return
    }

    // ✅ Django 400 string error
    if (status === 400 && typeof data === 'string') {
      error(`${fallbackSummary} (400)`, data)
      return
    }

    // ✅ Django detail message (DRF default)
    if (data?.detail) {
      error(`${fallbackSummary}${status ? ` (${status})` : ''}`, data.detail)
      return
    }

    // ✅ Known HTTP status messages
    const statusMessages = {
      401: 'انتهت جلستك — سجّل دخولك من جديد',
      403: 'مش عندك صلاحية تعمل الإجراء ده',
      404: 'العنصر مش موجود',
      409: 'البيانات دي موجودة بالفعل',
      413: 'الملف كبير أوي — قلّل الحجم وحاول تاني',
      422: 'البيانات المرسلة فيها مشكلة',
      429: 'طلبات كتير — استنى لحظة وحاول تاني',
      500: 'خطأ في السيرفر — راجع الـ Django logs',
      502: 'السيرفر مش شغّال دلوقتي',
      503: 'الخدمة متوقفة مؤقتاً',
    }

    const detail = statusMessages[status] || err?.message || 'خطأ غير معروف'
    error(`${fallbackSummary}${status ? ` (${status})` : ''}`, detail)
  }

  // ─────────────────────────────────────────
  // Return
  // ─────────────────────────────────────────
  return { success, error, warn, info, info, cancelled, apiError }
}
