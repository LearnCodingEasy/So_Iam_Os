// ============================================================
//  useAsyncAction.js
//  src/composables/useAsyncAction.js
//
//  UX Engine — بيتحكم في كل API call بطريقة موحدة:
//   ✅ Loading guard     → يمنع الـ double-submit
//   ✅ Validation        → يتحقق من الـ form قبل ما يبعت
//   ✅ tracker.execute   → كل request يظهر في ApiFlowPanel
//   ✅ Toast             → success/error رسائل موحدة
//   ✅ onSuccess/onError → callbacks للـ business logic
//
//  الاستخدام:
//  ─────────────────────────────────────────
//  const programAction = useAsyncAction()
//
//  programAction.run(
//    () => programStore.createProgram(),
//    {
//      validate:       () => programStore.validateForm(),
//      successSummary: 'تم إنشاء البرنامج',
//      errorSummary:   'فشل إنشاء البرنامج',
//      onSuccess: (result) => { createVisible.value = false },
//      onError:   (err)    => { /* rollback */ },
//    }
//  )
// ============================================================

import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useApiTracker } from '@/composables/useApiTracker'

export function useAsyncAction() {
  const loading = ref(false)
  const toast   = useToast()
  const tracker = useApiTracker()

  // ─────────────────────────────────────────
  // run() — الـ UX Engine
  // ─────────────────────────────────────────
  const run = async (apiFn, options = {}) => {
    if (loading.value) return  // ✅ Guard: منع double-submit

    const {
      validate       = null,
      successSummary = null,
      successDetail  = null,
      errorSummary   = 'حصل خطأ',
      onSuccess      = null,
      onError        = null,
    } = options

    // ✅ Validation — قبل أي API call
    if (validate) {
      const validErr = validate()
      if (validErr) {
        toast.add({ severity: 'warn', summary: '⚠️ تحقق من البيانات', detail: validErr, life: 4000 })
        return
      }
    }

    loading.value = true

    try {
      // ✅ tracker.execute → يظهر في ApiFlowPanel تلقائياً
      const result = await tracker.execute({ serviceFn: apiFn })

      if (successSummary)
        toast.add({ severity: 'success', summary: `✅ ${successSummary}`, detail: successDetail, life: 4000 })

      if (onSuccess) await onSuccess(result)
      return result

    } catch (err) {
      // ✅ Smart error: يقرأ Django 400 validation errors field-by-field
      const status = err?.response?.status
      const body   = err?.response?.data
      let detail   = err?.message || 'خطأ غير متوقع'

      if (status === 400 && body && typeof body === 'object') {
        detail = Object.entries(body)
          .map(([f, m]) => `${f}: ${Array.isArray(m) ? m[0] : m}`)
          .slice(0, 3).join(' | ')
      } else if (status === 401) { detail = 'انتهت جلستك — سجّل دخول من جديد'
      } else if (status === 403) { detail = 'مش عندك صلاحية لهذه العملية'
      } else if (status === 404) { detail = 'العنصر المطلوب غير موجود'
      } else if (status === 413) { detail = 'الملف كبير جداً — الحد الأقصى 5MB'
      } else if (status === 500) { detail = 'خطأ في السيرفر — حاول مرة أخرى' }

      toast.add({ severity: 'error', summary: `❌ ${errorSummary}`, detail, life: 6000 })
      if (onError) onError(err)
      throw err

    } finally {
      loading.value = false
    }
  }

  return { run, loading, tracker }
}
